from odoo import api, fields, models

DESIGNS = [
    ("1", "Design 1 - Centered Card"),
    ("2", "Design 2 - Split Screen"),
    ("3", "Design 3 - Floating Glass Card"),
    ("4", "Design 4 - Card on the Right"),
    ("5", "Design 5 - Colour Panel"),
    ("6", "Design 6 - Branded Top Bar"),
]


class SmLoginSettings(models.Model):
    _name = "sm.login.settings"
    _description = "Login Layout Settings"

    name = fields.Char(default="Login Layout", readonly=True)
    enabled = fields.Boolean(string="Enable Custom Login", default=False)
    design = fields.Selection(DESIGNS, string="Design", default="1", required=True)

    overlay_color = fields.Char(string="Overlay Colour", default="#0E2D59")
    overlay_opacity = fields.Float(string="Overlay Opacity", default=0.45)
    card_opacity = fields.Float(string="Card Opacity", default=1.0)
    blur = fields.Integer(string="Background Blur (px)", default=0)
    show_logo = fields.Boolean(string="Show Company Logo", default=True)

    night_enabled = fields.Boolean(string="Separate Night Wallpaper", default=False)
    night_start = fields.Integer(string="Night Starts (hour 0-23)", default=19)
    night_end = fields.Integer(string="Night Ends (hour 0-23)", default=6)
    slideshow_interval = fields.Integer(string="Slideshow Interval (seconds)", default=8)

    wallpaper_ids = fields.One2many("sm.login.wallpaper", "settings_id", string="Wallpapers")

    @api.model
    def _get_singleton(self):
        record = self.search([], limit=1)
        if not record:
            record = self.create({"name": "Login Layout"})
        return record

    @staticmethod
    def _clamp(value, low, high, default):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return default
        return max(low, min(value, high))

    @api.model
    def _sm_login_config(self):
        """Values the login template and the frontend script need, read as sudo."""
        record = self.sudo()._get_singleton()
        if not record.enabled:
            return {"enabled": False}
        walls = record.wallpaper_ids.filtered(lambda w: w.active and w.image)
        day = [str(w.id) for w in walls if w.moment in ("any", "day")]
        night = [str(w.id) for w in walls if w.moment in ("any", "night")]
        return {
            "enabled": True,
            "design": record.design or "1",
            "overlay_color": record.overlay_color or "#000000",
            "overlay_opacity": self._clamp(record.overlay_opacity, 0.0, 1.0, 0.45),
            "card_opacity": self._clamp(record.card_opacity, 0.2, 1.0, 1.0),
            "blur": int(self._clamp(record.blur, 0, 40, 0)),
            "show_logo": record.show_logo,
            "night_enabled": bool(record.night_enabled and night),
            "night_start": record.night_start % 24,
            "night_end": record.night_end % 24,
            "interval": int(self._clamp(record.slideshow_interval, 2, 120, 8)),
            "day": ",".join(day),
            "night": ",".join(night),
        }

    def action_open_login_settings(self):
        record = self._get_singleton()
        return {
            "type": "ir.actions.act_window",
            "name": "Login Layout",
            "res_model": "sm.login.settings",
            "view_mode": "form",
            "res_id": record.id,
            "target": "current",
        }


class SmLoginWallpaper(models.Model):
    _name = "sm.login.wallpaper"
    _description = "Login Wallpaper"
    _order = "sequence, id"

    settings_id = fields.Many2one("sm.login.settings", ondelete="cascade", required=True)
    name = fields.Char(default="Wallpaper")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    moment = fields.Selection(
        [("any", "Any Time"), ("day", "Day"), ("night", "Night")],
        string="Shown", default="any", required=True)
    image = fields.Image(string="Image", required=True)
