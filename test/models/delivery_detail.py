# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class DeliveryDetail(models.Model):
    _name = 'delivery.detail'

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------
    def action_mark_invoiced(self):
        """
        Marca los detalles de entrega como facturados solo si no están ya facturados
        y pagada
        """
        for record in self:
            if not record.invoiced and record.account_move_id and record.account_move_id.payment_state == 'paid':
                record.invoiced = True

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

    account_move_id = fields.Many2one(
        'account.move',
        string='Factura',
        required=True,
        help='Factura de cliente asociada a este detalle de entrega.',
    )

    picking_id = fields.Many2one(
        'stock.picking',
        string='Entrega (Picking)',
        required=True,
        help='Documento de entrega asociado a esta factura.',
    )

    invoiced = fields.Boolean(
        string='Facturado',
        help='Indica si este detalle ya ha sido facturado.',
    )

    delivery_detail_line_ids = fields.One2many(
        'delivery.detail.line',
        'delivery_detail_id',
        string='Líneas de detalle de entrega',
        help='Líneas asociadas a este detalle de entrega.',
    )
