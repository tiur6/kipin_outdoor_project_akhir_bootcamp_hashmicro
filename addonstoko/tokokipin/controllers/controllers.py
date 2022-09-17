# -*- coding: utf-8 -*-
# from odoo import http


# class Tokokipin(http.Controller):
#     @http.route('/tokokipin/tokokipin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tokokipin/tokokipin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tokokipin.listing', {
#             'root': '/tokokipin/tokokipin',
#             'objects': http.request.env['tokokipin.tokokipin'].search([]),
#         })

#     @http.route('/tokokipin/tokokipin/objects/<model("tokokipin.tokokipin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tokokipin.object', {
#             'object': obj
#         })
