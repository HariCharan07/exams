import requests
from app.settings import MSG91_API_KEY


def sendsms(mobile_no, template):
    smsEndpoint = " https://api.msg91.com/api/sendhttp.php?authkey={0}&mobiles={1}&country=91&DLT_TE_ID=1307166131907545907&message={2}&route=4".format(MSG91_API_KEY,mobile_no, template)
    res = requests.get(smsEndpoint)
    print(res.text,"otp sent")
    return {"status":res.status_code, "message":res.text}