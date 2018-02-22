# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re


class ProductCategory(models.Model):
    _name = "cms.product.category"
    _inherit = 'mail.thread'
    _description = "Product Category"
    _order = 'name'

    name = fields.Char('Product Category', required=True, track_visibility='onchange')
