from odoo import models, fields, api, _
import re, datetime


class OrderDetail(models.Model):
    _name = 'cms.order.detail'
    _description = 'Order Detail'

    order_id = fields.Many2one('cms.order', 'Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('cms.product', 'Product', required=True)
    quantity = fields.Integer('Quantity', required=True, default=1)
    price = fields.Integer('Price', related='product_id.price', readonly=True)
    select = fields.Boolean('Select')

