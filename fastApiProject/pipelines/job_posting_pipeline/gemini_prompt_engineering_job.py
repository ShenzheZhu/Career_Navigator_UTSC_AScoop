import google.generativeai as genai
import os

from google.ai.generativelanguage_v1 import HarmCategory
from google.generativeai.types import HarmBlockThreshold

from resources import cloud_config
from resources import config
from bs4 import BeautifulSoup
from resources import prompt_config
from utils import utils


class GeminiPrompting:

    def __init__(self, job_desciption):
        self.job_description = job_desciption
        self.safety_settings = safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    def generate_content(self, question, api_key, model_name):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(question, generation_config={"temperature":0}, safety_settings=self.safety_settings)

        return response.text

    def result_generation(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIAL_PATH
        processed_text = utils.clean_html(self.job_description)
        response = self.generate_content(prompt_config.job_information_prompt_combining(processed_text),
                                         cloud_config.GOOGLE_GENMINI_API, cloud_config.model_name)

        return response

