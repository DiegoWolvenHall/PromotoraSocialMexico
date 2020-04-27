# -*- coding: utf-8 -*-
# from odoo import http


# class ApiJsonrpc(http.Controller):
#     @http.route('/api_jsonrpc/api_jsonrpc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

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
