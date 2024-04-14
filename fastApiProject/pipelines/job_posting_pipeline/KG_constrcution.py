import os
from neo4j import GraphDatabase
import json
from utils import utils
from resources import cloud_config
from resources import config


class Neo4jConnector:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()

    @staticmethod
    def _create_and_link_job(tx, job_id, subjects, skills):
        tx.run("MERGE (j:Job {id: $job_id})", job_id=job_id)

        for subject in subjects:
            subject = subject.strip()
            if subject != "not specified":
                tx.run("MERGE (sub:Subject {name: $subject}) "
                       "MERGE (j:Job {id: $job_id}) "
                       "MERGE (j)-[:IDEAL_FOR]->(sub)", subject=subject, job_id=job_id)

        for skill in skills:
            skill = skill.strip()
            if skill != "n/a":
                tx.run("MERGE (sk:Skill {name: $skill}) "
                       "MERGE (j:Job {id: $job_id}) "
                       "MERGE (j)-[:NEEDS_SKILL]->(sk)", skill=skill, job_id=job_id)

    def add_job(self, job_id, subjects, skills):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_link_job, job_id, subjects, skills)

    def reset_knowledge_graph(self):
        with self.driver.session() as session:
            session.write_transaction(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))

    def create_KG(self, directory_path, filename):
        file_path = os.path.join(directory_path, filename)
        jobs_data = utils.load_data(file_path)
        for job_id, job_details in jobs_data.items():
            subjects = job_details['classLevel']
            skills = job_details['skills']
            self.add_job(job_id, subjects, skills)



