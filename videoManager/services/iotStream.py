import requests
import json


def sendIot(device,token,msgtp,messages):
	pass
	url="https://iotMessageReceiver.cfapps.eu10.hana.ondemand.com/iotmms"
	headers={'Content-Type':'application/json',
			'Cache-Control':'no-cache',
			'Authorization':'Bearer '+token}	
	data={"device":device,
			"messageType":msgtp,
			"messages":messages}
	r=requests.post(url,data=json.dumps(data),headers=headers)
	print("status_code",r.status_code)
	print("response", r.text)