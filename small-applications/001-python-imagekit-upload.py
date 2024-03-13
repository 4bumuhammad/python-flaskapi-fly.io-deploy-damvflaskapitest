import io
import base64
import json
from PIL import Image
from imagekitio import ImageKit


class ImageUploader:
    def __init__(self, private_key, public_key, url_endpoint):
        self.imagekit = ImageKit(
            private_key=private_key,
            public_key=public_key,
            url_endpoint=url_endpoint
        )

    def upload(self, image_pil, filename):
        result = {}
        try:
            print('- Uploading the result image to the ImageKit repository ...')
            buffer = io.BytesIO()
            image_pil.save(buffer, format="PNG")
            buffer.seek(0)
            image_bytes = buffer.getvalue()

            print('- Convert the result image to base64.')
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            print('- Perform upload to ImageKit repository ...')
            resp = self.imagekit.upload_file(
                file=image_base64,
                file_name=f"{filename}.jpg"
            )

            result['status'] = 'Success'
            result['fileId'] = resp.file_id
            result['url'] = resp.url
            result['height'] = resp.height
            result['width'] = resp.width
            result['size'] = resp.size

            print('- Upload to ImageKit repository successful.')

        except Exception as e:
            result['status'] = 'Unsuccessful'
            result['error'] = str(e)
            print('- Upload to ImageKit repository failed:', str(e))

        return result


if __name__ == "__main__":
    private_key = 'private_tMllcpEGq4gf7TzbqEWpqQzupac='
    public_key = 'public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA='
    url_endpoint = 'https://ik.imagekit.io/2fbeg9wdr'

    file_path = './car-green.png'
    image_pil = Image.open(file_path)

    uploader = ImageUploader(private_key, public_key, url_endpoint)
    result_json = uploader.upload(image_pil, filename='mobil-hijau')
    print(json.dumps(result_json))
