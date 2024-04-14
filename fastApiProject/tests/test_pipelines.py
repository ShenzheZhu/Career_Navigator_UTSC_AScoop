import json
import os

from algorithm.algorithms import Neo4jRecommender
from pipelines.job_posting_pipeline.KG_constrcution import Neo4jConnector
from pipelines.job_posting_pipeline.job_post_processing import JobFetcher
from pipelines.resume_pipeline.resume_processing_basic import ResumeAnalyzer
from resources import config, cloud_config
from pipelines.resume_pipeline.resume_processing_gemini import ResumeAnalyzerGemini


def resume_process_basic_test():
    analyze = ResumeAnalyzer(config.RESUME_PATH, config.SUBJECT_LIST)
    analyze.process_resume()


def resume_process_gemini_test():
    analyze = ResumeAnalyzerGemini(config.RESUME_PATH)
    analyze.process_resume()


def job_data_test():
    agent = Neo4jConnector(cloud_config.NEO4J_URI, cloud_config.NEO4J_USERNAME, cloud_config.NEO4J_PASSWORD)
    agent.reset_knowledge_graph()
    agent.create_KG(config.LOCAL_JOB_KEYWORDS_BUCKET, config.LOCAL_JOB_KEYWORDS_NAME)
    agent.close()
    print("KG construction finished")


def job_post_process_test():
    keyword = cloud_config.KEYWORD
    per_page = cloud_config.PER_PAGE
    token = cloud_config.TOKEN
    job_fetcher = JobFetcher(keyword, per_page, token)
    final_result = job_fetcher.process_job_post()
    print("Job post processing finished")


def recommender_algorithm_test():
    recommender = Neo4jRecommender(cloud_config.NEO4J_URI, cloud_config.NEO4J_USERNAME, cloud_config.NEO4J_PASSWORD)
    try:
        student_info_path = os.path.join(config.LOCAL_RESUME_KEYWORDS_BUCKET, config.LOCAL_RESUME_KEYWORDS_NAME)
        recommender.pipeline_executor(student_info_path)
    finally:
        recommender.close()


if __name__ == '__main__':
    # resume_data_test()
    resume_process_gemini_test()
    # job_post_process_test()
    # job_data_test()
    # recommender_algorithm_test()
