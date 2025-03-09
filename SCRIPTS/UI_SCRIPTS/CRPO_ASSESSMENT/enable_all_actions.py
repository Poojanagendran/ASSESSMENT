from SCRIPTS.COMMON.io_path import amsin_automation_crpo_login, chrome_driver_path, automation_manage_actions
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_pooja_automation
from SCRIPTS.UI_COMMON.crpo_ui_common import *

class EnableGridActions:
    def __init__(self):
        print("Inside enable actions ")

    @staticmethod
    def enable_all_actions():
        try:
            browser = crpo_ui_obj.initiate_browser(amsin_automation_crpo_login, chrome_driver_path)
            crpo_ui_obj.ui_login_to_crpo(cred_crpo_pooja_automation.get('user'), cred_crpo_pooja_automation.get('password'))
            crpo_ui_obj.move_to_manage_actions_page(automation_manage_actions)
            crpo_ui_obj.select_and_save_all_actions()
            # print("hello")


        except Exception as e:
            print(f"Error occurred while enabling actions: {e}")

        finally:
            if 'browser' in locals() and browser:
                browser.quit()


enable_actions_obj = EnableGridActions()
