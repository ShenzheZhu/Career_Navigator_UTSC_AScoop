#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024-04-14 9:41 p.m.
# @Author  : FywOo02
# @FileName: recommender_executor.py
# @Software: PyCharm
import os

from algorithm.algorithms import Neo4jRecommender
from resources import config, cloud_config
from pipelines.resume_pipeline.resume_processing_gemini import ResumeAnalyzerGemini


if __name__ == '__main__':
    analyze = ResumeAnalyzerGemini(config.RESUME_PATH_4)
    analyze.process_resume()

    recommender = Neo4jRecommender(cloud_config.NEO4J_URI, cloud_config.NEO4J_USERNAME, cloud_config.NEO4J_PASSWORD)
    try:
        student_info_path = os.path.join(config.LOCAL_RESUME_KEYWORDS_BUCKET, config.LOCAL_RESUME_KEYWORDS_NAME)
        recommender.pipeline_executor(student_info_path)
    finally:
        recommender.close()