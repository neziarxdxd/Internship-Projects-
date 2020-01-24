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
        


import pandas as pd 
import json
excel_file = 'report-20191126T2222.xlsm'
sale_report = pd.ExcelFile(excel_file)
# DATA FOR SERVICES SHEET
services_dataframe = sale_report.parse('ServiceFees') 
services_json =services_dataframe.to_json(orient='records')
services_data = json.loads(services_json)


# DATA FOR ROWS SHEET
rows_dataframe = sale_report.parse('Rows')
rows_json = rows_dataframe.to_json(orient='records')
rows_data = json.loads(rows_json)

for data in rows_data:    
    send_request(data["PaymentBooked"],data["OrderID"],data["InvoicedAmount"],data["Currency"])
