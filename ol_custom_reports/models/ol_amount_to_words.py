from odoo import models, fields, api, _
 

class AmountToWords(models.Model):
    _inherit = 'account.move'

    amount_in_words = fields.Char(string='Amount in Words', compute='get_amount_in_words')

    @api.depends('amount_total')
    def get_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount_total))

class AmountToWords_Sale(models.Model):
    _inherit = 'sale.order'

    amount_in_words = fields.Char(string='Amount in Words', compute='get_amount_in_words')

    #invoice credit without leterhead
    epson_print = fields.Boolean(string="EPSON Print")

    @api.depends('amount_total')
    def get_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount_total))

class StockMove(models.Model):
    _inherit = 'stock.move'

    amount_in_words = fields.Char(string='Amount in Words')

    unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price")

    @api.depends('product_id', 'origin')
    def _compute_unit_price(self):
        for line in self:
            if line.origin:
                sale_order = self.env['sale.order'].search([('name', '=', line.origin)])
                for sale_line in sale_order.order_line:
                    if line.product_id == sale_line.product_id:
                        line.unit_price = sale_line.price_subtotal
                        break
                else:
                    line.unit_price = 0
            else:
                line.unit_price = 0


class StockPicking_tax(models.Model):
    _inherit = 'stock.picking'

    amount_in_words = fields.Char(string='Amount in Words', compute='get_amount_in_words')
    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount")

    #invoice credit without leterhead
    epson_print = fields.Boolean(string="EPSON Print")

    @api.depends('move_ids_without_package')
    def _compute_tax_amount(self):
        for line in self:
            sale_order = self.env['sale.order'].search([('name', '=', line.origin)])
            line.tax_amount = sale_order.amount_tax

    @api.depends('move_ids_without_package')
    def get_amount_in_words(self):
        for rec in self:
            sale_order = self.env['sale.order'].search([('name', '=', rec.origin)])
            if sale_order:
                rec.amount_in_words = str(sale_order.currency_id.amount_to_text(sale_order.amount_total))
            else:
                rec.amount_in_words = ''

