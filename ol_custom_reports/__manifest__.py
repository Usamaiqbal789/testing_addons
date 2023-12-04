{
    'name': 'Custom Reports Abufaisal',
    'version': '1.0',
    'summary': 'Custom Reports',
    'description': """
            Custom Reports
            ====================
    """,
    'author': 'Muhammad Abdullah & Rayyan Ismail',
    'depends':['account','sale','stock','ol_sale_order_display_price'],
    'data': [
        'reports/ol_custom_reports_button.xml',
        'reports/ol_custom_reports_tax_invoice_view.xml',
        'reports/ol_custom_reports_tax_invoice_cash_view.xml',
        'reports/ol_custom_reports_quotation_view.xml',
        'reports/ol_custom_reports_delivery_view.xml',
        'reports/ol_internal_transfer_report_custom_view.xml',
        'reports/ol_dummy_tax_invoice_custom_view.xml',
        'views/ol_custom_epson_field.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}