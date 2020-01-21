
Invoice Object Field Mapping:
https://developer.fortnox.se/documentation/resources/invoices/
Rows Tab
PaymentBooked = InvoiceDate
OrderID = ExternalInvoiceReference2
InvoicedAmount = Total
Currency = Currency

VATIncluded = True
Invoice Row Description = "Sales via Cdon Marketplace"


Invoice Payment Object Field mapping:
https://developer.fortnox.se/documentation/resources/invoice-payments/
Rows Tab
Commission = Writeoff
ServiceFees tab
OrderID = ExternalInvoiceReference2 
FeeAmount = Writeoff


Formula for Paid Amount in Invoice payment
**Amount - Amount of the payment
In order to find how much money the merchant was paid by Cdon, we must reduce the commission and service fee amount from the total sales amount.

TotalFees = Commision + Servicefee 
VATFee = TotalFee * 0.25
Amount = TotalSalesAmount - (TotalFees + VATFee )

So for this sale the invoice payment Amount is 332.66 SEK.
Example:
TotalFees = 51.072 + 2  is 53.072
VATFee = 53.072 * 0.25 is 13.268
399 - (53.072 +13.268 ) = 332.66
