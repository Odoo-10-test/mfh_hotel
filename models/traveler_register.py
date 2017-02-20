# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (C) 2016 MARLON FALCON HDEZ (<http://www.marlonfalcon.cl>).
# contact: contacto@marlonfalcon.cl

# _  = Decoradores
# api  = Decoradores

from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError

class TravelerRegister(models.Model):
    _name = "traveler.register"
    # Campo para ordenar
    _order = 'name asc'
    # campo rereferente de cada registro que va en la vista
    _rec_name = 'name'
    # descripcion
    _description = 'Viajero'

    _inherit = ['mail.thread']

    # campos basisos
    name = fields.Char('Código', help="Código de Identificación del Registro", readonly=True, default='new')
    doc_number = fields.Char('RUT', size=14,help="Número de Documento de Identidad")
    doc_type = fields.Selection(
            [('D','RUT Chile'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir Chile '),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia Chile ')],
            'Tipo de Documento', size=1)
    document_date = fields.Date('Fecha de Expedición')
    last_name1 = fields.Char('Primer Apellido', size=30)
    last_name2 = fields.Char('Segundo Apellido', size=30)
    first_name = fields.Char('Nombre', size=30)
    gender = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1)
    birth_date = fields.Date('Fecha de Nacimiento')

    #  1 - 1 Buscamos la relación 
    birth_country = fields.Many2one('res.country','Pais de Nacionalidad')
    
 
    entry_date = fields.Datetime('Fecha de Entrada', default = lambda self: datetime.today()) 
    
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)

    company_id = fields.Many2one('res.company', string='Compañía', change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('traveler.register'))
            
    category_ids = fields.Many2many('res.partner.category', 'traveler_register_res_partner_ategory_rel',string="Tipo de Empresas")
    
    tags_count = fields.Integer(string='Cantidad de Etiquetas:', compute='_get_tags',
                                        help="Cantidad de Etiquetas", store=True)
                                        
    tags_count_2 = fields.Integer(string='Cantidad de Etiquetas:', compute='_get_tags_2',
                                        help="Cantidad de Etiquetas", store=True)
                                        
    @api.multi
    def set_to_sent(self):
        self.write({'state':'sent'}) 
    
    # Ejemplo de Onchange - Clase 02
                                        
    partner_id = fields.Many2one('res.partner','Socio')
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        partner_id = self.partner_id
        if partner_id:
            self.first_name = partner_id.name
            if not partner_id.country_id:
                raise UserError(_('Error 0001: No existe el pais'))
            self.birth_country = partner_id.country_id.id
                                        
    @api.multi
    @api.depends('category_ids')  # campo que se recalculará
    def _get_tags(self):
        for traveler in self:
             #self.tags_count = len([x.id for x in traveler.category_ids])
            contador = 0
            for var in traveler.category_ids:
                contador += 1
            traveler.tags_count = contador

    @api.one
    @api.depends('category_ids')  # campo que se recalculará
    def _get_tags_2(self):
        contador = 0
        for var in self.category_ids:
            contador += 1
            print "El contador es:", contador
        self.tags_count_2 = contador                       

    state = fields.Selection(
        [('draft','Nuevo'),
        ('printed','Impreso'),
        ('sent','Enviado'),],
        string='Estatus', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * 'Nuevo' Registro por imprimir.\n"
             " * 'Impreso' Cuando se ha impreso el formulario de Registro de Viajeros.\n"
             " * 'Enviado' Cuando se ha enviado el Registro de Viajeroa la Guardia.")
    
    @api.model
    def create(self, values):
        if not values.get('name'):
            values['name'] = self.env['ir.sequence'].next_by_code('traveler.register') or 'new'
        register = super(TravelerRegister, self).create(values)
        register.message_post(body=_("Registro de viajeros %s creado"%values["name"]))
        return register
