# -*- coding: utf-8 -*-

{
    'name': 'Product Creation Customization',
    'version': '1.0.0',
    'category': 'Sale',
    'author':'Odoo mates',
    'sequence': -100,
    'summary': 'Product Creation Customization',
    'description': """Product Creation View Customization""",
    'depends': ['product','ol_produt_custom_2','sale','account', 'stock', 'purchase','bi_automated_sale_order'],
    'data': [
        'views/ol_product_dashboard_customization_view.xml',
        'views/ol_inventory_dasboard_customization_view.xml',
        'views/ol_sale_order_line_customization.xml',
        'views/ol_invoice_custom_fields_view.xml',
        
        ],
    'demo': [],
    'application':True,
    'installable': True,
    'assets': {},
    #'post_init_hook': '_synchronize_cron',
    'license': 'LGPL-3',
}
