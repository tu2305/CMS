# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re


class ProductCategory(models.Model):
    _name = "cms.product"
    _inherit = 'mail.thread'
    _description = "Product"
    _order = 'product_category'

    name = fields.Char('Product', required=True, track_visibility='onchange')
    product_category = fields.Many2one('cms.product.category', 'Product Category', required=True,
                                       track_visibility='onchange')
    image = fields.Binary("Image", attachment=True)
    price = fields.Integer('Price', required=True, track_visibility='onchange')
    description = fields.Text('Description')
    active = fields.Boolean(default=True)
