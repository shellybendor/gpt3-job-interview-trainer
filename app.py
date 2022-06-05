import sv_ttk
import tkinter as tk

from interview_bot import InterviewManager


class ChatApplication:

    def __init__(self):
        self.window = tk.Tk()
        self.main_page = tk.Frame(self.window)
        self.start_page = tk.Frame(self.main_page)
        self.chat_page = tk.Frame(self.main_page)
        sv_ttk.use_light_theme()
        self._setup_main_window()
        self.main_page.pack(side="top", fill="both", expand=True)
        self._setup_start_page()
        self.start_page.pack(side="top", fill="both", expand=True)
        self.start_page.place(in_=self.main_page, x=0, y=0, relwidth=1, relheight=1)
        self._setup_chat_page()
        self.chat_page.pack(side="top", fill="both", expand=True)
        self.chat_page.place(in_=self.main_page, x=0, y=0, relwidth=1, relheight=1)
        self.start_page.lift()
    
    def run(self):
        self.window.mainloop()
    
    def _setup_start_page(self):
        # head_label
        head_label = tk.Label(self.start_page, text="What position are you interviewing for?", pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = tk.Label(self.start_page, width=450, height=600)
        line.place(relwidth=1, rely = 0.07, relheight=0.012)

        # center label
        center_label = tk.Label(self.start_page)
        center_label.place(relwidth=1, relheight=1, rely=0.25)

        # position entry box
        self.position_entry = tk.Entry(center_label)
        self.position_entry.place(relwidth=0.5, relheight=0.06, rely=0, relx=0.20)
        self.position_entry.focus()
        self.position_entry.bind("<Return>", self._on_entered_position)

        # send button
        send_button = tk.Button(center_label, text="Let's Start", 
                             command=lambda: self._on_entered_position(None))
        send_button.place(relx=0.72, rely=0.008, relheight=0.06, relwidth=0.22)
    
    def _setup_chat_page(self):
        # head_label
        head_label = tk.Label(self.chat_page, text="Welcome To the Interview Trainer", pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = tk.Label(self.chat_page, width=450, height=600)
        line.place(relwidth=1, rely = 0.07, relheight=0.012)
        
        # text widget
        self.text_widget = tk.Text(self.chat_page, width=20, height=2, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        # bottom Label
        bottom_label = tk.Label(self.chat_page, height=100)
        bottom_label.place(relwidth=1, rely=0.8)

        # message entry box
        self.msg_entry = tk.Entry(bottom_label)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = tk.Button(bottom_label, text="Reply", 
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _setup_main_window(self):
        self.window.title("Job Interview Training")
        self.window.geometry("1000x600")
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())
        x_cordinate = int((self.window.winfo_screenwidth() / 2) - (self.window.winfo_width() / 2))
        y_cordinate = int((self.window.winfo_screenheight() / 2) - (self.window.winfo_height() / 2))
        self.window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
        
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_apllicant_response(msg)
        self._insert_feedback_and_question()
    
    def _on_entered_position(self, event):
        self.pos = self.position_entry.get()
        self.chat_page.lift()
        self._start_interview(self.pos)

    def _start_interview(self, pos):
        self.interview_manager = InterviewManager(pos)
        start_msg = self.interview_manager.interview_greeting
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, start_msg)
        self.text_widget.configure(state=tk.DISABLED)
    
    def _insert_apllicant_response(self, msg):
        if not msg:
            return
        
        self.msg_entry.delete(0, tk.END)
        answer = f" {msg}\n\n"
        self.interview_manager.add_applicant_response_to_log(msg)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, answer)
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.see(tk.END)
    
    def _insert_feedback_and_question(self):
        feedback = self.interview_manager.get_feedback_line()
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, feedback)
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.see(tk.END)
        question = self.interview_manager.get_next_question_line()
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, question)
        self.text_widget.insert(tk.END, self.interview_manager.APPLICANT_START)
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.see(tk.END)
        self.interview_manager.add_to_log(question, feedback)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()