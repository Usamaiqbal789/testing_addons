from odoo import fields, models, api, _
from odoo.exceptions import ValidationError



class SaleOrderLineSrno(models.Model):
    _inherit = "sale.order.line"

    sr_no = fields.Integer(string="Sr No", readonly=True,compute='_compute_sr_no')
    @api.depends("order_id.order_line")
    def _compute_sr_no(self):
        for index, line in enumerate(self):
            line.sr_no = str(index + 1)

    @api.constrains('price_unit')
    def _check_unit_price(self):
        for record in self:
            if record.price_unit == 0:
                raise ValidationError("Unit price cannot be zero.")


class InvoiceLinesSrno(models.Model):
    _inherit = "account.move.line"

    sr_no = fields.Integer(string="Sr No", readonly=True, compute='_compute_sr_no')

    @api.depends('move_id.line_ids')
    def _compute_sr_no(self):
        for index, line in enumerate(self):
            line.sr_no = str(index + 1)


class StockPickingSrno(models.Model):
    _inherit = "stock.move.line"

    sr_no = fields.Integer(string="Sr No", readonly=True, compute='_compute_sr_no')

    @api.depends("picking_id.move_line_ids")
    def _compute_sr_no(self):
        for index, line in enumerate(self):
            line.sr_no = str(index + 1)



class PurchaseOrderlineSrno(models.Model):
    _inherit = "purchase.order.line"

    sr_no = fields.Integer(string="Sr No", readonly=True, compute='_compute_sr_no')
    @api.depends('order_id.order_line')
    def _compute_sr_no(self):
        for index, line in enumerate(self):
            line.sr_no = str(index + 1)
