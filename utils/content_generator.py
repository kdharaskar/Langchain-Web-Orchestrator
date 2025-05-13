import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent))

from langchain.chains.llm import LLMChain
import config
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_personalized_content(professor_details, user_name, user_mobile_number):
    """
    Generates personalized email content for a professor using Google's Gemini model.

    Args:
        professor_details (dict): Dictionary containing details about the professor.
        user_name (str): The name of the user.
        user_mobile_number (str): The mobile number of the user.

    Returns:
        str: The generated email body content.
    """
    try:
        # Validate input parameters
        if not all([professor_details, user_name, user_mobile_number]):
            raise ValueError("Missing required parameters")

        # Extracting necessary details from the professor's information
        prof_name = professor_details.get('prof_name')
        prof_research_speciality = professor_details.get('prof_research_speciality')
        prof_biography_and_papers = professor_details.get('prof_biography_and_papers')

        if not all([prof_name, prof_research_speciality, prof_biography_and_papers]):
            raise ValueError("Missing required professor details")

        # Set up Google API
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API Key not found in configuration")
        
        os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY

        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=config.LLM_TEMPERATURE,
            top_p=0.8,
            top_k=40,
            max_output_tokens=1024
        )

        # Create the prompt template
        BODY_PROMPT_TEMPLATE = PromptTemplate(
            input_variables=['your_name', 'prof_name', 'prof_research_speciality', 'prof_biography_and_papers',
                           'your_introduction_text', 'your_skills_for_alignment', 'your_mobile_number'],
            template="""
Generate a professional and personalized email to Professor {prof_name}.

Context:
- Professor's Research: {prof_research_speciality}
- Professor's Background: {prof_biography_and_papers}
- Your Name: {your_name}
- Your Introduction: {your_introduction_text}
- Your Skills: {your_skills_for_alignment}
- Your Contact: {your_mobile_number}

Guidelines:
1. Start with "Dear Professor {prof_name},"
2. First paragraph: Brief introduction and purpose
3. Second paragraph: Connect your skills to their research
4. Final paragraph: Express interest in collaboration and thank them
5. End with "Best regards," followed by your name and contact

Keep the email concise, professional, and focused on research alignment.
"""
        )

        # Create an LLMChain and generate the response
        chain = LLMChain(llm=llm, prompt=BODY_PROMPT_TEMPLATE)
        response = chain.run({
            'your_name': user_name,
            'prof_name': prof_name,
            'prof_research_speciality': prof_research_speciality,
            'prof_biography_and_papers': prof_biography_and_papers[:1000],  # Truncate to avoid token limits
            'your_introduction_text': config.INTRODUCTION_TEXT,
            'your_skills_for_alignment': config.SKILLS_FOR_ALIGNMENT,
            'your_mobile_number': user_mobile_number
        })

        return response.strip()

    except Exception as e:
        print(f"Error generating email content: {str(e)}")
        return None

if __name__ == '__main__':
    # Example usage
    PROFESSOR_DETAILS = {
        'prof_name': 'John Doe',
        'prof_research_speciality': 'Artificial Intelligence',
        'prof_biography_and_papers': 'Published papers on deep learning and neural networks.'
    }
    USER_NAME = 'Jane Smith'
    USER_MOBILE_NUMBER = '+1234567890'

    email_body = generate_personalized_content(
        professor_details=PROFESSOR_DETAILS,
        user_name=USER_NAME,
        user_mobile_number=USER_MOBILE_NUMBER
    )
    
    if email_body:
        print("Generated Email Body:")
        print("-" * 50)
        print(email_body)
        print("-" * 50)
    else:
        print("Failed to generate email content")