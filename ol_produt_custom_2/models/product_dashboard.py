from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError

class Inheritproductpricelistitem(models.Model):
    _inherit = 'product.pricelist.item'

    min_price = fields.Float('Min Price')

    trade_price = fields.Float('Trader')
    export_price = fields.Float(string="Export Price")


class Inheritproductpricelist(models.Model):
    _inherit = 'product.pricelist'

    warehouse_id = fields.Many2one('stock.warehouse','Warehouse')

class Dashboardcustomwarehouse(models.TransientModel):
    _name = 'dashboard.warehouseshop'

    branch = fields.Many2one('stock.warehouse')
    qty_inhand= fields.Integer('Quantity In Hand')
    loc_ids = fields.Many2many('stock.location',string='Location')
    cost = fields.Float('Cost')
    min_price = fields.Float(string="Min Price")
    max_price = fields.Float(string="Max price")
    trader = fields.Float(string="Trader")
    export_price = fields.Float(string="Export Price")
    reorder_level = fields.Char('Re Order Level')
    reorder_qty = fields.Char('Reorder Qty')
    warehouse_shop = fields.Selection([
        ('shop', 'Shop'),
        ('warehouse', 'Warehouse')
    ], string='Shop/WareHouse')

class Dashboardcustomwarehouse(models.TransientModel):
    _name = 'dashboard.shop'

    branch = fields.Many2one('stock.warehouse')
    #Saif
    qty_inhand= fields.Text('Quantity In Hand')
    loc_ids = fields.Text(string='Location')
    #Saif
    # qty_inhand= fields.Integer('Quantity In Hand')
    # loc_ids = fields.Many2many('stock.location',string='Location')
    cost = fields.Float('Cost')
    min_price = fields.Float(string="Min Price")
    max_price = fields.Float(string="Max price")
    trader = fields.Float(string="Trader")
    export_price = fields.Float(string="Export Price")
    reorder_level = fields.Char('Re Order Level')
    reorder_qty = fields.Char('Reorder Qty')
    warehouse_shop = fields.Selection([
        ('shop', 'Shop'),
        ('warehouse', 'Warehouse')
    ], string='Shop/WareHouse')


# class InheritPurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#     order_type= fields.Selection(
#         [('purchase_order', 'Purchase Order'), ('lpo', 'Lpo')],
#         string='Purchase Order/Lpo',
#         default='')

class prodInherit(models.Model):
    _inherit = "product.product"
    def name_get(self):
        result = []
        for rec in self:
            if not self.env.context.get('hide_code'):
                name=str(rec.default_code)
            else:
                name=rec.name
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain_name = ['|', ('name', 'ilike', name), ('default_code', 'ilike', name)]
        recs = self.search(domain_name + args, limit=limit)
        return recs.name_get()






class CustomDashboard(models.TransientModel):
    _name = 'product.dashboard'
    # _rec_name = 'product_db_id'

    
    
    #ahzam
    product_own_ref_no = fields.Many2one('product.product', string="Part Number")
    product_db_id = fields.Char(string="Part Name")
    own_ref_no = fields.Char(string="Own Ref No", related='product_own_ref_no.own_ref_no')
    #ahzam

    product_image = fields.Binary('Image',related='product_own_ref_no.image_1920')
    # product_image = fields.Binary('Image')
    part_name = fields.Char(string="Part Name",related='product_own_ref_no.name')
    part_no = fields.Char(string="Part No", related='product_own_ref_no.default_code')
    product_brand = fields.Many2one(string="Product Brand", related='product_own_ref_no.brand_id')
    # db_detailed_type = fields.Selection(related="product_own_ref_no.type", string='Stock Type')
    db_detailed_type = fields.Selection(related="product_own_ref_no.detailed_type", string='Stock Type')
    product_description= fields.Text('Product Details',related="product_own_ref_no.description_sale")
    # product_description = fields.Html('Product Details', related="product_own_ref_no.description")
    db_origin = fields.Many2one('res.country',related='product_own_ref_no.origin', string='Origin')
    db_make_type = fields.Many2one('product.make.type', string='Product Make Type',related='product_own_ref_no.product_make_type_id')
    db_product_group=fields.One2many('groups.product',related="product_own_ref_no.group_product_ids")
    spec = fields.Char(string="Specification",related='product_own_ref_no.specification')
    db_packaging = fields.One2many('product.packaging', related='product_own_ref_no.packaging_ids',string='Product Packaging')
    sale_uom = fields.Many2one('uom.uom',related='product_own_ref_no.uom_id' ,string='Sale UOM')
    purchase_uom = fields.Many2one('uom.uom',related='product_own_ref_no.uom_id' ,string='Purchase UOM')
    alternatives = fields.Many2many('product.product', related='product_own_ref_no.alternative_products' , string='Subtitute products')
    to_date = fields.Date(string="TO", default=fields.Datetime.now())
    db_warehouse_ids = fields.Many2many('dashboard.warehouseshop',compute='get_warehoueinfo')
    state = fields.Many2many('stock.warehouse',string="state")
    db_shop_ids = fields.Many2many(comodel_name='dashboard.shop',compute='get_warehoueinfo')
    logs_description = fields.Char('Description')
    logs_price = fields.Char('Price')
    logs_partner_id = fields.Many2one('res.partner', string='Customer')
    logs_contact = fields.Char(string="Contact")
    dashboard_logs_ids = fields.Many2many('dasboard.logs', string='Dashboard Logs', compute='add_log_ids_dash')

    # def name_get(self):
    #     if context is None:
    #         context = {}
    #     res = []
    #     if context.get('own_ref_no', False):
    #         for record in self:
    #             res.append(record.id, rec.own_ref_no)
    #     else:
    #         for record in self:
    #             res.append(record.id, record.name)
    #     return res

    @api.onchange('product_own_ref_no')
    def get_ref_prod_id(self):
        self.product_db_id=''
        get_prod=self.env['product.product'].search([('id',"=",self.product_own_ref_no.id)])
        self.product_db_id=get_prod.name

        

      

        

        
        

    @api.onchange('to_date')
    def sub_six_months(self):
        if self.to_date:
            self.from_date = self.to_date - relativedelta(months=6)


    from_date = fields.Date(string="From", default=sub_six_months)

    @api.depends('product_own_ref_no')
    def add_log_ids_dash(self):
        logs=self.env['dasboard.logs'].search([('product_id','=',self.product_own_ref_no.id)])
        self.dashboard_logs_ids=logs
    # add_log_id = fields.Many2many(comodel_name='add.log')


    @api.onchange('product_own_ref_no')
    # @api.depends('product_own_ref_no')
    def get_warehoueinfo(self):
        warehoues= self.env['stock.warehouse'].search([])
        locations=[]
        def get_locations(childs):
            locations_childs = self.env['stock.location']
            for c in childs:
                if c.child_ids:
                   ans= get_locations(c.child_ids)
                   for val in ans:
                       locations_childs += val
                   locations_childs += c
                else:
                    locations_childs+=c
            return locations_childs

        data_all=[]
        for w in warehoues:
            #Saif
            quantities = ""
            # quantities = 0
            locations=get_locations(w.view_location_id)

            loations_stock=[]
            price_list = self.env['product.pricelist'].search([('warehouse_id', '=', w.id)])
            
            price_list_item = self.env['product.pricelist.item']
            if self.product_own_ref_no:
                # price_list_item = self.env['product.pricelist.item'].search([('pricelist_id','=',price_list.id),('product_id', '=', self.product_own_ref_no.id)])
                price_list_item = price_list_item.search([('pricelist_id','=',price_list.id),('product_id', '=', self.product_own_ref_no.id)])
            else:

                ll = self.env['product.pricelist.item'].search([])
                for i in ll:
                    price_list_item = i
                    break
            cost = self.env['product.product'].search([('id', '=', self.product_own_ref_no.id)])

            reorder_qty="Not Maintanied"
            reorder_level="Not Maintanied"
            for l in locations:
                for q in l.quant_ids:
                    if q.product_id == self.product_own_ref_no:
                        #saif
                        # quantities.append(q.available_quantity)
                        quantities+= (str(int(q.available_quantity)) + "\n")
                        # quantities+= q.available_quantity
                        #saif
                re_order=self.env['stock.warehouse.orderpoint'].search([('location_id','=',l.id),('product_id','=',self.product_own_ref_no.id)])
                for ro in re_order:
                    if ro:
                        reorder_qty=str(ro.product_min_qty)
                        reorder_level=str(ro.product_max_qty)
                    if  q.quantity>0 and l.id not in loations_stock:
                        loations_stock.append(l.id)
          
            data_all.append({
                'branch':w.id,
                # 'loc_ids':[(6,0,loations_stock)],
                'qty_inhand':quantities,
                'max_price':price_list_item.fixed_price,
                'min_price':price_list_item.min_price,
                'trader':price_list_item.trade_price,
                'export_price':price_list_item.export_price,
                'cost':cost.standard_price,
                'reorder_qty':reorder_qty,
                'reorder_level':reorder_level,
                'warehouse_shop':w.ware_type
            })


        enter_data_shop=self.env['dashboard.shop']
        enter_data_warehouse=self.env['dashboard.warehouseshop']

        for da in data_all:
            if da['warehouse_shop'] =="shop":
                dev_lines1 = self.env['dashboard.shop'].create(da)
                enter_data_shop+=dev_lines1

            elif da['warehouse_shop'] =="warehouse":
                dev_lines = self.env['dashboard.warehouseshop'].create(da)
                enter_data_warehouse+=dev_lines
        self.db_shop_ids = enter_data_shop
        self.db_warehouse_ids = enter_data_warehouse



    quotation_his_id = fields.Many2many(comodel_name='sale.order.line',
                                        relation='contents_found',
                                        column1='lot_id',
                                        column2='content_id',
                                        string="Quotation History",compute="_get_quotation_history")

    customer_order_ids = fields.Many2many(comodel_name='sale.order.line',
                                          relation='contents_found',
                                          column1='lot_id',
                                          column2='content_id',
                                          string="Order History",compute="_get_quotation_history")
    # quotation history
    @api.onchange('product_own_ref_no')
    def _get_quotation_history(self):
        sale_line_q = self.env['sale.order.line'].search([("product_id", "=", self.product_own_ref_no.id)])
        sa_ids = []
        so_ids = []
        for line in sale_line_q:
            if line.order_id.state == 'draft':
                sa_ids.append(line.id)
            elif line.order_id.state == 'sale':
                so_ids.append(line.id)
        self.quotation_his_id = sa_ids
        self.customer_order_ids = so_ids

    purchase = fields.Many2many(comodel_name='purchase.order.line',compute="purchase_lines")
    local_puchase = fields.Many2many(comodel_name='purchase.order.line',relation='contents_found',
                                          column1='lot_id',
                                          column2='content_id',
                                            compute="purchase_lines")

    rfq_puchase = fields.Many2many(comodel_name='purchase.order.line', relation='contents_found',
                                     column1='lot_id',
                                     column2='content_id',
                                     compute="purchase_lines")

    rfq_local_puchase = fields.Many2many(comodel_name='purchase.order.line', relation='contents_found',
                                   column1='lot_id',
                                   column2='content_id',
                                   compute="purchase_lines")
    # quotation history
    @api.onchange('product_own_ref_no')
    def purchase_lines(self):
        purchase_line_q = self.env['purchase.order.line'].search([("product_id", "=", self.product_own_ref_no.id)])
        po_ids = []
        lpo_ids =[]
        lporfo =[]
        porfo =[]
        for line in purchase_line_q:
            if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                # Condition Changed by Saif to get FPO
                # if line.order_id.order_type == 'purchase_order':
                if line.order_id.supplier_type_po == 'import':
                    po_ids.append(line.id)
                elif line.order_id.order_type == 'lpo':
                    lpo_ids.append(line.id)
            if line.order_id.state == 'draft':
                # if line.order_id.order_type == 'purchase_order':
                if line.order_id.supplier_type_po == 'import':
                    porfo.append(line.id)
                elif line.order_id.order_type == 'lpo':
                    lporfo.append(line.id)

        self.purchase = po_ids
        self.local_puchase = lpo_ids
        self.rfq_puchase = porfo
        self.rfq_local_puchase = lporfo

    supplier_reference=fields.Char(compute="get_supplier",string="Supplier Ref. No")
    last_supplier=fields.Many2one('res.partner',compute="get_supplier",string="Last Supplier")
    last_purchase_cost=fields.Float('Last Purchase Cost',compute="get_supplier")
    avg_purchase_cost=fields.Float('Average Purchase Cost',compute="get_supplier")
    def get_supplier(self):
        po=self.env['purchase.order.line'].search([('product_id','=',self.product_own_ref_no.id)], order='id asc')
        self.last_supplier=False
        self.supplier_reference=""
        self.last_purchase_cost=0
        self.avg_purchase_cost=0
        cost_sum=0
        for pol in po:
            if pol.order_id.state == 'purchase' or pol.order_id.state == 'done':
                self.last_supplier=pol.partner_id
                self.supplier_reference=pol.order_id.partner_ref
                self.last_purchase_cost=pol.price_unit
                cost_sum+=pol.price_unit
        if po.ids:
            self.avg_purchase_cost=cost_sum/len(po.ids)



    def addlogs(self):

        if self.product_own_ref_no:
            self.write({
                "dashboard_logs_ids":  [(0, 0, {
                    'product_id': self.product_own_ref_no.id,
                    'description': self.logs_description,
                    'user_id': self.env.user.id,
                    'cus_contact': self.logs_contact,
                    'price': self.logs_price,
                    'partner_id': self.logs_partner_id.id if self.logs_partner_id else False
                })]
            })
            #Saif (clear add log placeholder values)
            self.logs_description = ''
            self.logs_price= ''
            self.logs_contact = ''
            self.logs_partner_id = False
            #Saif
        else:
            raise UserError("Select Product First")

    def action_refresh(self):

        # def add_log_ids_dash():
        #     logs = self.env['dasboard.logs'].search([('product_id', '=', self.product_own_ref_no.id)])
        #     self.dashboard_logs_ids = logs

        # add_log_id = fields.Many2many(comodel_name='add.log')



        def get_warehoueinfo(self):
            warehoues = self.env['stock.warehouse'].search([])
            locations = []

            def get_locations(childs):
                locations_childs = self.env['stock.location']
                for c in childs:
                    if c.child_ids:
                        ans = get_locations(c.child_ids)
                        for val in ans:
                            locations_childs += val
                        locations_childs += c
                    else:
                        locations_childs += c
                return locations_childs

            data_all = []
            for w in warehoues:

                quantities = 0
                locations = get_locations(w.view_location_id)

                loations_stock = []
                price_list = self.env['product.pricelist'].search([('warehouse_id', '=', w.id)])
                price_list_item = self.env['product.pricelist.item'].search(
                    [('pricelist_id', '=', price_list.id), ('product_id', '=', self.product_own_ref_no.id)])
                cost = self.env['product.product'].search([('id', '=', self.product_own_ref_no.id)])

                reorder_qty = "Not Maintanied"
                reorder_level = "Not Maintanied"
                for l in locations:
                    for q in l.quant_ids:
                        if q.product_id == self.product_own_ref_no:
                            quantities += q.available_quantity
                    re_order = self.env['stock.warehouse.orderpoint'].search(
                        [('location_id', '=', l.id), ('product_id', '=', self.product_own_ref_no.id)])
                    for ro in re_order:
                        if ro:
                            reorder_qty = str(ro.product_min_qty)
                            reorder_level = str(ro.product_max_qty)

                        if q.quantity > 0 and l.id not in loations_stock:
                            loations_stock.append(l.id)


                data_all.append({
                    'branch': w.id,
                    'loc_ids': [(6, 0, loations_stock)],
                    'qty_inhand': quantities,
                    'max_price': price_list_item.fixed_price,
                    'min_price': price_list_item.min_price,
                    'trader': price_list_item.trade_price,
                    'export_price': price_list_item.export_price,
                    'cost': cost.standard_price,
                    'reorder_qty': reorder_qty,
                    'reorder_level': reorder_level,
                    'warehouse_shop': w.ware_type
                })

            enter_data_shop = self.env['dashboard.shop']
            enter_data_warehouse = self.env['dashboard.warehouseshop']

            for da in data_all:
                if da['warehouse_shop'] == "shop":
                    dev_lines1 = self.env['dashboard.shop'].create(da)
                    enter_data_shop += dev_lines1

                elif da['warehouse_shop'] == "warehouse":
                    dev_lines = self.env['dashboard.warehouseshop'].create(da)
                    enter_data_warehouse += dev_lines
            self.db_shop_ids = enter_data_shop
            self.db_warehouse_ids = enter_data_warehouse


            def _get_quotation_history():
                sale_line_q = self.env['sale.order.line'].search([("product_id", "=", self.product_own_ref_no.id)])
                sa_ids = []
                so_ids = []
                for line in sale_line_q:
                    if line.order_id.state == 'draft':
                        sa_ids.append(line.id)
                    elif line.order_id.state == 'sale':
                        so_ids.append(line.id)
                self.quotation_his_id = sa_ids
                self.customer_order_ids = so_ids

            def purchase_lines():
                purchase_line_q = self.env['purchase.order.line'].search([("product_id", "=", self.product_own_ref_no.id)])
                po_ids = []
                lpo_ids = []
                lporfo = []
                porfo = []
                for line in purchase_line_q:
                    if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                        if line.order_id.order_type == 'purchase_order':
                            po_ids.append(line.id)
                        elif line.order_id.order_type == 'lpo':
                            lpo_ids.append(line.id)
                    if line.order_id.state == 'draft':
                        if line.order_id.order_type == 'purchase_order':
                            porfo.append(line.id)
                        elif line.order_id.order_type == 'lpo':
                            lporfo.append(line.id)

                self.purchase = po_ids
                self.local_puchase = lpo_ids
                self.rfq_puchase = porfo
                self.rfq_local_puchase = lporfo

            def get_supplier():
                po = self.env['purchase.order.line'].search([('product_id', '=', self.product_own_ref_no.id)],
                                                            order='id asc')
                self.last_supplier = False
                self.supplier_reference = ""
                self.last_purchase_cost = 0
                self.avg_purchase_cost = 0
                cost_sum = 0
                for pol in po:
                    if pol.order_id.state == 'purchase' or pol.order_id.state == 'done':
                        self.last_supplier = pol.partner_id
                        self.supplier_reference = pol.order_id.partner_ref
                        self.last_purchase_cost = pol.price_unit
                        cost_sum += pol.price_unit
                if po.ids:
                    self.avg_purchase_cost = cost_sum / len(po.ids)

            # def addlogs():

            #     if self.product_own_ref_no:
            #         self.write({
            #             "dashboard_logs_ids": [(0, 0, {
            #                 'product_id': self.product_own_ref_no.id,
            #                 'description': self.logs_description,
            #                 'user_id': self.env.user.id,
            #                 'price': self.logs_price,
            #                 'partner_id': self.logs_partner_id.id if self.logs_partner_id else False
            #             })]
            #         })
            #     else:
            #         raise UserError("Select Product First")







class DashboardLogs(models.Model):
    _name = 'dasboard.logs'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    cus_contact = fields.Char(string="Contact")
    price = fields.Float('Price')
    description = fields.Char('Description')

    def DEl_button(self):

        if self:
           self.unlink()


class ADDlog(models.Model):
    _name = 'add.log'

    add_description = fields.Char('Description')
    add_price = fields.Char('Price')
    add_partner_id = fields.Many2one('res.partner', string='Customer')

