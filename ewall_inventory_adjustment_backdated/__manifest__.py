# -*- coding: utf-8 -*-
{
    'name': 'Inventory Adjustment Backdated',

    'summary': """ The Odoo Inventory Adjustments Backdate module provides businesses with the ability to make inventory adjustments for past dates, ensuring that inventory records remain accurate and up-to-date. By allowing backdated adjustments, this module helps maintain consistency across product moves, stock moves, stock valuation layers, and journal entries, enhancing the overall reliability of inventory data. It offers a comprehensive audit trail of adjustments, making it easier for businesses to track and review historical changes. With a user-friendly interface that supports adding notes to backdated adjustments, the module simplifies inventory management and supports compliance with accounting standards. """,

    'description': """ The Odoo Inventory Adjustments Backdate module is an essential tool for businesses needing to adjust inventory levels for previous dates, providing accurate tracking and transparency across the entire system. It integrates seamlessly with key areas of Odoo, including product and stock moves, stock valuation layers, and journal entries, ensuring all backdated adjustments are reflected accurately. The module automatically updates related entries, aligning inventory and accounting records for products with real-time valuation methods. This feature not only supports maintaining accurate inventory data but also ensures compliance with financial reporting requirements by offering a clear audit trail of all adjustments. The intuitive interface allows users to backdate adjustments and add relevant notes, making it an ideal solution for businesses seeking precise control over their inventory records and corrections.Odoo Inventory Adjustments Backdate, Odoo Inventory Module, Odoo Backdated Inventory Adjustments, Odoo Stock Adjustments, Odoo Real-time Valuation, Odoo Inventory Management, Odoo Stock Valuation, Inventory Adjustment Module for Odoo, Odoo Audit Trail Inventory, Odoo Inventory Correction, Inventory Adjustments backdate, Inventory date change, Stock Quantity Backdated, Stock Move Backdated, Stock Move Line Backdated, Stock Valuation Backdated, Account Move Backdated, Backdated, Product Move Backdated, Move History Backdated, Journal Entry Backdated, Valuation Backdated, Force Date in Inventory Adjustment, Inventory Backdate, Change Effective Date, Backdate In Inventory, Stock Backdate, Warehouse Backdate, Stock Force Date, Inventory Force Date, Inventory Adjustment Force Date. """,

    'version': '17.0',
    'category': 'Inventory',
    'author': "EWall Solutions Pvt. Ltd.",
    'company': "EWall Solutions Pvt. Ltd.",
    'maintainer': 'EWall Solutions Pvt. Ltd.',
    "support": "support@ewallsolutions.com",
    "website": "https://www.ewallsolutions.com",
    'license': 'OPL-1',
    'price':'20.00',
    'currency':'USD',
    'depends': ['stock', 'account', 'stock_account'],
    'data': [
        'views/inventory_adjustment_views.xml',
    ],
    'images': ['static/description/images/banner.png',],
    'installable': True,
    'application': False,
}