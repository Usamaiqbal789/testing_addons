from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountPaymentRegisterFields(models.TransientModel):
    _inherit = "account.payment.register"

    #Hot Fix
    receive_amount = fields.Float(string="Receive Amount")
    return_amount = fields.Float(string="Return Amount",  compute="_compute_return_amount")
    payment_mode = fields.Char(string="Pament_mode")

    #Hot fix
    @api.depends("receive_amount")
    def _compute_return_amount(self):
        for rec in self:
            if rec.receive_amount:
                rec.return_amount = rec.receive_amount - rec.amount
            else:
                rec.return_amount = 0