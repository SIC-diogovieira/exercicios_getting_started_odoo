# -*- coding: utf-8 -*-
{
    'name': "Estate",
    'application': True,
    'summary': "Defines the 'gallery' view",
    'description': """
        Defines a new type of view ('Estate') which allows to visualize images.
    """,

    'version': '0.1',
    'depends': ['web',"base","sale","sale_management","stock","mrp","purchase", "contacts","purchase_stock"],
    'data': ['Security/ir.model.access.csv',
             'Views/estate_property_views.xml',
             'Views/estate_property_type_views.xml',
             'Views/estate_property_tags_views.xml',
             'Views/estate_property_offers_views.xml',
             'Views/estate_menus.xml'],
    'license': 'AGPL-3'
}
