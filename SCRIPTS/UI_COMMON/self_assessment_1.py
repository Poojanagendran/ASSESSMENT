import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException


class SelfAssessmentLogin:
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
        self.driver.switch_to.window(self.driver.window_handles[0])
        return self.driver

    def ui_login_to_tenant(self, user_name, password):
        time.sleep(5)
        try:
            # To select vendors/tpo/placecom option before login page
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Vendors/TPO/Placecom")]').click()
            time.sleep(2)
            self.driver.find_element(By.NAME, 'loginName').clear()
            self.driver.find_element(By.NAME, 'loginName').send_keys(user_name)
            self.driver.find_element(By.XPATH, "//input[@type='password']").clear()
            self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-default button_style login ng-binding"]').click()
            # self.driver.get(
            #     "https://amsin.hirepro.in/crpo/#/crpodemo/assessment/selfAssessment/eyJ0ZXN0SWQiOjE5NzgxfQ==/question")

            time.sleep(5)
            login_status = 'SUCCESS'

        except Exception as e:
            print(e)
            login_status = 'FAILED'
        return login_status

    def create_test_sa(self, test_name):
        time.sleep(2)
        # value = "Automation_sa_" + test_name
        growl_message_locator = (By.XPATH, "//div[@class='growl-message ng-binding']")
        try:
            # select new test
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@class = "btn-group show_form no-padding pointer btn button_radius '
                               'ng-binding ng-scope"]'))).click()
            # self.driver.find_element(By.XPATH,
            #                          '//*[@class = "btn-group show_form no-padding pointer btn button_radius '
            #                          'ng-binding ng-scope"]').click()
            # time.sleep(15)
            value = f"Automation_sa_{test_name}"
            time.sleep(5)

            self.driver.find_element(By.XPATH, "//input[@ng-model='vm.test.name']").send_keys(value)
            # create test
            add_section = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class = "btn btn-primary_"]')))
            add_section.click()
            # self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary_"]').click()

            print("test created")
            growl_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(growl_message_locator)
            )
            print("Test status ", growl_message.text)
            x = growl_message.text

            if x == 'Test Created Successfully.':
                test_status = 'SUCCESS'
            else:
                test_status = 'FAILED'

           # time.sleep(10)
        except Exception as e:
            print(f"Exception occurred: {e}")
            test_status = 'FAILED'
        # except TimeoutException as e:
        #     print(f"TimeoutException occurred: {e}")
        #     self.driver.save_screenshot('timeout_exception.png')
        #     test_status = 'FAILED'
        # except NoSuchElementException as e:
        #     print(f"NoSuchElementException occurred: {e}")
        #     self.driver.save_screenshot('no_such_element_exception.png')
        #     test_status = 'FAILED'
        # except WebDriverException as e:
        #     print(f"WebDriverException occurred: {e}")
        #     self.driver.save_screenshot('webdriver_exception.png')
        #     test_status = 'FAILED'
        # except Exception as e:
        #     print(f"Exception occurred: {e}")
        #     self.driver.save_screenshot('general_exception.png')
        #     test_status = 'FAILED'

        return test_status

    def select_plus(self, index):
        try:
            plus = self.driver.find_elements(By.XPATH, '//*[@class = "fa fa-plus"]')
            plus[index].click()
            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def select_text_toggle_button(self, index):
        try:
            text = self.driver.find_element(By.XPATH, "//i[@class='fa fa-fw fa-text-width']")
            text[index].click
            time.sleep(2)

            # plus = self.driver.find_elements(By.XPATH, '//*[@class = "fa fa-plus"]')
            # plus[index].click()
            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def select_question_attributes(self):
        try:

            wait = WebDriverWait(self.driver, 20)
            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tad-container button.dropdown-toggle")))
            dropdown_button.click()

            difficulty = self.driver.find_element(By.XPATH,
                                                  '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if difficulty.is_displayed():
                ele = self.driver.find_element(By.XPATH, '//a[@title="Low"]')
                ele.click()
                # print("Selected difficulty")
            else:
                print("Difficulty not selected")

            self.driver.find_element(By.XPATH,
                                     '//input[@placeholder="Author"]/following-sibling::div/button').click()
            category = self.driver.find_element(By.XPATH,
                                                '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if category.is_displayed():
                ele = self.driver.find_element(By.XPATH, "//a[@title='administrator']")
                ele.click()
                # print("Selected author")
            else:
                print("Author not selected")

            self.driver.find_element(By.XPATH,
                                     '//input[@placeholder="Category"]/following-sibling::div/button').click()
            category = self.driver.find_element(By.XPATH,
                                                '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if category.is_displayed():
                ele = self.driver.find_element(By.XPATH, '//a[@title="Automobile Engineering"]')
                ele.click()
                # print("Selected category")
            else:
                print("Category not selected")

            self.driver.find_element(By.XPATH,
                                     '//input[@placeholder="Topic"]/following-sibling::div/button').click()
            topic = self.driver.find_element(By.XPATH,
                                             '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if topic.is_displayed():
                ele = self.driver.find_element(By.XPATH, '//a[@title="Automotive Chassis"]')
                ele.click()
                # print("Selected topic")
            else:
                print("Topic not selected")

            self.driver.find_element(By.XPATH,
                                     '//input[@placeholder="Status"]/following-sibling::div/button').click()
            status = self.driver.find_element(By.XPATH,
                                              '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if status.is_displayed():
                ele = self.driver.find_element(By.XPATH, '//a[@title="QA Approved"]')
                ele.click()
                # print("Selected status")
            else:
                print("Status not selected")

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def create_mcq_q(self):
        try:
            print("creating mcq q")
            # add question - mcq
            time.sleep(10)
            self_assessment_obj.select_plus(3)
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@class = "tab-option"]').click()
            self_assessment_obj.select_question_attributes()

            time.sleep(2)
            self.driver.find_element(By.XPATH, "//i[@class='fa fa-fw fa-text-width']").click()
            time.sleep(2)
            ele2 = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Question Description']")
            ele2.send_keys("po mcq create q sa automation don't use /ans : B ")
            time.sleep(5)

            elements = self.driver.find_elements(By.XPATH,
                                                 "//textarea[@class='form-control ng-pristine ng-untouched ng-valid "
                                                 "ng-empty']")
            c = 1
            for e in elements:
                e.send_keys(c)
                c += 1
            time.sleep(2)

            option = self.driver.find_elements(By.XPATH, "//*[@name='answer']")
            option[1].click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-default btn-success btn-sm ng-scope"]').click()

            time.sleep(10)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def create_rtc_q(self):
        try:
            print("creating rtc q")
            # creating question - rtc
            time.sleep(5)
            self_assessment_obj.add_new_section()
            wait = WebDriverWait(self.driver, 20)
            rtc_sec = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Paragraph Section']")))
            rtc_sec.click()
            time.sleep(1)

            self_assessment_obj.select_plus(3)

            self.driver.find_element(By.XPATH, '//*[@class = "tab-option"]').click()

            self_assessment_obj.select_question_attributes()

            time.sleep(2)
            # self_assessment_obj.select_text_toggle_button(1)
            self.driver.find_element(By.CSS_SELECTOR,
                                     '''label[ng-class="{'btn-primary':vm.data.paragraphAsText}"] i[class='fa fa-fw fa-text-width']''').click()
            rtc_parent_text = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Paragraph']")
            rtc_parent_text.send_keys("po RTC create q with 2 child sa automation don't use ")
            self.driver.find_element(By.XPATH,
                                     '''//label[@ng-class="{'btn-primary':!question.questionStringAsHtml}"]//i[@class='fa fa-fw fa-text-width']''').click()
            rtc_child_text = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Question']")
            rtc_child_text.send_keys("child q1 sa automation /ans : A ")

            elements = self.driver.find_elements(By.XPATH,
                                                 "//textarea[@class='form-control ng-pristine ng-untouched ng-valid "
                                                 "ng-empty']")
            options = 1
            for e in elements:
                e.send_keys(options)
                options += 1
            time.sleep(1)

            option = self.driver.find_elements(By.XPATH, "//*[@name='answer']")
            option[0].click()
            time.sleep(2)

            self.driver.find_element(By.CSS_SELECTOR,
                                     '''button[ng-click="vm.actionClicked('addNewQuestion');"]''').click()
            time.sleep(2)

            self.driver.find_element(By.XPATH,
                                     '''//label[@ng-class="{'btn-primary':!question.questionStringAsHtml}"]//i[@class='fa fa-fw fa-text-width']''').click()
            rtc_child_text = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Question']")
            rtc_child_text.send_keys("child q2 sa automation /ans : B ")

            elements = self.driver.find_elements(By.XPATH,
                                                 "//textarea[@class='form-control ng-pristine ng-untouched ng-valid "
                                                 "ng-empty']")
            options = 1
            for e in elements:
                e.send_keys(options)
                options += 1
            time.sleep(2)

            option = self.driver.find_elements(By.XPATH, "//*[@name='answer']")
            option[1].click()
            time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-success.btn-sm.ng-scope').click()

            time.sleep(10)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def create_subjective_q(self):
        try:
            growl_message_locator = (By.XPATH, "//div[@class='growl-message ng-binding']")
            print("creating subjective q")
            # creating question - subjective
            time.sleep(5)
            self_assessment_obj.add_new_section()
            wait = WebDriverWait(self.driver, 20)
            subjective_sec = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Subjective Section']")))
            subjective_sec.click()
            time.sleep(1)

            self_assessment_obj.select_plus(4)

            self.driver.find_element(By.XPATH, '//*[@class = "tab-option"]').click()

            self_assessment_obj.select_question_attributes()

            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR,
                                     '''label[ng-class="{'btn-primary':vm.data.questionAsText}"] i[class='fa fa-fw fa-text-width']''').click()

            subjective_qd = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Question Description']")
            subjective_qd.send_keys('''po subjective create q with all config self-assessment automation don't use
            self_assessment.xls
            Which is your favourite food, dish or cuisine? Write two paragraphs about your favourite food, dish or cuisine. Make sure you follow all the rules about sentences and paragraphs you have learnt.''')

            sample_answer = self.driver.find_element(By.XPATH,
                                                     "//textarea[@placeholder='Sample Answer']")
            sample_answer.send_keys(
                '''I am very foodie. I love to eat. Among the number of foods, Pizza is my favourite food because it tastes and smells fabulous. My Mom cooks the best Pizzas in the world. I always ask her to make Pizza. In Pizzas, I love onion cheese Pizza a lot. This is because cheese pizza is healthy and makes me strong. To create fun we also organize pizza races in terms of who can eat the maximum number of pizzas. I can eat many pizzas at a time.''')

            self.driver.find_element(By.CSS_SELECTOR,
                                     '''label[ng-class="{'btn-primary':vm.data.questionInfo.isDynamicAnswerConfig === true}"]''').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH,
                                     "//span[text()='TextArea']/ancestor::div[contains(@class,'panel')]/descendant::input[@type='text' and @ng-model='answerConfig.name']").send_keys(
                'TextArea')
            self.driver.find_element(By.XPATH,
                                     "//span[text()='TextArea']/ancestor::div[contains(@class,'panel')]/descendant::label[normalize-space()='Yes']").click()

            self.driver.find_element(By.XPATH,
                                     "//span[text()='Attachment']/ancestor::div[contains(@class,'panel')]/descendant::input[@type='text' and @ng-model='answerConfig.name']").send_keys(
                'Attachment ')
            self.driver.find_element(By.XPATH,
                                     "//span[text()='Attachment']/ancestor::div[contains(@class,'panel')]/descendant::label[text()='Yes']").click()
            self.driver.find_element(By.XPATH,
                                     "//span[text()='Attachment']/ancestor::div[contains(@class,'panel')]/descendant::div[@title='Extensions']//span[@class='caret']").click()
            self.driver.find_element(By.CSS_SELECTOR, "button[data-ng-click='vm.moveAllItemsRight();']").click()
            self.driver.find_element(By.XPATH, "//a[text()='Done']").click()

            self.driver.find_element(By.XPATH,
                                     "//span[text()='Capture']/ancestor::div[contains(@class,'panel')]/descendant::input[@type='text' and @ng-model='answerConfig.name']").send_keys(
                'Capture ')
            self.driver.find_element(By.XPATH,
                                     "//span[text()='Capture']/ancestor::div[contains(@class,'panel')]/descendant::label[normalize-space()='Yes']").click()

            time.sleep(5)
            label = self.driver.find_element(By.XPATH,
                                             "//b[normalize-space()='Do you want to Upload File in Question Description']")
            actions = ActionChains(self.driver)
            actions.move_to_element(label).perform()
            label.click()
            checkbox = self.driver.find_element(By.XPATH,
                                                "//input[@type='checkbox' and @ng-model='vm.data.attachment.replaceQuestionDescription']")
            print("File uploaded in Question Description : ", checkbox.is_selected())

            self.driver.find_element(By.XPATH,
                                     "//input[@placeholder='File name to be saved with extensions. Eg: fileName.csv,fileName.txt']").send_keys(
                'self_assessment.xls')

            upload_element = self.driver.find_element(By.XPATH, "//div[@class='ng-isolate-scope']//input[@type='file']")
            file_path = 'D:/automation_new/ASSESSMENT/PythonWorkingScripts_InputData/UI/Assessment/self_assessment.xls'
            # Use send_keys to simulate selecting a file
            upload_element.send_keys(file_path)
            growl_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(growl_message_locator)
            )
            print(growl_message.text)
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-success.btn-sm.ng-scope').click()
            time.sleep(5)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def create_fib_q(self):
        try:
            # growl_message_locator = (By.XPATH, "//div[@class='growl-message ng-binding']")
            print("creating FIB q")
            # creating question - subjective
            time.sleep(5)
            self_assessment_obj.add_new_section()
            wait = WebDriverWait(self.driver, 20)
            subjective_sec = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Fill In The Blank Section']")))
            subjective_sec.click()
            time.sleep(1)

            self_assessment_obj.select_plus(5)
            self.driver.find_element(By.XPATH, '//*[@class = "tab-option"]').click()
            self_assessment_obj.select_question_attributes()
            time.sleep(2)

            iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@class, 'cke_wysiwyg_frame')]")
            self.driver.switch_to.frame(iframe)
            editable_body = self.driver.find_element(By.XPATH,
                                                     "//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")
            editable_body.get_attribute("innerHTML")
            editable_body.send_keys("po fib create q self-assessment automation don't use\n int(1234) ")

            self.driver.switch_to.default_content()
            create_blank_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create Blank')]"))
            )
            create_blank_button.click()
            self.driver.find_element(By.XPATH,
                                     '//input[@placeholder="Answer Type"]/following-sibling::div/button').click()
            category = self.driver.find_element(By.XPATH,
                                                '//*[@class = "dropdown-menu ng-scope am-fade bottom-left"]')
            time.sleep(1)
            if category.is_displayed():
                ele = self.driver.find_element(By.XPATH, "//a[@title='Distinct']")
                ele.click()
            else:
                print("answer type not selected")

            self.driver.find_element(By.XPATH, "//input[@placeholder='Single Answer']").send_keys("1234")
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-sm btn-primary']").click()
            # self.driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-success btn-sm ng-scope']")
            self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-success.btn-sm.ng-scope').click()
            time.sleep(5)
            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def add_q_local(self, question_id):
        try:
            print("Adding question from my question library")
            time.sleep(1)
            qid = self.driver.find_element(By.XPATH, "//input[@placeholder='Eg: 1234, 2312,...']")
            qid.send_keys(question_id)
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-primary_ pull-right']").click()
            time.sleep(2)
            self.driver.find_element(By.NAME, 'grid_items').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-success_ pull-right']").click()
            time.sleep(5)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def add_rtc_local(self):
        try:
            print("Adding question from my question library")
            time.sleep(2)
            self_assessment_obj.select_plus(3)
            time.sleep(1)
            qid = self.driver.find_element(By.XPATH, "//input[@placeholder='Eg: 1234, 2312,...']")
            qid.send_keys("141427")
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-primary_ pull-right']").click()
            time.sleep(1)
            self.driver.find_element(By.NAME, 'grid_items').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-success_ pull-right']").click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//button[@class='btn btn-success pull-right']").click()
            time.sleep(5)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def add_q_hirepro(self, question_id):
        try:
            print("Adding question from hirepro tenant")

            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Hirepro Library")]').click()
            time.sleep(2)
            qid = self.driver.find_element(By.XPATH, '//*[@type="text"]')
            qid.send_keys(question_id)
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary_ pull-right"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@name="grid_items"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-success_ pull-right"]').click()
            time.sleep(10)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def add_rtc_hirepro(self):
        try:
            print("Adding rtc question from hirepro tenant")
            # add question from hirepro- rtc
            time.sleep(5)
            self_assessment_obj.select_plus(3)
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Hirepro Library")]').click()
            time.sleep(2)
            qid = self.driver.find_element(By.XPATH, '//*[@type="text"]')
            qid.send_keys("141417")
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary_ pull-right"]').click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@name="grid_items"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-success_ pull-right"]').click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//button[@class="btn btn-success pull-right"]').click()
            time.sleep(10)

            return 'SUCCESS'

        except Exception as e:
            print(e)

        return 'FAILED'

    def add_new_group(self):
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, '//*[@class = "btn btn-link ng-scope"]').click()
            time.sleep(2)

        except Exception as e:
            print(e)

    def add_new_section(self):
        time.sleep(2)
        try:
            # wait = WebDriverWait(self.driver, 20)
            # add_section = wait.until(
            #     EC.element_to_be_clickable((By.XPATH, "//strong[text()='Add Section']")))
            # add_section.click()
            add_section = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, "//strong[text()='Add Section']")))
            add_section.click()

        except Exception as e:
            print(e)


self_assessment_obj = SelfAssessmentLogin()
