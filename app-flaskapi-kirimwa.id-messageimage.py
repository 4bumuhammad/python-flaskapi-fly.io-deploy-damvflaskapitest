# - - - - - - - - - - - - - - - - - - - - - - - - -
# Standard flash data formulir
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
# - - - - - - - - - - - - - - - - - - - - - - - - -

app = Flask(__name__)
api = Api(app)

CORS(app)

class AppResource(Resource):
    def post(self):
        # Pastikan bidang yang diharapkan ada dalam data formulir
        if "token_kirimwaid" in request.form:
            _token_kwi = request.form["token_kirimwaid"]
            _phone_numb = request.form["phone_number"] 
            _device_id = request.form["device_id"]
            response = {}

            response["_token_kwi"] = _token_kwi
            response["_phone_numb"] = _phone_numb
            response["_device_id"] = _device_id

            payload_text = "Assalamualaikum Warrahmatullah Wabarakatuh"

            url = 'https://api.kirimwa.id/v1/messages'
            hed = {'Authorization': 'Bearer ' + _token_kwi}
            data = {"phone_number": _phone_numb, \
                    "message": payload_text, \
                    "device_id": _device_id, \
                    "message_type": "text" \
                    }  
            try:
                i = 1
                tried = True
                while tried == True:

                    resp_send = requests.post(url, json=data, headers=hed)
                    print('--> i : {0}'.format(str(i)))
                    print('--> Response Send message KirimWA.id -- Code:', resp_send.status_code)
                    print('--> Response Send message KirimWA.id -- Detail:',resp_send.json())

                    if i < 4 and resp_send.status_code != 201:
                        i = i + 1
                        tried = True
                    else:
                        tried = False
                    
                response['code'] = resp_send.status_code
                response['detail'] = resp_send.json() 

            except Exception as er:
                response["error"] = str(er) 
            return response
        else:
            return {"error": "Data 'token_kirimwaid' tidak ditemukan dalam permintaan"}, 400


# setup resource
api.add_resource(AppResource, "/api", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5006)
