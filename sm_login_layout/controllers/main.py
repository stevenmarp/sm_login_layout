import base64

from odoo import http
from odoo.http import request
from odoo.tools.mimetypes import guess_mimetype


class SmLoginController(http.Controller):

    @http.route("/sm_login/wallpaper/<int:wid>", type="http", auth="public", website=False)
    def wallpaper(self, wid, **kwargs):
        """Serve a login wallpaper to the unauthenticated login page.

        Public route, read as sudo, but nothing leaks: it only returns an image that an
        administrator marked active while the custom login is enabled.
        """
        settings = request.env["sm.login.settings"].sudo()._get_singleton()
        wallpaper = request.env["sm.login.wallpaper"].sudo().browse(wid).exists()
        if not settings.enabled or not wallpaper or not wallpaper.active or not wallpaper.image:
            return request.not_found()
        content = base64.b64decode(wallpaper.image)
        headers = [
            ("Content-Type", guess_mimetype(content, "image/jpeg")),
            ("Content-Length", len(content)),
            ("Cache-Control", "public, max-age=3600"),
        ]
        return request.make_response(content, headers=headers)
