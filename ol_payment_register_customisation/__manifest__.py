# -*- coding: utf-8 -*-

{
    'name': 'payment Register View',
    'version': '1.0.0',
    'category': 'Accounting',
    'author':'Odoo mates',
    'sequence': -100,
    'summary': 'Payment Register Fields',
    'description': """Receive Amount and REturn Amount fields added in account.payment.register""",
    'depends': ['account','account_payment_multi_deduction', 'sale', 'base','bi_automated_sale_order'],
    'data': [
        'wizard/payment_amount_fields_view.xml',
        'views/ol_sale_order_line_customer_price_view.xml',
        # 'views/ol_journal_user_view.xml',
        'views/ol_customer_payment_mode_view.xml',
        'views/ol_cus_payment_mode_view.xml',
        ],
    'demo': [],
    'application':True,
    'installable': True,
    'assets': {},
    #'post_init_hook': '_synchronize_cron',
    'license': 'LGPL-3',
}
