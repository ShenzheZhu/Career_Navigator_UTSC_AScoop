import json
from pipelines.job_posting_pipeline.KG_constrcution import Neo4jConnector
from pipelines.job_posting_pipeline.job_post_processing import JobFetcher
from pipelines.resume_pipeline.resume_processing import ResumeAnalyzer
from resources import config, cloud_config


def resume_data_test():
    analyze = ResumeAnalyzer(config.RESUME_PATH,config.SUBJECT_LIST)
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
    print(json.dumps(final_result, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    resume_data_test()
    # job_data_test()

