from odoo import fields, models, api
from odoo.exceptions import UserError


class SaleOrderModification(models.Model):
    _inherit = "sale.order"

    remarks = fields.Char(string="Remarks")
    
    # @api.model
    # def _get_default_workflow_process_id(self):
    #     # default_workflow_process = self.env['automated.sale'].search([('name', 'ilike', 'Full Delivery')], limit=1)
    #     # return default_workflow_process.id if default_workflow_process else False
    #     raise UserError(self.env['automated.sale'].search([('name', 'ilike', 'Full Delivery')], limit=1).name)
    #     return self.env['automated.sale'].search([('name', 'ilike', 'Full Delivery')], limit=1).id

    work_process_order_id = fields.Many2one("automated.sale", string="Workflow Process")
    @api.onchange('warehouse_id','partner_id')
    def _onchange_other_field(self):
        # Update the work_process_order_id based on other_field's value
        for record in self:
            if record.warehouse_id.id == 6:
                record.work_process_order_id = self.env['automated.sale'].search([('id', '=', 2)], limit=1).id
            elif record.warehouse_id.id == 7:
                record.work_process_order_id = self.env['automated.sale'].search([('id', '=', 4)], limit=1).id
            elif record.warehouse_id.id == 12:
                record.work_process_order_id = self.env['automated.sale'].search([('id', '=', 7)], limit=1).id
            # if self.warehouse_id.id == 7:
            #     self.work_process_order_id = self.env['automated.sale'].search([('id', '=', 4)], limit=1).id
            else:
                # Set a different default value or leave it empty as needed
                record.work_process_order_id = False

    @api.onchange("warehouse_id", "partner_id")
    def onchangewarehouse(self):
        for rec in self:
            if rec.pricelist_id.warehouse_id.id != rec.warehouse_id.id:
               price = self.env['product.pricelist'].search([('warehouse_id','=',rec.warehouse_id.id)])
               rec.pricelist_id = price
            else:
                rec.pricelist_id = rec.pricelist_id


    