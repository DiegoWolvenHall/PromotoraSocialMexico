# Copyright 2016 Florent de Labarre
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import uuid

from odoo import api, fields, models, exceptions

from odoo.addons import base
base.models.res_users.USER_PRIVATE_FIELDS.\
    append('oauth_master_uuid')


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _generate_oauth_master_uuid(self):
        return uuid.uuid4().hex

    oauth_access_token_ids = fields.One2many(
        comodel_name='auth.oauth.multi.token',
        inverse_name='user_id',
        string='OAuth tokens',
        copy=False,
        readonly=True,
        groups='base.group_system'
    )
    oauth_access_max_token = fields.Integer(
        string='Max number of simultaneous connections',
        default=10,
        required=True
    )
    oauth_master_uuid = fields.Char(
        string='Master UUID',
        copy=False,
        readonly=True,
        required=True,
        default=lambda self: self._generate_oauth_master_uuid(),
    )

    @property
    def multi_token_model(self):
        return self.env['auth.oauth.multi.token']

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """Override to handle sign-in with multi token."""
        res = super()._auth_oauth_signin(
            provider, validation, params)

        oauth_uid = validation['user_id']
        # Lookup for user by oauth uid and provider
        user = self.search([
            ('oauth_uid', '=', oauth_uid),
            ('oauth_provider_id', '=', provider)]
        )
        if not user:
            raise exceptions.AccessDenied()
        user.ensure_one()
        # user found and unique: create a token
        self.multi_token_model.create({
            'user_id': user.id,
            'oauth_access_token': params['access_token'],
            'active_token': True,
        })

        # Asigna tipo de usuario : Interno al usuario de Microsoft
        # Asigna id de usuario a empleado ya existente
        try:

            id_e = self.env['hr.employee'].search([('work_email', 'ilike', validation['userPrincipalName'])],
                                                  limit=1).id

            if not (id_e is None):

                id_u = self.env['hr.employee'].search([('id', '=', id_e), ('user_id', '=', user.id)], limit=1).id

                if id_u is False:

                    employee = self.env['hr.employee'].search([('id', '=', id_e)])
                    employee.write({'user_id': user.id})

                    id_p = self.env['res.partner'].search([('email', 'ilike', validation['userPrincipalName'])],
                                                          limit=1).id

                    if id_u is False:
                        partner = self.env['res.partner'].search([('id', '=', id_p)])
                        partner.write({'company_id': '1'})

                        # self.env.cr.execute("""UPDATE res_users SET share = false WHERE id = """ + str(user.id))
                    # self.env.cr.commit()

                    # self.env.cr.execute("""insert into res_groups_users_rel(gid,uid) values(11,""" + str(user.id)
                    #                     + """)""")
                    # self.env.cr.commit()

                    self.env.cr.execute("""insert into res_groups_users_rel(gid,uid) values(10,""" + str(user.id)
                                        + """)""")
                    self.env.cr.commit()

                    self.env.cr.execute("""insert into res_groups_users_rel(gid,uid) values(6,""" + str(user.id)
                                        + """)""")
                    self.env.cr.commit()

                    self.env.cr.execute("""insert into res_groups_users_rel(gid,uid) values(7,""" + str(user.id)
                                        + """)""")
                    self.env.cr.commit()

                    self.env.cr.execute("""UPDATE res_groups_users_rel SET gid = 1 WHERE uid = """ + str(user.id))
                    self.env.cr.commit()

                    user = self.env['res.users'].search([('id', '=', user.id)])
                    user.write({'share': False})

        except():

            print("An exception occurred")

        return res

    def action_oauth_clear_token(self):
        """Inactivate current user tokens."""
        self.mapped('oauth_access_token_ids')._oauth_clear_token()
        for res in self:
            res.oauth_master_uuid = self._generate_oauth_master_uuid()

    @api.model
    def _check_credentials(self, password):
        """Override to check credentials against multi tokens."""
        try:
            return super()._check_credentials(password)
        except exceptions.AccessDenied:
            res = self.multi_token_model.sudo().search([
                ('user_id', '=', self.env.uid),
                ('oauth_access_token', '=', password),
                ('active_token', '=', True),
            ])
            if not res:
                raise

    def _get_session_token_fields(self):
        res = super()._get_session_token_fields()
        res.remove('oauth_access_token')
        return res | {'oauth_master_uuid'}
