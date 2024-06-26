from datetime import datetime
import json
import requests
from resources import cloud_config
from pipelines.job_posting_pipeline.gemini_prompt_engineering_job import GeminiPrompting
from utils import utils
from resources import config


class JobFetcher:
    def __init__(self, keyword, per_page, token):
        self.keyword = keyword
        self.per_page = per_page
        self.token = token
        self.headers = {"Authorization": f"Token {token}"}
        self.base_url = f"{cloud_config.BASE_URL}?keywords={keyword}&perPage={per_page}"
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
        return [job for job in self.all_jobs if
                job['expirationDate'] and datetime.strptime(job['expirationDate'], '%Y-%m-%d') >= datetime.now()]

    def filter(self):
        current_year = datetime.now().year
        return [job for job in self.all_jobs if
                job['expirationDate'] and
                datetime.strptime(job['expirationDate'], '%Y-%m-%d').year == current_year]

    def extract_job_info(self, jobs):
        jobs_info = {}
        for job in jobs:
            job_id = job['id']
            class_level = [level['label'].lower() for level in job.get('classLevel', []) if 'label' in level]
            if not class_level:
                class_level = ['not specified']
            description = job.get('description', 'not specified')

            jobs_info[job_id] = {
                'classLevel': class_level,
                'description': description
            }
        return jobs_info

    def process_descriptions(self, jobs_info):
        for job_id, job_info in jobs_info.items():
            description = job_info['description']
            processed_result = GeminiPrompting(description).result_generation()
            job_info['skills'] = [skill.lower().strip() for skill in processed_result.split(', ')]
            del job_info['description']
        return jobs_info

    def process_job_post(self):
        self.fetch_jobs()
        valid_jobs = self.filter()
        jobs_info = self.extract_job_info(valid_jobs)
        # jobs_info = dict(list(jobs_info.items())[:10])
        updated_jobs_info = self.process_descriptions(jobs_info)
        utils.upload_to_local(config.LOCAL_JOB_KEYWORDS_BUCKET, config.LOCAL_JOB_KEYWORDS_NAME, updated_jobs_info)
        return updated_jobs_info
