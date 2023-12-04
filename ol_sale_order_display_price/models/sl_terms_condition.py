from odoo import models, fields, api, _

class SaleOrderTermsAndCondition(models.Model):
    _inherit = 'sale.order'

    note_term =fields.Html(string="Quotation Terms And Conditions", default="Quotation Terms & Conditions<br>1. Ex-stock Subject to Availability Prior to Sales.<br>2. Prices Valid until 15 days.<br>3. Prices Quoted are in AED")
    advance_payment_term = fields.Char(string="Advance Payment Condition", default="50% of Advance Payment of order value")
    print_payment_term = fields.Boolean(string="Print Payment Term")
    print_part_no = fields.Boolean(string="Quotation with Part No")

class InvoiceWithPartNo(models.Model):
    _inherit = 'account.move'

    print_part_no = fields.Boolean(string="Invoice with Part No")

