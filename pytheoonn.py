import tkinter as tk
from tkinter import messagebox
import time
import threading

# ---------------------- TO-DO LIST --------------------------
class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do + Pomodoro App")
        self.master.geometry("500x500")
        self.master.resizable(False, False)

        self.tasks = []

        # Title
        tk.Label(master, text="📝 To-Do List", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Input field
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=5)

        # Buttons
        tk.Button(master, text="Add Task", command=self.add_task).pack(pady=2)
        tk.Button(master, text="Delete Selected", command=self.delete_task).pack(pady=2)

        # Task list
        self.listbox = tk.Listbox(master, width=50, height=10, selectmode=tk.SINGLE)
        self.listbox.pack(pady=5)

        # Separator
        tk.Label(master, text="-----------------------------").pack(pady=5)

        # Timer section
        self.timer_label = tk.Label(master, text="Pomodoro Timer", font=("Helvetica", 16, "bold"))
        self.timer_label.pack(pady=5)

        self.time_display = tk.Label(master, text="25:00", font=("Helvetica", 28))
        self.time_display.pack(pady=5)

        tk.Button(master, text="Start Work Session", command=lambda: self.start_timer(25, 5)).pack(pady=2)
        tk.Button(master, text="Reset Timer", command=self.reset_timer).pack(pady=2)

        self.running = False
        self.current_seconds = 1500  # 25 minutes default

    def add_task(self):
        task = self.entry.get()
        if task:
            self.tasks.append(task)
            self.listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.listbox.delete(index)
            del self.tasks[index]

    def update_timer_display(self):
        mins, secs = divmod(self.current_seconds, 60)
        self.time_display.config(text=f"{mins:02}:{secs:02}")

    def countdown(self):
        while self.running and self.current_seconds > 0:
            time.sleep(1)
            self.current_seconds -= 1
            self.update_timer_display()

        if self.running and self.current_seconds == 0:
            messagebox.showinfo("Break Time", "Time for a 5-minute break!")
            self.running = False

    def start_timer(self, work_minutes, break_minutes):
        if not self.running:
            self.current_seconds = work_minutes * 60
            self.update_timer_display()
            self.running = True
            threading.Thread(target=self.countdown).start()

    def reset_timer(self):
        self.running = False
        self.current_seconds = 25 * 60
        self.update_timer_display()

# ---------------------- MAIN --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
