import fitz  # PyMuPDF library for working with PDF files
import json  # Library for JSON operations
import re  # Regular expression library for text matching
from utils import utils  # Importing utility functions
from resources import config  # Importing configuration settings
from resources import cloud_config

class ResumeAnalyzer:
    def __init__(self, pdf_path, subjects_path):
        self.pdf_path = pdf_path  # Path to the PDF file
        self.education_keywords = self.load_keywords(subjects_path)  # Load education-related keywords

    def load_keywords(self, filepath):
        # Load keywords from a file, one keyword per line
        with open(filepath, 'r') as file:
            return [line.strip().lower() for line in file if line.strip()]

    def find_section_positions(self, doc):
        # Find the positions of the 'education' and 'skills' sections in the resume
        sections = {'education': None, 'skills': None}
        titles = ['education', 'skills']  # Matching titles in the resume

        for page_num, page in enumerate(doc):
            blocks = page.get_text("blocks")
            for i, block in enumerate(blocks):
                block_text = block[4].lower()
                for title in titles:
                    if title in block_text and not sections[title]:
                        sections[title] = {'page': page_num, 'start_rect': block[:4]}
                        if i + 1 < len(blocks):
                            sections[title]['end_rect'] = blocks[i + 1][:4]
                        else:
                            sections[title]['end_rect'] = blocks[i][:4]
                        break

        return sections

    def extract_section_text(self, doc, section):
        # Extract text from a specified section
        if not section:
            return ""
        page = doc[section['page']]
        start_rect = fitz.Rect(section['start_rect'])
        end_rect = fitz.Rect(section['end_rect'])
        clip_rect = fitz.Rect(start_rect.x0, start_rect.y0, end_rect.x1, end_rect.y1)
        return page.get_text("text", clip=clip_rect)

    def analyze_education(self, text):
        # Identify education entities in the text
        education_entities = []
        text_lower = text.lower()

        for keyword in self.education_keywords:
            if keyword in text_lower:
                start = text_lower.find(keyword)
                end = start + len(keyword)
                education_entities.append(text[start:end].lower())
        return education_entities

    def analyze_skills(self, text):
        # Analyze and extract skills from the text
        skills = []

        # Split the skills section into blocks, assuming they may start with a title followed by skills
        blocks = [block.strip() for block in re.split(r'\n', text) if block.strip()]

        for block in blocks:
            if ':' in block:
                _, skill_part = block.split(':', 1)
            else:
                skill_part = block

            skill_items = [item.strip().lower() for item in re.split(r',|;', skill_part) if item.strip()]

            skills.extend(skill_items)

        return skills

    def process_resume(self):
        # Main method to process the resume and extract education and skills information
        with fitz.open(self.pdf_path) as doc:
            sections = self.find_section_positions(doc)

            education_text = self.extract_section_text(doc, sections['education'])
            skills_text = self.extract_section_text(doc, sections['skills'])

            education_info = self.analyze_education(education_text)
            skills_info = self.analyze_skills(skills_text)

            # Compile the extracted information into a dictionary
            output = {
                "education": education_info,
                "skills": skills_info
            }
            # Upload the extracted information to Google Cloud Storage
            #utils.upload_to_gcs(config.GCS_RESUME_KEYWORDS_BUCKET_NAME,config.LOCAL_RESUME_KEYWORDS_NAME,output)
            utils.upload_to_local(config.LOCAL_RESUME_KEYWORDS_BUCKET, config.LOCAL_RESUME_KEYWORDS_NAME, output)
            return output
