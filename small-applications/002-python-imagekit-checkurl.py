import requests
import sys

class ImageChecker:
    def __init__(self):
        pass

    def is_url_image(self, image_url):
        img_formats = ("image/png", "image/jpeg", "image/jpg")
        try:
            r = requests.head(image_url)
            if r.headers["content-type"] in img_formats:
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

    # Check if the provided URL points to an imageß
    if checker.is_url_image(image_url):
        print("The provided URL points to an image.")
    else:
        print("The provided URL does not point to an image or cannot be reached.")
