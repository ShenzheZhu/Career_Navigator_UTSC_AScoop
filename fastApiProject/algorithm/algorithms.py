import json
from neo4j import GraphDatabase
from utils import utils
from resources import cloud_config
from resources import config
import os


class Neo4jRecommender:
    def __init__(self, uri, username, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()

    def recommend_jobs(self, student_data):
        skills = student_data['skills']
        fields = student_data['education']

        # 更新后的Cypher查询字符串
        recommend_query = """ """

        with self.driver.session() as session:
            # 执行查询，传入学生的技能和教育领域作为参数
            results = session.run(recommend_query, skills=skills, fields=fields)
            # 将查询结果整理成列表形式返回
            return [(record['JobID'], record['MatchedSkills'], record['TotalScore']) for record in results]

    def pipeline_executor(self, student_info_path):
        student_info = utils.load_data(student_info_path)
        print("\nRecommended Jobs:")
        recommendations = self.recommend_jobs(student_info)
        for recommendation in recommendations:
            print(recommendation)
