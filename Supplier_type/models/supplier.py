
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json

class ext(models.Model):
    _inherit="product.product"

    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'), ('product', 'Storable Product')], string='Product Type', default='product', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')

class inheritPartner(models.Model):
    _inherit="res.partner"

    vendor_supplier_type = fields.Selection([
        ('local', 'Local'),
        ('import', 'Import')], string='Supplier Type', default='local')

class inheritPOrder(models.Model):
    _inherit="purchase.order"

    supplier_type_po = fields.Selection([
        ('local', 'Lpo'),
        ('import', 'Fpo')], string='Purchase Order/Lpo', default='local')

    @api.onchange('supplier_type_po')
    def _get_vendor_domain(self):
        self.partner_id = False
        local_vendor = self.env['res.partner'].search([('vendor_supplier_type','=',self.supplier_type_po)])
        local_vendor_ids =  local_vendor.ids
        return  {'domain':{'partner_id':[('id', 'in', local_vendor_ids)]}}
   



    
  