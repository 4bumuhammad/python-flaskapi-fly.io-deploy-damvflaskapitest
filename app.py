# import library
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

        # reference https://github.com/bitmario/uuid0
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