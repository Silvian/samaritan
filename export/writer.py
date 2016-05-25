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
import time, datetime
from django.utils.translation import ugettext


def write_to_excel(download_data, report_title=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)

    # Here we will adding the code to add data
    worksheet_s = workbook.add_worksheet("Summary")

    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    # title_text = u"{0} {1}".format(report_title, ugettext("Report"))
    # worksheet_s.merge_range('B2:H2', title_text, title)

    # worksheet_s.write(4, 0, ugettext("No"), header)
    # worksheet_s.write(4, 1, ugettext("Town"), header)
    # worksheet_s.write(4, 3, ugettext(u"Max T. (℃)"), header)
    # the rest of the headers from the HTML file

    # for idx, data in enumerate(download_data):
    #     row = 5 + idx
    #     worksheet_s.write_number(row, 0, idx + 1, cell_center)
    #     worksheet_s.write_string(row, 1, data.town.name, cell)
    #     worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)
    #     # the rest of the data
    #
    # description_col_width = 10
    # # ...
    # for idx, data in enumerate(download_data):
    #     # ...
    #     worksheet_s.write_string(row, 3, data.description, cell)
    #     if len(data.description) > description_col_width:
    #         description_col_width = len(data.description)
    #         # ...
    # worksheet_s.set_column('D:D', description_col_width)
    #
    # observations_col_width = 25
    # # ...
    # for idx, data in enumerate(download_data):
    #     # ...
    #     observations = data.observations.replace('\r', '')
    #     worksheet_s.write_string(row, 9, observations, cell)
    #     observations_rows = compute_rows(observations, observations_col_width)
    #     worksheet_s.set_row(row, 15 * observations_rows)
    # # ...
    # worksheet_s.set_column('J:J', observations_col_width)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for member in download_data:
        worksheet_s.write(row, col, member.first_name)
        worksheet_s.write(row, col + 1, member.last_name)
        worksheet_s.write(row, col + 2, member.date_of_birth.strftime('%d-%m-%Y'))
        worksheet_s.write(row, col + 3, member.telephone)
        worksheet_s.write(row, col + 4, member.address.number)
        worksheet_s.write(row, col + 5, member.address.street)
        worksheet_s.write(row, col + 6, member.address.locality)
        worksheet_s.write(row, col + 7, member.address.city)
        worksheet_s.write(row, col + 8, member.address.post_code)
        worksheet_s.write(row, col + 9, member.email)
        worksheet_s.write(row, col + 10, member.is_baptised)
        if member.baptismal_date is not None:
            worksheet_s.write(row, col + 11, member.baptismal_date.strftime('%d-%m-%Y'))
        else:
            worksheet_s.write(row, col + 11, "N/A")
        worksheet_s.write(row, col + 12, member.baptismal_place)
        worksheet_s.write(row, col + 13, member.is_member)
        if member.membership_type is not None:
            worksheet_s.write(row, col + 14, member.membership_type.name)
        else:
            worksheet_s.write(row, col + 14, "Not specified")
        if member.membership_date is not None:
            worksheet_s.write(row, col + 15, member.membership_date.strftime('%d-%m-%Y'))
        else:
            worksheet_s.write(row, col + 15, "N/A")
        worksheet_s.write(row, col + 16, member.is_active)
        worksheet_s.write(row, col + 17, member.church_role.name)
        worksheet_s.write(row, col + 18, member.notes)

        row += 1

        # Write a total using a formula.
        # worksheet_s.write(row, 0, 'Total')
        # worksheet_s.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
    file_data = output.getvalue()
    # file_data contains the Excel file
    return file_data


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')

    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows += 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows += 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows += 1
    return rows


def file_name_date():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H.%M.%S')
