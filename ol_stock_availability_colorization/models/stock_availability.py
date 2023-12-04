from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockAvailable(models.Model):
    _inherit = 'sale.order.line'

    check_stock = fields.Boolean(string="Check Stock", readonly=True)

    @api.onchange('product_id', 'product_uom_qty')
    def stock_available_check(self):
        for line in self:
            product = line.product_id
            quantity = line.product_uom_qty
            warehouse = line.order_id.warehouse_id
            warehouse_product = warehouse.lot_stock_id.quant_ids
            check_stock = True  # Initialize check_stock to True

            for exist_product in warehouse_product:
                if product.id == exist_product.product_id.id:
                    if quantity <= exist_product.available_quantity:
                        check_stock = False  # Set to False only if the condition is met

                line.check_stock = check_stock  # 

    # @api.onchange('product_id', 'product_uom_qty')
    # def stock_available_check(self):
    #     warehouse = self.order_id.warehouse_id
    #     for line in self:
    #         product = line.product_id
    #         quantity = line.product_uom_qty
    #         warehouse_product = warehouse.lot_stock_id.quant_ids
    #         for exist_product in warehouse_product:
    #             if (product.id) == (exist_product.product_id.id):
    #                 if quantity <= (exist_product.available_quantity):
    #                     line.check_stock = False
    #                 else:
    #                     line.check_stock = True
    #             else:
    #                 line.check_stock = True
        #     else:
        #         line.check_stock = True
        # else:
        #     line.check_stock = True

                

class StockAvailable(models.Model):
    _inherit = 'sale.order'
    
#     @api.model
#     def stock_available_check(self):
#         for rec in self:
#             warehouse = rec.warehouse_id
#             for line in rec.order_line:
#                 product = line.product_id
#                 warehouse_product = warehouse.lot_stock_id.quant_ids
#                 for exist_product in warehouse_product:
#                     if product.id == exist_product.product_id.id:
#                         if line.product_uom_qty <= exist_product.available_quantity:
#                             line.check_stock = False
#                         else:
#                             line.check_stock = True
#                     else:
#                         line.check_stock = True

            