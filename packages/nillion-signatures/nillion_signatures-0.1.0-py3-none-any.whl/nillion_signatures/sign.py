import base64
import re
from typing import Optional, List, Dict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from nillion_signatures import nildb_api
from nillion_signatures.nilql_encryption import DataEncryption


def sign(signature_scheme: str, nodes_jwts_store_ids: List[Dict], message: str, store_id: str, encryption: DataEncryption, schema_id) -> dict:
    """
    Sign a message and return encrypted shares.

    Args:
        signature_scheme (str): Either "ECDSA" or "EdDSA"
        nodes_jwts_store_ids (List[Dict]): List of dicts with node info, JWTs & store_ids
        example: [
            {
                "node_url_1": "node1.com",
                "node_jwt": "XXXX",
                "store_id": "YYYY"
            },
            {
                "node_url_2": "node2.com",
                "node_jwt": "YYYY",
                "store_id": "YYYY"
            }
        ]
        message (str): Message to sign
        public_key (Optional[str]): public key for shares to be (optionally) encrypted

    Returns:
        Dict: Public key (if provided) and (encrypted) shares of signed message
    """
    # recover shares
    # Fetch from all nodes
    shares = []
    for node in nodes_jwts_store_ids:
        # response = nildb_api.query_execute(node, "7fad8d3a-6e16-48ec-9d8b-8f63867e53c0", variables={"store_id": store_id})
        response = nildb_api.data_read(node, schema_id, filter_dict={"_id": store_id})
        shares.append(response[0]["key_share"])

    # Decrypt private_key
    if len(shares) == len(nodes_jwts_store_ids):
        pem_private_key = encryption.decrypt(shares)
        restored_private_key = serialization.load_pem_private_key(
            pem_private_key.encode("utf-8"),
            password=None
        )
    else:
        return {}

    # Mock signing operation
    if signature_scheme == "EdDSA":
        signed_message = restored_private_key.sign(message.encode())
    elif signature_scheme == "ECDSA":
        signed_message = restored_private_key.sign(
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
    else:
        return {}

    # Encrypt password into shares. We have to encode bytes into str
    signed_message_b64 = base64.b64encode(signed_message).decode('utf-8')
    signed_message_shares = encryption.encrypt(signed_message_b64)

    pem_public_key = restored_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    pem_cleaned = re.sub(r"-----.*?-----\n?", "", pem_public_key).strip()

    # Format response
    response = {
        "shares": signed_message_shares,
        "public_key": pem_cleaned,
    }
    
    return response