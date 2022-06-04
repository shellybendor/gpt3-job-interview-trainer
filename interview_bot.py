from dotenv import load_dotenv
import os
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class InterviewManager:
      INTERVIEWER_START = "Interview Trainer:"
      APPLICANT_START = "Applicant:"
      FEEDBACK_START = "Feedback:"
      FEEDBACK_INTRO = "You are a job interview trainer, helping an applicant practice interviewing for a job. After each question you give feedback on the answers the applicant gives.\n\n"

      def __init__(self, pos):
            self.interview_intro = f"You are a job interviewer, interviewing an applicant for a job as a {pos}.\n\n"
            self.interview_greeting = f"Interview Trainer: Hello and thank you for taking the time to interview with us today for the position of a {pos}.\n\nApplicant: "
            self.interiew_log = self.interview_greeting
            self.feedback_log = self.interview_greeting

      def get_next_question_line(self):
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=self.interview_intro+self.interiew_log+self.INTERVIEWER_START,
              temperature=0.9,
              max_tokens=150,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0.6,
              stop=[self.INTERVIEWER_START, self.APPLICANT_START]
            )
            return f"{self.INTERVIEWER_START} {response.choices[0].text.strip()}\n\n"
      
      def get_feedback_line(self):
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=self.FEEDBACK_INTRO+self.feedback_log+self.FEEDBACK_START,
              temperature=0.9,
              max_tokens=150,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0.6,
              stop=[self.INTERVIEWER_START, self.APPLICANT_START, self.FEEDBACK_START]
            )
            return f"{self.FEEDBACK_START} {response.choices[0].text.strip()}\n\n"
      
      def add_applicant_response_to_log(self, response):
            self.interiew_log += f"{response}\n\n"
            self.feedback_log += f"{response}\n\n"
      
      def add_question_to_log(self, question):
            self.interiew_log += f"{question}{self.APPLICANT_START}"
            self.feedback_log += f"{question}{self.APPLICANT_START}"
            # print(f"LOGGGG: \n{self.interiew_log}")

      def run(self):
            applicant_response = input(self.interview_greeting)
            while(True):
              self.add_applicant_response_to_log(applicant_response)
              next_question = self.get_next_question_line()
              feedback = self.get_feedback_line()
              self.add_question_to_log(next_question)
              applicant_response = input(f"{feedback}{next_question}{self.APPLICANT_START} ")


if __name__ == '__main__':
      pos = input("What position are you interviewing for? ")
      manager = InterviewManager(pos)
      applicant_response = input(manager.interview_greeting)
      while(True):
        manager.add_applicant_response_to_log(applicant_response)
        next_question = manager.get_next_question_line()
        feedback = manager.get_feedback_line()
        manager.add_question_to_log(next_question)
        applicant_response = input(f"{feedback}{next_question}{manager.APPLICANT_START} ")
