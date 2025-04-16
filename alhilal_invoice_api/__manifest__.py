{
    "name": "Alhilal Academy Apis",
    "version": "1.0",
    "description": """AMS Api""",
    "author": "Raneem Obeidat",
    "depends": [
        "base",
        "account",
        # TODO : Update alhilal_custom_modules to the correct module name custom_modules
        "custom_modules",
        "subscriptions_modification",
        "hr",
    ],
    "data": [
        "views/add_analytic_distribution.xml",
        "views/account_move_inherit.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
