import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class CrpoCommon:
    def __init__(self):
        self.delay = 120

    def initiate_browser(self, url, path):
        # chrome option is needed in VET cases - ( its handling permissions like mic access)
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        # self.driver.switch_to.window(self.driver.window_handles[1])
        return self.driver

    def ui_login_to_crpo(self, user_name, password):
        time.sleep(5)
        self.driver.find_element(By.NAME, 'loginName').clear()
        self.driver.find_element(By.NAME, 'loginName').send_keys(user_name)
        self.driver.find_element_by_xpath('//*[@type="password"]').clear()
        # self.driver.find_element(By.XPATH, "//*[@class='form-control ng-pristine ng-untouched ng-valid ng-empty']").click()
        self.driver.find_element_by_xpath('//*[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@class="btn btn-default button_style login ng-binding"]').click()

    def crpo_more_functionality(self):
        self.driver.find_element(By.LINK_TEXT, 'More').click()

    def crpo_assessment_candidates(self):
        self.driver.find_element_by_xpath('//*[@class="ng-binding ng-scope"]').click()
        #self.driver.find_element(By.LINK_TEXT, 'Assessment Candidates').click()
        # time.sleep(5)

    def crpo_assessment_candidates_filter(self):
        time.sleep(30)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, 'cardlist-view-filter'))).click()

    def crpo_assessment_candidates_filter_by_id(self, value):
        self.driver.find_element(By.NAME, 'Ids').send_keys(value)

    def crpo_assessment_candidates_filter_search(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

    def crpo_assessment_candidates_view_video_review(self):
        self.driver.find_element(By.XPATH, '//*[@class="img_margin_1 pointer ng-binding ng-scope"]').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(5)

    def review_page_is_suspicious(self):
        value = "//*[@class='btn btn-default dropdown-toggle pull-right']"
        self.driver.find_element_by_xpath(value).click()
        time.sleep(2)

    def review_page_is_suspicious_comments(self, comments):
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '//*[@class = "form-control ng-pristine ng-untouched ng-valid ng-empty"]').send_keys(comments)
        # self.driver.find_element_by_xpath(
        #     '//*[@class = "form-control ng-pristine ng-valid ng-not-empty ng-touched"]').send_keys(comments)

    def review_page_is_suspicious_submit(self):
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        # self.driver.find_element(By.LINK_TEXT('Submit')).click()

    def select_dropdown_yes(self):
        self.driver.find_element(By.LINK_TEXT, 'Yes').click()


crpo_ui_obj = CrpoCommon()
