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
        try:
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
                    score = skill_count * 5 + (10 if subject_matched else 0)
                    scored_jobs.append((job_id, matched_skills, skill_count, subject_matched, score))

                # Sort jobs by score in descending order
                scored_jobs.sort(key=lambda x: x[4], reverse=True)
                return scored_jobs
        except Exception as e:
            return []

    def pipeline_executor(self, student_info_path):
        try:
            student_info = utils.load_data(student_info_path)
            recommendations = self.recommend_jobs(student_info)

            if recommendations:
                return [
                    {
                        'job_id': recommendation[0],
                        'matched_skills': recommendation[1],
                        'skill_count': recommendation[2],
                        'subject_matched': recommendation[3],
                        'score': recommendation[4]
                    }
                    for recommendation in recommendations
                ]
            else:
                print("No recommendations available or an error occurred.")
            return []
        except Exception as e:
            print(f"An error occurred while executing the pipeline: {str(e)}")
            return []