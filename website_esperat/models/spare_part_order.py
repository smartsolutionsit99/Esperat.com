# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api,_
import json

class esperatOrder(models.Model):
    _name = 'spare.order'
    _description = 'Spare Parts Orders'
    _inherit = ['mail.thread']

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('spare.order.seq') or 'New'
        ids = self.env['spare.order.stage'].search([])
        if ids:
            vals['stage_id'] = ids[0].id
        rec = super(esperatOrder, self).create(vals)
        if vals.get('line_string') and rec:
            line_portal = json.loads(vals.get('line_string'))
            for line in line_portal:
                line_vals = {}
                line_vals['part_no'] = line_portal[line]['part_no']
                line_vals['serial'] = line_portal[line]['serial']
                line_vals['part_name'] = line_portal[line]['part_name']
                line_vals['model_text'] = line_portal[line]['model_text']
                line_vals['maker_id'] = self.env['maker.maker'].search([('name','=',line_portal[line]['maker_id'])],limit=1).id or False
                line_vals['model_id'] = self.env['model.model'].search([('name','=',line_portal[line]['model_id'])],limit=1).id or False
                line_vals['qty'] = line_portal[line]['qty']
                line_vals['year'] = line_portal[line]['year']
                line_vals['order_id'] = rec.id
                self.env['spare.order.line'].create(line_vals)
            rec.write({'line_string': False})
        return rec

    #Customer Info
    customer_name = fields.Char(
        string='Name',
        required=False)
    customer_phone = fields.Char(
        string='Phone',
        required=False)
    customer_address = fields.Text(
        string='Address',
        required=False)
    name = fields.Char(
        string='Order No.',
        readonly=True)

    category  = fields.Selection(
        string='Category',
        selection=[('car', 'Cars'),
                   ('truck', 'Trucks'),
                   ('heavy_equipment', 'Heavy Equipment'),
                   ('generator', 'Generators'),],
        required=False, )

    stage_id = fields.Many2one(
        comodel_name='spare.order.stage',
        string='Status',
        required=False)
    line_ids  = fields.One2many(
        comodel_name='spare.order.line',
        inverse_name='order_id',
        string='Order Lines',
        required=False)
    line_string = fields.Char(
        string='Line String Creator',
        required=False)


class esperatOrderLine(models.Model):
    _name = 'spare.order.line'
    _description = 'Spare Parts Order Lines'

    order_id = fields.Many2one(
        comodel_name='spare.order',
        string='Order',
        required=False)
    # part no for all
    part_no = fields.Char(
        string='Part No.',
        required=False)
    # truck /car -- vin 'shace ni'
    # or serial/engine no mandatory for generator and heavy

    serial = fields.Char(
        string='Serial/Engine/Vin No.',
        required=False)

    part_name = fields.Char(
        string='Part Name',
        required=False)
    # for car/
    maker_id = fields.Many2one(
        comodel_name='maker.maker',
        string='Maker',
        required=False)

    model_id = fields.Many2one(
        comodel_name='model.model',
        string='Model',
        required=False)
    #for anything other than car
    model_text = fields.Char(
        string='Model',
        required=False)

    year = fields.Char(
        string='Year',
        required=False, )

    vendor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor',
        required=False)
    qty = fields.Float(
        string='Quantity',
        required=False)
    price = fields.Float(
        string='Price',
        required=False)
    total = fields.Float(
        string='Total',readonly=True)

    @api.onchange('qty','price')
    def _onchange_qty_price(self):
        self.total = self.qty * self.price

class orderSages(models.Model):
    _name = 'spare.order.stage'
    _description = 'Order Stages'
    _order = 'sequence'

    name  = fields.Char(
        string='Name',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        required=False)


class makerMarker(models.Model):
    _name = 'maker.maker'
    _description = 'Car/Equipment Maker'

    image = fields.Binary(string="Image",)

    name = fields.Char(
        string='',
        required=False)

    category = fields.Selection(
        string='Category',
        selection=[('car', 'Cars'),
                   ('truck', 'Trucks'),
                   ('heavy_equipment', 'Heavy Equipment'),
                   ('generator', 'Generators'), ],
        required=True, )


class modelModel(models.Model):
    _name = 'model.model'
    _description = 'Car/Equipment Model'

    name = fields.Char(
        string='Name',
        required=True)

    maker_id  = fields.Many2one(
        comodel_name='maker.maker',
        string='Maker',
        required=True)

    category = fields.Selection(
        string='Category',
        selection=[('car', 'Cars'),
                   ('truck', 'Trucks'),
                   ('heavy_equipment', 'Heavy Equipment'),
                   ('generator', 'Generators'), ],related="maker_id.category",store=True )


    #
    # def website_form_input_filter(self, request, values):
    #     values['medium_id'] = values.get('medium_id') or \
    #                           self.default_get(['medium_id']).get('medium_id') or \
    #                           self.sudo().env.ref('utm.utm_medium_website').id
    #     values['team_id'] = values.get('team_id') or \
    #                         request.website.crm_default_team_id.id
    #     values['user_id'] = values.get('user_id') or \
    #                         request.website.crm_default_user_id.id
    #     return values

#
# class Website(models.Model):
#     _inherit = 'website'
#
#     def _get_crm_default_team_domain(self):
#         if self.env.user.has_group('crm.group_use_lead'):
#             return [('use_leads', '=', True)]
#         else:
#             return [('use_opportunities', '=', True)]
#
#     crm_default_team_id = fields.Many2one(
#         'crm.team', string='Default Sales Teams',
#         default=lambda self: self.env['crm.team'].search([], limit=1),
#         domain=lambda self: self._get_crm_default_team_domain(),
#         help='Default Sales Team for new leads created through the Contact Us form.')
#     crm_default_user_id = fields.Many2one(
#         'res.users', string='Default Salesperson', domain=[('share', '=', False)],
#         help='Default salesperson for new leads created through the Contact Us form.')
