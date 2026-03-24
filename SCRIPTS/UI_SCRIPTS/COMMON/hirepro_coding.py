# Allow running this file directly: python3 SCRIPTS/UI_SCRIPTS/COMMON/sql.py
import os
import sys
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *


class SQL_Validation:
    def __init__(self):
        self.row = 1
        self.browser = None
        self._login_success = False
        write_excel_object.save_result(output_path_ui_coding_compilation)
        header = ['Coding Verification']
        write_excel_object.write_headers_for_scripts(0, 0, header, write_excel_object.black_color_bold)
        header = ['Test Cases', 'Status', 'Run Code', 'Run Tests', 'Submit&Continue']
        write_excel_object.write_headers_for_scripts(1, 0, header, write_excel_object.black_color_bold)

    def login_once(self, candidate_details):
        """
        Open browser, log in, I agree, and start test once. Call before the testcase loop.
        Uses userName/password from candidate_details (same keys as testsecurity).
        """
        self.browser = assess_ui_common_obj.initiate_browser(amsin_at_assessment_url)
        login_details = assess_ui_common_obj.ui_login_to_test(
            candidate_details.get('userName', 'AT79471566268'),
            candidate_details.get('password', 'Q*&Qzrux'),
            reload_first=True,
        )
        self._login_success = login_details == 'SUCCESS'
        if not self._login_success:
            print('login_once: login failed, status=', login_details)
            return False
        i_agreed = assess_ui_common_obj.select_i_agree()
        if not i_agreed:
            print('login_once: I Agree not completed')
            self._login_success = False
            return False
        assess_ui_common_obj.start_test_button_status()
        assess_ui_common_obj.start_test()
        time.sleep(2)
        return True

    def sql_validation(self, candidate_details):
        """Run one testcase; assumes login_once() already succeeded."""
        self.row = self.row + 1
        write_excel_object.current_status = 'Pass'
        write_excel_object.current_status_color = write_excel_object.green_color

        run_code_status = 'Fail'
        run_tests_status = 'Fail'
        submit_status = 'Fail'

        if not self._login_success:
            write_excel_object.current_status = 'Fail'
            write_excel_object.current_status_color = write_excel_object.red_color
            write_excel_object.compare_results_and_write_vertically(
                candidate_details.get('testCases'), None, self.row, 0
            )
            write_excel_object.compare_results_and_write_vertically(
                'Pass', run_code_status, self.row, 2, compare_but_write_actual_only=True
            )
            write_excel_object.compare_results_and_write_vertically(
                'Pass', run_tests_status, self.row, 3, compare_but_write_actual_only=True
            )
            write_excel_object.compare_results_and_write_vertically(
                'Pass', submit_status, self.row, 4, compare_but_write_actual_only=True
            )
            write_excel_object.compare_results_and_write_vertically(
                write_excel_object.current_status, None, self.row, 1
            )
            return

        # Select language/catalog before ACE editor if dropdown is present and not disabled
        catalog = candidate_details.get('catalog')
        if catalog:
            assess_ui_common_obj.select_coding_catalog_if_enabled(catalog)

        assess_ui_common_obj.set_ace_editor_value(
            candidate_details.get('code', 'dummy code')
        )
        time.sleep(5)

        # Run Code — expected Pass; actual Pass/Fail (green/red at col 2)
        try:
            assess_ui_common_obj.click_run_code()
            ok, err = assess_ui_common_obj.validate_run_code_finished(
                timeout=15, require_results_panel=True
            )
            if ok:
                run_code_status = 'Pass'
            else:
                print('Run Code finished validation failed:', err)
                write_excel_object.current_status = 'Fail'
                write_excel_object.current_status_color = write_excel_object.red_color
        except Exception as e:
            print('Run Code step failed:', e)
            write_excel_object.current_status = 'Fail'
            write_excel_object.current_status_color = write_excel_object.red_color

        time.sleep(5)

        # Run Tests — expected Pass; actual at col 3
        if run_code_status == 'Pass':
            try:
                assess_ui_common_obj.click_run_tests()
                ok, err = assess_ui_common_obj.validate_run_tests_finished(
                    timeout=45, require_results_panel=True, require_pass_message=True
                )
                if ok:
                    run_tests_status = 'Pass'
                else:
                    print('Run Tests finished validation failed:', err)
                    write_excel_object.current_status = 'Fail'
                    write_excel_object.current_status_color = write_excel_object.red_color
            except Exception as e:
                print('click_run_tests failed:', e)
                write_excel_object.current_status = 'Fail'
                write_excel_object.current_status_color = write_excel_object.red_color

        # Submit — expected Pass; actual at col 4
        if run_tests_status == 'Pass':
            try:
                assess_ui_common_obj.click_submit_and_continue_coding()
                ok, err = assess_ui_common_obj.validate_submit_and_continue_finished(
                    timeout=candidate_details.get('submit_banner_timeout', 25),
                    require_success_banner=candidate_details.get('require_success_banner', True),
                )
                if ok:
                    submit_status = 'Pass'
                else:
                    print('Submit & Continue finished validation failed:', err)
                    write_excel_object.current_status = 'Fail'
                    write_excel_object.current_status_color = write_excel_object.red_color
            except Exception as e:
                print('Submit step failed:', e)
                write_excel_object.current_status = 'Fail'
                write_excel_object.current_status_color = write_excel_object.red_color

        # Same pattern as testsecurity.py: write columns then Status last (col 1)
        write_excel_object.compare_results_and_write_vertically(
            candidate_details.get('testCases'), None, self.row, 0
        )
        write_excel_object.compare_results_and_write_vertically(
            'Pass', run_code_status, self.row, 2, compare_but_write_actual_only=True
        )
        write_excel_object.compare_results_and_write_vertically(
            'Pass', run_tests_status, self.row, 3, compare_but_write_actual_only=True
        )
        write_excel_object.compare_results_and_write_vertically(
            'Pass', submit_status, self.row, 4, compare_but_write_actual_only=True
        )
        write_excel_object.compare_results_and_write_vertically(
            write_excel_object.current_status, None, self.row, 1
        )

    def go_to_next_question(self, question_index):
        """
        Jump to question by index (btnQuestionIndex{question_index}).
        Call after a testcase completes so the next sql_validation runs on that question.
        """
        assess_ui_common_obj.next_question(question_index)
        time.sleep(2)
        try:
            assess_ui_common_obj.wait_for_question_to_load(question_index, timeout=10)
        except Exception:
            pass

    def close_browser(self):
        """Call once after all testcases."""
        if self.browser is not None:
            try:
                self.browser.quit()
            except Exception:
                pass
            self.browser = None


print(datetime.datetime.now())
test_security_obj = SQL_Validation()
# excel_read_obj.excel_read(input_path_ui_test_security, 0)
# excel_data = excel_read_obj.details
# catalog: string must match the coding catalog dropdown label exactly (case/spacing).
# password: leading space kept if required by login; remove if not.
testcases = [
    {
        'testCases': 'PHP',
        'userName': 'AT79471566152',
        'password': 'A$)GqKWD',
        'catalog': 'PHP',
        'code': r"""<?php  
$number=1233456;  
if($number%2==0)  
{  
 echo "$number is Even Number";   
}  
else  
{  
 echo "$number is Odd Number";  
}   """,
    },
    {
        'testCases': 'C#',
        'userName': 'crpodemotest266051582609',
        'password': ' 2Uv}',
        'catalog': 'C#',
        'code': r"""using System; using System.Collections.Generic; using System.Linq; using System.Text; namespace check1 { class Program { static void Main(string[] args) { int i; Console.Write("Enter an integer\n"); i = int.Parse(Console.ReadLine()); if (i % 2 == 0) { Console.Write("Even\n"); Console.Read(); } else { Console.Write("Odd\n"); Console.Read(); } } } }""",
    },
    {
        'testCases': 'C',
        'userName': 'crpodemotest266051582609',
        'password': ' 2Uv}',
        'catalog': 'C',
        'code': r"""#include <stdio.h>
 
int main()
{
   int n;
   
   printf("Enter an integer\n");
   scanf("%d", &n);
   
   if (n%2 == 0)
      printf("Even\n");
   else
      printf("Odd\n");
     
   return 0;
}""",
    },
    {
        'testCases': 'C++',
        'userName': 'crpodemotest266051582609',
        'password': ' 2Uv}',
        'catalog': 'C++',
        'code': r"""#include <iostream>
using namespace std;


int main()
{
   int n;
   
   cout <<"Enter an integer\n";
   cin >> n;
   
   if (n%2 == 0)
      cout <<"Even\n";
   else
      cout<<"Odd\n";
     
   return 0;
}""",
    },
]
# Login once using first row (or any row with same credentials)
if testcases:
    test_security_obj.login_once(testcases[0])
# First testcase runs on question 1 (after start_test). After each testcase except the last,
# jump to the next question so the following testcase executes there (2, 3, ...).
for i, current_excel_row in enumerate(testcases):
    print(current_excel_row)
    test_security_obj.sql_validation(current_excel_row)
    if i < len(testcases) - 1:
        next_q = i + 2  # after 1st testcase -> question 2, after 2nd -> question 3, etc.
        print('Moving to question', next_q, 'for next testcase')
        test_security_obj.go_to_next_question(next_q)

test_security_obj.close_browser()
write_excel_object.write_overall_status(len(testcases))
