def prompt_combining(preprocessed_text):
    prompt = f"""
    Given the following job description text, extract all the skill keywords related to the job. Present the extracted skills in a comma separated list. Ignore any non-text formatting characters and focus only on identifying skills related to programming, technology, or any job mentioned in the text.

    Text:
    {preprocessed_text}

    Extracted Skills:
    """