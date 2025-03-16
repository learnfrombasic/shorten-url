import hashlib


class URLShortener:
    def __init__(self):
        self.url_map = {}  # Dictionary to store shortURL -> longURL mappings
        self.salt = "abc123"  # Predefined string for handling collisions

    def generate_short_url(self, long_url):
        """Generates a short URL using SHA-256 hashing with collision handling."""
        attempt = 0

        while True:
            # Append salt if retrying due to collision
            url_to_hash = long_url + (self.salt * attempt if attempt > 0 else "")

            # Generate a hash
            hash_obj = hashlib.sha256(url_to_hash.encode())
            short_url = hash_obj.hexdigest()[:6]  # Take the first 6 characters

            # Check for collision
            if short_url not in self.url_map:
                self.url_map[short_url] = long_url
                return short_url  # Return the generated short URL
            else:
                attempt += (
                    1  # Increase attempt to modify the hash in the next iteration
                )

    def get_long_url(self, short_url):
        """Retrieves the original URL from the short URL."""
        return self.url_map.get(short_url, "URL not found")


if __name__ == "__main__":
    # Example usage
    shortener = URLShortener()
    long_url = "https://docs.python.org/3/library/hashlib.html"

    short_url = shortener.generate_short_url(long_url)
    print(f"Short URL: {short_url}")

    # Retrieve original URL
    retrieved_url = shortener.get_long_url(short_url)
    print(f"Original URL: {retrieved_url}")
