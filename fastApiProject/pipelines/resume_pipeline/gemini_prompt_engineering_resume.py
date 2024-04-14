import google.generativeai as genai
import os
from resources import cloud_config
from resources import config
from bs4 import BeautifulSoup
from resources import prompt_config
from utils import utils

class GeminiPrompting:
    def __init__(self,prompt):
        self.prompt = prompt

    def generate_content(self, question, api_key, model_name):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(question, generation_config={"temperature":0})

        return response.text

    def result_generation(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIAL_PATH
        response = self.generate_content(self.prompt, cloud_config.GOOGLE_GENMINI_API, cloud_config.model_name)

        return response