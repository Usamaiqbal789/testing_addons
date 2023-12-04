
from odoo import models, fields,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class AccountInvoiceStatus(models.Model):
    _inherit = "account.move"
    
    invoice_status = fields.Selection([('cash', 'Cash'),
                                       ('credit_sales', 'Credit Sales'),
                                       ('credit_card', 'Cash Card'),
                                       ('cheque', 'Cheque')],string="Invoice Status" , default = "cash")