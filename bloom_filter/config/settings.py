import math
import os

class Settings:
    # Defaults
    BLOOM_EXPECTED_ITEMS = int(os.getenv("BLOOM_EXPECTED_ITEMS", 100000))
    BLOOM_FALSE_POSITIVE_RATE = float(os.getenv("BLOOM_FALSE_POSITIVE_RATE", 0.01))

    @staticmethod
    def calculate_bloom_parameters(expected_items: int, false_positive_rate: float):
        """
        Calculate m (bits) and k (hash functions).
        m = -(n * ln(p)) / (ln(2)^2)
        k = (m / n) * ln(2)
        """
        if expected_items <= 0 or false_positive_rate <= 0 or false_positive_rate >= 1:
            raise ValueError("Invalid parameters for Bloom Filter calculation")

        m_bits = - (expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        k_hashes = (m_bits / expected_items) * math.log(2)

        return math.ceil(m_bits), math.ceil(k_hashes)

settings = Settings()
