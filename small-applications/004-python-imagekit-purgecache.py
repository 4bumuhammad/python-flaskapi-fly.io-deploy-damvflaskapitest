import sys
import time
from imagekitio import ImageKit

class ImageCachePurger:
    def __init__(self, private_key, public_key, url_endpoint):
        self.imagekit = ImageKit(
            private_key=private_key,
            public_key=public_key,
            url_endpoint=url_endpoint
        )

    def purge_cache(self, url):
        try:
            print("- Purging cache for the image...")
            purge_response = self.imagekit.purge_cache(url)
            request_id = purge_response.request_id
            print("Request ID:", request_id)

            polling_count = 0

            while True:

                purge_cache_status = self.imagekit.get_purge_cache_status(purge_cache_id=request_id)

                if polling_count <= 2 and purge_cache_status.status == 'Pending':
                    print("Cache status: Pending")
                
                if polling_count > 2 and purge_cache_status.status == 'Pending':
                    print("Cache status: In progress")
                
                if purge_cache_status.status == 'Completed':
                    break
                
                polling_count += 1
                time.sleep(1)  
            
            return purge_cache_status.status

        except Exception as e:
            print("- Failed to purge cache:", str(e))
            return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 004-python-imagekit-purgecache.py <url_image>")
        sys.exit(1)

    private_key = 'private_tMllcpEGq4gf7TzbqEWpqQzupac='
    public_key = 'public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA='
    url_endpoint = 'https://ik.imagekit.io/2fbeg9wdr'

    url_image = sys.argv[1]

    cache_purger = ImageCachePurger(private_key, public_key, url_endpoint)

    purge_result = cache_purger.purge_cache(url_image)
    if purge_result:
        print("Purge result:", purge_result)
