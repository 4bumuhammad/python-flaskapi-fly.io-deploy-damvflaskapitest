# Python fastapi fly.io deploy damvflaskapitest


#### files structure :

    ❯ tree -L 2 -I 'gambar-petunjuk|README.md'

        ├── Dockerfile
        ├── app.py
        ├── arial.ttf
        ├── fly.toml
        └── requirements.txt

        0 directories, 5 files

#### Begin Project :

    ❯ python -m venv venv

    ❯ source ./venv/bin/activate

    ❯ pip install flask
    ❯ pip install flask-restful
    ❯ pip install flask-cors
    ❯ pip install imagekitio
    ❯ pip install pillow
    ❯ pip install requests
    ❯ pip install segno
    ❯ pip install uuid0


#### &#x2B55; Reference :

- uuid0 - better timestamped UUIDs in Python --> `https://github.com/bitmario/uuid0`


### &#x1FAB6; code :

- python 

        ❯ vim app.py


            from crypt import methods
            from urllib import response
            from flask import Flask, request
            from flask_restful import Resource, Api
            from flask_cors import CORS

            import io
            import segno
            import uuid0
            import base64
            import requests
            from imagekitio import ImageKit
            from PIL import Image, ImageDraw, ImageFont, ImageOps

            app=Flask(__name__)

            api=Api(app)

            CORS(app)

            class AppResource(Resource):

                def generate(_self,_url_logo, _queue_numb, _date_caption):

                    uuid = uuid0.generate()
                    data_to_encode = "{0};{1}".format(uuid,_queue_numb)

                    qr_code = segno.make_qr(data_to_encode, error='H')
                    buffer = io.BytesIO()

                    qr_code.save(buffer, kind="png", finder_dark='#fc3d21', dark = '#0b3d91', scale=50) # color logo NASA
                    buffer.flush()
                    buffer.seek(0)
                    myimg = buffer.getvalue() 

                    img = Image.open(io.BytesIO(myimg)).convert("RGBA")
                    width, height = img.size
                    logo_size = 750

                    response = requests.get(_url_logo)
                    logo = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    buffer.close()

                    txt = Image.new('RGBA', logo.size, (255,255,255,0))
                    font_queue = ImageFont.truetype("arial.ttf", 220)
                    d = ImageDraw.Draw(txt)

                    logo_width, logo_height = logo.size 
                    left, top, right, bottom = font_queue.getbbox(_queue_numb)

                    textwidth = right - left
                    textheight = bottom

                    x=logo_width/2-textwidth/2
                    y=logo_height-textheight-250

                    d.text((x,y), _queue_numb, fill=(255,0,0, 185), font=font_queue, stroke_width=5)

                    watermarked = Image.alpha_composite(logo, txt)

                    buffer = io.BytesIO()
                    watermarked.save(buffer,format="PNG")
                    buffer.flush()
                    buffer.seek(0)
                    mylogo = buffer.getvalue() 

                    watermarked_logo = Image.open(io.BytesIO(mylogo)).convert("RGBA")
                    buffer.close()

                    xmin = ymin = int((width / 2) - (logo_size / 2))
                    xmax = ymax = int((width / 2) + (logo_size / 2))

                    watermarked_logo = watermarked_logo.resize((xmax - xmin, ymax - ymin))
                    img.paste(watermarked_logo, (xmin, ymin, xmax, ymax))

                    watermarked_logo.close()

                    caption1 = "QR ANTRIAN DOKTER PRAKTEK"
                    caption2 = "BEKASI, {0}".format(str(_date_caption))
                    caption3 = "PERHATIAN !"
                    caption4 = "Lakukan mendaftar kehadiran di lokasi 20 menit \nsebelum nomor antrian {0} Anda dipanggil.\n\nTerima kasih.".format(_queue_numb)

                    expanded_image = ImageOps.expand(img, border=(0,150,0,515), fill='white')
                    font_up = ImageFont.truetype('arial.ttf', 100)
                    font_CAPITAL = ImageFont.truetype('arial.ttf',75)
                    font_bottom = ImageFont.truetype('arial.ttf', 82)

                    draw_object = ImageDraw.Draw(expanded_image)
                    draw_object.text(xy=(width/2,143), text=caption1, fill=(0,0,0), font=font_up, anchor="mm")
                    draw_object.text(xy=(width/2,243), text=caption2, fill=(0,0,0), font=font_up, anchor="mm")

                    shape = [(200, height), (width - 200, height + 560)]
                    draw_object.rectangle(shape, width = 25, outline =(255,0,0,255))
                    draw_object.text(xy=(245,height + 43), text=caption3, fill=(255,0,0,255), font=font_CAPITAL, stroke_width=2)
                    draw_object.multiline_text(xy=(245,height + 130), text=caption4, fill=(255,0,0,255), font=font_bottom,spacing=20)

                    return uuid, expanded_image

                def upload(_self, imgPIL, _filename):
                    result = {}

                    print('- . . .')
                    print('- Start uploading the result image into the imageKit repository.')
                    imagekit = ImageKit(
                        private_key='private_tMllcpEGq4gf7TzbqEWpqQzupac=',
                        public_key='public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA=',
                        url_endpoint='https://ik.imagekit.io/2fbeg9wdr'
                    )

                    buffer = io.BytesIO()
                    imgPIL.save(buffer,format="PNG") 
                    buffer.seek(0)
                    myimage = buffer.getvalue() 

                    print('- Convert the result image to b64encode.')
                    image_base64 = base64.b64encode(myimage).decode('utf-8')
                    
                    print('- Performs an upload to the imageKit repositories.')

                    bErr = False
                    resp = None
                    try:
                        resp = imagekit.upload_file(
                            file = image_base64, 
                            file_name = "{}.jpg".format(_filename))        
                    except Exception as er:
                        bErr = True
                        result['status'] = 'Unsuccessful'
                        result['error'] = str(er)

                    if bErr == False:
                        result['status'] = 'Success'
                        result['fileId'] = resp.file_id
                        result['url'] = resp.url
                        result['height'] = resp.height
                        result['width'] = resp.width
                        result['size'] = resp.size

                    print('- Upload imageKit response status:', result['status'])
                    return result

                def delete(_self, _file_id):
                    imagekit = ImageKit(
                        private_key='private_tMllcpEGq4gf7TzbqEWpqQzupac=',
                        public_key='public_Gw9y5gNm5ZfCzIfa49kR3QUJ1dA=',
                        url_endpoint='https://ik.imagekit.io/2fbeg9wdr'
                    )
                    delete = imagekit.delete_file(file_id = _file_id)
                    return delete.response_metadata.raw

                def is_url_image(_self,image_url):
                    img_formats = ("image/png", "image/jpeg", "image/jpg")
                    r = requests.head(image_url)
                    if r.headers["content-type"] in img_formats:
                        return True
                    return False

                def post(self):
                    _token_kwi = request.form["token_kirimwaid"]
                    _phone_numb = request.form["phone_number"] 
                    _device_id = request.form["device_id"]
                    _caption = request.form['caption']
                    _queue_numb = request.form['queue_number']
                    _date_caption = request.form['date_caption']

                    response = {}

                    url_logo = 'https://i.ibb.co/K6BHQJd/output-onlinepngtools-3.png'
                    uuid, img_pil = self.generate(url_logo, _queue_numb, _date_caption)
                    resp_upload = self.upload(img_pil, 'myQRregist')
                    urlImg_upload = resp_upload['url']
                    img_pil.close()
                    print('--> Response ImageKit Upload','raw:',resp_upload)

                    url = 'https://api.kirimwa.id/v1/messages'
                    hed = {'Authorization': 'Bearer ' + _token_kwi}
                    data = {"phone_number": _phone_numb, \
                            "message": urlImg_upload, \
                            "device_id": _device_id, \
                            "message_type": "image", \
                            "caption": _caption \
                            }        

                    try:
                        i = 1
                        tried = True
                        while tried == True:
                            resp_send = requests.post(url, json=data, headers=hed)
                            print('--> i : {0}'.format(str(i)))
                            print('--> Response Send message KirimWA.id -- Code:', resp_send.status_code)
                            print('--> Response Send message KirimWA.id -- Detail:',resp_send.json())
                            if i < 4 and resp_send.status_code != 201 and self.is_url_image(urlImg_upload) == True:
                                i = i + 1
                                tried = True
                            else:
                                tried = False

                        response['uuid'] = str(uuid)
                        response['code'] = resp_send.status_code
                        response['detail'] = resp_send.json()            

                        if resp_send.status_code == 201:
                            delete = self.delete(resp_upload['fileId'])

                    except Exception as er:
                        response["error"] = str(er) 
                    return response 

            # setup resourcenya
            api.add_resource(AppResource, "/api", methods=["GET","POST"])

            if __name__ == "__main__":
                app.run(debug=True, host='0.0.0.0', port=5005)



### &#x1F31F; Test application in local

    ❯ python3 app.py

        * Serving Flask app 'app'
        * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on all addresses (0.0.0.0)
        * Running on http://127.0.0.1:5005
        * Running on http://192.168.100.XXX:5005
        Press CTRL+C to quit
        * Restarting with stat
        * Debugger is active!
        * Debugger PIN: 142-136-969


- Dockerfile


### &#x1F31F; Test application with Docker container



&#x1F535; list :




#### application :

- CURL :


- Postman :


#### Reset containers :

    ❯ docker rm -f $(docker ps -aq) && docker rmi -f $(docker images -q)






---

<p align="center">
    <img src="./gambar-petunjuk/fly-io-logo.svg" alt="fly-io-logo" style="display: block; margin: 0 auto;">
</p>


---

## Stages in deploying the application to fly.io


#### code :

- toml [Tom's Obvious Minimal Language]

        ❯ vim fly.toml


### check version :

    ❯ flyctl version


### &#x1F530; create Apps :

    ❯ flyctl apps create --name damvflaskapitest

check and watch for updates on the fly.io console dashboard



### &#x1F530; deploy Apps :

    ❯ flyctl deploy


check and watch for updates on the fly.io console dashboard


### &#x1F530; check

    ❯ flyctl status

    ❯ flyctl ips list

    ❯ flyctl services list


### &#x1F530; open :

    ❯ flyctl open


#### &#x1F535; postman : 


---

<p align="center">
    <img src="./gambar-petunjuk/well_done.png" alt="well_done" style="display: block; margin: 0 auto;">
</p>


---


### Remove Apps :



---


### Notes :

    ❯ pip list

        Package            Version
        ------------------ --------
        aniso8601          9.0.1
        blinker            1.7.0
        certifi            2024.2.2
        charset-normalizer 3.3.2
        click              8.1.7
        Flask              3.0.2
        Flask-Cors         4.0.0
        Flask-RESTful      0.3.10
        idna               3.6
        imagekitio         4.0.0
        itsdangerous       2.1.2
        Jinja2             3.1.3
        MarkupSafe         2.1.5
        pillow             10.2.0
        pip                22.0.4
        pybase62           1.0.0
        pytz               2024.1
        requests           2.31.0
        requests-toolbelt  0.10.1
        segno              1.6.1
        setuptools         58.1.0
        six                1.16.0
        urllib3            1.26.18
        uuid0              0.2.7
        Werkzeug           3.0.1