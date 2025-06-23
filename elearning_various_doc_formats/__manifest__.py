# -*- coding: utf-8 -*-
{
    'name': "eLearning Office Doc Formats",

    'summary': """eLearning Various Doc Format
           elearning student progress
           video
           school
           Microsoft Office Viewer only previews office document types, listed below:
            Microsoft Word (.DOCX, .DOCM, .DOTM, .DOTX, .DOC)
            Microsoft Excel (.XLSX, .XLSB, .XLS, .XLSM)
            Microsoft PowerPoint (.PPTX, .PPSX, .PPT, .PPS, .PPTM, .POTM, .PPAM, .POTX, .PPSM)""",


        'description': """
         eLearning Various Doc Format
           elearning student progress
           video
           school
           Microsoft Office Viewer only previews office document types, listed below:
            Microsoft Word (.DOCX, .DOCM, .DOTM, .DOTX, .DOC)
            Microsoft Excel (.XLSX, .XLSB, .XLS, .XLSM)
            Microsoft PowerPoint (.PPTX, .PPSX, .PPT, .PPS, .PPTM, .POTM, .PPAM, .POTX, .PPSM)

           
        """,
    'author': 'David Montero Crespo',
    'license': 'AGPL-3',
    'category': 'Website',
    'version': '16.0',
    'website': "https://softwareescarlata.com/",
    # any module necessary for this one to work correctly
    'images': ['static/description/1.png'],
    'depends': ['base','website_slides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/slide_slide.xml',

    ],
    'currency': 'EUR',
    'price': 40,
    # only loaded in demonstration mode

}
