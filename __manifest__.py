{
    'name':'Harnest Level Industries',
    'version':'1.0',
    'category': 'Productivity',
    'website': 'https://www.odoo.com/app',
    'depends':['crm','sale_management'],
    'data':[
        'security/ir.model.access.csv',
        'data/harnest_data.xml',
        'views/harnest_views.xml',
    ],
    'icon': '',
    'installable': True,
    'application': True,
    'auto_install':False,
    'description':'Custom module for Harnest Label Industries to manage inquiries, sample development, and sales.'
}