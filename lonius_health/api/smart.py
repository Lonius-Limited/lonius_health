import requests
import json

BASE_URL = "https://data.smartapplicationsgroup.com/api/smartlink/json"
api_key = ""

def get_member_profile(patient_id):
    r = requests.get("{}/getmemberprofile".format(BASE_URL), 
            params={"patientid":patient_id}, 
            headers={"X-Gravitee-Api-Key": api_key}).json()
    return r


def get_benefits(data):
    return data["Benefits"]["Benefit"]


def submit_invoice(patient_id):
    global_id = get_member_profile()["AdmissionInformation"]["B1"]["global_id"]
    r = requests.get("{}/submitinvoice".format(BASE_URL), 
            params={"patientid":patient_id, "globalid": global_id},
            headers={"X-Gravitee-Api-Key": api_key},).json()
    


def build_claim(invoice):
    s = {}
    with open('./sample-claim.json') as f:
        s = json.loads(f.read())
    

    return {
        "":""
    }