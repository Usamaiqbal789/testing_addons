from odoo import fields, models, api, _


class InvoiceCustomFields(models.Model):
    _inherit = "account.move"

    lpo = fields.Char(string="LPO")
    remarks = fields.Char(string="Remarks")

    invoice_name = fields.Char(string='Invoice Name', compute='_compute_invoice_name')

    #invoice credit without leterhead
    epson_print = fields.Boolean(string="EPSON Print")


    #invoice no on credit note
    @api.depends('invoice_origin')
    def _compute_invoice_name(self):
        for record in self:
            if record.move_type == "out_refund":
                sale_order = self.env['sale.order'].search([('name', '=', record.invoice_origin)])
                if sale_order.invoice_ids:
                    record.invoice_name = sale_order.invoice_ids[0].name
                else:
                    record.invoice_name = ''
            else:
                record.invoice_name = ''