from dotenv import load_dotenv
from random import choice
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# completion = openai.Completion()

def get_name_and_position():
    return input("What is your name?"), input("What position are you interviewing for?")

name, pos = get_name_and_position()

start_sequence = "\nYou:"
restart_sequence = f"\n{name}:"

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=f"You are interviewing {name} for a job as a {pos}.\n\nYou : Hello and thank you for taking the time to interview with us today.\n{name}: Thank you for having me.",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=["You:", "{name}:"]
)

print(response)



