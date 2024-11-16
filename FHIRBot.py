#This code was optimised for Google Colab.

!pip install groq
!pip install gradio


from groq import Groq
from google.colab import userdata
import gradio as gr
from groq import Groq
from google.colab import userdata
import gspread
from google.auth import default
from google.colab import auth

# Setting up Gradio UI elements.

def ask_fhir_question_gradio(question):
  """
  Asks a question about FHIR to the LLM and saves the conversation in Google Sheets.
  """
  client = Groq(api_key=userdata.get('Groq_Key'))
  completion = client.chat.completions.create(
      model="llama-3.2-90b-text-preview",
      messages=[
          {
              "role": "system",
              "content": "You are an expert on the FHIR documentation and can help healthcare developers quickly with any query about the FHIR protocol. Scrap every single sub-page on this website https://hl7.org/fhir/documentation.html and provide answers to the healthcare developers only faculty accurate answers from the website. Don't hallucinate. "
          },
          {
              "role": "user",
              "content": question
          }
      ],
      temperature=1,
      max_tokens=1024,
      top_p=1,
      stream=True,
      stop=None,
  )

  answer = ""
  for chunk in completion:
      answer += chunk.choices[0].delta.content or ""

  # Save the question and answer to Google Sheets
  
  row = [question, answer]
  worksheet.append_row(row)
  return answer

iface = gr.Interface(
    fn=ask_fhir_question_gradio,
    inputs=gr.Textbox(lines=2, placeholder="Ask your FHIR question here..."),
    outputs="text",
    title="FHIR Chatbot",
    description="Ask any question about the FHIR protocol."
)

iface.launch(share=True)