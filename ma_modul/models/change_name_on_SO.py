from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLineChangeName(models.Model):
    _inherit = "sale.order.line"


    product_name_in_sale_order_line =fields.Char(string="Description")
    @api.onchange('product_id')
    def onchange_serial(self):
        if self.product_id:
            self.product_name_in_sale_order_line = self.product_id.name


class PurchaseOrderLineChangeName(models.Model):
    _inherit = "purchase.order.line"


    product_name_in_purchase_order_line =fields.Char(string="Description")

    @api.onchange('product_id')
    def onchange_serial(self):
        if self.product_id:
            self.product_name_in_purchase_order_line = self.product_id.name
