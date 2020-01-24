import requests
import json

def send_request():
    # Customer (POST https://api.fortnox.se/3/customers)

    try:
        r = requests.post(
            url="https://api.fortnox.se/3/customers",
            headers = {
                "Access-Token":"61cf63ae-4ab9-4a95-9db5-753781c4f41f",
                "Client-Secret":"3Er4kHXZTJ",
                "Content-Type":"application/json",
                "Accept":"application/json",
            },
            data = json.dumps({
                "Customer": {
                    "Name": "RAIZEN SANGALANG TESTING"
                }
            })
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
send_request()