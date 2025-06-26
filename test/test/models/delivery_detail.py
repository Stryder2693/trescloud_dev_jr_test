# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class DeliveryDetail(models.Model):
    _name = 'delivery.detail'

    account_move_id = fields.Many2one(
        'account.move',
    )
    picking_id = fields.Many2one(
        'stock.picking',
    )

    invoiced = fields.Boolean(
    )

    delivery_detail_line_ids = fields.One2many(
        'delivery.detail.line',
        'delivery_detail_id',
    )