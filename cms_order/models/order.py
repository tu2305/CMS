# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re, datetime


class Order(models.Model):
    _name = 'cms.order'
    _inherit = 'mail.thread'
    _description = 'Order'

    # code = fields.Char('Code', compute='_compute_code')
    code = fields.Char('Code')
    temp_code = fields.Integer('Temp Code')
    user_id = fields.Many2one('res.users', 'User', readonly=True, default=lambda self: self.env.uid)
    date = fields.Datetime('Date', required=True, readonly=True, default=lambda self: fields.datetime.now())
    order_detail_ids = fields.One2many('cms.order.detail', 'order_id', 'Product(s)')
    total_price = fields.Integer('Total Price', compute='_compute_total_price')

    @api.multi
    @api.depends('order_detail_ids')
    def _compute_total_price(self):
        for record in self.order_detail_ids:
            self.total_price += record.quantity * record.price

    # @api.multi
    # @api.depends('date')
    # def _compute_code(self):
    #     order_value = []
    #     orders = self.env['cms.order'].search([])
    #     # for order in orders:
    #     #     order_id = {'order_id': order.id}
    #     #     order_value.append(order_id)
    #     if not orders:
    #         self.temp_code = 1
    #         self.code = self.date.strftime('%d-%m-%y') + '00' + self.temp_code
    #     else:
    #         value = 0
    #         for order in orders:
    #             if order.temp_code > value:
    #                 value = order.temp_code
    #         value += 1
    #         if value < 10:
    #             self.code = self.date.strftime('%d-%m-%y') + '00' + value
    #         elif value < 100:
    #             self.code = self.date.strftime('%d-%m-%y') + '0' + value
    #         else:
    #             self.code = self.date.strftime('%d-%m-%y') + value
