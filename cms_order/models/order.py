# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re, datetime


class Order(models.Model):
    _name = 'cms.order'
    _inherit = 'mail.thread'
    _description = 'Order'

    code = fields.Char('Code')
    user_id = fields.Many2one('res.users', 'User', readonly=True, default=lambda self: self.env.uid)
    date = fields.Datetime('Date', required=True, readonly=True, default=lambda self: fields.datetime.now())
    product_category_id = fields.Many2one('cms.product.category', 'Product Category')
    product_id = fields.Many2one('cms.product', 'Product', domain="[('product_category','=',product_category_id)]")
    order_detail_ids = fields.One2many('cms.order.detail', 'order_id', 'Product(s)')
    total_price = fields.Integer('Total Price', compute='_compute_total_price')

    @api.multi
    @api.depends('order_detail_ids')
    def _compute_total_price(self):
        for record in self.order_detail_ids:
            self.total_price += record.quantity * record.price

    @api.multi
    def choose_product_button(self):
        values = []
        products = self.env['cms.product'].search([('id', '=', self.product_id.id)])
        for product in products:
            product_id = {'product_id': product.id}
            values.append(product_id)
        self.order_detail_ids = values
