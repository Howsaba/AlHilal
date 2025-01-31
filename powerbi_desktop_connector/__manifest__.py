# -*- coding: utf-8 -*-
{
  'name': "PowerBI Direct Connector",

     'summary': """
       	odoo power bi connector, odoo powerbi connector, odoo powerbi desktop, Power bi, desktop, power bi desktop, powerbi desktop, powerbi service, power bi service, power bi dashboard, powerbi dashboard, microsoft power bi, microsoft powerbi, ms powerbi ,ms, ms office, Google Looker studio, look, looker data sources, analytics, analytic, analysis, report, reports, chart, charts, dashboard, dashboards,  , power bi cloud, powerbi cloud, KPI, kpis, slicer, slicers, graph, graphs, bar graph, forecasting, forcasting, prediction, google, datastudio, data studio, data refresh, gateway, data gateway, refresh, schedule, scheduled,AI, ML, artificial, artificial intelligence, intelligence, intelligent, sale forecasting, sales forecasting, inventory, datasource, data source, sources, community, connector, excel, spreadsheet, SAS, Qlik, Qlik VIew, QlikView, KNIME, python, spark, apache, apache spark, sisense, talend, ibm, zoho, domo, klip folio, klipfolio,  bigdata, big data, google data studio, datastudio, google datastudio,  connectors, odoo connector, odoo connecter, connecter, odoo connectors, odoo analytics, odoo ai, odoo dahboard, odoo powerbi, odoo power bi,  , connecter,   datasources, google bigquery, big query, AI Dashboard, Google AI, AI analytics, Looker studio, data studio, dashboard ai, dashboard with ai, connecter, ai connector, connector ai, data hub, data lake, machine learning, ML, artificial intelligence, AI reports,. powerbi, Powerbi connector, power bi connector, power bi data, powerbi data, odoo power bi connection. Odoo Dashboard, CRM Dashboard, Inventory Dashboard, Sales Dashboard, Account Dashboard, Invoice Dashboard, Revamp Dashboard, Best Dashboard, Odoo Best Dashboard, Odoo Apps Dashboard, Best Ninja Dashboard, Analytic Dashboard, Pre Configured Dashboard, Create Dashboard, Beautiful Dashboard, Customized Robust Dashboard, Predefined Dashboard, Multiple Dashboards, Advance Dashboard, Beautiful Powerful Dashboards, Chart Graphs Table View, All In One Dynamic Dashboard, Accounting Stock Dashboard, Pie Chart Dashboard, Modern Dashboard, Dashboard Studio, Dashboard Builder, Dashboard Designer, Odoo Studio. Azure, data gateway, datagateway, onpremises,powerbi service, service,online,data analytics, business intelligence, odoo17, odoo18, real-time data, data analysis, power bi integration,
       """,

    'description': """
        Power bi, Google Looker studio, look, looker data sources, analytics, analytic, analysis, report, reports, chart, charts, dashboard, dashboards,  , power bi cloud, powerbi cloud, KPI, kpis, slicer, slicers, graph, graphs, bar graph, forecasting, forcasting, prediction, google, datastudio, data studio, data refresh, gateway, data gateway, refresh, schedule, scheduled,AI, ML, artificial, artificial intelligence, intelligence, intelligent, sale forecasting, sales forecasting, inventory, datasource, data source, sources, community, connector, excel, spreadsheet, SAS, Qlik, Qlik VIew, QlikView, KNIME, python, spark, apache, apache spark, sisense, talend, ibm, zoho, domo, klip folio, klipfolio,  bigdata, big data, google data studio, datastudio, google datastudio,  connectors, odoo connector, odoo connecter, connecter, odoo connectors, odoo analytics, odoo ai, odoo dahboard, odoo powerbi, odoo power bi,  , connecter,   datasources, google bigquery, big query, AI Dashboard, Google AI, AI analytics, Looker studio, data studio, dashboard ai, dashboard with ai, connecter, ai connector, connector ai, data hub, data lake, machine learning, ML, artificial intelligence, AI reports,. powerbi, Powerbi connector, power bi connector, power bi data, powerbi data, odoo power bi connection. Odoo Dashboard, CRM Dashboard, Inventory Dashboard, Sales Dashboard, Account Dashboard, Invoice Dashboard, Revamp Dashboard, Best Dashboard, Odoo Best Dashboard, Odoo Apps Dashboard, Best Ninja Dashboard, Analytic Dashboard, Pre Configured Dashboard, Create Dashboard, Beautiful Dashboard, Customized Robust Dashboard, Predefined Dashboard, Multiple Dashboards, Advance Dashboard, Beautiful Powerful Dashboards, Chart Graphs Table View, All In One Dynamic Dashboard, Accounting Stock Dashboard, Pie Chart Dashboard, Modern Dashboard, Dashboard Studio, Dashboard Builder, Dashboard Designer, Odoo Studio. Azure, data gateway, datagateway, onpremises,powerbi service, service,online
    """,

    'author': "TechFinna",
    'website': "https://techfinna.com/odoo-powerbi-connector/pricing/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Connector',
    'version': '1.2',
    'price': 949,
    'currency': 'USD',
    'live_test_url': 'https://www.youtube.com/watch?v=XfjPP8LW0l4',
    'support': "info@techfinna.com",
    'license': 'OPL-1',
    # any module necessary for this one to work correctly
    'depends': ['base',],
    'images': ['static/description/banner.png'],
    "external_dependencies": {"python" : ["pip"]},

    # always loaded
    'data': [
        'views/settings.xml',
    ],


    "application": True,
    "installable": True,
    
}
