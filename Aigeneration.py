
import os
import google.generativeai as genai
import os


genai.configure(api_key="AIzaSyA4Fnj1nNXarOr7FQggxUE9pamU9Vgu7eY")

def gemini_run(prompt):

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(prompt)
  
  print(response.text)
  return response.text
