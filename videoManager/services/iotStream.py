import requests
import json


def sendIot(device,token,msgtp,message):
	pass
	url="https://iotmmss0018881710trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/"+device
	headers={'Content-Type':'application/json',
			'Cache-Control':'no-cache',
			'Authorization':'Bearer '+token}	
	data={"mode":"sync",
			"messageType":msgtp,
			"messages":message}
	r=requests.post(url,data=json.dumps(data),headers=headers)
	print("status_code",r.status_code)
	print("response", r.text)