from odoo import models, fields, api, _
from time import time

class AccountInvoice(models.Model):
    _inherit = 'account.move.line'

    ol_cus_unit_price = fields.Float(string="Customer Unit Price" , compute="_compute_cus_unit_price")
    ol_cus_sub_total = fields.Float(string="Customer Sub Total" )

    # in other info tab name other_tab there is a field source document search this in sale.order to get sale order and then get sale order lines and loop on this and get the cus_unit_price, cus_sub_total
    @api.depends('product_id', 'move_id')
    def _compute_cus_unit_price(self):
        for line in self:
            if line.move_id:
                sale_order = self.env['sale.order'].search([('name', '=', line.move_id.invoice_origin)])
                for sale_line in sale_order.order_line:
                    if line.product_id == sale_line.product_id:
                        line.ol_cus_unit_price = sale_line.cus_unit_price
                        line.ol_cus_sub_total = sale_line.cus_sub_total
                        break
                else:
                    line.ol_cus_unit_price = 0
                    line.ol_cus_sub_total = 0
            else:
                line.ol_cus_unit_price = 0
                line.ol_cus_sub_total = 0





