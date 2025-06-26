# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class DeliveryDetailLine(models.Model):
    _name = 'delivery.detail.line'
    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CONSTRAINTS AND VALIDATIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # OTHER METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    delivery_detail_id = fields.Many2one(
        'delivery.detail',
        string='Detalle de Entrega',
        help='Referencia al detalle de entrega al que pertenece esta línea.',
    )

    stock_move_id = fields.Many2one(
        'stock.move',
        string='Movimiento de Stock',
        required=True,
        help='Movimiento de stock asociado a esta línea de entrega.',
    )

    qty = fields.Float(
        string='Cantidad',
        related='stock_move_id.quantity_done',
        store=True,
        help='Cantidad entregada según el movimiento de stock.',
    )

    uom_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        related='stock_move_id.product_uom',
        store=True,
        help='Unidad de medida utilizada en el movimiento de stock.',
    )