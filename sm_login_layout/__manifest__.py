{
    "name": "Background Login Layout",
    "version": "1.0.0",
    "category": "Website",
    "summary": "Custom background images and six ready made designs for the login, signup and reset pages",
    "description": """
Background Login Layout
=======================

Give the login, signup and reset password screens a background of your own:

- Custom background images on the login, signup and reset password pages.
- Several wallpapers at once, shown as a slideshow.
- Separate day and night wallpapers, switched by the visitor local time.
- Six ready made designs, from a centered card to a split screen.
- Overlay colour, opacity, blur and card transparency, all without code.
- Company logo kept on top of every design.
- Fully compatible with Odoo 19.
    """,
    "author": "Steven Marp",
    "website": "https://apps.odoo.com/apps/modules/browse?author=Steven Marp",
    "license": "OPL-1",
    "depends": ["web", "auth_signup"],
    "data": [
        "security/ir.model.access.csv",
        "data/sm_login_data.xml",
        "views/sm_login_settings_views.xml",
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "sm_login_layout/static/src/css/sm_login_layout.css",
            "sm_login_layout/static/src/js/sm_login_layout.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["static/description/banner.gif", "static/description/icon.png"],
    "price": 34.99,
    "currency": "USD",
}
