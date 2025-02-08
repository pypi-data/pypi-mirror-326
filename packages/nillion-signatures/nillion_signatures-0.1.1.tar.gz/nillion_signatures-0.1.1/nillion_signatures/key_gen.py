import uuid

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, ec

from nillion_signatures import nildb_api
from nillion_signatures.nilql_encryption import DataEncryption


def key_gen(sign_scheme: str, nodes_and_jwts: list[dict], encryption: DataEncryption, schema_id: str) -> str:
    """
    Generate keys for the specified signature scheme.
    
    Args:
        sign_scheme (str): Either "ECDSA" or "EdDSA"
        nodes_and_jwts (list): List of dicts with node info and JWTs
        example: [
            {
                "node_url_1": "node1.com",
                "node_jwt": "XXXX"
            },
            {
                "node_url_2": "node2.com",
                "node_jwt": "YYYY"
            }
        ]
    
    Returns:
        list: List of dicts with node URLs and store IDs
    """
    # Mock key generation based on signature scheme
    if sign_scheme == "EdDSA":
        private_key = ed25519.Ed25519PrivateKey.generate()
    else:  # ECDSA
        private_key = ec.generate_private_key(ec.SECP256K1())

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")

    # Generate store_id
    store_id = str(uuid.uuid4())
    # Encrypt password into shares
    encrypted_shares = encryption.encrypt(pem_private_key)

    # Store shares across nodes
    success = True
    for i, node in enumerate(nodes_and_jwts):
        payload = {
            "_id": store_id,
            "key_share": encrypted_shares[i]
        }
        if not nildb_api.data_upload(node, schema_id, [payload]):
            success = False
            break

    if not success:
        return ""


    return store_id
