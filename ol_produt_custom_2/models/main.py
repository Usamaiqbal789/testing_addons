from odoo import models, fields,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import base64
import requests
import datetime
from odoo.exceptions import ValidationError


class SOThermalPrint(models.Model):
    _inherit = 'sale.order'

    print_download =  fields.Boolean(string="Termal Print Downloaded")

    def makeittrue(self):
        self.print_download=True
    
    # @api.onchange("state")
    # def _onchange_check_print_downloaded(self):
    #     if self.state != "sale":
    #         self.print_download = False

class image(models.Model):
    _inherit = 'product.template'

    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Files')




class AccountmoveINherit(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char("Part Number")
    # product_i = fields.Many2one(related="product_variant_id.alternative_product_ids", string='Reference')
    alternative_product_ids = fields.One2many('alternative.product.line','alternative_product_id')
    brand_id = fields.Many2one('brand.main.custom', string="Brand")
    grp_id = fields.Many2many('brand.custom', string="Group",compute='_group_comp', store=True)
    sub_grp_id = fields.Many2many('sub.group.custom', string="Sub Group" ,compute='_sub_group_comp', store=True)
    sub_sub_grp_id = fields.Many2many('sub.sub.group.custom', string="Sub Sub Group",compute='_sub_sub_group_comp', store=True)
    product_make_type_id = fields.Many2one('product.make.type', string="Product Make Type")
    parts_family_id = fields.Many2one('parts.family',  string="DEf", invisible=True)
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Files')
    oem_code = fields.Char('OEM Code')

    product_make_type = fields.Selection([('genuine', 'Genuine'), ('replacement', 'Replacement'), ('commercial', 'Commerical')],
                                               string='Product Make Type',
                                               default='')

    # own_ref_no = fields.Integer('Own Reference Number',compute='check_own_ref_no_dup',store=True)
    own_ref_no = fields.Char(string='Own Reference', required=False, copy=False, index=True, )
    origin = fields.Many2one('res.country',string='Origin')

    part_num = fields.Char('Part Number' , invisible=True)
    part_name = fields.Char('Part Name', invisible=True)
    part_family = fields.Selection(
        [('engine', 'Engine'), ('body', 'Body'), ('electrical', 'Electrical'), ('cooling', 'Cooling'), ('transmission', 'Transmission')],
        string='ABC',
        default='', invisible=True)
    des_arabic = fields.Char('Description in Arabic')
    min_unit_price = fields.Float('Min Unit Price')
    alternative_products = fields.Many2many(
        comodel_name='product.product',
        relation='contents_found_rel',
        column1='lot_id',
        column2='content_id',
        string='Alternative Products')
    product_notes_ids = fields.One2many('product.notes.line','notes_id')
    trader = fields.Float('Trader')
    export_price = fields.Float('Export Price')
    specification = fields.Char('Specification')
    @api.model
    def create(self, vals):
        # print(vals.get('name_seq'))
        if vals.get('own_ref_no', _('New')) == _('New'):
            vals['own_ref_no'] = self.env['ir.sequence'].next_by_code('product.product') or _('New')
        result = super(AccountmoveINherit, self).create(vals)
        return result





    @api.depends('group_product_ids', 'group_product_ids.grp_id')
    def _group_comp(self):
        g_ids=[]
        if self.group_product_ids:
            for g in self.group_product_ids:
                if g.grp_id:
                    g_ids.append(g.grp_id.id)
            self.grp_id = [(6,0,g_ids)]
        else:
            self.grp_id = [(6, 0, [])]

    @api.depends('group_product_ids', 'group_product_ids.sub_grp_id')
    def _sub_group_comp(self):
        g_ids=[]
        if self.group_product_ids:
            for g in self.group_product_ids:
                if g.sub_grp_id:
                    g_ids.append(g.sub_grp_id.id)
            self.sub_grp_id = [(6,0,g_ids)]
        else:
            self.sub_grp_id = [(6, 0, [])]

    @api.depends('group_product_ids', 'group_product_ids.sub_sub_grp_id')
    def _sub_sub_group_comp(self):
        g_ids=[]
        if self.group_product_ids:
            for g in self.group_product_ids:
                if g.sub_sub_grp_id:
                    g_ids.append(g.sub_sub_grp_id.id)
            self.sub_sub_grp_id = [(6,0,g_ids)]
        else:
            self.sub_sub_grp_id = [(6, 0, [])]

    # Saif
    # Changed logic for product default code to only change brand code not entire part no
    @api.onchange('brand_id')
    def check_brand(self):
        if self.brand_id:
            new_default_code = ''
            # Find the brand record
            brand_record = self.env['brand.main.custom'].search([('name', '=', self.brand_id.name)], limit=1)
            if not brand_record:
                raise UserError('No Brand found with the selected name')            
            # Get the brand code
            brand_code = brand_record.code
            # Extract the first two characters of brand code from the existing default code
            if self.default_code:
                existing_code_prefix = self.default_code[:2]
                if existing_code_prefix.isalpha():
                    # Reconstruct the default code with the new brand code and the remaining characters    
                    new_default_code = brand_code + self.default_code[2:]
                else:
                    new_default_code = brand_code + self.default_code
            else:
                new_default_code = brand_code 
            # Check if the brand code is not present in the default code
            # if brand_code not in new_default_code:
            #     raise UserError('No Brand Code in Part No')
            # Update the default code
            self.default_code = new_default_code
            # Check if no brand code in default code not allow to save it.
            # if brand_code not in self.default_code:
            #     raise ValidationError('No Brand Code in Part No')

    # Previos code to change the part no on chnaging brand name
    '''@api.onchange('brand_id')
    def check_brand(self):
        check_brand_name = self.env['brand.main.custom'].search([('name', '=', self.brand_id.name)])

        # part_no =""
        if self.brand_id:
            part_no =""
            #Saif
            part_no = str(check_brand_name.code) + str(self.default_code)
            self.default_code = part_no
            # self.default_code = check_brand_name.code
            #Saif
        if check_brand_name.code not in self.default_code:
            raise UserError('No Brand Code in Part No')
        else:
            self.default_code= part_no'''
            
    # Saif

    @api.constrains('default_code')
    def validate_part_num(self):
        for record in self:
            if record.default_code:
                check_record = self.env['product.product'].search([('default_code', '=', record.default_code), ('id', '!=', record.id)])
                if check_record:
                    raise ValidationError(
                        _('This Part Number has been already  registered'))




    @api.onchange('grp_id')
    def set_domain_sub_grp(self):


        # self.sub_grp_id = False
        if self.grp_id:
            return {'domain': {'sub_grp_id': [('grp_id', 'in', self.grp_id.ids)]}}

        else:
            # remove the domain if no grp is selected
            return {'domain': {'sub_grp_id': []}}

    @api.onchange('sub_grp_id')
    def set_domain_sub_sub_grp(self):

        # self.sub_grp_id = False
        if self.sub_grp_id:
            return {'domain': {'sub_sub_grp_id': [('sub_grp_id', 'in', self.sub_grp_id.ids)]}}

        else:
            # remove the domain if no contrat is selected
            return {'domain': {'sub_sub_grp_id': []}}


    pricelist_ids= fields.One2many('product.pricelist.item','product_id',string="Price List")


    alternate_product_warning=fields.Char("Warning")
    alternate_product_warning_show=fields.Char("Warning_show",default=False)
    def commit_alternativeproducts(self):
        # @api.onchange('alternative_products', 'alternative_products.default_code')
        # def check_alternat_product(self):
        all_product = self.alternative_products.ids
        

        # self.alternate_product_warning_show = False
        # self.alternate_product_warning = ""

        # thisid = 0
        # try:
        #     thisid = int(self.id)

        # except:
        #     # raise ValidationError(self.id)
        #     try:
        #         thisid = int(str(self.id)[6:])
        #         print(thisid, 'self id')

        #     except:
        #         self.alternate_product_warning_show = True
        #         self.alternate_product_warning = "You cannot add alternate products without saving this product. Please save this product first and then try again."
        #         self.write({"alternative_products": [(6, 0, [])]})
        #         return
        form_id=self._origin.id

        all_product.append(form_id)
       

        altproducts = self.env['product.product'].search([('id', 'in', all_product)])

        for altproduct in altproducts:

            print(altproduct)
            for id in altproduct.alternative_products.ids:
                

                if id not in all_product:
                    all_product.append(id)
           

        altproducts = self.env['product.product'].search([('id', 'in', all_product)])

        for altproduct in altproducts:
            print("print", altproduct.id, self.ids)
            appendableProducts = [i for i in all_product if i != altproduct.id]

            altproduct.write({"alternative_products": [(6, 0, appendableProducts)]})
       

        appendableProducts = [i for i in all_product if i != self.ids[0]]
       
        self.write({"alternative_products": [(6, 0, appendableProducts)]})






    def delete_product(self):

        product_ls=[]

        if self:
            print(self.id,'line id')
            for i in self.alternative_products.ids:
                alternative_products = self.env['product.product'].search([('id', '=', i)])
                for y in alternative_products.alternative_products.ids:
                    if y == self.id :
                        alternative_products.write({
                            'alternative_products': [(3, y)]
                        })


                        self.write({
                            'alternative_products': [(3, i)]
                        })

    def add_alternativeproduct(self):
        print('hello')





class Brandsclass(models.Model):
    _name ='brand.custom'


    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')










class SubGroupClass(models.Model):
    _name ='sub.group.custom'


    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')
    grp_id = fields.Many2one('brand.custom',string="Group")





class SubSubGroupClass(models.Model):
    _name ='sub.sub.group.custom'


    name = fields.Char('Name',required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')
    sub_grp_id = fields.Many2one('sub.group.custom',string="Sub Group")
    grp_id = fields.Many2one('brand.custom', string="Group")
    # brand_main_ids = fields.Many2one('brand.main.custom', string="Brand ID")




class BRandClass(models.Model):
    _name ='brand.main.custom'


    name = fields.Char('Name',required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')



class ProductMaketype(models.Model):
    _name ='product.make.type'


    name = fields.Char('Name',required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')



class PartsFamily(models.Model):
    _name ='parts.family'


    name = fields.Char('Name',required=True)
    code = fields.Char('Code')
    description = fields.Char('Description')





class AlternativeProduct(models.Model):
    _name = 'alternative.product.line'

    alternative_product_id = fields.Many2one('product.product', string='Alternate Product')
    product_id = fields.Many2one('product.product', string='Product Name')
    price_unit = fields.Float(string='Unit Price', default=1)


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one('res.partner',related="order_id.partner_id", string='Customer')

    # @api.onchange("product_id")
    # def product_id_change(self):
    #     res = super(InheritSaleOrderLine, self).product_id_change()
    #     for i in self:
    #         if i.product_id:
    #             product = self.env['product.product'].search([("id", "=", self.product_id.id)])
    #             # print(product)
    #             i.name = product.parts_family_id.name
    #             # print(self.name)
    #
    #         else:
    #             self.name = ''
    #
    #     return res






class ProductNotes(models.Model):
    _name = 'product.notes.line'

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    current_date = fields.Datetime(default=fields.datetime.now(), store=True, string="Date")
    des = fields.Char(string="Description")
    notes_id = fields.Many2one('product.product')

class Inheritstockwarehouse(models.Model):
    _inherit = 'stock.warehouse'

    ware_type = fields.Selection([('shop', 'Shop'), ('warehouse', 'Ware House')])

class Inheritstocklocation(models.Model):
    _inherit = 'stock.location'

    type = fields.Char('Type')
    cus_warehouse_id = fields.Many2one('stock.warehouse')
    # type = fields.Selection([],related="cus_warehouse_id.ware_type")
    type = fields.Char('Type')




    @api.onchange('location_id')
    def _get_type_from_stockwarehouse(self):
        print('ware location')
        self.cus_warehouse_id = self.location_id.id
        print(self.cus_warehouse_id.id,'stock.warehouse')
        # warehouse = self.env['stock.warehouse'].search([("name", "=", self.cus_warehouse_id.name)])
        warehouse = self.env['stock.warehouse'].search([("id", "=", 1)])
        print(warehouse.name,'warehouse type')

    # type = fields.Selection('Type', related="cus_warehouse_id.ware_type")






class InheritAccountMoveCustom(models.Model):
    _inherit = 'account.move.line'

    custom_amount = fields.Float(string="Custom Amount")

    @api.onchange('custom_amount')
    def custom_ammount(self):
        for line in self:
            if line.custom_amount:
               line.price_unit = line.custom_amount/line.quantity