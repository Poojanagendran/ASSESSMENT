import requests
import json
import urllib.request


class VersantDirectLink:
    def __init__(self):
        self.username = 'AT204341558952'
        self.password = r'W${tsEsZ'
        self.tenant = 'AT'
        self.versant_direct_link()

    def versant_direct_link(self):
        hirepro_link_path = 'F:/ASSESSMENT/PythonWorkingScripts_Output/hirepro_link.html'
        direct_link_path = 'F:/ASSESSMENT/PythonWorkingScripts_Output/nav9.html'
        header = {"content-type": "application/json", "X-APPLMA": "true", "APP-NAME": "onlineassessment",
                  "App-Server": "py310app"}
        data = {"LoginName": self.username, "Password": self.password, "TenantAlias": self.tenant}
        response = requests.post("https://pearsonstg.hirepro.in/py/assessment/htmltest/api/v2/login_to_test/",
                                 headers=header, data=json.dumps(data), verify=False)
        login_response = response.json()
        req_header = {"content-type": "application/json", "X-AUTH-TOKEN": login_response.get("Token"),
                      "X-APPLMA": "true"}

        response = requests.post('https://pearsonstg.hirepro.in/py/assessment/htmltest/api/v1/initiate-tua/',
                                 headers=req_header,
                                 data=json.dumps({}, default=str), verify=False)
        itua_resp = response.json()
        print(itua_resp)
        urllib.request.urlretrieve(itua_resp.get('versantLoginUrl'), hirepro_link_path)
        with open(hirepro_link_path, 'r', encoding='utf-8') as file:
            content = file.read()
        old_url = "https://pearsonltistg.hirepro.in/"
        new_url = "https://lti-stg.versantqa.zone/"
        updated_content = content.replace(old_url, new_url)
        with open(direct_link_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(" Direct url generated successfully.")


ob = VersantDirectLink()