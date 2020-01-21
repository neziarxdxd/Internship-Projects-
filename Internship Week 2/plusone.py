
import requests

def send_request():
    # Invoices (GET https://api.fortnox.se/3/invoices/203)

    try:
        r = requests.get(
            url="https://api.fortnox.se/3/invoices/203",
            headers = {
                "Access-Token":"81cf63ae-4ab9-4b95-9db5-754780c4f61f",
                "Client-Secret":"7Er4jHXZVJ",
                "Content-Type":"application/json",
                "Accept":"application/json",
            },
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

send_request()