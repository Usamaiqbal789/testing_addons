from odoo import models, api, fields, _
from odoo.exceptions import UserError


class CreditNoteReturn(models.Model):
    _inherit = 'stock.picking'

    def create_credit_note(self):

        sale_order = self.sale_id

        so_unit_price = {}

        for line in sale_order.order_line:
            so_unit_price[line.product_id.id] = line.price_unit

        inv_line = []
        
        for line in self.move_ids_without_package:

            inv_line.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_id.uom_id.id,
                    'price_unit': so_unit_price.get(line.product_id.id),
                    'quantity': line.quantity_done,
                    'tax_ids': [(6, 0, line.sale_line_id.tax_id.ids)]

                }))

            
        credit_note = self.env['account.move'].create({'partner_id': self.partner_id.id,
                                                    'move_type': 'out_refund',
                                                    'invoice_origin': sale_order.name,
                                                    'invoice_line_ids': inv_line,

                                                    })


class CreditFromTransfer(models.Model):
    _inherit = 'sale.order'

    
    credit_count = fields.Integer(compute='_compute_credit_count', string='Credit Notes')


    def action_view_credit_note(self):
        
        for rec in self:

            credit_notes = self.env['account.move'].search([('move_type','=','out_refund'),('invoice_origin','=',str(self.name))])
            

            credit_related_transfer = [i.id for i in credit_notes]
            # # raise UserError(invoice_related_attachment)

            return {
                'name': 'Credit Notes',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', credit_related_transfer)],

            }

    
    def _compute_credit_count(self):
        for record in self:
            credit_notes = self.env['account.move'].search([('move_type','=','out_refund'),('invoice_origin','=',str(self.name))])
            record.credit_count = len(credit_notes)