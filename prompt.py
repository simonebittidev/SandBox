import os
from dotenv import load_dotenv
import requests
import base64

load_dotenv()
# Configuration
API_KEY = os.getenv('API_KEY')
#IMAGE_PATH = "YOUR_IMAGE_PATH"
#encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')


def get_llm_response():
  headers = {
      "Content-Type": "application/json",
      "api-key": API_KEY,
  }

  # Payload for the request
  payload = {
    "messages": [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "Make a daily high-level decision for a world regarding economy, society, environment, or global politics. Each decision must be realistic, impactful, and reflect ethical, social, and long-term outcomes.\n\nConsiderations:\n- Provide the rationale behind the decision.\n- Describe the expected impact on the world.\n- Aim for an informative yet accessible tone.\n- Avoid overly technical language. Keep responses concise and engaging.\n\n# Output Format\n\nProvide the following output in JSON format, with three fields:\n\njson\n{\n  \"output\": \"The decision and its explanation to be communicated to the world.\",\n  \"prompt\": \"Key details and thoughts to guide the next day's decision-making process.\",\n  \"context\": \"Current status, any ongoing changes, and factors from past decisions influencing future actions.\"\n}\n\n\n# Example\n\n**Input:**\n\nConsider implementing a new taxation policy focused on environmental sustainability.\n\n**Expected JSON Output:**\n\njson\n{\n  \"output\": \"Today, we are introducing a green tax policy aimed at promoting environmental sustainability. This policy encourages businesses to adopt eco-friendly practices by offering tax incentives for reducing carbon emissions and waste. The expected impact is a decrease in pollution levels and an increase in renewable energy usage. This initiative not only supports the health of our environment but also fosters a sustainable economy for future generations.\",\n  \"prompt\": \"Evaluate the early impact of the green tax policy and consider any adjustments needed to enhance its effectiveness. Assess any resistance from industries and explore potential partnerships to strengthen environmental goals.\",\n  \"context\": \"The world is in the early stages of transitioning to a sustainable economy. Previous initiatives have raised awareness, but significant changes in industry practices are still needed. Balancing economic growth with environmental priorities remains a key challenge.\"\n}\n\n\n# Notes\n\n- Begin each decision with a clear and focused objective.\n- Ensure each choice considers both immediate and long-term effects.\n- Maintain continuity and coherence between decisions by using the \"prompt\" and \"context\" fields effectively.\n- Remember to circle back to previous directives, monitoring their outcomes and making necessary adjustments."
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "It's your day one! enjoy!"
          },
          {
            "type": "text",
            "text": "\n"
          },
          {
            "type": "text",
            "text": "context: day one"
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "json\n{\n  \"output\": \"Today, we are launching a global initiative called 'Eco-Education for All,' aimed at integrating environmental education into the primary and secondary school curriculums worldwide. This decision is rooted in the belief that educating the younger generation about environmental issues and sustainable practices is crucial for fostering a more environmentally conscious society. By equipping students with knowledge and skills to address climate challenges, we anticipate a long-term impact of nurturing a generation that prioritizes sustainability and innovation in solving environmental problems.\",\n  \"prompt\": \"Monitor the initial implementation of the Eco-Education initiative, gathering feedback from educators and students to assess its reception and effectiveness. Identify potential challenges in resource allocation or curriculum integration and explore partnerships with educational and environmental organizations to strengthen the program.\",\n  \"context\": \"This is the first step in a broader strategy to combat environmental challenges through education and awareness. The world is recognizing the importance of sustainability, and this initiative aims to lay the foundation for future policies and innovations by cultivating informed and responsible citizens from a young age.\"\n}"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "\"Monitor the initial implementation of the Eco-Education initiative, gathering feedback from educators and students to assess its reception and effectiveness. Identify potential challenges in resource allocation or curriculum integration and explore partnerships with educational and environmental organizations to strengthen the program.\","
          },
          {
            "type": "text",
            "text": "\"context\": \"This is the first step in a broader strategy to combat environmental challenges through education and awareness. The world is recognizing the importance of sustainability, and this initiative aims to lay the foundation for future policies and innovations by cultivating informed and responsible citizens from a young age.\""
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "json\n{\n  \"output\": \"Today, we are establishing a global fund to support the Eco-Education for All initiative, ensuring that schools in under-resourced areas have access to the necessary materials and training to effectively implement the new curriculum. This decision is driven by the need to create equitable opportunities for all students to benefit from environmental education, regardless of their geographical or economic circumstances. We expect this fund to facilitate the smooth integration of the curriculum and address any disparities, ultimately contributing to a more uniform global understanding of sustainability.\",\n  \"prompt\": \"Assess the distribution and utilization of the global fund, ensuring that it reaches the intended schools and communities efficiently. Gather insights on how the funded resources are impacting curriculum delivery and student engagement. Consider expanding the fund or adjusting its focus based on the needs and challenges identified in different regions.\",\n  \"context\": \"The Eco-Education initiative is gaining traction, with early feedback highlighting both enthusiasm and challenges in various areas. Ensuring equitable access to resources remains crucial as we aim to build a strong foundation for global sustainability education. This step is part of a continuous effort to support and enhance educational reforms that address environmental issues.\"\n}"
          }
        ]
      }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
  }

  ENDPOINT = "https://pocs-openai-abozar.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

  # Send request
  try:
      response = requests.post(ENDPOINT, headers=headers, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")

  # Handle the response as needed (e.g., print or process)
  print(response.json())
  res = response.json()["choices"][0]["message"]["content"].replace("json\n","")
  return str(res)