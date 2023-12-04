from odoo import models, fields,api
from odoo.exceptions import UserError


class ReconciledAccountPayment(models.Model):
    _inherit = 'account.payment'


