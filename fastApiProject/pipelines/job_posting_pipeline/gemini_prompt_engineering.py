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

        return response['content']

    def result_generation(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIAL_PATH
        processed_text = self.clean_html(self.job_description)
        response= self.generate_content(prompt_config.prompt_combining(processed_text),cloud_config.GOOGLE_GENMINI_API,cloud_config.model_name)

        return response['content']

# 使用示例
html_text = """
"<p><strong>Internship Team Notes:</strong></p>\r\n<ul>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"1\" data-aria-level=\"1\">There are five (5) Exclusive U of T DPES MEnvSc x UNA-Canada positions for Summer 2024. The UNA-Canada calls their job postings &ldquo;Terms of Reference (ToRs)&rdquo;.&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"1\" data-aria-level=\"1\">Note: the full position title for this role is \"JPC for Climate Change, Environment and Disaster Cluster\"</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"2\" data-aria-level=\"1\">This role is exclusive to the MEnvSc program. The process for MEnvSc students is to submit application(s) via CSM for the UNA-Canada roles of interest and the Internship Team will send all applications to UNA-Canada (following the deadline). UNA-Canada will short-list students to conduct first round interviews. Upon receiving an offer email from the Internship Team, and offer acceptance you will be guaranteed a spot in the UNA-Canada IDDIPs program. Once confirmed by UNA-Canada to be a Junior Professional Consultant (JPC) -&gt; student will receive support with travel visas from UNA-Canada -&gt; student will go abroad to one of the three UNA-Canada destinations (Indonesia, Vietnam (~x3 roles), or Bangladesh) starting in May 2024.&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"3\" data-aria-level=\"1\">Apply through CSM only as there is no dual application on the employer&rsquo;s website.&nbsp; The MEnvSc Team will be forwarding your application following the deadline to apply.&nbsp;&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"4\" data-aria-level=\"1\">Apply directly on CSM with resume (up to 3 pages), cover letter (up to 2 pages), and unofficial transcript. *Note: the UNA-Canada will accept slightly longer application documents as they are screening for high caliber candidates and thus students can include all relevant experiences.&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"5\" data-aria-level=\"1\">International Work Duration: May 1, 2024 - October 31, 2024 (6 months).&nbsp;</li>\r\n</ul>\r\n<p><strong>ADDITIONAL PROGRAM INFORMATION:&nbsp;</strong></p>\r\n<ul>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"6\" data-aria-level=\"1\">Need more information about UNA-Canada's IDDIPs - University Division: International Internship Programme For Students (IIPS): <a href=\"https://www.unac.org/iips\" target=\"_blank\" rel=\"noopener\">https://www.unac.org/iips</a>&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"7\" data-aria-level=\"1\">A webinar recording of the UNA-Canada information session for MEnvSc students (from October 18th) is available for viewing in the EES1100 Quercus page: <a href=\"https://q.utoronto.ca/courses/318858/pages/una-canada-information-session\" target=\"_blank\" rel=\"noopener\">UNA-Canada Information Session: EES1100H Y LEC0101 20239:Advanced Seminar in Environmental Science (utoronto.ca)</a></li>\r\n</ul>\r\n<p><strong>AWARDS &amp; FINANCIAL SUPPORT FROM UTSC DPES and U of T:&nbsp;</strong></p>\r\n<ul>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"8\" data-aria-level=\"1\">This role requires relocation to a country outside of Canada. Students relocating for this role may be eligible to apply for the &ldquo;Relocation Assistance Award&rdquo; (generally valued at the cost of the flight/travel, needs based) if they are not returning to their home country.&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"9\" data-aria-level=\"1\">This is an&nbsp;<b>unpaid</b>&nbsp;internship, however, MEnvSc students will be eligible to apply for the &ldquo;MEnvSc Internship Award&rdquo; (generally valued at $5,000 - $8,000, needs based).&nbsp;</li>\r\n<li data-leveltext=\"\" data-font=\"Symbol\" data-listid=\"11\" data-list-defn-props=\"{\" aria-setsize=\"-1\" data-aria-posinset=\"10\" data-aria-level=\"1\">Students accepted for this UNA-Canada x DPES international experience, will be eligible to apply for the U of T Tri-campus &ldquo;International Experience (IE) Awards&rdquo; (generally valued at $500-5,000, needs based) -&gt; see this link for more details: <a href=\"https://learningabroad.utoronto.ca/learning-abroad/prepare_plan/funding/centre-for-international-experience/\" target=\"_blank\" rel=\"noopener\">https://learningabroad.utoronto.ca/learning-abroad/prepare_plan/funding/centre-for-international-experience/</a> &nbsp;</li>\r\n</ul>\r\n<p>&nbsp;---</p>\r\n<p><strong>Programme: </strong>CIDA International Youth Internship Programme<strong><br />Role title:</strong> Junior Professional Consultant (JPC) for Climate Change, Environment and Disaster Cluster</p>\r\n<p><strong>Background</strong></p>\r\n<p>The Climate Change, Environment and Disaster (CCED) cluster of UNDP Bangladesh supports the Government of Bangladesh to address national challenges related to sustainable economic growth ensuring environmental sustainability, environmental management, access to low carbon energy, reducing risk to disaster and climate change impacts, responding to disaster and strengthen climate change governance. All these contribute to UNDP&rsquo;s overarching goal to empower people and build resilient nation. CCED cluster leads UNDP Country Office resilience agenda. <br />The cluster manages an array of programmes and projects--and some of them are flagship in nature--with multi-million dollar fund from various donor agencies. These projects are set out to achieve two specific outcomes of Bangladesh Country Programme Document (2012-2016):</p>\r\n<ul>\r\n<li>Populations vulnerable to climate change and natural disaster have become more resilient to adapt to risks. The other is focused on natural resource management and climate change mitigation, such that:</li>\r\n<li>Vulnerable populations benefit from better natural resource management and access to low carbon energy. CCED cluster&rsquo;s upcoming programming endeavors will primarily focus on enhancing resilience, mainstreaming climate change adaptation and disaster risk reduction and promotion of green growth opportunities for environmental sustainability.</li>\r\n</ul>\r\n<p>The cluster is managed by a group of top national and international specialists.</p>\r\n<p><br /><strong>Duties and Responsibilities</strong><br />Working under the supervision of the Assistant Country Director, the JPC is responsible for the overall support to the implementation of the cluster work plan. The JPC contributes to enhanced CCED knowledge through substantive inputs as necessary, analysis and implementation of programme strategies and facilitation of knowledge building. The person will also assist the relevant programme lead in developing project and carrying out country office special initiatives<br />assigned to the cluster i.e. Resilience Building.</p>\r\n<p><strong>Outputs and Deliverables</strong></p>\r\n<ul>\r\n<li>Carry out background policy analysis. Identification of sources of information related to policy-driven issues. Identification and synthesis of best practices and lessons learned directly linked to programme country policy goals;</li>\r\n<li>Assist in project development. Analysis and synthesis of proposals on the areas for support and interventions within the practice area specialization assigned;</li>\r\n<li>Support to UNDAF/CPD implementation (support to pillar 5 convening, monitoring and implementation);</li>\r\n<li>Effective planning and logistical support to workshops and ensuring that lessons learnt are disseminated;</li>\r\n<li>Provide technical support to cluster projects to ensure key project deliverables are met;</li>\r\n<li>Work closely with projects and identify issues merit for wider communication and policy advocacy. With input from relevant specialist, produce communication materials and policy briefings.</li>\r\n<li>Contribute to increasing the visibility of the cluster&rsquo;s projects both internally within UNDP, and to the development partners by producing promotional materials and communication materials in close cooperation with communication team of the country <br />office.</li>\r\n</ul>\r\n<p></p>\r\n<ul></ul>"
"""

agent = GeminiPrompting(html_text)
print(agent.clean_html(html_text))
