from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError

class ProductTemplateDetailedType(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Char(string='Product Type', required=False)

# class ProductVarientRef(models.Model):
#     _inherit = 'product.product'
    
#     @api.model
#     def create(self, vals):
#         # print(vals.get('name_seq'))
#         if vals.get('own_ref_no', _('New')) == _('New'):
#             vals['own_ref_no'] = self.env['ir.sequence'].next_by_code('product.product') or _('New')
#         result = super(ProductVarientRef, self).create(vals)
#         # result = self.create(vals)
#         return result