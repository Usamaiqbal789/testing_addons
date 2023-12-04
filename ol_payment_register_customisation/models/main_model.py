from odoo import models, fields, api, _


class AccountPaymentFields(models.Model):
    _inherit = "account.payment"

class SaleOrderCustomePrice(models.Model):
    _inherit = "sale.order.line"

    cus_unit_price = fields.Float(string="Customer Unit Price")
    cus_sub_total = fields.Float(string="Customer Sub Total")

    @api.onchange("cus_unit_price","product_uom_qty")
    def _onchange_cus_sub_total(self):
        for rec in self:
            if rec.cus_unit_price:
                rec.cus_sub_total = rec.cus_unit_price * rec.product_uom_qty
            else:
                rec.cus_sub_total = 0