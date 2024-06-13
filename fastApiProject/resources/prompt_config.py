def job_information_prompt_combining(preprocessed_text):
    prompt = \
        f""" Below are several job descriptions followed by the extracted skills in a comma-separated list. Note that 
        the skills should be single word or brief noun phrases that clearly represent a skill or ability.

    Example 1: 
    Job Description: The candidate should have experience in Java programming, teamwork, and effective 
    communication. Knowledge of database management and the ability to work under pressure are essential. Extracted 
    Skills: Java, teamwork, communication, database management, work under pressure

    Example 2: 
    Job Description: Seeking a professional with skills in graphic design, Adobe Photoshop, 
    client interaction, and project management. Must be innovative and possess problem-solving skills. Extracted 
    Skills: graphic design, Adobe Photoshop, client interaction, project management, innovative, problem-solving
    
    Example 3:
    Job Description: Required skills include social media management, content creation, analytical thinking, and SEO optimization.
    Extracted Skills: social media management, content creation, analytical thinking, SEO optimization

    Example 4:
    Job Description: The ideal candidate will have expertise in Python, data analysis, machine learning, and clear communication.
    Extracted Skills: Python, data analysis, machine learning, communication

    Example 5:
    Job Description: Responsibilities include network security, hardware troubleshooting, customer service, and teamwork.
    Extracted Skills: network security, hardware troubleshooting, customer service, teamwork

    Example 6:
    Job Description: Looking for someone with strong leadership, budget management, negotiation skills, and experience in event planning.
    Extracted Skills: leadership, budget management, negotiation, event planning

    Example 7:
    Job Description: The job requires proficiency in HTML, CSS, JavaScript, and responsive web design, along with a knack for problem-solving.
    Extracted Skills: HTML, CSS, JavaScript, responsive web design, problem-solving

    Example 8:
    Job Description: Candidates should have a background in bioinformatics, statistical analysis, research, and written communication.
    Extracted Skills: bioinformatics, statistical analysis, research, written communication

    Example 9:
    Job Description: The role involves customer relationship management, sales strategy development, market analysis, and product knowledge.
    Extracted Skills: customer relationship management, sales strategy, market analysis, product knowledge

    Example 10:
    Job Description: We are seeking expertise in renewable energy systems, project financing, regulatory compliance, and public speaking.
    Extracted Skills: renewable energy systems, project financing, regulatory compliance, public speaking

    Now, given the following job description, extract the skill keywords related to the job. Present the extracted 
    skills in a comma-separated list and don't include any special symbols(besides +, #, -) other than letters and 
    numbers in your output skill, such as "()*&^%$@!~|?>". If no skills can be identified, output 'n/a'. Ignore any 
    non-text formatting characters and focus solely on identifying technical skills and soft skills related to the 
    job in the text.

    Job Description: {preprocessed_text}

    Extracted Skills:

    """
    return prompt


def resume_education_prompt_combining(preprocessed_text):
    prompt = f""" Given the text extracted from student resumes, specifically the education section, identify the 
    subject for each student. 
    
    The subject you find must be one from the following list, If you can't find an exact match, please choose the most similar 
    one according to your experience: 
    
    [African Studies,
    Anthropology,
    Art History and Visual Culture,
    Arts and Science Co-op,
    Arts, Culture and Media,
    Arts Management,
    Astronomy,
    Biological Sciences,
    Certificates,
    Chemistry,
    City Studies,
    Classical Studies,
    Combined Degree Programs,
    Computer Science,
    Concurrent Teacher Education,
    Curatorial Studies,
    Diaspora and Transnational Studies,
    Double Degree Programs,
    Economics for Management Studies,
    English,
    Environmental Science,
    Environmental Studies,
    Food Studies,
    French,
    Geography,
    Global Asia Studies,
    Global Leadership,
    Health Studies,
    Historical and Cultural Studies,
    History,
    International Development Studies,
    International Development Studies (IDS) Co-op,
    International Studies,
    Journalism,
    Languages,
    Linguistics,
    Management,
    Management Co-op,
    Mathematics,
    Media, Journalism, and Digital Cultures - see Media Studies,
    Music and Culture,
    Neuroscience,
    New Media Studies,
    Paramedicine,
    Philosophy,
    Physical Sciences,
    Physics and Astrophysics,
    Political Science,
    Psycholinguistics - see Linguistics,
    Psychology,
    Public Policy,
    Religion,
    Sociology,
    Statistics,
    Studio Art,
    Teaching and Learning, Centre for,
    Theatre and Performance,
    Women's and Gender Studies]
    
    The following examples show some of the possible forms of subject expressions in the Education section.

    Example 1:
    Education Section: 'Bachelor of Science in Computer Science'
    Identified Subject: computer science

    Example 2:
    Education Section: 'BSc in Computer Science'
    Identified Subject: computer science

    Example 3:
    Education Section: 'Master of Science in Mechanical Engineering'
    Identified Subject: mechanical engineering

    Example 4:
    Education Section: 'MSc in Mechanical Engineering'
    Identified Subject: mechanical engineering

    Example 5:
    Education Section: 'BA in Art History'
    Identified Subject: art history

    Example 6:
    Education Section: 'Bachelor of Arts in Art History'
    Identified Subject: art history

    Example 7:
    Education Section: 'PhD in Neuroscience'
    Identified Subject: neuroscience

    Example 8:
    Education Section: 'Doctor of Philosophy in Neuroscience'
    Identified Subject: neuroscience
    
    Now, given the following resume description, extract the subject. Don't include any special symbols(besides +, #, -) other than letters and 
    numbers in your output skill, such as "()*&^%$@!~|?>". If no subject can be identified, output 'n/a'. Ignore any 
    non-text formatting characters and focus solely on identifying subject.
    New Resume:
    {preprocessed_text}

    Identify Subject:
    """
    return prompt


def resume_skill_prompt_combining(preprocessed_text):
    prompt = f"""
    Given the text extracted from a student's resume, analyze the 'Skills' section to identify all the skills mentioned. Skills are typically summarized under specific headings followed by a colon. For example, 'Languages: Python, Java, C, C#'.

    Example 1:
    Resume Text: ' Languages: Python(pandas,numpy), Java, C, C#. Software: Eclipse, Visual Studio.'
    Extracted Skills: python, pandas, numpy, java, c, c#, eclipse, visual studio

    Example 2:
    Resume Text: 'Technical Skills: Data analysis with Excel and SQL, Web development using HTML, CSS, and JavaScript.'
    Extracted Skills: excel, sql, html, css, javascript

    Example 3:
    Resume Text: 'Languages: C/C++'
    Extracted Skills: c, c++

    Example 4:
    Resume Text: 'Professional Skills: Negotiation, Teamwork, Decision making, Time management.'
    Extracted Skills: negotiation, teamwork, decision making, time management

    Example 5:
    Resume Text: 'Engineering Skills: CAD design, Circuit analysis, Thermodynamics.'
    Extracted Skills: cad design, circuit analysis, thermodynamics
    
    Example 6:
    Resume Text: 'ROS 1/2, V-Rep, SQL (Postgres, MS-SQL, MySQL), Linux (Configuring and Managing)'
    Extracted Skills: ros 1/2, v-rep, sql, postgres, ms-sql, mysql, linux

    Now, given the following resume text, extract the skill keywords in skills sections. Present the extracted skills 
    in a comma-separated list, and don't include any special symbols(besides +, #, -) other than letters and numbers in your output skill, 
    such as "()*&^%$@!~|?>". If no skills can be identified, output 'n/a'. Ignore any non-text formatting 
    characters and focus solely on identifying technical skills and soft skills in the text.
        
    New Resume Text:
    {preprocessed_text}
    
    Extracted Skills:
    """
    return prompt
