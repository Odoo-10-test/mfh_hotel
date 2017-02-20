# -*- coding: utf-8 -*-
{
    'name': 'MFH Hotel',
    'author': 'Marlon Falcón Hernández',
    'category': 'Sales',
    'description': """
Ejemplo de módulo
=====================================================
        """,
    'version': '10.0.0.1',
    'depends': ['base','mail','report'],
    'data': [
         'data/ir_sequence.xml',    
         'views/traveler_register_view.xml',
         'report/paper_format.xml',
         'report/report_traveler_register.xml',
         'report/report.xml',
    ],
    'demo': [],
    'auto_install': False,
}
