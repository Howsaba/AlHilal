from odoo import models, api
from passlib.context import CryptContext


class ResUsersApikeys(models.Model):
    _inherit = "res.users.apikeys"
    _crypt_context = CryptContext(
        schemes=["pbkdf2_sha512", "plaintext"], deprecated="auto"
    )

    def _get_apikey_name(self, *, scope, key):
        index = key[:8]
        self.env.cr.execute(
            """
        SELECT name, user_id, key
        FROM {} INNER JOIN res_users u ON (u.id = user_id)
        WHERE u.active AND index = %s AND (scope IS NULL OR scope = %s)
      """.format(
                self._table
            ),
            [index, scope],
        )
        for name, user_id, stored_key in self.env.cr.fetchall():
            if self._crypt_context.verify(key, stored_key):
                return {"name": name, "user_id": user_id}
        return None
