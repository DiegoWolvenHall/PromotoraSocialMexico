# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Controller, request

class ApiJsonrpc(http.Controller):
    @http.route('/api/auth', type='json', auth='none', methods=["POST"])
    def authenticate(self, db, login, password):        
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()
    
    @http.route('/api/get_contacts', type='json', auth='user')
    def get_contacts(self):
        contact_rec = request.env['res.partner'].search([])
        contacts = []
        for rec in contact_rec:
            vals = {
                'id': rec.id,
                'name': rec.name
            }
            contacts.append(vals)
        data = {'status': 200, 'response': contacts, 'message': 'Success'}
        return data
    
    @http.route('/api/create_partner', type='json', auth='user')
    def create_contacts(self, **rec):
        global response
        if request.jsonrequest:
            
            if rec['name'] and rec['vat']:
                vals = {
                    'name': rec['name'],
                    'vat': rec['vat'],
                    'website': rec['website'],
                    'street': rec['street'],
                    'street2': rec['street2'],
                    'zip': rec['zip'],
                    'city': rec['city'],
                    'state_id': rec['state_id'],
                    'email': rec['email'],
                    'phone': rec['phone'],
                    'mobile': rec['mobile'],
                    'is_company': rec['is_company']
                }
                try:
                    new_contact = request.env['res.partner'].sudo().create(vals)
                    response = {'success': True, 'message': 'Success', 'ID': new_contact.id}
                except ValueError:
                    print(ValueError)
                    response = {'success': True, 'message': 'Error al insertar valores'}
            else:
                response = {'success': True, 'message': 'Faltan valores'}
        args = response
        return args           
                        
#     @http.route('/api_jsonrpc/api_jsonrpc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('api_jsonrpc.listing', {
#             'root': '/api_jsonrpc/api_jsonrpc',
#             'objects': http.request.env['api_jsonrpc.api_jsonrpc'].search([]),
#         })

#     @http.route('/api_jsonrpc/api_jsonrpc/objects/<model("api_jsonrpc.api_jsonrpc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('api_jsonrpc.object', {
#             'object': obj
#         })
