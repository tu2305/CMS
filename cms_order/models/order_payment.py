# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re, datetime, dateutil.parser
import logging

_logger = logging.getLogger(__name__)


class Order(models.Model):
    _name = 'cms.order.payment'
    _inherit = 'mail.thread'
    _description = 'Order'

    order_id = fields.Many2one('cms.order', 'Order Payment')
    code = fields.Char('Code', related='order_id.code', readonly=True)
    user_id = fields.Many2one('res.users', 'User', related='order_id.user_id', readonly=True)
    date = fields.Datetime('Date', related='order_id.date', readonly=True)
    order_detail_ids = fields.One2many('cms.order.detail', 'order_id', 'Product(s)',
                                       related='order_id.order_detail_ids', readonly=True)
    total_price = fields.Integer('Total Price', related='order_id.total_price', readonly=True)
