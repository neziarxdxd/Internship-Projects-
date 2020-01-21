import requests
import json

def send_request():
    # Invoices (POST https://api.fortnox.se/3/invoices)

    try:
        r = requests.post(
            url="https://api.fortnox.se/3/invoices",
            headers = {
                "Access-Token":"61cf63ae-4ab9-4a95-9db5-753781c4f41f",
                "Client-Secret":"3Er4kHXZTJ",
                "Content-Type":"application/json",
                "Accept":"application/json",
            },
            data = json.dumps({
                "Invoice": {
                    "InvoiceRows": [
                        {
                            "DeliveredQuantity": "10.00",
                            "ArticleNumber": "66892"
                        }
                    ],
                    "CustomerNumber": "100"
                }
            })
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
x= send_request()
print(x)

