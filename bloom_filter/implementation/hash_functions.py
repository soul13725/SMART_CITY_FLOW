import hashlib

class HashFunctions:
    @staticmethod
    def _hash_md5(item: str) -> int:
        return int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16)

    @staticmethod
    def _hash_sha256(item: str) -> int:
        return int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16)

    @staticmethod
    def get_hash(item: str, index: int, num_bits: int) -> int:
        """
        Double hashing strategy: h_i(x) = (h1(x) + i * h2(x)) % m
        Using md5 as h1 and sha256 as h2.
        """
        h1 = HashFunctions._hash_md5(item)
        h2 = HashFunctions._hash_sha256(item)
        return (h1 + index * h2) % num_bits
