from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    cus_total = fields.Float(string="Customer Total", compute="_compute_cus_total")
    cus_sub_total = fields.Float(string="Customer Untaxed Amout", compute="_compute_cus_sub_total")
    cus_discount = fields.Float(string="Customer Discount", compute="_compute_cus_discount")


    @api.depends('order_line')
    def _compute_cus_sub_total(self):
        for order in self:
            sub_total = sum(order.order_line.mapped('cus_sub_total'))
            order.cus_sub_total = sub_total - (sub_total*(order.discount_rate/100))


    @api.depends('order_line')
    def _compute_cus_discount(self):
        for order in self:
            sub_total = sum(order.order_line.mapped('cus_sub_total'))
            order.cus_discount = (sub_total*(order.discount_rate/100))
            # order.cus_discount = (order.cus_total-order.cus_tax) - order.cus_sub_total

    @api.depends('order_line')
    def _compute_cus_total(self):
        for order in self:
            order.cus_total = sum(order.order_line.mapped('cus_sub_total')) + order.cus_tax

    
