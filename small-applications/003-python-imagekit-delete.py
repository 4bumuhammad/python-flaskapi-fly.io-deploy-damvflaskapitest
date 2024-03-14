import sys
from imagekitio import ImageKit

class ImageUploader:
    def __init__(self, private_key, public_key, url_endpoint):
        self.imagekit = ImageKit(
            private_key=private_key,
            public_key=public_key,
            url_endpoint=url_endpoint
        )

    def delete(self, file_id):
        try:
            print("- Deleting the file from the ImageKit repository...")
            delete_response = self.imagekit.delete_file(file_id=file_id)
            print("- File deleted successfully.")
            return delete_response.response_metadata.raw
        except Exception as e:
            print("- Failed to delete file:", str(e))
            return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python_imagekit_delete.py <file_id>")
        sys.exit(1)

    private_key = 'private_tMllcpEGq4gf7TzbqEWpqQzupac='
    public_key = 'public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA='
    url_endpoint = 'https://ik.imagekit.io/2fbeg9wdr'

    file_id_to_delete = sys.argv[1]
    uploader = ImageUploader(private_key, public_key, url_endpoint)

    # Attempt to delete the file using the provided file ID
    deletion_result = uploader.delete(file_id_to_delete)
    if deletion_result:
        print("Deletion result:", deletion_result)
