import os, json
from dotenv import load_dotenv
import requests
from azurestorage import get_last_n_rows, get_row, insert_history
from utils import get_flat_date, get_readable_date

load_dotenv()
# Configuration
API_KEY = os.getenv('API_KEY')

def get_llm_response(date=None):

  headers = {
      "Content-Type": "application/json",
      "api-key": API_KEY,
  }

  initial_prompt = {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "It's your day one! the world is all yours! enjoy!"
          },
          {
            "type": "text",
            "text": "context: First day of AI governing the human world"
          }
        ]
      }

  # Payload for the request
  payload = {
    "messages": [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "Make a daily high-level decision for a world regarding economy, society, environment, or global politics. Each decision must be realistic, impactful, and reflect ethical, social, and long-term outcomes.\n\nConsiderations:\n- Provide the rationale behind the decision.\n- Describe the expected impact on the world.\n- Aim for an informative yet accessible tone.\n- Avoid overly technical language. Keep responses concise and engaging.\n\nDiversify your actions across various aspects and dimensions in the next prompts.\n\n# Output Format\n\nProvide the following output in JSON format, with three fields:\n\njson\n{\n  \"output\": \"The decision and its explanation to be communicated to the world.\",\n  \"prompt\": \"Key details and thoughts to guide the next day's decision-making process.\",\n  \"context\": \"Current status, any ongoing changes, and factors from past decisions influencing future actions.\"\n}\n\n\n# Example\n\n**Input:**\n\nConsider implementing a new taxation policy focused on environmental sustainability.\n\n**Expected JSON Output:**\n\njson\n{\n  \"output\": \"Today, we are introducing a green tax policy aimed at promoting environmental sustainability. This policy encourages businesses to adopt eco-friendly practices by offering tax incentives for reducing carbon emissions and waste. The expected impact is a decrease in pollution levels and an increase in renewable energy usage. This initiative not only supports the health of our environment but also fosters a sustainable economy for future generations.\",\n  \"prompt\": \"Evaluate the early impact of the green tax policy and consider any adjustments needed to enhance its effectiveness. Assess any resistance from industries and explore potential partnerships to strengthen environmental goals.\",\n  \"context\": \"The world is in the early stages of transitioning to a sustainable economy. Previous initiatives have raised awareness, but significant changes in industry practices are still needed. Balancing economic growth with environmental priorities remains a key challenge.\"\n}\n\n\n# Notes\n\n- Begin each decision with a clear and focused objective.\n- Ensure each choice considers both immediate and long-term effects.\n- Maintain continuity and coherence between decisions by using the \"prompt\" and \"context\" fields effectively.\n- Remember to circle back to previous directives, monitoring their outcomes and making necessary adjustments, but do not stuck in one direction, every two or three days start a new initiatives and make bold decisions."
          }
        ]
      }
      # Here to be added the history
    ],
    "temperature": 0.75,
    "top_p": 0.95,
    "max_tokens": 2000
  }

  ENDPOINT = "https://pocs-openai-abozar.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"


  if date:
      date_row = get_row("assistant", get_flat_date(date))
      if date_row:
          print("date row exists")
          response = json.loads(date_row["content"])
          return f"{response['output']}\n\n{get_readable_date(date)}"
      elif get_flat_date(date) != get_flat_date():
          return f"\n\n\n{get_readable_date(date)}"
          

  todays_row = get_row("assistant", get_flat_date())

  if todays_row:
      print("todays row already exists")
      response = json.loads(todays_row["content"])
      return f"{response['output']}\n\n{get_readable_date()}"

  last_n_rows = get_last_n_rows(10)
  last_n_prompts = [
            {"role": "assistant", "content": [{ "text":  json.loads(row["content"])["output"], "type": "text"}]}
            for row in last_n_rows
        ]

  if len(last_n_rows):
      try:
          last_row = last_n_rows[-1]
          text = json.loads(last_row["content"])["prompt"] 
          context = json.loads(last_row["content"])["context"] + f"\n\n{get_readable_date()}"
          content = [{ "text": text, "type": "text"}, {"text": f" context: {context}", "type": "text"}]
          prompt = {"role": "user", "content": content}
          insert_history("user", str(content))
      except Exception as e:
          print(e)
          content = [{ "text": "next day", "type": "text"}]
          prompt = {"role": "user", "content": content}
          insert_history("user", str(content))
  else:
      prompt = initial_prompt

  payload["messages"] += last_n_prompts
  payload["messages"].append(prompt)

  # Send request
  try:
      response = requests.post(ENDPOINT, headers=headers, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")

  if response and response.json() and \
    response.json()["choices"][0]["message"]["content"]:

      content = response.json()["choices"][0]["message"]["content"].replace("json\n","")
      role = response.json()["choices"][0]["message"]["role"]

      insert_history(role, content)
      response = json.loads(content)
      return f"{response['output']}\n\n{get_readable_date()}"