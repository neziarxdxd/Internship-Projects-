import requests
import json

def bookKeep(number):
    try:
        r = requests.put(
            url= "https://api.fortnox.se/3/invoices/{number}/bookkeep".format(number =number)
        )
    except:
        print("LORD TULUNGAN MOKO ",r.content)

def send_request():
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
                "Invoice":{
                    "InvoiceRows":[{
                           "DeliveredQuantity": "1",
                           "Description": "RAIZEN via Cdon",
                           "Price": 332.00,}
                    ],
                    "CustomerNumber": "991228106",
                     "ExternalInvoiceReference1":"23",
                     "Currency":"SEK",
                     "DeliveryAddress1": "Anunas",
                        "InvoiceDate": "2019-01-12",
                        "DueDate": "2019-02-11",
                         "DeliveryName": "Mr. Sangalang",
                         "DeliveryZipCode": "2009", 
                         "DeliveryCountry": "Philippines",
                         "DeliveryDate": "2019-03-11",




                            
       
     
 
                     
                     "VATIncluded":True,
                    }               

            })
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
        x=json.loads((r.content))
        return(x)
        
        
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')


data=send_request()

num=data['Invoice']['DocumentNumber']
bookKeep(num)

