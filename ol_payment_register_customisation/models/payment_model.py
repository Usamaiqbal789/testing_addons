from odoo import models, fields, api


class AccountPaymentMode(models.Model):
    _name = "account.payment.mode"

    name = fields.Char(string="Mode Name")

class CustomerPaymentMode(models.Model):
    _inherit="res.partner"
    payment_mode = fields.Many2one(comodel_name="account.payment.mode", string="Payment Mode" )
    # journal_ids = fields.Many2many('account.journal',string="Journals")
    vat = fields.Char(required=True)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         # raise UserError(self.env.context.get('hide_code'))
    #         if not self.env.context.get('hide_code'):
                
    #             name=str(rec.name)
    #         else:
    #             name=rec.name
    #         result.append((rec.id, name))
    #     return result

    @api.model
    def name_search(self, name=None, args=None, operator='ilike', limit=100):
        args = args or []
        # domain_name = ['|', ('name', 'ilike', name), ('default_code', 'ilike', name), ('own_ref_no', 'ilike', name) ]
        domain_name = ['|','|', ('name', 'ilike', name), ('vat', 'ilike', name),('id', 'ilike', name)]
        recs = self.search(domain_name + args, limit=limit)
        return recs.name_get()

class UserJournal(models.Model):
    _inherit="res.users"
    # payment_mode = fields.Many2one(comodel_name="account.payment.mode", string="Payment Mode" )
    journal_ids = fields.Many2many('account.journal',string="Journals")
    workflow_ids = fields.Many2many('automated.sale', String="Work Flow Process")

class CustomerPaymentModeInvoice(models.Model):
    _inherit="account.move"
    payment_mode = fields.Many2one(comodel_name="account.payment.mode", string="Payment Mode")

   

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.payment_mode = self.partner_id.payment_mode.id

class UserJournars(models.Model):
    _inherit = "account.journal"
    check_record = fields.Many2many('res.users')
    
    @api.onchange('journal_id')
    def area_filter_onchange(self):
        user = self.env.user
        return {'domain': {'|': [('id', '=', False), ('id', 'in', user.partner_id.journal_ids.ids)]}}