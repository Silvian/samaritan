#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""


import StringIO
import xlsxwriter
import time
import datetime
from samaritan.constants import WriterConstants
from django.utils.translation import ugettext


def write_to_excel(download_data, report_title=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    title_text = u"{0} {1}".format(report_title, ugettext(WriterConstants.TITLE_TEXT))

    # Here we will adding the code to add data
    worksheet_s = workbook.add_worksheet(title_text)

    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bold': True,
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    worksheet_s.merge_range('B2:H2', title_text, title)

    worksheet_s.write(4, 0, ugettext(WriterConstants.FIRST_NAME), header)
    worksheet_s.set_column('A:A', 15)
    worksheet_s.write(4, 1, ugettext(WriterConstants.LAST_NAME), header)
    worksheet_s.set_column('B:B', 15)
    worksheet_s.write(4, 2, ugettext(WriterConstants.DATE_OF_BIRTH), header)
    worksheet_s.set_column('C:C', 15)
    worksheet_s.write(4, 3, ugettext(WriterConstants.TELEPHONE), header)
    worksheet_s.set_column('D:D', 15)
    worksheet_s.write(4, 4, ugettext(WriterConstants.ADDRESS_NO), header)
    worksheet_s.set_column('E:E', 5)
    worksheet_s.write(4, 5, ugettext(WriterConstants.ADDRESS_STREET), header)
    worksheet_s.set_column('F:F', 15)
    worksheet_s.write(4, 6, ugettext(WriterConstants.ADDRESS_LOCALITY), header)
    worksheet_s.set_column('G:G', 15)
    worksheet_s.write(4, 7, ugettext(WriterConstants.ADDRESS_CITY), header)
    worksheet_s.set_column('H:H', 15)
    worksheet_s.write(4, 8, ugettext(WriterConstants.ADDRESS_POSTCODE), header)
    worksheet_s.set_column('I:I', 15)
    worksheet_s.write(4, 9, ugettext(WriterConstants.EMAIL), header)
    worksheet_s.set_column('J:J', 30)
    worksheet_s.write(4, 10, ugettext(WriterConstants.DETAILS), header)
    worksheet_s.set_column('K:K', 30)
    worksheet_s.write(4, 11, ugettext(WriterConstants.IS_BAPTISED), header)
    worksheet_s.set_column('L:L', 10)
    worksheet_s.write(4, 12, ugettext(WriterConstants.BAPTISMAL_DATE), header)
    worksheet_s.set_column('M:M', 15)
    worksheet_s.write(4, 13, ugettext(WriterConstants.BAPTISMAL_PLACE), header)
    worksheet_s.set_column('N:N', 20)
    worksheet_s.write(4, 14, ugettext(WriterConstants.IS_MEMBER), header)
    worksheet_s.set_column('O:O', 10)
    worksheet_s.write(4, 15, ugettext(WriterConstants.MEMBERSHIP_TYPE), header)
    worksheet_s.set_column('P:P', 15)
    worksheet_s.write(4, 16, ugettext(WriterConstants.MEMBERSHIP_DATE), header)
    worksheet_s.set_column('Q:Q', 15)
    worksheet_s.write(4, 17, ugettext(WriterConstants.IS_ACTIVE), header)
    worksheet_s.set_column('R:R', 10)
    worksheet_s.write(4, 17, ugettext(WriterConstants.GDPR), header)
    worksheet_s.set_column('S:S', 10)
    worksheet_s.write(4, 18, ugettext(WriterConstants.CHURCH_ROLE), header)
    worksheet_s.set_column('T:T', 15)
    worksheet_s.write(4, 19, ugettext(WriterConstants.NOTES), header)
    worksheet_s.set_column('U:U', 30)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 5
    col = 0

    # Iterate over the data and write it out row by row.
    for member in download_data:
        worksheet_s.write(row, col, member.first_name)
        worksheet_s.write(row, col + 1, member.last_name)
        worksheet_s.write(row, col + 2, member.date_of_birth.strftime(WriterConstants.DATE_FORMAT))
        worksheet_s.write(row, col + 3, member.telephone)
        worksheet_s.write(row, col + 4, member.address.number)
        worksheet_s.write(row, col + 5, member.address.street)
        worksheet_s.write(row, col + 6, member.address.locality)
        worksheet_s.write(row, col + 7, member.address.city)
        worksheet_s.write(row, col + 8, member.address.post_code)
        worksheet_s.write(row, col + 9, member.email)
        worksheet_s.write(row, col + 10, member.details)
        if member.is_baptised:
            worksheet_s.write(row, col + 11, WriterConstants.YES)
        else:
            worksheet_s.write(row, col + 11, WriterConstants.NO)
        if member.baptismal_date is not None:
            worksheet_s.write(row, col + 12, member.baptismal_date.strftime(WriterConstants.DATE_FORMAT))
        else:
            worksheet_s.write(row, col + 12, WriterConstants.NOT_APPLICABLE)
        worksheet_s.write(row, col + 13, member.baptismal_place)
        if member.is_member:
            worksheet_s.write(row, col + 14, WriterConstants.YES)
        else:
            worksheet_s.write(row, col + 14, WriterConstants.NO)
        if member.membership_type is not None:
            worksheet_s.write(row, col + 15, member.membership_type.name)
        else:
            worksheet_s.write(row, col + 15, WriterConstants.NOT_SPECIFIED)
        if member.membership_date is not None:
            worksheet_s.write(row, col + 16, member.membership_date.strftime(WriterConstants.DATE_FORMAT))
        else:
            worksheet_s.write(row, col + 16, WriterConstants.NOT_APPLICABLE)
        if member.is_active:
            worksheet_s.write(row, col + 17, WriterConstants.YES)
        else:
            worksheet_s.write(row, col + 17, WriterConstants.NO)
        if member.gdpr:
            worksheet_s.write(row, col + 17, WriterConstants.YES)
        else:
            worksheet_s.write(row, col + 17, WriterConstants.NO)
        worksheet_s.write(row, col + 18, member.church_role.name)
        worksheet_s.write(row, col + 19, member.notes)

        row += 1

    workbook.close()
    file_data = output.getvalue()
    # file_data contains the Excel file
    return file_data


def file_name_date():
    return datetime.datetime.fromtimestamp(time.time()).strftime(WriterConstants.FILE_NAME_DATE)
