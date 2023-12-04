from odoo import models, fields, api, _

class SaleOrderDisplayPrice(models.Model):
    _inherit = 'sale.order.line'

    display_qty =fields.Integer(string="DQ")
    display_tax = fields.Float(string="DT")


    @api.onchange('cus_unit_price', 'display_qty','tax_id')
    def _onchange_display_tax(self):
        for rec in self:
            if rec.tax_id:
                dt = rec.display_qty* rec.cus_unit_price * ((rec.tax_id.amount)/100)
                rec.display_tax = dt
            else:
                rec.display_tax= 0

    @api.onchange('cus_unit_price', 'display_qty', 'display_tax')
    def _onchange_cus_total(self):
        for rec in self:
            if rec.display_qty:
                rec.cus_sub_total = (rec.cus_unit_price*rec.display_qty) 
            else:
                rec.cus_sub_total=0

    # @api.onchange('display_price')
    @api.model
    def _onchange_total_tax(self):
        total_tax = 0
        for rec in self:
            if rec.display_tax:
                total_tax += rec.display_tax
            else:
                total_tax = total_tax
            rec.order_id.amount_tax = total_tax

    # @api.onchange('cus_sub_total','display_tax','display_qty')
    @api.model
    def _onchange_display_fields(self):
        invoice = self.env['account.move'].search([('invoice_origin', '=',self.order_id.name)])
        for rec in self:
            for line in invoice:
                line.write({
                'display_qty': rec.display_qty,
                'display_price': rec.cus_unit_price,
                'display_tax': rec.display_tax,
                'dp_total':rec.cus_sub_total
                # Set custom field values here
            })


class SaleOrderDisplayPrice(models.Model):
    _inherit = 'sale.order'

    cus_tax = fields.Float(string="Customer Tax")

    @api.onchange('order_line')
    def _onchange_cus_tax(self):
        for order in self:
            display_tax = sum(order.order_line.mapped('display_tax'))
            order.cus_tax = display_tax


class InvoiceDisplayPrice(models.Model):
    _inherit = 'account.move.line'

    display_qty =fields.Integer(string="DQ")
    display_price =fields.Float(string="DP")
    display_tax = fields.Float(string="DT")
    dp_total = fields.Float(string='DPT')

     


    @api.onchange('display_price', 'display_qty','tax_ids')
    def _onchange_display_tax(self):
        for rec in self:
            if rec.tax_ids:
                dt = rec.display_qty* rec.display_price * ((rec.tax_ids.amount)/100)
                rec.display_tax = dt
            else:
                rec.display_tax= 0

    @api.onchange('display_price', 'display_qty', 'display_tax')
    def _onchange_cus_total(self):
        for rec in self:
            if rec.display_qty:
                rec.dp_total = (rec.display_price*rec.display_qty) 
            else:
                rec.dp_total=0
    
class InvoiceDisplayTotal(models.Model):
    _inherit = 'account.move'

    cus_untax_amount = fields.Monetary(string="Customer Untaxed Amount")
    cus_discount = fields.Monetary(string="Customer Discount")
    cus_tax = fields.Monetary(string="Customer Tax")
    cus_total = fields.Monetary(string="Customer Total")
    amount_in_words_dummy = fields.Char(string='Amount in Words', compute='get_amount_in_words_dummy')
    cus_name = fields.Char(string="Customer Name")
    cus_phone = fields.Char(string="Customer Phone No: ", required=False)
    cus_required = fields.Boolean(string="Customer Required")

    @api.onchange('move_type')
    def _onchange_type(self):
        if self.move_type == 'out_refund': 
            self.cus_required = True
        else:
            self.cus_name = False
            self.cus_phone = False
            self.cus_required = False
    
    @api.depends('cus_total')
    def get_amount_in_words_dummy(self):
        for rec in self:
            rec.amount_in_words_dummy = str(rec.currency_id.amount_to_text(rec.cus_total))


    @api.onchange('invoice_line_ids')
    def _onchange_cus_tax(self):
        for order in self:
            tax = sum(order.invoice_line_ids.mapped('display_tax'))
            order.cus_tax = tax

    @api.onchange('invoice_line_ids')
    def _compute_cus_untax_amount(self):
        for order in self:
            sub_total = sum(order.invoice_line_ids.mapped('dp_total'))
            order.cus_untax_amount = sub_total - (sub_total*(order.discount_rate/100))


    @api.onchange('invoice_line_ids')
    def _compute_cus_discount(self):
        for order in self:
            sub_total = sum(order.invoice_line_ids.mapped('dp_total'))
            order.cus_discount = (sub_total*(order.discount_rate/100))

    @api.onchange('invoice_line_ids')
    def _compute_cus_total(self):
        for order in self:
            total = sum(order.invoice_line_ids.mapped('dp_total'))
            tax = sum(order.invoice_line_ids.mapped('display_tax'))
            order.cus_total = total+ tax