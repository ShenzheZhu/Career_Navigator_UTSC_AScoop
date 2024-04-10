from pipelines.job_posting_pipeline.KG_constrcution import Neo4jConnector
from pipelines.resume_pipeline.resume_processing import ResumeAnalyzer
from resources import config

def resume_data_test():
    analyze = ResumeAnalyzer(config.RESUME_PATH,config.SUBJECT_LIST)
    analyze.process_resume()
def job_data_test():
    connector = Neo4jConnector(config.NEO4J_URI,config.NEO4J_USERNAME,config.NEO4J_PASSWORD)
    connector.create_KG(config.LOCAL_JOB_KEYWORDS_BUCKET,config.LOCAL_JOB_KEYWORDS_NAME)
    connector.close()
    print("KG created")


if __name__ == '__main__':
    # resume_data_test()
    job_data_test()

