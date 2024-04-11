import google.generativeai as genai
import os
from resources import cloud_config
from resources import config
from bs4 import BeautifulSoup
from resources import prompt_config

class GeminiPrompting:
    def __init__(self,job_desciption):
        self.job_description = job_desciption
    def clean_html(self,html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()

    def generate_content(self, question, api_key, model_name):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(question)

        return response.text

    def result_generation(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIAL_PATH
        processed_text = self.clean_html(self.job_description)
        response = self.generate_content(prompt_config.prompt_combining(processed_text),cloud_config.GOOGLE_GENMINI_API,cloud_config.model_name)

        return response

# 使用示例
"""
html_text = Education Recommendations

Currently a candidate for a Bachelor's degree or diploma in Computer Science, Software Engineering, or a related field with an accredited school in Canada.

REQUIRED SKILLS
You have:

 A deep technical understanding of web basics, browser interactions, HTML/CSS, and JavaScript
 Experience using React or other modern Javascript frameworks such as Angular, Vue, and NextJS.
 Be comfortable working with JSON object models, REST APIs, etc
 
It would be nice if you also had:

Familiarity with Java and Spring
Appreciation for databases and

agent = GeminiPrompting(html_text)
result = agent.result_generation()
print(result)
"""