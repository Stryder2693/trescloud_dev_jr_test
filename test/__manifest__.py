{
    'name': 'Test jr developer',
    'version': '1.0',
    'category': 'Test',
    'sequence': 15,
    'summary': 'Test Module',
    'website': 'trescloud.com',
    'depends': [
        'stock',
        'account',
        'sale_management',
    ],
    'data': [
        #view
        'views/delivery_detail_views.xml',
        'views/account_move_views.xml',
        #security
        'security/delivery_detail_security.xml',
        'security/ir.model.access.csv',
        #report
        'report/report_invoice_templates.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
