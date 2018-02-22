# -*- coding: utf-8 -*-

{
    'name': 'CMS Product',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    "sequence": 1,
    'summary': 'Product Details',
    'complexity': "easy",
    'author': 'Tu Vo',
    'website': '',
    'depends': ['mail'],
    'data': [
        'views/product_view.xml',
        'views/product_category_view.xml',
        'product_menu.xml'
    ],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
