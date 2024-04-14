import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 登录页面的URL
username = 'cho.zhu@mail.utoronto.ca'
password = 'password123'
code = '92350'
job_id = '3b3be992b69363989cee06478dbafc97'

login_url = 'https://utsc-utoronto-csm.symplicity.com/manager/'
second_url = 'https://utsc-utoronto-csm.symplicity.com/manager/?s=jobs&_ksl=1'
search_url = 'https://utsc-utoronto-csm.symplicity.com/manager/index.php'
target_url = f'https://utsc-utoronto-csm.symplicity.com/manager/index.php?mode=form&id={job_id}'
back_url = 'https://utsc-utoronto-csm.symplicity.com/manager/index.php?mode=list&'

# 配置Selenium WebDriver
options = Options()
options.headless = False  # 如果不需要浏览界面，可以设置为True
driver = webdriver.Chrome(options=options)


def extract_skills(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    textarea = soup.find('textarea', {"name": "dnf_class_values[job][qualifications]"})
    if textarea:
        return textarea.get_text(strip=True)
    return None


# 创建一个Session对象，它会自动处理cookies
session = requests.Session()

# 登录信息，根据实际情况填写
login_data = {
    'username': username,  # 替换为你的邮箱地址
    'password': password,  # 替换为你的密码
    '_keepmeloggedin': 'on'  # 如果需要保持登录，使用这个选项
}

# 发送POST请求进行登录
response = session.post(login_url, data=login_data)

Next = session.get(target_url)

result = extract_skills(Next.text)

print(result)
