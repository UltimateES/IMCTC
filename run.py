import requests
from requests.auth import HTTPDigestAuth
import json
import xmltodict
from datetime import datetime, timedelta
import time
import base64
import requests

def sendData(platetype,platenumber,platechar1,platechar2,platechar3):
    print(platetype,platenumber,platechar1,platechar2,platechar3)
    pass

CameraIP = "http://10.10.36.2"
CameraUser = "admin"
CameraPass = "TEKTRON@123"
CameraId = "10.10.36.2"
ServerURL = "http://10.10.24.224/Kashef/API/Kashef/VehicleLogs"


now = datetime.now() - timedelta(days = 1)
date_time = now.strftime("%Y%m%dT%H%M%S")
print(date_time)

lastDetectedVehicleTime = ""
while True:
    try:
        #print(date_time)
        url = CameraIP + '/ISAPI/Traffic/channels/1/vehicleDetect/plates/'
        data = "<AfterTime><picTime>"+date_time+"</picTime></AfterTime>"
        r=requests.get(url, data =data,auth=HTTPDigestAuth(CameraUser, CameraPass))
        #print(r.text)
        data_dict = xmltodict.parse(r.text)
        #print(data_dict)
        intx = 0
        try:
            print(len(data_dict["Plates"]["Plate"]))
            intx = isinstance(len(data_dict["Plates"]["Plate"]), int)
        except:
            pass

        if(intx):
            i = len(data_dict["Plates"]["Plate"])-1
            picName = data_dict["Plates"]["Plate"][i]["picName"]
            if(picName != lastDetectedVehicleTime):
                lastDetectedVehicleTime = picName
                print("New Vehicle Detected")
                plateNumberx = data_dict["Plates"]["Plate"][i]["plateNumber"]
                captureTime = data_dict["Plates"]["Plate"][i]["captureTime"]
                country = data_dict["Plates"]["Plate"][i]["country"]
                laneNo = data_dict["Plates"]["Plate"][i]["laneNo"]
                direction = data_dict["Plates"]["Plate"][i]["direction"]
                imageurl = CameraIP + "/doc/ui/images/plate/"+ picName+ ".jpg"
                print(imageurl)
                Base64Image = base64.b64encode(requests.get(imageurl).content)
                
                plateType = "1"
                plateNumber = plateNumberx[:-3]
                plateEnLetter1 = plateNumberx[-3]
                plateEnLetter2 = plateNumberx[-2]
                plateEnLetter3 = plateNumberx[-1]
                CameraIPx = CameraId
                CaptureTimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Country = "Saudi Arabia"
                PhotoB64 = Base64Image.decode('UTF-8')
                BodyParams = {
                            "plateType":"1", 
                            "plateNumber":plateNumber,
                            "plateEnLetter1":plateEnLetter1,
                            "plateEnLetter2":plateEnLetter2,
                            "plateEnLetter3":plateEnLetter3,
                            "CameraIP":CameraIPx,
                            "CaptureTimeStamp":CaptureTimeStamp,
                            "Country":Country,
                            "PhotoB64":PhotoB64,
                        }
                Resp = requests.post(ServerURL, json = BodyParams)
                print(Resp.text)
                
        now = datetime.now() - timedelta(days = 1) 
        date_time = now.strftime("%Y%m%dT%H%M%S")
        time.sleep(2)
    except:
        pass
