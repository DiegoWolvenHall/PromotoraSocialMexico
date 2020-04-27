# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route

from odoo.odoo import http


class RestApi(Controller):

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
        print("Contacts List ---->", contacts)
        data = {'status': 200, 'response': contacts, 'message': 'Success'}
        return data

    @http.route('/api/create_contact', type='json', auth='user')
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

    @route('/api/update_contact', type='json', auth='user')
    def update_contacts(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                contact = request.env['res.partner'].sudo().search([('id', '=', rec['id'])])
                if contact:
                    contact.sudo().write(rec)
        args = {'success': True, 'message': 'Success'}
        return args

    @route('/api/auth', type='json', auth='none', methods=["POST"])
    def authenticate(self, db, login, password):
        # Before calling /api/auth, call /web?db=*** otherwise web service is not found
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()
