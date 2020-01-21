'''

"InvoiceData": PaymentBook,
"ExternalInvoiceReference2":OrderID,
"Total":InvoicedAmount,
"Curreny":Currency,
"VatIncluded":True,
"Invoice Row Description":"Sales via Cdon Marketplace"

'''

import pandas as pd 
import json
excel_file = 'report-20191126T2222.xlsm'
sale_report = pd.ExcelFile(excel_file)

# DATA FOR SERVICES 
services_dataframe = sale_report.parse('ServiceFees') 
services_json =services_dataframe.to_json(orient='records')

services_data = json.loads(services_json)
print("Data Frame for SERVICES")
print(services_dataframe)

# 
rows_dataframe = sale_report.parse('Rows')
rows_json = rows_dataframe.to_json(orient='records')
rows_data = json.loads(rows_json)


index = 0
commission =rows_data[index]["Commission"]
oder_id = services_data[index]["OrderID"]
fee_amount = services_data[index]["FeeAmount"]
total_sales_amount = float(rows_data[index]["InvoicedAmount"])

total_fees = float(commission) + float(fee_amount)
vat_fee = (total_fees *.25)
amount = total_sales_amount - (total_fees+vat_fee)
