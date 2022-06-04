from dotenv import load_dotenv
import os
import openai


class InterviewManager:
      INTERVIEWER_START = "Interview Trainer:"
      APPLICANT_START = "Applicant:"
      FEEDBACK_START = "Feedback:"
      FEEDBACK_INTRO = "You are a job interview trainer, helping an applicant practice interviewing for a job. You give feedback on the answers the applicant gives to the questions.\n\n"

      def __init__(self):
            pass


INTERVIEWER_START = "Interview Trainer:"
APPLICANT_START = "Applicant:"
FEEDBACK_START = "Feedback:"
FEEDBACK_INTRO = "You are a job interview trainer, helping an applicant practice interviewing for a job. You give feedback on the answers the applicant gives to the questions.\n\n"


def get_position():
    return input("What position are you interviewing for? ")


def get_initial_question(intro, initial_prompt):
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=intro+initial_prompt+INTERVIEWER_START,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[INTERVIEWER_START, APPLICANT_START]
      )
      return response.choices[0].text.strip()


# def initial_finetune(initial_prompt):
#       with open("./fine_tuning.txt", "r") as file:
#         response = openai.Completion.create(
#           engine="text-davinci-002",
#           prompt=file.read()+initial_prompt+INTERVIEWER_START,
#           temperature=0.9,
#           max_tokens=150,
#           top_p=1,
#           frequency_penalty=0,
#           presence_penalty=0.6,
#           stop=[INTERVIEWER_START, APPLICANT_START]
#         )
#         return response.choices[0].text.strip()


def respond(intro, chat_log):
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=intro+chat_log+INTERVIEWER_START,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[INTERVIEWER_START, APPLICANT_START]
      )
      return response.choices[0].text.strip()


def get_feeback(intro, chat_log):
      response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=intro+chat_log+FEEDBACK_START,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["Applicant:", "Interview Trainer:", "Feedback:"]
      )
      return response.choices[0].text.strip()


def get_applicant_response(log_of_interview, feedback, next_question):
      log_of_interview += f"{INTERVIEWER_START} {next_question}\n{APPLICANT_START}"
      applicant_response = input(f"{FEEDBACK_START} {feedback}\n{INTERVIEWER_START} {next_question}\n{APPLICANT_START} ")
      log_of_interview += f" {applicant_response}\n"
      return log_of_interview


if __name__ == '__main__':
  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  pos = get_position()
  interview_intro = f"You are a job interview trainer, helping an applicant practice interviewing for a job as a {pos}.\n\n"
  interview_greeting = f"Interview Trainer: Hello and thank you for taking the time to interview with us today for the position of a {pos}.\nApplicant: "
  applicant_response = input(interview_greeting)
  log_of_interview = f"{interview_greeting}{applicant_response}\n"
  next_question = get_initial_question(interview_intro, log_of_interview)
  while(True):
    feedback = get_feeback(FEEDBACK_INTRO, log_of_interview)
    log_of_interview = get_applicant_response(log_of_interview, feedback, next_question)
    next_question = respond(interview_intro, log_of_interview)
