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
from django.utils.translation import ugettext


DATE_FORMAT = '%d-%m-%Y'
FILE_NAME_DATE = '%Y-%m-%d-%H.%M.%S'


def write_to_excel(download_data, report_title=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    title_text = u"{0} {1}".format(report_title, ugettext("Report"))

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

    worksheet_s.write(4, 0, ugettext("First Name"), header)
    worksheet_s.set_column('A:A', 15)
    worksheet_s.write(4, 1, ugettext("Last Name"), header)
    worksheet_s.set_column('B:B', 15)
    worksheet_s.write(4, 2, ugettext("Date of Birth"), header)
    worksheet_s.set_column('C:C', 15)
    worksheet_s.write(4, 3, ugettext("Telephone"), header)
    worksheet_s.set_column('D:D', 15)
    worksheet_s.write(4, 4, ugettext("No."), header)
    worksheet_s.set_column('E:E', 5)
    worksheet_s.write(4, 5, ugettext("Street"), header)
    worksheet_s.set_column('F:F', 15)
    worksheet_s.write(4, 6, ugettext("Locality"), header)
    worksheet_s.set_column('G:G', 15)
    worksheet_s.write(4, 7, ugettext("City"), header)
    worksheet_s.set_column('H:H', 15)
    worksheet_s.write(4, 8, ugettext("Postcode"), header)
    worksheet_s.set_column('I:I', 15)
    worksheet_s.write(4, 9, ugettext("Email"), header)
    worksheet_s.set_column('J:J', 30)
    worksheet_s.write(4, 10, ugettext("Details"), header)
    worksheet_s.set_column('K:K', 30)
    worksheet_s.write(4, 11, ugettext("Is Baptised"), header)
    worksheet_s.set_column('L:L', 10)
    worksheet_s.write(4, 12, ugettext("Baptismal Date"), header)
    worksheet_s.set_column('M:M', 15)
    worksheet_s.write(4, 13, ugettext("Baptismal Place"), header)
    worksheet_s.set_column('N:N', 20)
    worksheet_s.write(4, 14, ugettext("Is Member"), header)
    worksheet_s.set_column('O:O', 10)
    worksheet_s.write(4, 15, ugettext("Membership Type"), header)
    worksheet_s.set_column('P:P', 15)
    worksheet_s.write(4, 16, ugettext("Membership Date"), header)
    worksheet_s.set_column('Q:Q', 15)
    worksheet_s.write(4, 17, ugettext("Is Active"), header)
    worksheet_s.set_column('R:R', 10)
    worksheet_s.write(4, 18, ugettext("Church Role"), header)
    worksheet_s.set_column('S:S', 15)
    worksheet_s.write(4, 19, ugettext("Notes"), header)
    worksheet_s.set_column('T:T', 30)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 5
    col = 0

    # Iterate over the data and write it out row by row.
    for member in download_data:
        worksheet_s.write(row, col, member.first_name)
        worksheet_s.write(row, col + 1, member.last_name)
        worksheet_s.write(row, col + 2, member.date_of_birth.strftime(DATE_FORMAT))
        worksheet_s.write(row, col + 3, member.telephone)
        worksheet_s.write(row, col + 4, member.address.number)
        worksheet_s.write(row, col + 5, member.address.street)
        worksheet_s.write(row, col + 6, member.address.locality)
        worksheet_s.write(row, col + 7, member.address.city)
        worksheet_s.write(row, col + 8, member.address.post_code)
        worksheet_s.write(row, col + 9, member.email)
        worksheet_s.write(row, col + 10, member.details)
        worksheet_s.write(row, col + 11, member.is_baptised)
        if member.baptismal_date is not None:
            worksheet_s.write(row, col + 12, member.baptismal_date.strftime(DATE_FORMAT))
        else:
            worksheet_s.write(row, col + 12, "N/A")
        worksheet_s.write(row, col + 13, member.baptismal_place)
        worksheet_s.write(row, col + 14, member.is_member)
        if member.membership_type is not None:
            worksheet_s.write(row, col + 15, member.membership_type.name)
        else:
            worksheet_s.write(row, col + 15, "Not specified")
        if member.membership_date is not None:
            worksheet_s.write(row, col + 16, member.membership_date.strftime(DATE_FORMAT))
        else:
            worksheet_s.write(row, col + 16, "N/A")
        worksheet_s.write(row, col + 17, member.is_active)
        worksheet_s.write(row, col + 18, member.church_role.name)
        worksheet_s.write(row, col + 19, member.notes)

        row += 1

    workbook.close()
    file_data = output.getvalue()
    # file_data contains the Excel file
    return file_data


def file_name_date():
    return datetime.datetime.fromtimestamp(time.time()).strftime(FILE_NAME_DATE)
