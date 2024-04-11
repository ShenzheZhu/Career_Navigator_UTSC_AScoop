from datetime import datetime
import json
import requests
from resources import cloud_config


class JobFetcher:
    def __init__(self, keyword, per_page, token):
        self.keyword = keyword
        self.per_page = per_page
        self.token = token
        self.headers = {"Authorization": f"Token {token}"}
        self.base_url = f"https://utsc-utoronto-csm.symplicity.com/api/public/v1/jobs?keywords={keyword}&perPage={per_page}"
        self.all_jobs = []

    def fetch_jobs(self):
        page = 1
        while True:
            api_url = f"{self.base_url}&page={page}"
            response = requests.get(api_url, headers=self.headers)

            if response.status_code == 200:
                job_data = response.json()
                self.all_jobs.extend(job_data['models'])

                if page * job_data['perPage'] >= job_data['total']:
                    break  # 如果当前页是最后一页，结束循环
                page += 1  # 准备请求下一页
            else:
                print(f"Error: Unable to fetch job data. Status code: {response.status_code}")
                break

    def filter_valid_jobs(self):
        return [job for job in self.all_jobs if job['expirationDate'] and datetime.strptime(job['expirationDate'], '%Y-%m-%d') >= datetime.now()]

    def extract_job_info(self, jobs):
        jobs_info = {}
        for job in jobs:
            job_id = job['id']
            class_level = [level['label'] for level in job.get('classLevel', []) if 'label' in level]
            if not class_level:
                class_level = ['Not specified']
            description = job.get('description', 'Not specified')

            jobs_info[job_id] = {
                'classLevel': class_level,
                'description': description
            }
        return jobs_info

    def process_job_post(self):
        self.fetch_jobs()
        valid_jobs = self.filter_valid_jobs()
        jobs_info = self.extract_job_info(valid_jobs)
        print(json.dumps(jobs_info, indent=4, ensure_ascii=False))


# 使用
keyword = cloud_config.KEYWORD
per_page = cloud_config.PER_PAGE
token = cloud_config.TOKEN
job_fetcher = JobFetcher(keyword, per_page, token)
job_fetcher.process_job_post()
