from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_position():
    return input("What position are you interviewing for? ")

pos = get_position()


START_SEQUENCE = "You : "
RESTART_SEQUENCE = "Applicant : "
INITIAL_PROMPT = f"You are interviewing an applicant for a job as a {pos}.\n\n"
INITIAL_CHAT_LOG = f"You : Hello and thank you for taking the time to interview with us today for the position of a {pos}.\nApplicant: Thank you for having me.\n"


def get_initial_question():
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=INITIAL_PROMPT+INITIAL_CHAT_LOG+START_SEQUENCE,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[START_SEQUENCE, RESTART_SEQUENCE, "\n"]
      )
      # import ipdb; ipdb.set_trace()
      return response.choices[0].text.strip()


def initial_finetune():
      with open("./fine_tuning.txt", "r") as file:
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=file.read()+INITIAL_PROMPT+INITIAL_CHAT_LOG+START_SEQUENCE,
          temperature=0.9,
          max_tokens=150,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.6,
          stop=[START_SEQUENCE, RESTART_SEQUENCE, "\n"]
        )
        return response.choices[0].text.strip()


def respond(chat_log):
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=chat_log,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[START_SEQUENCE, RESTART_SEQUENCE, "\n"]
      )
      # import ipdb; ipdb.set_trace()
      return response.choices[0].text.strip()


chat_log = f"{INITIAL_CHAT_LOG}{START_SEQUENCE}{get_initial_question()}"
while(True):
      chat_log= f"{chat_log}\n{RESTART_SEQUENCE}"
      applicant_response = input(chat_log)
      chat_log = f"{chat_log}{applicant_response}\n{START_SEQUENCE}"
      chat_log = f"{chat_log}{respond(chat_log)}"
