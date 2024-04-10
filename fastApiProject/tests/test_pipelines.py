from pipelines.resume_pipeline.resume_processing import ResumeAnalyzer
from resources import config
if __name__ == '__main__':
    analyze = ResumeAnalyzer(config.RESUME_PATH,config.SUBJECT_LIST)
    analyze.process_resume()
