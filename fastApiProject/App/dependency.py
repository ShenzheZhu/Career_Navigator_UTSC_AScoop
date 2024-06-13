from algorithm.algorithms import Neo4jRecommender
from pipelines.resume_pipeline.resume_processing_gemini import ResumeAnalyzerGemini
from resources import cloud_config, config
import os
import requests


def recommender_execute(file_stream):
    analyze = ResumeAnalyzerGemini(file_stream)
    analyze.process_resume()

    recommender = Neo4jRecommender(cloud_config.NEO4J_URI, cloud_config.NEO4J_USERNAME, cloud_config.NEO4J_PASSWORD)
    try:
        student_info_path = os.path.join(config.LOCAL_RESUME_KEYWORDS_BUCKET, config.LOCAL_RESUME_KEYWORDS_NAME)
        result = recommender.pipeline_executor(student_info_path)
    finally:
        recommender.close()
    return result


def get_job_details(job):
    job_id = job['job_id']
    base_url = f"{cloud_config.BASE_URL}/{job_id}"
    headers = {"Authorization": f"Token {cloud_config.TOKEN}"}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        job_details = response.json()
        job.update({
            'job_name': job_details.get('title'),
            'job_number': job_details.get('visualId')
        })
        return job
    else:
        return job