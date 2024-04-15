#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024-04-14 4:30 p.m.
# @Author  : FywOo02
# @FileName: resume_processing_gemini.py
# @Software: PyCharm
import fitz
from pipelines.resume_pipeline.gemini_prompt_engineering_resume import GeminiPrompting
from resources import config
from utils import utils
from resources import prompt_config
from utils import utils


class ResumeAnalyzerGemini:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path  # Path to the PDF file

    def text_extraction(self, pdf_path):
        document = fitz.open(pdf_path)
        full_text = ""
        for page in document:
            text = page.get_text()
            full_text += text
        document.close()

        return full_text

    def analyze_education(self, prompt):
        processed_result = GeminiPrompting(prompt).result_generation()
        return processed_result.lower()

    def analyze_skills(self, prompt):
        processed_result = GeminiPrompting(prompt).result_generation()
        return [skill.lower().strip() for skill in processed_result.split(', ')]

    def process_resume(self):
        resume_text = self.text_extraction(self.pdf_path)
        education_info = self.analyze_education(prompt_config.resume_education_prompt_combining(resume_text))
        skills_info = self.analyze_skills(prompt_config.resume_skill_prompt_combining(resume_text))

        cleaned_education_info = utils.sanitize_for_neo4j_regex(education_info)
        # 清洗skills_info中的每一个元素
        cleaned_skills_info = [utils.sanitize_for_neo4j_regex(skill) for skill in skills_info]

        output = {
            "education": cleaned_education_info,
            "skills": cleaned_skills_info
        }
        utils.upload_to_local(config.LOCAL_RESUME_KEYWORDS_BUCKET, config.LOCAL_RESUME_KEYWORDS_NAME, output)
        return output
