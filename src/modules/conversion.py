import string

class Base24URLShortener:
    def __init__(self):
        self.charset = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Base-24 characters (excluding 0, O, 1, I)
        self.base = len(self.charset)
        self.url_map = {}  # Stores ID-to-URL mappings
        self.counter = 1  # Simulated auto-incrementing ID (would be a DB ID in real-world applications)

    def encode(self, num):
        """Converts an integer ID to a Base-24 short URL."""
        if num == 0:
            return self.charset[0]
        
        short_url = []
        while num > 0:
            remainder = num % self.base
            short_url.append(self.charset[remainder])
            num //= self.base
        
        return "".join(short_url[::-1])  # Reverse the result for correct encoding

    def decode(self, short_url):
        """Converts a Base-24 short URL back to an integer ID."""
        num = 0
        for char in short_url:
            num = num * self.base + self.charset.index(char)
        return num

    def generate_short_url(self, long_url):
        """Generates a short URL using Base-24 encoding."""
        short_url = self.encode(self.counter)
        self.url_map[short_url] = long_url
        self.counter += 1  # Increment the ID for the next URL
        return short_url

    def get_long_url(self, short_url):
        """Retrieves the original long URL from the short URL."""
        return self.url_map.get(short_url, "URL not found")
