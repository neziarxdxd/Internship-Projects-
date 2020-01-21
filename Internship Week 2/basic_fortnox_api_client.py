import json
import logging
import os
import re
import sys
import time
import requests
from datetime import datetime, timedelta



logger = logging.getLogger('fortnox_api_app')


class FortnoxAPI:

    def createCustomer(self, name, customer_data=None, **kwargs):
            # Customer (POST https://api.fortnox.se/3/customers)
            customer = {"Name": str(name)}
            if customer_data and isinstance(customer_data, dict):
                customer.update(customer_data)

                post_data = {
                    "Customer": customer
                }

                response = self.get_response('customers', method='post', data=post_data)
                if response and response.status_code == 201:
                    return json.loads(byte_to_string(response.content))['Customer']['CustomerNumber']
                    
                    
                    
    def createInvoiceCdon(self, date, amount, shopname, customerNumber,):
           # Invoices (POST https://api.fortnox.se/3/invoices)
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
                   "YourReference": str(orderId),
                   "InvoiceDate": (datetime.strptime(str(date), "%Y-%m-%d") + timedelta(days=-30)).date().__str__(),
                   "DueDate": str(date),
               }
           }

           response = self.get_response('invoices', method='post', data=post_data)
           if response:
               invoice_data = json.loads(byte_to_string(response.content)).get('Invoice', None)
               if invoice_data and response.status_code == 201:
                   invoice_id = invoice_data['DocumentNumber']
                   invoice = self.bookkeepInvoice(invoice_id)
                   if invoice:
                       return invoice
            
            
            
            
            
            
    def bookkeepInvoice(self, invoiceId, logger=None):
        # Invoice (POST https://api.fortnox.se/3/invoices/{id}/bookkeep)
        fn_name = sys._getframe(0).f_code.co_name
        response = self.get_response(f'invoices/{invoiceId}/bookkeep', method='put')
        content = json.loads(byte_to_string(response.content))
        if response.status_code == 200:
            return content["Invoice"]
        else:
            if logger:
                logger(
                    f"Bookkeep invoice failed!: {content!r}",
                    type_info="script",
                    status=False,
                    fn_name=fn_name,
                    line_no=get_lineno())          
            
            


    
    def createInvoicePaymentCdon(self, accountNumber, providerFee, feeFrom, Amount, amountDiscrepancy, invoiceNumber,
                                   date, feeInSek, vatFeeInSek, feeAcct=None, currencyAmt=None):
        # invoicepayments (POST https://api.fortnox.se/3/invoicepayments)
        PaymentDate = date
        post_data = {
            "InvoicePayment": {
                "Amount": Amount,
                "InvoiceNumber": invoiceNumber,
                "PaymentDate": PaymentDate,
                "ModeOfPaymentAccount": accountNumber,
                "WriteOffs": [
                    {
                        "Amount": feeInSek,
                        "AccountNumber": providerFee,
                        "TransactionInformation": "Avgifter Cdon"
                    },
                ]
            }
        }
        if vatFeeInSek:
            post_data["InvoicePayment"]["WriteOffs"].append({
                "Amount": vatFeeInSek,
                "AccountNumber": feeAcct,
                "TransactionInformation": f"{feeFrom} Moms Cdon Avgifter"
            })

        if currencyAmt:
            if 'AmountCurrency' in post_data['InvoicePayment']:
                post_data['InvoicePayment']['AmountCurrency'] = currencyAmt
            else:
                post_data['InvoicePayment'].setdefault('AmountCurrency', currencyAmt)
        else:
            post_data['InvoicePayment']['WriteOffs'].append({
                "Amount": amountDiscrepancy,
                "AccountNumber": 3740,
                "TransactionInformation": "Sammanlagd fakturabeloppsskillnad"
            })

        response = self.get_response('invoicepayments', method='post', data=post_data)
        if response:
            content = json.loads(byte_to_string(response.content))
            if (response.status_code == 400):
                status = False
                fee_acct = None
                err_msg = content["ErrorInformation"]["message"]
                print((err_msg))
                if 'Angivet bortskrivningskonto "%s" är inte aktivt' % accountNumber == err_msg:
                    status = self.activateAccount(accountNumber)
                elif 'Angivet bortskrivningskonto "%s" är inte aktivt' % providerFee == err_msg:
                    status = self.activateAccount(providerFee)
                elif 'Angivet bortskrivningskonto "3740" är inte aktivt' == err_msg:
                    status = self.activateAccount(3740)
                elif 'Angivet bortskrivningskonto "2640" är inte aktivt' == err_msg:
                    fee_acct = 2641
                if status or fee_acct:
                    return self.createInvoicePaymentCdon(accountNumber, providerFee, feeFrom, Amount,
                                                           amountDiscrepancy, invoiceNumber, date, feeInSek,
                                                           vatFeeInSek, feeAcct=fee_acct, currencyAmt=currencyAmt)
                return content
            invoicepayment_data = content.get("InvoicePayment", {})
            if invoicepayment_data and "Number" in invoicepayment_data:
                return self.bookkeepInvoicePayment(invoicepayment_data['Number'])

    




    def bookkeepInvoicePayment(self, invoiceId, financialyeardate=None):
        # All Invoice Payments must be followed by a Bookkeep Action in order to change 
        # the status of the invoice payment from a draft to a registered invoicepayment
        # invoicepayments (POST https://api.fortnox.se/3/invoicepayments)
      
        payload = {}
        if financialyeardate:
            payload.setdefault('financialyeardate', financialyeardate)

        res = self.get_response(
            f'invoicepayments/{invoiceId}/bookkeep',
            method='put',
            params=payload)

        acct_inactive_err = re.compile('Konto "(\w+)" är inte aktivt.')

        if res is not None:
            content = json.loads(byte_to_string(res.content))
            if content and "ErrorInformation" in content:
                if "message" in content["ErrorInformation"]:
                    err_msg = content["ErrorInformation"]["message"]
                else:
                    err_msg = content["ErrorInformation"]["Message"]
                match_acct_no = acct_inactive_err.findall(err_msg)
                if match_acct_no:
                    status = self.activateAccount(
                        match_acct_no[0],
                        financialyeardate=PaymentDate)
                    if status:
                        content = selff.bookkeepInvoicePayment(
                            invoiceId,
                            financialyeardate=financialyeardate)
            if res.status_code == 200:
                print('Bookkeep invoicepayment')
            return content        
            
           
 
            
#Other functions that might come in handy futurewise
            


    def activateAccount(self, acctId, financialyeardate=None):
        # Account (PUT https://api.fortnox.se/3/accounts/1070)
        payload = {}
        if financialyeardate:
            payload.setdefault('financialyeardate', financialyeardate)

        post_data = {
            "Account": {
                "Active": True,
            }
        }
        response = self.get_response(f"accounts/{acctId}", method="put", data=post_data, params=payload)
        if response and response.status_code == 200:
            return True
        return False                   




class FortnoxAPIException(Exception):
    """An error occurred in the Fortnox API """

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        super(FortnoxAPIException, self).__init__(*args, **kwargs)

    def get_response(self):
        return self.response

    def get_content(self):
        if self.response is not None:
            return json.loads(byte_to_string(self.response.content))


fortnox = FortnoxAPI()
x = fortnox.createCustomer("Raizen")
print(x)
