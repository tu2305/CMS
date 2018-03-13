# -*- coding: utf-8 -*-

{
    'name': 'CMS Order',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    "sequence": 1,
    'summary': 'Orders Details',
    'complexity': "easy",
    'author': 'Tu Vo',
    'website': '',
    'depends': ['cms_product'],
    'data': [
        'views/order_view.xml',
        'views/order_payment_view.xml',
        'order_menu.xml'
    ],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
