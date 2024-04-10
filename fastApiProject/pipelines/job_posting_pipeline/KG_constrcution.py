import os

from neo4j import GraphDatabase
import json
from utils import utils
class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_job(self, job_id, subjects, skills):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_link_job, job_id, subjects, skills)

    @staticmethod
    def _create_and_link_job(tx, job_id, subjects, skills):
        for subject in subjects:
            tx.run("MERGE (sub:Subject {name: $subject}) "
                   "MERGE (j:Job {id: $job_id}) "
                   "MERGE (j)-[:IDEAL_FOR]->(sub)", subject=subject, job_id=job_id)

        for skill in skills:
            tx.run("MERGE (sk:Skill {name: $skill}) "
                   "MERGE (j:Job {id: $job_id}) "
                   "MERGE (j)-[:NEEDS_SKILL]->(sk)", skill=skill, job_id=job_id)

    def create_KG(self, directory_path,filename):
        file_path = os.path.join(directory_path, filename)
        jobs_data = utils.load_data(file_path)
        for job in jobs_data['jobs']:
            self.add_job(job['job_id'], job['subjects'], job['skills'])



