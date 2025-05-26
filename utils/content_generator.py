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
        prof_name = professor_details.get('Name')
        prof_research_speciality = professor_details.get('Research-Speciality', "")
        prof_biography_and_papers = professor_details.get('Biography', "")

        # Set up Google API
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API Key not found in configuration")
        
        os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY

        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=config.LLM_TEMPERATURE,
            top_p=0.8,
            top_k=40,
        )

        # Create the prompt template
        BODY_PROMPT_TEMPLATE = PromptTemplate(
            input_variables = ['your_name', 'prof_name', 'prof_research_speciality', 'prof_biography_and_papers', 'your_skills_for_alignment', 'your_mobile_number'],
            template="""
You are an AI assistant specializing in crafting personalized outreach emails to professors for research opportunities. You are provided with the following information:

Professor's Name: {prof_name}
Professor's Biography: {prof_biography_and_papers}

Generic Email Template:

Dear Professor [Professor Name],

Greetings for the day!

I am Krushna Dharaskar. A graduate with a B.Tech in Artificial Intelligence with 1.5 years of experience in data analytics with a strong foundation in Python, Big Data, ML, Gen AI, and SQL, and was an undergraduate researcher in the center of excellence lab.

I have been following your work in [] and I found it very interesting. I am strongly interested in being part of your research projects, and I believe my mindset to make a greater contribution to research and my data analytical skills could be a valuable asset in supporting your research.

I request if there is an open position for any of the projects you work on.

I will be committed to the work. I plan to pursue a PhD in the future in management studies. I hope you will consider my application for research collaboration. I have also attached my resume for your reference.

Thank you for your time and consideration.

Yours Sincerely,
Krushna Dharaskar

Instructions:

Replace [Professor Name]: Substitute the provided Professor's Name into the email template.

Identify Research Area: Carefully analyze the Professor's Biography to identify the Professor's primary research area(s). Look for keywords, specific project mentions, publications, and overall themes. The research area should be a specific topic, not just a general field like "Computer Science". Examples could be "Natural Language Processing for Education", "Quantum Computing Algorithms", "Sustainable Energy Policy", etc.

Replace [] with Research Area: Replace the [] placeholder in the sentence "I have been following your work in [] and I found it very interesting." with a concise and accurate description of the Professor's research area as determined in step 2. The sentence should read in a natural and grammatically correct manner. Make sure it fits the flow of the sentence and sounds genuinely interested in the Professor's work.

Output: Provide the complete modified email, with both placeholders replaced. Only output the full email with the edits made.

"""
        )

        # Create an LLMChain and generate the response
        chain = LLMChain(llm=llm, prompt=BODY_PROMPT_TEMPLATE)
        response = chain.run({
            'prof_name': prof_name,
            'prof_biography_and_papers': prof_biography_and_papers,
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