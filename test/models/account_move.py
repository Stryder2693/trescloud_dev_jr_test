# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------
    def action_show_delivery_details(self):
        """
        Muestra los detalles de entrega (delivery.detail) asociados a la factura (account.move).
        Este método se utiliza para abrir una vista de lista y formulario de los detalles de entrega"""
        self.ensure_one()

        return {
            'name': 'Delivery Details',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.detail',
            'view_mode': 'tree,form',
            'domain': [('account_move_id', '=', self.id)],
            'target': 'current',
            'context': {'default_account_move_id': self.id},
        }



    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Sobrescribe el método create para crear detalles de entrega (delivery.detail) automáticamente
        """
        moves = super().create(vals_list)
        moves.create_delivery_detail()

        return moves
    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------
    
    def _compute_delivery_detail_count(self):
        """"
        Obtiene la cantidad de detalles de entrega (delivery.detail) asociados a cada factura (account.move).
        """
        for move in self:
            
            count = self.env['delivery.detail'].sudo().search_count([
                ('account_move_id', '=', move.id)
            ])
            move.delivery_detail_count = count

    def _compute_delivery_detail_ids(self):
        """
        Obtiene los detalles de entrega (delivery.detail) asociados a cada factura (account.move).
        """
        for move in self:
            details = self.env['delivery.detail'].sudo().search([
                ('account_move_id', '=', move.id)
            ])
            move.delivery_detail_ids = details

    # ------------------------------------------------------
    # CONSTRAINTS AND VALIDATIONS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # OTHER METHODS
    # ------------------------------------------------------
    def create_delivery_detail(self):
        """
        Este método crea registros de detalle de entrega (delivery.detail) para cada factura de cliente.
        La lógica es la siguiente:
        - Para cada factura (account.move):
            - Verifica que sea factura de cliente (move_type 'out_invoice') y que tenga exactamente una orden de venta asociada.
            - Busca el picking relacionado a la orden de venta que no esté cancelado y verifica que solo haya uno.
            - Comprueba que el picking esté en estado 'done' (entregado).
            - Asegura que todas las líneas de la orden de venta estén completamente entregadas (qty_delivered igual a product_uom_qty).
        """

        for move in self:
            # Si no tiene una única orden de venta, no es una factura de cliente o no tiene un delivery.picking de entrega, no hacemos nada
            source_orders = move.line_ids.mapped('sale_line_ids.order_id')
            if move.move_type != 'out_invoice' and  len(source_orders) != 1:
                continue
            order = source_orders[0]

            pickings = order.picking_ids.filtered(lambda p: p.state != 'cancel')
            if len(pickings) != 1:
                continue

            picking = pickings[0]

            if picking.state != 'done':
                continue
            # Verificar que todas las líneas estén completamente entregadas
            if any(line.qty_delivered != line.product_uom_qty for line in order.order_line):
                continue
            #Aunque no exista el permiso no se debe limitar la creación de facturas.
            detail = self.env['delivery.detail'].sudo().create({
                'account_move_id': move.id,
                'picking_id': picking.id,
                'invoiced': False,  # Por defecto, no está facturado aunque no es necesario poner el campo
            })
            # Crear las líneas desde los stock.move entregados
            for stock_move in picking.move_ids:
                if stock_move.state == 'done' and stock_move.quantity_done > 0:
                    self.env['delivery.detail.line'].sudo().create({
                        'delivery_detail_id': detail.id,
                        'stock_move_id': stock_move.id,
                    })


    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------
    delivery_detail_count = fields.Integer(
        string="Delivery Details Count",
        compute='_compute_delivery_detail_count',
    )

    delivery_detail_ids = fields.One2many(
        'delivery.detail',
        'account_move_id',
        string='Detalles de Entrega',
        compute='_compute_delivery_detail_ids',
    )




    

   

