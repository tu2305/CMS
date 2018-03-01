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
    @api.depends('product_id')
    def _choose_product(self):
        values = []
        product_select_id = []
        if len(self.order_detail_ids) > 0:
            for obj in self.order_detail_ids:
                if obj.select == True:
                    product_id = {'product_id': obj.product_id.id, 'select': True}
                    values.append(product_id)
                    product_select_id.append(obj.product_id.id)
        products = self.env['cms.product'].search(['product_id', '=', self.product_id])
        for product in products:
            product_id = {'product_id': product.id}
            values.append(product_id)
        self.order_detail_ids = values

    @api.multi
    def choose_product_button(self):
        data = self.read(['product_id', 'order_detail_ids'])[0]
        list_product = data['order_detail_ids']
        choose_product = self.env['cms.order.detail'].search(['&', ('id', 'in', list_product), ('select', '=', True)])
        for product in choose_product:
            self.env['cms.product'].search([('id', '=', product.product_id.id)]).write()
        self.env['cms.order.detail'].search([('select', '=', False)]).unlink()
        return {
            'name': 'Product',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'cms.product',
            'target': 'pivot',
            'domain': []
        }
