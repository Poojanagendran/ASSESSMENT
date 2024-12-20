import xlrd
import xlsxwriter
import datetime
from pathlib import Path


class Excel:

    def __init__(self):
        self.now = datetime.datetime.now()
        self.started_time = self.now.strftime("%d-%m-%Y %H:%M")

    def save_result(self, save_excel_path):
        self.started = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.write_excel = xlsxwriter.Workbook(Path(save_excel_path + self.started + '.xls'))
        self.ws = self.write_excel.add_worksheet()
        self.black_color = self.write_excel.add_format({'font_color': 'black', 'font_size': 9})
        self.red_color = self.write_excel.add_format(
            {'bg_color': 'red', 'bold': True, 'font_color': 'black', 'font_size': 9})
        # self.red_color = self.write_excel.add_format({'font_color': 'red', 'font_size': 9})
        self.green_color_bold = self.write_excel.add_format({'font_color': 'green', 'font_size': 9, 'bold': True})
        self.green_color = self.write_excel.add_format({'font_color': 'green', 'font_size': 9})
        self.orange_color = self.write_excel.add_format({'font_color': 'orange', 'font_size': 9})
        self.black_color_bold = self.write_excel.add_format({'font_color': 'black', 'bold': True, 'font_size': 9})
        self.over_all_status_pass = self.write_excel.add_format({'font_color': 'green', 'bold': True, 'font_size': 9})
        self.over_all_status_failed = self.write_excel.add_format({'font_color': 'red', 'bold': True, 'font_size': 9})
        self.over_all_status_color = self.over_all_status_pass
        self.current_status = "Pass"
        self.current_status_color = write_excel_object.green_color
        self.overall_status = "Pass"
        self.overall_status_color = write_excel_object.green_color

    def excelReadExpectedSheet(self, excepted_sheet_path):
        print(excepted_sheet_path)
        self.expected_excel = xlrd.open_workbook(excepted_sheet_path)
        self.expected_excel_sheet1 = self.expected_excel.sheet_by_index(0)

    def excelReadActualSheet(self, actual_sheet_path):
        print(actual_sheet_path)
        self.actual_excel = xlrd.open_workbook(actual_sheet_path)
        self.actual_excel_sheet1 = self.actual_excel.sheet_by_index(0)

    def write_headers_for_scripts(self, row, col, header_data, color):
        for header in header_data:
            self.ws.write(row, col, header, color)
            col = col + 1

    def excelWriteHeaders(self, hierarchy_headers_count):
        for i in range(0, hierarchy_headers_count):
            expected_sheet_rows = self.expected_excel_sheet1.row_values(i)
            self.ws.write(i + 1, 0, "Header - " + str(i + 1), self.black_color_bold)
            for j in range(1, self.expected_excel_sheet1.ncols):
                self.ws.write(i + 1, j + 2, expected_sheet_rows[j], self.black_color_bold)

    @staticmethod
    # this is not in USE
    def write_excel1(data_to_be_written_in_excel):
        # This is a normal write excel script without comparing any, so far not used anywhere
        # 0th index is row
        # 1st index is column
        # 2nd index is value
        # 3rd index is color coding
        for final_data in data_to_be_written_in_excel:
            write_excel_object.ws.write(final_data[0], final_data[1], final_data[2], final_data[3])

    def excelMatchValues(self, usecase_name, comparision_required_from_index, total_testcase_count):
        # This is for excel to excel comparision
        self.ws.write(0, 0, usecase_name, self.black_color_bold)
        self.write_position = comparision_required_from_index + 1
        self.overall_status = 'Pass'
        self.overall_status_color = self.green_color

        for row_indx in range(comparision_required_from_index, self.expected_excel_sheet1.nrows):
            expected_sheet_rows = self.expected_excel_sheet1.row_values(row_indx)
            actual_sheet_rows = self.actual_excel_sheet1.row_values(row_indx)
            self.ws.write(self.write_position, 0, "Expected ", self.black_color)
            self.ws.write(self.write_position + 1, 0, "Actual ", self.black_color)
            self.status = 'Pass'
            self.color = self.green_color
            for col_indx in range(0, self.expected_excel_sheet1.ncols):
                if expected_sheet_rows[col_indx] == actual_sheet_rows[col_indx]:
                    self.ws.write(self.write_position, col_indx + 2, expected_sheet_rows[col_indx], self.black_color)
                    self.ws.write(self.write_position + 1, col_indx + 2, actual_sheet_rows[col_indx], self.green_color)
                else:
                    self.ws.write(self.write_position, col_indx + 2, expected_sheet_rows[col_indx], self.black_color)
                    if not actual_sheet_rows[col_indx] or actual_sheet_rows[col_indx] == ' ':
                        self.ws.write(self.write_position + 1, col_indx + 2, "EMPTY",
                                      self.red_color)
                    else:
                        self.ws.write(self.write_position + 1, col_indx + 2, actual_sheet_rows[col_indx],
                                      self.red_color)
                        # print(expected_sheet_rows[col_indx])
                        # print(actual_sheet_rows[col_indx])
                        # print(type(expected_sheet_rows[col_indx]))
                        # print(type(actual_sheet_rows[col_indx]))
                    self.status = 'Fail'
                    self.color = self.red_color
                    self.overall_status = 'Fail'
                    self.overall_status_color = self.red_color
                self.ws.write(self.write_position, 1, self.status, self.color)
            self.write_position += 3
        self.ws.write(0, 1, "OverAll Status:- " + self.overall_status, self.overall_status_color)
        self.ws.write(0, 2, "Total Testcase Count:- " + str(total_testcase_count), self.black_color_bold)
        self.ws.write(0, 3, "Started :- " + str(self.started_time), self.black_color_bold)
        self.now = datetime.datetime.now()
        self.endeded_time = self.now.strftime("%d-%m-%Y %H:%M")
        self.ws.write(0, 4, "Ended :- " + str(self.endeded_time), self.black_color_bold)
        self.write_excel.close()

    def compare_results_and_write_vertically(self, expected_data, actual_data, row_index, column_index,
                                             compare_but_write_actual_only=None):
        if column_index == 1:
            # this logic is used to write the row status
            write_excel_object.ws.write(row_index, column_index, expected_data, self.current_status_color)
        else:
            if expected_data is not None and actual_data is not None:
                if not compare_but_write_actual_only:
                    write_excel_object.ws.write(row_index, column_index, expected_data, write_excel_object.black_color)
                    if expected_data == actual_data:
                        write_excel_object.ws.write(row_index, column_index + 1, actual_data,
                                                    write_excel_object.green_color)
                    else:
                        write_excel_object.ws.write(row_index, column_index + 1, actual_data,
                                                    write_excel_object.red_color)
                        self.current_status = 'Fail'
                        self.overall_status = 'Fail'
                        self.current_status_color = write_excel_object.red_color
                        self.overall_status_color = write_excel_object.red_color
                # some cases we want to compare the expected and actual but don't want the expected to be written
                # using this for co-cubes proctoring.
                else:
                    if expected_data == actual_data:
                        write_excel_object.ws.write(row_index, column_index, actual_data,
                                                    write_excel_object.green_color)
                    else:
                        write_excel_object.ws.write(row_index, column_index, actual_data,
                                                    write_excel_object.red_color)
                        print("This is for co-cubes test")
                        self.current_status = 'Fail'
                        self.overall_status = 'Fail'
                        self.current_status_color = write_excel_object.red_color
                        self.overall_status_color = write_excel_object.red_color

            elif expected_data is None:
                # In some special cases we don't have the expected data but want to verify weather we are getting
                # actual data in the response ex- code compiler we cannot compare memory
                # and execution time since its changing every execution this will vary so we dont have expected but
                # we know something will be returned by the api so we need below check

                if actual_data:
                    write_excel_object.ws.write(row_index, column_index, actual_data, write_excel_object.green_color)
                else:
                    write_excel_object.ws.write(row_index, column_index, actual_data, write_excel_object.red_color)
                    self.current_status = 'fail'
                    self.overall_status = 'fail'
                    self.current_status_color = write_excel_object.red_color
                    self.overall_status_color = write_excel_object.red_color
            else:
                # this part used for writing data without comparison,
                # some information does not need cmp but need to be written in every row
                write_excel_object.ws.write(row_index, column_index, expected_data, write_excel_object.black_color)

    @staticmethod
    def write_overall_status(testcases_count):
        ended = datetime.datetime.now()
        ended = "Ended:- %s" % ended.strftime("%Y-%m-%d-%H-%M-%S")
        # print(ended)
        write_excel_object.ws.write(0, 1, "Overall Status is - %s" % write_excel_object.overall_status,
                                    write_excel_object.overall_status_color)
        write_excel_object.ws.write(0, 2, 'Started:- ' + write_excel_object.started,
                                    write_excel_object.green_color_bold)
        write_excel_object.ws.write(0, 3, ended, write_excel_object.green_color_bold)
        write_excel_object.ws.write(0, 4, "Total_Test case_Count:- %s" % testcases_count,
                                    write_excel_object.green_color_bold)
        write_excel_object.write_excel.close()


write_excel_object = Excel()
