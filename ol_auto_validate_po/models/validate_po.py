
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json

class AutoValidatePurchaseOrder(models.Model):
    _inherit="purchase.order"


    work_process = fields.Many2one('automated.sale' , string='Workflow Process' , domain="[('name' , '=' , 'standard')]")



    def button_confirm(self):
        super(AutoValidatePurchaseOrder, self).button_confirm()

        # Create supplier bill
        for order in self:
            #Saif
            if order.supplier_type_po == "local":
                # if order.work_process.name == 'standard':
            #     bill_vals = {
            #         'partner_id': order.partner_id.id,
            #         'invoice_origin': order.name,
            #         'move_type': 'in_invoice',
            #         # Add other necessary fields for the bill
            #         # ...
            #     }
            #     bill = self.env['account.move'].create(bill_vals)
            
                picking_obj = self.env['stock.picking'].search([('origin','=',order.name)])
    
                for pick in picking_obj:
                    for qty in pick.move_lines:

                        qty.write({
                        'quantity_done' : qty.product_uom_qty
                                })

                    pick.button_validate()
                        # pick._action_done()


                        # for line in order.order_line:
                        #     line.write({
                        #         'qty_delivered' : line.product_uom_qty,
                        #                 })
                        # pick.button_validate()
                    # order.action_view_picking()

                    # for line in order.picking_ids:
                    #     line.button_validate()
                    # order.picking_ids.button_validate()
                    # obj.process()
                bill = order.action_create_invoice()
                    # Validate the bill
                    # bill.action_post()
                    # raise UserError(str(bill))
                    # bill_obj = order.env['account.move'].search([('id','=',bill['id']),('move_type','=','in_invoice')])
                for invoice in order.invoice_ids:
                    invoice.invoice_date = fields.date.today()
                    invoice.action_post()
            # bi    ll_obj.action_post()

                    # Validate the delivery

