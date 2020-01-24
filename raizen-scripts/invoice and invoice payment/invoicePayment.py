import json

def addInvoicementPaymentJSON(amount,oder_id,commission,fee_amount):
    invoicePayment={
    "InvoicePayment": {
        "@url": "https://api.fortnox.se/3/invoicepayments/1",
        "Amount": amount,
        "ExternalInvoiceReference2":oder_id, 
        "WriteOffs": [commission, fee_amount]       
    }
    }
    #This is will convert dictionary to python
    dump_invoicePayment = json.dumps(invoicePayment)
    #this will return JSON File
    return dump_invoicePayment





import pandas as pd 
import json
excel_file = 'report-20191126T2222.xlsm'
sale_report = pd.ExcelFile(excel_file)
# DATAFRAME FOR SERVICES SHEET
services_dataframe = sale_report.parse('ServiceFees') 
services_json =services_dataframe.to_json(orient='records')
services_data = json.loads(services_json)


# DATAFRAME FOR ROWS SHEET
rows_dataframe = sale_report.parse('Rows')
rows_json = rows_dataframe.to_json(orient='records')
rows_data = json.loads(rows_json)


# incase that there are multliple number of data you can use for loop to do it 
for index in range(len(rows_data)):
    #You can get this part also if there are no multiple number of data 
    commission =rows_data[index]["Commission"]
    oder_id = services_data[index]["OrderID"]
    fee_amount = services_data[index]["FeeAmount"]
    total_sales_amount = float(rows_data[index]["InvoicedAmount"])
    total_fees = float(commission) + float(fee_amount)
    vat_fee = (total_fees *.25)
    amount = total_sales_amount - (total_fees+vat_fee)    
    addInvoicementPaymentJSON(amount,oder_id,commission,fee_amount)
    #upto here
    

    

