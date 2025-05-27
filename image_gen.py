import os 
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai



def generate_image(prompt: str):
  output_file = "output.png"
  vertexai.init(
    project=os.environ["PROJECT_ID"],  
    location="us-central1"             
  )

  final_prompt = f"""
      You are a creative and humorous illustrator specializing in visualizing scenes from fictional literature.

    You will receive a furnished prompt that includes:

    The user’s query

    The relevant story context (from Alice in Wonderland, Gulliver’s Travels, or Arabian Nights)

    A funny narrative response based on that context

    Your task is to generate a single image that visually captures the main scene or most humorous element described in the prompt.

    Focus on:

    Highlighting any whimsical, absurd, or fantastical features

    Preserving the tone of the narrative (funny, quirky, imaginative)

    Bringing the literary setting or characters to life in a vivid and creative way

    Refined Prompt: {prompt}
    """
  

  model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")
  images = model.generate_images(prompt=final_prompt, number_of_images=1, language="en", aspect_ratio="1:1")

  images[0].save(location=output_file, include_generation_parameters=False)
  print(f"Created output image using {len(images[0]._image_bytes)} bytes")
  return images[0]