# from tkinter import *
import sv_ttk
import tkinter as tk
from tkinter import ttk

# BG_GRAY = "#ABB2B9"
# BG_COLOR = "#17202A"
# TEXT_COLOR = "#EAECEE"

# FONT = "Raleway 14"
# FONT_BOLD = "Raleway 13 bold"

class ChatApplication:

    def __init__(self):
        self.window = tk.Tk()
        sv_ttk.use_light_theme()
        self._setup_main_window()
    
    def run(self):
        self.window.mainloop()
    
    def _setup_main_window(self):
        self.window.title("Job Interview Training")
        self.window.geometry("1000x600")
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())
        x_cordinate = int((self.window.winfo_screenwidth() / 2) - (self.window.winfo_width() / 2))
        y_cordinate = int((self.window.winfo_screenheight() / 2) - (self.window.winfo_height() / 2))
        self.window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

        # head_label
        head_label = tk.Label(self.window, text="Welcome", pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = tk.Label(self.window, width=450, height=600)
        line.place(relwidth=1, rely = 0.07, relheight=0.012)
        
        # text widget
        self.text_widget = tk.Text(self.window, width=20, height=2, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        # scroll bar
        scrollbar = tk.Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom Label
        bottom_label = tk.Label(self.window, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = tk.Entry(bottom_label)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = tk.Button(bottom_label, text="Reply", 
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
    
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Applicant")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, tk.END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg1)
        self.text_widget.configure(state=tk.DISABLED)
        
        msg2 = f"bot: placeholder\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg2)
        self.text_widget.configure(state=tk.DISABLED)
        
        self.text_widget.see(tk.END)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()