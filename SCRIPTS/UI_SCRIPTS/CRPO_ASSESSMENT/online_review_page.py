from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin
from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import *
import time
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.UI_COMMON.crpo_ui_common import *


class OnlineReviewPage:
    def __init__(self):
        self.browser = crpo_ui_obj.initiate_browser(amsin_at_crpo_login)
        crpo_ui_obj.ui_login_to_crpo('admin', 'At@2023$$')
        crpo_ui_obj.crpo_more_functionality()
        crpo_ui_obj.crpo_assessment_candidates()
        crpo_ui_obj.crpo_assessment_candidates_filter()
        crpo_ui_obj.crpo_assessment_candidates_filter_by_id(2549989)
        crpo_ui_obj.crpo_assessment_candidates_filter_search()
        crpo_ui_obj.crpo_assessment_candidates_view_video_review()
        crpo_ui_obj.review_page_is_suspicious()
        crpo_ui_obj.select_dropdown_yes()
        crpo_ui_obj.review_page_is_suspicious_comments("This is trial")
        crpo_ui_obj.review_page_is_suspicious_submit()


online_review = OnlineReviewPage()
