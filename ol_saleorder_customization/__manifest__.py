{
    'name': 'Sale Order Customization',
    'version': '1.0',
    'category': 'Sales',
    'description': """
        This module is used to customize the sale order.
    """,
    'depends': ['sale','ol_payment_register_customisation'],
    'data': [
        'views/ol_sale_order_customer_price.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}