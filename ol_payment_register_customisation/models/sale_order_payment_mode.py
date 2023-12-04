from odoo import models, fields, api


class CustomerPaymentMode(models.Model):
    _inherit="sale.order"

    payment_mode = fields.Many2one(comodel_name="account.payment.mode", string="Payment Mode")

    customer_total = fields.Float(string="Customer Total")

    @api.onchange("amount_total")
    def _onchange_customer_total(self):
        for rec in self:
            cus_total = 0
            if rec.order_line:
                for line in rec.order_line:
                    if line.cus_sub_total:
                        cus_total += line.cus_sub_total
                    else:
                        cus_total = cus_total

            rec.customer_total = cus_total - rec.amount_discount + rec.amount_tax 

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.payment_mode = self.partner_id.payment_mode.id



