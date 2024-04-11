from datetime import datetime
import json
import requests

keyword = "2024 summer"
per_page = 500
api_url = f"https://utsc-utoronto-csm.symplicity.com/api/public/v1/jobs?keywords={keyword}&perPage={per_page}"
token = "tVgo170rYtSBdPv1yTUOP1oRvzxm8wlq75+r0Vyl1QUIQrJ/SnWasBN2DmyrU5eMMsHBe045IwNopBsjVp83HXRu7aOzUa5MIFADpEvFw5+9Ic7tO7krBUw8FY82u5SznBbT4y1uoGybJSqICrsuqg=="
headers = {
    "Authorization": f"Token {token}"
}

page = 1
all_jobs = []

while True:
    api_url = f"{api_url}&page={page}"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        job_data = response.json()
        all_jobs.extend(job_data['models'])

        if page * job_data['perPage'] >= job_data['total']:
            break  # 如果当前页是最后一页，结束循环
        page += 1  # 准备请求下一页
    else:
        print(f"Error: Unable to fetch job data. Status code: {response.status_code}")
        break


valid_jobs = [job for job in all_jobs if job['expirationDate'] and datetime.strptime(job['expirationDate'], '%Y-%m-%d') >= datetime.now()]


jobs_info = {}

for job in valid_jobs:
    job_id = job['id']  # 获取职位ID
    class_level = [level['label'] for level in job.get('classLevel', []) if 'label' in level]
    # 如果 classLevel 为空，则标记为"Not specified"
    if not class_level:
        class_level = ['Not specified']
    description = job.get('description', 'Not specified')  # 获取描述，如果不存在则标记为"Not specified"

    # 将提取的信息存储到字典中
    jobs_info[job_id] = {
        'classLevel': class_level,
        'description': description
    }

# 现在 jobs_info 包含了所有职位的信息
# 打印看一下结果
print(json.dumps(jobs_info, indent=4, ensure_ascii=False))