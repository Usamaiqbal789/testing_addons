from odoo import fields, models, api, _


class ProductDashboardAddLogs(models.TransientModel):
    _inherit = "product.dashboard"

    # Get customer contact in add logs.
    @api.onchange("logs_partner_id")
    def get_customer_number(self):
        for rec in self:
            customer = rec.logs_partner_id
            if customer.mobile:
                rec.logs_contact = customer.mobile
            else:
                rec.logs_contact = customer.phone

    # method to get stock location in product dashboard
    @api.onchange('product_own_ref_no')
    def stocklocation(self):
        for rec in self:
            pro = self.env['product.product'].search([('default_code', '=', rec.product_own_ref_no.default_code)])
            loc_data = {}  # Dictionary to store locations for each warehouse

            if pro.stock_quant_ids:
                for location in pro.stock_quant_ids:
                    if location.quantity > 0:
                        warehouse_id = location.location_id.warehouse_id.id
                        if warehouse_id not in loc_data:
                            # loc_data[warehouse_id] = []
                            loc_data[warehouse_id] = ""
                        if location.location_id.name != "Stock":
                            # loc_data[warehouse_id].append(location.location_id.name)
                            loc_data[warehouse_id]+=str(location.location_id.name)+"\n"

            # Clear existing loc_ids
            for warehouse_id in loc_data:
                # rec.db_shop_ids.filtered(lambda shop: shop.branch.id == warehouse_id).loc_ids = [(6, 0, loc_data[warehouse_id])]
                rec.db_shop_ids.filtered(lambda shop: shop.branch.id == warehouse_id).loc_ids = loc_data[warehouse_id]