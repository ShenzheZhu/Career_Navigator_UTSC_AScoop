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

        recommend_query = """MATCH (j:Job)-[:NEEDS_SKILL]->(s:Skill)
WITH j, collect(s.name) AS JobSkills, $skills AS StudentSkills, $subject AS StudentSubject
OPTIONAL MATCH (j)-[:IDEAL_FOR]->(sub:Subject)
WITH j, JobSkills, StudentSkills, StudentSubject, collect(sub.name) AS JobSubjects
WITH j, JobSkills, StudentSkills, StudentSubject, JobSubjects,
     [skill IN JobSkills WHERE any(studentSkill IN StudentSkills WHERE skill =~ ('(?i)^' + studentSkill + '$'))] AS MatchedSkills,
     [subject IN JobSubjects WHERE subject =~ ('(?i).*' + StudentSubject + '.*')] AS MatchedSubjects
WITH j, MatchedSkills, size(MatchedSkills) AS MatchedSkillCount, MatchedSubjects, 
     CASE WHEN size(MatchedSubjects) > 0 THEN true ELSE false END AS SubjectMatched
RETURN j.id AS JobID, 
       MatchedSkills, 
       MatchedSkillCount, 
       MatchedSubjects,
       SubjectMatched,
       size(MatchedSubjects) AS MatchedSubjectCount
ORDER BY MatchedSkillCount DESC, MatchedSubjectCount DESC, SubjectMatched DESC
LIMIT 10

"""

        with self.driver.session() as session:
            results = session.run(recommend_query, skills=skills, subject=fields)
            scored_jobs = []
            for record in results:
                job_id = record['JobID']
                matched_skills = record['MatchedSkills']
                skill_count = record['MatchedSkillCount']
                subject_matched = record['SubjectMatched']

                # Calculate the score
                score = skill_count * 5 + (20 if subject_matched else 0)
                scored_jobs.append((job_id, matched_skills, skill_count, subject_matched, score))

            # Sort jobs by score in descending order
            scored_jobs.sort(key=lambda x: x[4], reverse=True)
            return scored_jobs

    def pipeline_executor(self, student_info_path):
        student_info = utils.load_data(student_info_path)
        print("\nRecommended Jobs:")
        recommendations = self.recommend_jobs(student_info)
        for recommendation in recommendations:
            print(f"Job ID: {recommendation[0]}, Matched Skills: {recommendation[1]}, Skill Count: {recommendation[2]}, Subject Matched: {recommendation[3]}, Score: {recommendation[4]}")
