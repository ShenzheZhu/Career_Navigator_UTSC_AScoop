#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024-04-14 9:29 p.m.
# @Author  : FywOo02
# @FileName: KG_construction_script.py
# @Software: PyCharm
from pipelines.job_posting_pipeline.KG_constrcution import Neo4jConnector
from pipelines.job_posting_pipeline.job_post_processing import JobFetcher
from resources import config, cloud_config

if __name__ == '__main__':
    keyword = cloud_config.KEYWORD
    per_page = cloud_config.PER_PAGE
    token = cloud_config.TOKEN
    job_fetcher = JobFetcher(keyword, per_page, token)
    final_result = job_fetcher.process_job_post()
    print("Job post processing finished")

    agent = Neo4jConnector(cloud_config.NEO4J_URI, cloud_config.NEO4J_USERNAME, cloud_config.NEO4J_PASSWORD)
    agent.reset_knowledge_graph()
    agent.create_KG(config.LOCAL_JOB_KEYWORDS_BUCKET, config.LOCAL_JOB_KEYWORDS_NAME)
    agent.close()
    print("KG construction finished")
