# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re, datetime, dateutil.parser
import logging

_logger = logging.getLogger(__name__)


class Order(models.Model):
    _name = 'cms.order'
    _inherit = 'mail.thread'
    _description = 'Order'

    code = fields.Char('Code', compute='_compute_code', readonly=True, store=True)
    user_id = fields.Many2one('res.users', 'User', readonly=True, default=lambda self: self.env.uid)
    date = fields.Datetime('Date', required=True, readonly=True, default=lambda self: fields.datetime.now())
    product_category_id = fields.Many2one('cms.product.category', 'Product Category',
                                          default=lambda self: self.env['cms.product.category'].search([])[0])
    product_id = fields.Many2one('cms.product', 'Product', domain="[('product_category','=',product_category_id)]")
    order_detail_ids = fields.One2many('cms.order.detail', 'order_id', 'Product(s)')
    total_price = fields.Float('Total Price', digits=(3, 0), compute='_compute_total_price', default=0)
    pay = fields.Float('Pay', required=True, digits=(3, 0))
    repay = fields.Float('Repay', digits=(3, 0), compute='_compute_repay')
    status = fields.Selection([('order', 'Order'), ('payment', 'Payment'), ('paid', 'Paid'), ('cancel', 'Cancel')],
                              default="order")

    @api.multi
    @api.onchange('product_category_id')
    def change_product_category(self):
        self.product_id = False

    @api.multi
    @api.depends('date')
    def _compute_code(self):
        for record in self:
            values = record.search([])
            _logger.warning(values)
            if not values:
                date = dateutil.parser.parse(record.date).date()
                date = str(date) + '-001'
                record.code = date
            else:
                record.code = '000'

    @api.multi
    @api.depends('order_detail_ids')
    def _compute_total_price(self):
        for record in self.order_detail_ids:
            self.total_price += record.quantity * record.price

    @api.multi
    @api.depends('total_price', 'pay')
    def _compute_repay(self):
        if self.pay > self.total_price:
            self.repay = self.pay - self.total_price

    @api.multi
    def choose_product_button(self):
        values = []
        if len(self.order_detail_ids) > 0:
            for order in self.order_detail_ids:
                if order.product_id == self.product_id:
                    order.quantity += 1
        else:
            products = self.env['cms.product'].search([('id', '=', self.product_id.id)])
            for product in products:
                product_id = {'product_id': product.id}
                values.append(product_id)
        self.order_detail_ids = values

    @api.multi
    def order(self):
        self.pay = 0
        self.status = 'order'

    @api.multi
    def payment(self):
        self.status = 'payment'

    @api.multi
    def paid(self):
        self.status = 'paid'
