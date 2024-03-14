from imagekitio import ImageKit

# Informasi kredensial
private_key = 'private_tMllcpEGq4gf7TzbqEWpqQzupac='
public_key = 'public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA='
url_endpoint = 'https://ik.imagekit.io/2fbeg9wdr'
url_image = 'https://ik.imagekit.io/2fbeg9wdr/mobil-hijau_2MGgmanuQ.jpg'

# Inisialisasi ImageKit
imagekit = ImageKit(
    private_key=private_key,
    public_key=public_key,
    url_endpoint=url_endpoint
)

# Fungsi untuk membersihkan cache
def purge_cache(url):
    response = imagekit.purge_cache(url)
    if response.status == 'success':
        print("Cache berhasil dihapus untuk:", url)
    else:
        print("Gagal menghapus cache.")

# Memanggil fungsi untuk membersihkan cache
purge_cache(url_image)
