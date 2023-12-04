from odoo import models, fields,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ReportParametersWizard(models.TransientModel):
    _name="report.parameters.wizard"
    _description = "Parameters to Generate Report"

    from_date = fields.Date(default=datetime.now() - timedelta(days=1))
    to_date = fields.Date(default=datetime.now())
    warehouse_dubai = fields.Boolean(string="SHOP-DXB")
    warehouse_auh = fields.Boolean(string="SHOP-AUH")
    warehouse_alain = fields.Boolean(string="SHOP-Al AIN")
    # warehouse_dubai = fields.Boolean(string="SHOP-DXB")

    def action_print_custom_report(self):
        if self.from_date<=self.to_date:
            sales_cash = 0
            sales_credit = 0 
            sales_credit_card = 0

            purchase_credit = 0
            purchase_cash = 0

            sales_return_cash = 0
            sales_return_credit = 0
            sales_return_credit_card = 0

            purchase_return_cash = 0
            purchase_return_credit = 0

            receipt_cash = 0
            payment_cash = 0
            #######################################################################################################################
            #######################################################################################################################
            
            # Warehouse DXB
            if self.warehouse_dubai:
                
                # sales Cash calculation
                customer_invoices_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_cash+=sum(invoice.amount for invoice in customer_invoices_cash)
                sales_cash=round(sales_cash,3)
            
                # sales credit calculation
                customer_invoices_credit=self.env['account.move'].search([
                    ('move_type','=','out_invoice'),
                    ('state','=','posted'),
                    ('invoice_status','=','credit_sales'),
                    ('journal_id','=',1),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])
                # customer_invoices_credit=self.env['account.payment'].search([
                #     ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','invoice'),
                #     ('journal_id','=',15),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])
                
                sales_credit += sum(invoice.amount_total for invoice in customer_invoices_credit)
                sales_credit = round(sales_credit,3)

                # sales credit card calculation
                customer_invoices_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',13),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_credit_card += sum(invoice.amount for invoice in customer_invoices_credit_card)
                sales_credit_card = round(sales_credit_card,3)

                #############################################################################################
                # purchase Cash calculation
                vendor_bills_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('partner_type','=','supplier'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                purchase_cash+=sum(invoice.amount for invoice in vendor_bills_cash)
                purchase_cash=round(purchase_cash,3)
            
                # purchase credit calculation
                vendor_bills_credit=self.env['account.move'].search([
                    ('move_type','=','in_invoice'),
                    ('state','=','posted'),
                    ('journal_id','=',2),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])
                
                purchase_credit += sum(invoice.amount_total for invoice in vendor_bills_credit)
                purchase_credit = round(purchase_credit,3)

                ##########################################################################################

                # sales return cash calculation
                customer_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                sales_return_cash += sum(invoice.amount for invoice in customer_credit_note_cash)
                sales_return_cash=round(sales_return_cash,3)


                # sales return credit calculation
                customer_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','out_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',1),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                sales_return_credit += sum(invoice.amount_total for invoice in customer_credit_note_credit)
                sales_return_credit = round(sales_return_credit,3)

                # sales return credit card calculation
                customer_credit_note_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',13),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                    
                sales_return_credit_card += sum(invoice.amount for invoice in customer_credit_note_credit_card)
                sales_return_credit_card = round(sales_return_credit_card,3)

                ###################################################################################################
            
                # Purchase return cash calculation
                vendor_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                


                purchase_return_cash += sum(invoice.amount for invoice in vendor_credit_note_cash)
                purchase_return_cash = round(purchase_return_cash,3)

                # # Purchase return credit calculation
                # vendor_credit_note_credit=self.env['account.payment'].search([
                #     ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','credit_note'),
                #     ('journal_id','=',2),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])

        ###################   Changes By Huzaifa 

                # Purchase return credit calculation
                vendor_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','in_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',2),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                purchase_return_credit += sum(invoice.amount_total for invoice in vendor_credit_note_credit)
                purchase_return_credit = round(purchase_return_credit,3)

                # Receipt Cash Calculation
                inbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('state','=','posted'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                receipt_cash += sum(payment.amount for payment in inbound_payment_cash)
                receipt_cash = round(receipt_cash,3)

                # Payment Cash Calculation
                outbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('state','=','posted'),
                    ('journal_id','=',9),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                payment_cash += sum(payment.amount for payment in outbound_payment_cash)
                payment_cash = round(payment_cash,3)
                
            #######################################################################################################################
            #######################################################################################################################

            # Warehouse AUH
            if self.warehouse_auh:
                # sales cash calculation
                customer_invoices_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_cash+=sum(invoice.amount for invoice in customer_invoices_cash)
                sales_cash=round(sales_cash,3)

                # sales credit calculation
                customer_invoices_credit=self.env['account.move'].search([
                    ('move_type','=','out_invoice'),
                    ('state','=','posted'),
                    ('invoice_status','=','credit_sales'),
                    ('journal_id','=',34),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])

                sales_credit += sum(invoice.amount_total for invoice in customer_invoices_credit)
                sales_credit = round(sales_credit,3)

                # customer_invoices_credit=self.env['account.payment'].search([
                #    ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','invoice'),
                #     ('journal_id','=',28),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])
                
                # sales_credit += sum(invoice.amount for invoice in customer_invoices_credit)
                # sales_credit = round(sales_credit,3)
                # sales credit card calculation
                customer_invoices_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',32),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_credit_card += sum(invoice.amount for invoice in customer_invoices_credit_card)
                sales_credit_card = round(sales_credit_card,3)

                ###############################################################################
                # purchase Cash calculation
                vendor_bills_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('partner_type','=','supplier'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                purchase_cash+=sum(invoice.amount for invoice in vendor_bills_cash)
                purchase_cash=round(purchase_cash,3)
            
                # purchase credit calculation
                vendor_bills_credit=self.env['account.move'].search([
                    ('move_type','=','in_invoice'),
                    ('state','=','posted'),
                    ('journal_id','=',2),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])
                
                purchase_credit += sum(invoice.amount_total for invoice in vendor_bills_credit)
                purchase_credit = round(purchase_credit,3)

                ##########################################################################################
            
                # sales return cash calculation
                customer_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                sales_return_cash += sum(invoice.amount for invoice in customer_credit_note_cash)
                sales_return_cash=round(sales_return_cash,3)


                # sales return credit calculation
                customer_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','out_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',34),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                sales_return_credit += sum(invoice.amount_total for invoice in customer_credit_note_credit)
                sales_return_credit = round(sales_return_credit,3)

                # sales return credit card calculation
                customer_credit_note_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',32),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                    
                sales_return_credit_card += sum(invoice.amount for invoice in customer_credit_note_credit_card)
                sales_return_credit_card = round(sales_return_credit_card,3)

                ###################################################################################################
            
                # Purchase return cash calculation
                vendor_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                purchase_return_cash += sum(invoice.amount for invoice in vendor_credit_note_cash)
                purchase_return_cash = round(purchase_return_cash,3)

                # # Purchase return credit calculation
                # vendor_credit_note_credit=self.env['account.payment'].search([
                #     ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','credit_note'),
                #     ('journal_id','=',2),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])
                
                ###################   Changes By Huzaifa 

                # Purchase return credit calculation
                vendor_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','in_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',2),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                purchase_return_credit += sum(invoice.amount_total for invoice in vendor_credit_note_credit)
                purchase_return_credit = round(purchase_return_credit,3)

                # Receipt Cash Calculation
                inbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('state','=','posted'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                receipt_cash += sum(payment.amount for payment in inbound_payment_cash)
                receipt_cash = round(receipt_cash,3)

                # Payment Cash Calculation
                outbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('state','=','posted'),
                    ('journal_id','=',30),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                payment_cash += sum(payment.amount for payment in outbound_payment_cash)
                payment_cash = round(payment_cash,3)

            #######################################################################################################################
            #######################################################################################################################

            # Warehouse AL-AIN
            if self.warehouse_alain:
                customer_invoices_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_cash+=sum(invoice.amount for invoice in customer_invoices_cash)
                sales_cash=round(sales_cash,3)

                # sales credit calculation
                customer_invoices_credit=self.env['account.move'].search([
                    ('move_type','=','out_invoice'),
                    ('state','=','posted'),
                    ('invoice_status','=','credit_sales'),
                    ('journal_id','=',35),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])

                sales_credit += sum(invoice.amount_total for invoice in customer_invoices_credit)
                sales_credit = round(sales_credit,3)
                # customer_invoices_credit=self.env['account.payment'].search([
                #     ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','invoice'),
                #     ('journal_id','=',29),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])
                
                # sales_credit += sum(invoice.amount for invoice in customer_invoices_credit)
                # sales_credit = round(sales_credit,3)

                customer_invoices_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',33),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                sales_credit_card += sum(invoice.amount for invoice in customer_invoices_credit_card)
                sales_credit_card = round(sales_credit_card,3)

            ####################################################################################################
                # purchase Cash calculation
                vendor_bills_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('partner_type','=','supplier'),
                    ('reconciled_invoices_type','=','invoice'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                purchase_cash+=sum(invoice.amount for invoice in vendor_bills_cash)
                purchase_cash=round(purchase_cash,3)
            
                # purchase credit calculation
                vendor_bills_credit=self.env['account.move'].search([
                    ('move_type','=','in_invoice'),
                    ('state','=','posted'),
                    ('journal_id','=',2),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])
                
                purchase_credit += sum(invoice.amount_total for invoice in vendor_bills_credit)
                purchase_credit = round(purchase_credit,3)

                ##########################################################################################
            
                # sales return cash calculation
                customer_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                sales_return_cash += sum(invoice.amount for invoice in customer_credit_note_cash)
                sales_return_cash=round(sales_return_cash,3)


               # sales return credit calculation
                customer_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','out_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',35),
                    ('invoice_date',">=",self.from_date),
                    ('invoice_date',"<=",self.to_date),
                    ])
                
                sales_return_credit += sum(invoice.amount_total for invoice in customer_credit_note_credit)
                sales_return_credit = round(sales_return_credit,3)

                # sales return credit card calculation
                customer_credit_note_credit_card=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',33),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                    
                sales_return_credit_card += sum(invoice.amount for invoice in customer_credit_note_credit_card)
                sales_return_credit_card = round(sales_return_credit_card,3)

                ###################################################################################################
            
                # Purchase return cash calculation
                vendor_credit_note_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('reconciled_invoices_type','=','credit_note'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                purchase_return_cash += sum(invoice.amount for invoice in vendor_credit_note_cash)
                purchase_return_cash = round(purchase_return_cash,3)

                # # Purchase return credit calculation
                # vendor_credit_note_credit=self.env['account.payment'].search([
                #     ('payment_type','=','inbound'),
                #     ('reconciled_invoices_type','=','credit_note'),
                #     ('journal_id','=',2),
                #     ('date',">=",self.from_date),
                #     ('date',"<=",self.to_date),
                #     ])

                ###################   Changes By Huzaifa 

                # Purchase return credit calculation
                vendor_credit_note_credit=self.env['account.move'].search([
                    ('move_type','=','in_refund'),
                    ('state','=','posted'),
                    ('payment_state','=','not_paid'),
                    ('journal_id','=',2),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                purchase_return_credit += sum(invoice.amount_total for invoice in vendor_credit_note_credit)
                purchase_return_credit = round(purchase_return_credit,3)

                # Receipt Cash Calculation
                inbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','inbound'),
                    ('state','=','posted'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])
                
                receipt_cash += sum(payment.amount for payment in inbound_payment_cash)
                receipt_cash = round(receipt_cash,3)

                # Payment Cash Calculation
                outbound_payment_cash=self.env['account.payment'].search([
                    ('payment_type','=','outbound'),
                    ('state','=','posted'),
                    ('journal_id','=',31),
                    ('date',">=",self.from_date),
                    ('date',"<=",self.to_date),
                    ])

                payment_cash += sum(payment.amount for payment in outbound_payment_cash)
                payment_cash = round(payment_cash,3)
            
            ###################################################################################################

            # total sales calculation
            total_sales = sales_cash + sales_credit + sales_credit_card
            total_sales=round(total_sales,3)

            # total purchase calculation
            total_purchase = round(purchase_cash + purchase_credit,3)

            # total sales return calculation
            total_sales_return = sales_return_cash + sales_return_credit + sales_return_credit_card
            total_sales_return = round(total_sales_return,3)

            # total purchase return 
            total_purchase_return= round(purchase_return_cash+purchase_return_credit,3)

            ##########################################################################################
            
            # net sales calculation
            net_sales=round(total_sales-total_sales_return,3)

            # net purchase
            net_purchase=round(total_purchase-total_purchase_return,3)

            
            ###################################################################################################
            
            ###################################################################################################
            
            # # Receipt Cash Calculation
            # inbound_payment_cash=self.env['account.payment'].search([
            #     ('payment_type','=','inbound'),
            #     ('state','=','posted'),
            #     ('journal_id','=',24),
            #     ('date',">=",self.from_date),
            #     ('date',"<=",self.to_date),
            #     ])
            
            # receipt_cash = sum(payment.amount for payment in inbound_payment_cash)
            # receipt_cash = round(receipt_cash,3)

            # Receipt Cheque Calculation
            inbound_payment_cheque=self.env['account.payment'].search([
                ('payment_type','=','inbound'),
                ('state','=','posted'),
                ('journal_id','=',26),
                ('date',">=",self.from_date),
                ('date',"<=",self.to_date),
                ])

            receipt_cheque = sum(payment.amount for payment in inbound_payment_cheque)
            receipt_cheque = round(receipt_cheque,3)

            total_receipt = round(receipt_cash+receipt_cheque,3)

            ###################################################################################################
            
            # # Payment Cash Calculation
            # outbound_payment_cash=self.env['account.payment'].search([
            #     ('payment_type','=','outbound'),
            #     ('state','=','posted'),
            #     ('journal_id','=',9),
            #     ('date',">=",self.from_date),
            #     ('date',"<=",self.to_date),
            #     ])

            # payment_cash = sum(payment.amount for payment in outbound_payment_cash)
            # payment_cash = round(payment_cash,3)

            # Payment Cheque Calculation
            outbound_payment_cheque=self.env['account.payment'].search([
                ('payment_type','=','outbound'),
                ('state','=','posted'),
                ('journal_id','=',25),
                ('date',">=",self.from_date),
                ('date',"<=",self.to_date),
                ])

            payment_cheque = sum(payment.amount for payment in outbound_payment_cheque)
            payment_cheque = round(payment_cheque,3)

            total_payment = round(payment_cash+payment_cheque,3)
            
            ###################################################################################################
            
            # VAT in Calculation
            vendor_bills_tax=self.env['account.move'].search([
                ('move_type','=','in_invoice'),
                ('state','=','posted'),
                ('invoice_date',">=",self.from_date),
                ('invoice_date',"<=",self.to_date),
                ])
            
            vat_in = sum(invoice.amount_tax_signed for invoice in vendor_bills_tax)
            vat_in=round(vat_in,3)
            
            # VAT out Calculation
            customer_invoices_tax=self.env['account.move'].search([
                ('move_type','=','out_invoice'),
                ('state','=','posted'),
                ('invoice_date',">=",self.from_date),
                ('invoice_date',"<=",self.to_date),
                ])
            
            vat_out = sum(invoice.amount_tax_signed for invoice in customer_invoices_tax)
            vat_out=round(vat_out,3)
            
            ###################################################################################################
            
            # Income Calculation
            journal_items = self.env['account.move.line'].search([
                ('account_id','=',144),
                ('parent_state','=','posted'),
                ('date',">=",self.from_date),
                ('date',"<=",self.to_date),
            ])

            income=sum(record.credit for record in journal_items)

            # Expence Calculation
            expence_data = self.env['hr.expense'].search([
                ('date',">=",self.from_date),
                ('date',"<=",self.to_date),
            ])

            expence = sum(record.total_amount_company for record in expence_data)
            expence = round(expence,3)

            ###################################################################################################
            
            cash_in_hand = round(receipt_cash - payment_cash,3)
            # cash_in_hand = round(net_sales - net_purchase,3)

            ###################################################################################################

            data = {

                'current_date':datetime.now().strftime("%d-%m-%Y"),
                'from_date':self.from_date.strftime("%d-%m-%Y"),
                'to_date':self.to_date.strftime("%d-%m-%Y"),

                'sales_cash':sales_cash,
                'sales_credit':sales_credit,
                'sales_credit_card':sales_credit_card,
                'total_sales':total_sales,

                'sales_return_cash':sales_return_cash,
                'sales_return_credit':sales_return_credit,
                'sales_return_credit_card':sales_return_credit_card,
                'total_sales_return':total_sales_return,

                'net_sales':net_sales,

                'purchase_cash':purchase_cash,
                'purchase_credit':purchase_credit,
                'total_purchase':total_purchase,

                'purchase_return_cash':purchase_return_cash,
                'purchase_return_credit':purchase_return_credit,
                'total_purchase_return':total_purchase_return,

                'net_purchase':net_purchase,

                'receipt_cash':receipt_cash,
                'receipt_cheque':receipt_cheque,
                'total_receipt':total_receipt,

                'payment_cash':payment_cash,
                'payment_cheque':payment_cheque,
                'total_payment':total_payment,

                'vat_in':vat_in,
                'vat_out':vat_out,

                'income': income,
                'expence':expence,

                'cash_in_hand':cash_in_hand,

            }

            return self.env.ref('custom_financial_report.action_custom_financial_report').report_action(self, data=data)
        else:
            raise UserError('"From date" can not be after the "To Date"')