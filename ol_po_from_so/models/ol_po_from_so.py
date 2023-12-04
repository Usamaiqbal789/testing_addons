from odoo import models, api, fields, _
from odoo.exceptions import UserError


class POfromSO(models.Model):
    _inherit = 'sale.order'

    custom_po_id = fields.One2many('purchase.order','so_ids', string='Related PO')
    po_count = fields.Integer(compute='_compute_po_count', string='Purchase Order Count')


    
    def po_creation(self):

        po = self.env['purchase.order'].create({
            'partner_id':7633,
            'so_ids':self.id,
        })

        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'purchase.order',
                'res_id': po.id
                }

    def action_view_purchase(self):
        
        for rec in self:
            po_related_so = [i.id for i in rec.custom_po_id]
            # raise UserError(invoice_related_attachment)

            return {
                'name': 'Purchase Order related Sale Order',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'purchase.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', po_related_so)],

            }

    @api.depends('custom_po_id')
    def _compute_po_count(self):
        for record in self:
            record.po_count = len(record.custom_po_id)

class POidfromSO(models.Model):
    _inherit = 'purchase.order'

    so_ids = fields.Many2one('sale.order', string='Related SO')
