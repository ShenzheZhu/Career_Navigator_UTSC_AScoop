def prompt_combining(preprocessed_text):
    prompt = \
        f"""
    Below are several job descriptions followed by the extracted skills in a comma-separated list. Note that the skills should be single words or brief noun phrases that clearly represent a skill or ability.

    Example 1:
    Job Description: The candidate should have experience in Java programming, teamwork, and effective communication. Knowledge of database management and the ability to work under pressure are essential.
    Extracted Skills: Java, teamwork, communication, database management, work under pressure

    Example 2:
    Job Description: Seeking a professional with skills in graphic design, Adobe Photoshop, client interaction, and project management. Must be innovative and possess problem-solving skills.
    Extracted Skills: graphic design, Adobe Photoshop, client interaction, project management, innovative, problem-solving
    
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

    Now, given the following job description, extract the skill keywords related to the job. Present the extracted skills in a comma-separated list. If no skills can be identified, output 'N/A'. Ignore any non-text formatting characters and focus solely on identifying technical skills and soft skills related to the job in the text.

    Job Description: {preprocessed_text}

    Extracted Skills:

    """

    return prompt
