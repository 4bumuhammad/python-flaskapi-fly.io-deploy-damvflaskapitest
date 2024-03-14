import requests
import sys

class ImageChecker:
    def __init__(self):
        pass

    def is_url_image(self, image_url):
        img_formats = ("image/png", "image/jpeg", "image/jpg")
        try:

            response = requests.get(image_url, stream=True)
            content_type = response.headers.get('content-type', '')
            content_length = response.headers.get('content-length', '')

            if response.status_code == 200 and content_type in img_formats and content_length:
                return True
            return False
        except Exception as e:
            print("Error:", str(e))
            return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python_imagekit_checkurl.py <image_url>")
        sys.exit(1)

    image_url = sys.argv[1]
    checker = ImageChecker()

    if checker.is_url_image(image_url):
        print("The provided URL points to an image.")
    else:
        print("The provided URL does not point to an image or cannot be reached.")





# #### all of the following URL lists have basically been removed from the Image Kit media-library ####
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_YgLdgRDQT.jpg" ---> safari  // The provided URL points to an image.
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_9AzU1A242.jpg" ---> chrome  // The provided URL does not point to an image or cannot be reached.
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_K6liBtV3M.jpg" ---> [Never] ID "65f20f7388c257da33b07a89" // The provided URL does not point to an image or cannot be reached.
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_rqF0G2_VC.jpg" ---> [Never] ID "65f2100588c257da33b27dca" // The provided URL points to an image.
        

# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_YgLdgRDQT.jpg"
# The provided URL points to an image.

# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_rqF0G2_VC.jpg"
# The provided URL points to an image.
        



# "fileId": "65f215ba88c257da33c59dbf", "url": "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_sbOT9Vuem9.jpg"
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_sbOT9Vuem9.jpg"
# The provided URL points to an image.
        
# "fileId": "65f21c6888c257da33e12efa", "url": "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_WxlGkkFM6.jpg"
# ❯ python3 002-python-imagekit-checkurl-revision-1.py "https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_WxlGkkFM6.jpg"