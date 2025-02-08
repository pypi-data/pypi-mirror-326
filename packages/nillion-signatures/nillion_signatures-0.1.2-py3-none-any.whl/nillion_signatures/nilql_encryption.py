"""Encryption utilities using nilql for secret sharing."""
import nilql
from typing import List, Union


class DataEncryption:
    def __init__(self, num_nodes: int, seed: Union[bytes, bytearray, str]):
        self.num_nodes = num_nodes
        self.secret_key = nilql.SecretKey.generate({'nodes': [{}] * num_nodes},{'store': True}, seed)

    def encrypt(self, payload: str) -> List[str]:
        """Encrypt payload using secret sharing."""
        try:
            encrypted_shares = nilql.encrypt(self.secret_key, payload)

            return list(encrypted_shares)
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt(self, encoded_shares: List[str]) -> str:
        """Decrypt payload from shares."""
        try:
            decoded_shares = []
            for share in encoded_shares:
                decoded_shares.append(share)
                
            return str(nilql.decrypt(self.secret_key, decoded_shares))
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")


