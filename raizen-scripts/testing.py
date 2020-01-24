import requests
import json

def send_request(PaymentBook, OrderID, InvoicedAmount,Currency):
    # Invoices (POST https://api.fortnox.se/3/invoices)

    try:
        r = requests.post(
            url="https://api.fortnox.se/3/invoices",
            headers = {
                "Access-Token":"f895dac6-9b6a-4885-8daa-2041512f0911",
                "Client-Secret":"I56Jh4yJSU",
                "Content-Type":"application/json",
                "Accept":"application/json",
            },
            data = json.dumps({
                "Invoice": {
                    "InvoiceRows": [
                        {
                            "InvoiceData": PaymentBook,
                            "ExternalInvoiceReference2":OrderID,
                            "Total":InvoicedAmount,
                            "Curreny":Currency,
                            "VatIncluded":True,
                            "Invoice Row Description":"Sales via Cdon Marketplace"
                        }
                    ]                    
                }
            })
        )
        print(r)
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')


post_data = {
               "Invoice": {
                   "InvoiceRows": [
                       {
                           "DeliveredQuantity": "1",
                           "Description": "Sales via Cdon",
                           "Price": amount
                       }
                   ],
                   "CustomerNumber": str(customerNumber),
                   "VATIncluded": "true",
                   
                   "InvoiceDate": (datetime.strptime(str(date), "%Y-%m-%d") + timedelta(days=-30)).date().__str__(),
                   "DueDate": str(date),
               }
           }
