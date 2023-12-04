# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Display Price',
    'version': '1.0.0',
    'category': 'Sale',
    'author':'Odoo mates',
    'sequence': -100,
    'summary': 'Sale Order Display Price',
    'description': """Display dummy prices in sale order line and invoice""",
    'depends': ['sale', 'account', 'stock'],
    'data': [
        'views/ol_sale_order_display_tax_view.xml',
        'views/ol_invoice_display_price.xml',
        'views/ol_sale_order_terms_&_condition_view.xml',
        'views/ol_sale_order_cus_tax_view.xml',
        'reports/ol_credit_note_button.xml',
        'reports/ol_credit_note_report_view.xml',
        ],
    'demo': [],
    'application':True,
    'installable': True,
    'assets': {},
    #'post_init_hook': '_synchronize_cron',
    'license': 'LGPL-3',
}
