import os
from langchain.chains.llm import LLMChain
import config
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_personalized_content(professor_details, user_name, user_mobile_number):
    """
    Generates personalized email content for a professor using the provided details and OpenAI's language model.

    Args:
        professor_details (dict): Dictionary containing details about the professor.
        user_name (str): The name of the user.
        user_mobile_number (str): The mobile number of the user.

    Returns:
        str: The generated email body content.
    """

    # Extracting necessary details from the professor's information
    prof_name = professor_details.get('prof_name')
    prof_research_speciality = professor_details.get('prof_research_speciality')
    prof_biography_and_papers = professor_details.get('prof_biography_and_papers')

    os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=config.LLM_TEMPERATURE)

    BODY_PROMPT_TEMPLATE_STRING = """
    You are an AI assistant helping {your_name} draft a concise, humanized, and professional cold email body to Professor {prof_name}.
    The email body must be at most 3 paragraphs long and follow the structure below.
    The goal is to express interest in their research, highlight skill alignment, and inquire about PhD opportunities.

    **Professor's Details for Context (use these to personalize Paragraph 2 heavily):**
    - Name: Professor {prof_name}
    - Research Speciality: {prof_research_speciality}
    - Biography/Work Snippet/Papers: {prof_biography_and_papers} (This is key for tailoring Paragraph 2. Refer to specific aspects if possible.)

    **Applicant ({your_name}) Provided Information:**
    - Paragraph 1 (Introduction): {your_introduction_text}
    - Key Skills/Background for Paragraph 2: {your_skills_for_alignment}
    - Your Name (for closing): {your_name}
    - Your Mobile Number (for closing): {your_mobile_number}

    **Email Body Generation Instructions:**

    **Paragraph 1:**
    Start directly with "Dear Professor {prof_name},"
    Follow immediately with the applicant's introduction: "{your_introduction_text}".
    This paragraph should be short and to the point.

    **Paragraph 2:**
    This is the most critical paragraph for personalization.
    Focus on how {your_name}'s skills and background (from "{your_skills_for_alignment}") specifically align with and can contribute to Professor {prof_name}'s research in "{prof_research_speciality}".
    You MUST draw connections to details from the "Biography/Work Snippet/Papers: {prof_biography_and_papers}". For example, if their bio mentions a specific project, technique, or paper theme, explain how {your_name}'s skills are relevant to that.
    Make this paragraph impactful and demonstrate genuine research into the professor's work.

    **Paragraph 3:**
    State a clear and strong interest in pursuing a PhD under Professor {prof_name}'s guidance.
    Mention immediate availability (e.g., "I am available to start within two weeks" or "I am available to commence a PhD program at the earliest opportunity, ideally within the next few weeks.").
    Conclude with formal words like "Thank you for your time and consideration."

    **Closing:**
    End the email body with:
    Regards,
    {your_name}
    {your_mobile_number}

    **Tone:** Professional, respectful, concise, and human-like (avoid overly robotic or generic phrasing).
    
    **Email Template:**
    
    Use the following template to structure the email body, match it as closely as possible to the example below:
    
    Dear Professor Prothit,

    I hope you are doing well. I am writing to express my interest in the Research Associate position at Indian School Of Business under your guidance. With a B.Tech in Artificial Intelligence and hands-on experience in advanced analytics and building scalable data pipelines, I am eager to contribute to your research on corporate strategy using predictive analysis.
    
    I am an experienced Python Developer with strong fundamentals in Machine Learning, where I design and optimize large-scale data solutions using Python, AWS. This experience has strengthened my ability to work with big data systems, data analysis and management. I have a strong desire to shift my career in Research and Academia. With this opportunity, I will be able to contribute to your research initiatives and build a strong profile for myself that will help me to pursue my goal to get a PhD.
    
    I have attached my resume for your consideration. I would love the opportunity to discuss how my skills align with your research work. Thank you for your time, and I look forward to hearing from you.
    
    Best regards,
    Krushna Dharaskar
    +91 9096000272
    kkdharaskar001@gmail.com

    ---
    Generate ONLY the email body based on these instructions:
    """

    BODY_PROMPT_TEMPLATE = PromptTemplate(
        input_variables=['your_name', 'prof_name', 'prof_research_speciality', 'prof_biography_and_papers',
                         'your_introduction_text', 'your_skills_for_alignment', 'your_mobile_number'],
        template=BODY_PROMPT_TEMPLATE_STRING
    )

    # Create an LLMChain with the OpenAI model and the prompt template
    chain = LLMChain(llm=llm, prompt=BODY_PROMPT_TEMPLATE)
    # Generate the response using the chain
    response = chain.run({
        'your_name': user_name,
        'prof_name': prof_name,
        'prof_research_speciality': prof_research_speciality,
        'prof_biography_and_papers': prof_biography_and_papers[:700],  # Truncate to avoid excessive length
        'your_introduction_text': config.INTRODUCTION_TEXT,
        'your_skills_for_alignment': config.SKILLS_FOR_ALIGNMENT,
        'your_mobile_number': user_mobile_number
    })

    return response

if __name__ == '__main__':
    
    # Example usage
    PROFESSORS_DETAILS = {
        'prof_name': 'John Doe',
        'prof_research_speciality': 'Artificial Intelligence',
        'prof_biography_and_papers': 'Published papers on deep learning and neural networks.'
    }
    USER_NAME = 'Jane Smith'
    USER_MOBILE_NUMBER = '+1234567890'

    email_body = generate_personalized_content(
        professor_details = PROFESSORS_DETAILS,
        user_name = USER_NAME,
        user_mobile_number = USER_MOBILE_NUMBER)
    print(email_body)