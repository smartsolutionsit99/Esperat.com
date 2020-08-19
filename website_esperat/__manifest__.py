{
    'name': 'Esperat',
    'category': 'Website',
    'sequence': 54,
    'summary': 'Esperat',
    'version': '2.0',
    'description': """
    """,
    'depends': ['website_form','mail'],
    'data': [
        'data/sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/spare_part.xml',
        'data/website_esperat_data.xml',
        'views/website_esperat_templates.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': True,
}
