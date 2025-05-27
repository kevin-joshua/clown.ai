from image_gen import generate_image
from retriever import query_db
from story_loader import load_stories_to_chroma
import google.generativeai as genai
import os
import re


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

if os.path.exists("chroma_db"):
    print("[✓] Chroma DB already exists. Skipping loading stories.")
else:
    load_stories_to_chroma()


def is_uninformative_response(response_text):
    """
    Returns True if the response is uninformative (e.g., 'I don't know'), False otherwise.
    Handles variations in punctuation and phrasing.
    """
    # Normalize different apostrophes and whitespace
    normalized = response_text.lower().replace("’", "'").strip()
    # Patterns to match "i don't know" at start or anywhere, possibly followed by punctuation/words
    patterns = [
        r"^i don't know\b",               # Starts with "I don't know"
        r"\bi don't know\b",              # Contains "I don't know" as a phrase
        r"^i do not know\b",
        r"\bi do not know\b",
        r"^no idea\b",
        r"\bno idea\b",
        r"^not sure\b",
        r"\bnot sure\b",
        r"^can't help\b",
        r"\bcan't help\b",
        r"^my storybook pages are blank\b",
        r"\bmy storybook pages are blank\b",
        r"^i have no clue\b",
        r"\bi have no clue\b"
    ]
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True
    return False


def generate_response(user_query="How does Gulliver attempt to communicate with the giants in Brobdingnag?"):
    # Retrieve relevant context using MMR
    """
    Generate a response to the user's query based on the context retrieved from the story database.
    This function uses a generative model to create a humorous and witty response, and also generates an image based on the context.
    """ 
    if os.path.exists("output.png"):
        os.remove("output.png")

    context = query_db(user_query)

    # Generate a response using the LLM
    model = genai.GenerativeModel(
          model_name="gemini-1.5-pro",  # or "gemini-1.5-pro" or any supported model
          generation_config={
              "temperature": 0.2,
              "max_output_tokens": 512,
          }
      )
    
    prompt = """
        You are a witty, humorous AI storyteller. You always answer using ONLY the story excerpt provided below.

        Your goals:
        - Answer the question using the story context provided.
        - Be funny, clever, and descriptive. Use sarcasm, exaggeration, or modern analogies.
        - DO NOT invent details outside the provided story.
        - DO NOT mention the story name or say you're using a story.
        - If the user query does NOT seem to come from the story context, start with “I don’t know”  and end in a humorous way. Avoid doing this unless you’re sure the context is unrelated.

        Now, answer the user's question using ONLY the story context below.
        Return ONLY the final witty answer, no extra notes or labels.
        """





    response = model.generate_content(prompt + f"""
                                      Context:{context}
                                      User Query: {user_query}
                                      """)

    # Extract the text from the response
    response_text = response.text.strip()

    print("Response Text:", response_text)

    followup_questions = generate_followup_question(context, response_text)
    questions = []
    for i in followup_questions.split("\n"):
        print("[i] Follow-up Question:", i.strip())
        if i.strip() != "":  # Only add non-empty questions
          questions.append(i.strip())

    if is_uninformative_response(response_text):
        print("[!] Skipping image generation due to uninformative response.")
        return {
            "response": response_text,
            "image_url": None,
            "followup": questions
        }
    
    try:
        image_prompt = image_prompt_generation(context, user_query)
        print("[i] Image Prompt:", image_prompt)
        image_url = generate_image(image_prompt)
        return {
            "response": response_text,
            "image_url": image_url,
            "followup": questions
        }
    except Exception as e:
        print(f"[!] Error during image generation: {e}")
        return {
            "response": response_text,
            "image_url": None,
            "followup": questions
        }




def image_prompt_generation(context, user_query):
    """
    Generates a descriptive image prompt based on the context and user query.
    This function is designed to create a vivid scene that can be used for image generation.
    """
    # Ensure context and user_query are provided
    if not context or not user_query:
        return "No context or user query provided for image generation."

    # Create a final prompt that combines the context and user query
    # This prompt will guide the image generation model to create a relevant image
    final_prompt = f"""
          You are a storyteller AI. Based on the following retrieved context and user query,
          generate a vivid and descriptive scene that can be used to generate an image.
          

          Context:
          {context}

          User Query:
          {user_query}

          Now, write a rich, image-descriptive prompt that can be used by an image generation model.
          """
    model = genai.GenerativeModel(
          model_name="gemini-1.5-pro",  # or "gemini-1.5-pro" or any supported model
          generation_config={
              "temperature": 0.3,
              "max_output_tokens": 512,
          }
      )
    response = model.generate_content(final_prompt)
    return response.text.strip()
  



def generate_followup_question(context, response):
    """
    Generate a follow-up question based on the context and response.
    This function uses a generative model to create a witty and engaging follow-up question.
    """

    model = genai.GenerativeModel(
          model_name="gemini-1.5-pro",  # or "gemini-1.5-pro" or any supported model
          generation_config={
              "temperature": 0.3,
              "max_output_tokens": 512,
          }
      )
    
    final_prompt = f"""

        You are a witty, humorous AI storyteller. Based on the context and response provided below,
        generate two follow-up questions that are engaging, clever, and relevant to the story context.
        - Keep the questions short, light-hearted and funny.
        - Don't number the questions.
        - Avoid asking about the story name or general plot.
        - Only ask questions that can be answered with the story context provided.

        Context:
        {context}

        Response: 
        {response}
        Your task is to create follow-up questions that encourage further exploration of the story,

        """ 
    response = model.generate_content(final_prompt)
    return response.text.strip()