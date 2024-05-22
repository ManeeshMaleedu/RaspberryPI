import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime, timedelta
import pickle
import picamera
from CameraModule import CameraModule
from PIL import Image, ImageTk

class DigitalTaskManager:
    def __init__(self, root):
        self.camera = CameraModule()
        self.root = root
        self.root.title("Digital Task Manager")
        self.tasks = []

        self.task_entry = None



    def add_task(self):
        task = self.task_entry.get()
        if task:
          self.tasks.append({"task": task, "completed": False, "deadline": None})
          self.update_task_listbox()
          self.task_entry.delete(0, tk.END)
          self.notify_deadlines()

    def capture_photo(self):
       selected_idx  = self.task_listbox.curselection()
       if selected_idx:
         idx = selected_idx[0]
         task = self.tasks[idx]
         if task.get("task"):
            filename = f"{task['task']}_photo.jpg"
            try:
                self.camera.capture_photo(filename)
                task['photo'] = filename
                self.update_task_listbox()
                messagebox.showinfo("Photo Captured", "Photo captured and linked to task successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
       else:
         messagebox.showwarning("No Task Selected", "please select a task before capturing a photo.")

    def mark_complete(self):
        selected_idx = self.task_listbox.curselection()
        if selected_idx:
           idx = selected_idx[0]
           self.tasks[idx]["completed"] = True
           self.update_task_listbox()
           self.notify_deadlines()

    def delete_task(self):
        selected_idx = self.task_listbox.curselection()
        if selected_idx:
           idx = selected_idx[0]
           del self.tasks[idx]
           self.update_task_listbox()
           self.save_tasks()
           self.notify_deadlines()

    def set_deadline(self):
        selected_idx = self.task_listbox.curselection()
        if selected_idx:
           idx = selected_idx[0]
           deadline_input = tk.simpledialog.askstring("Set Deadline", "Enter deadline (YYYY-MM-DD):")
           if deadline_input:
              try:
                 deadline = datetime.strptime(deadline_input, "%Y-%m-%d")
                 self.tasks[idx]["deadline"] = deadline
                 self.update_task_listbox()
                 self.notify_deadlines()
              except ValueError:
                 messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def save_tasks(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".dat", filetypes=[("Task Files", "*.dat")])
        if filename:
            with open(filename, "wb") as file:
                pickle.dump(self.tasks, file)
            messagebox.showinfo("Save", "Tasks saved successfully.")

    def load_tasks(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("Task Files", "*.dat")])
        if filename:
            with open(filename, "rb") as file:
                self.tasks = pickle.load(file)
                print("loaded tasks:", self.tasks)
                self.update_task_listbox()
            messagebox.showinfo("load", "Tasks loaded successfully.")

    def notify_deadlines(self):
        current_time = datetime.now()
        notification_time_threshold= current_time + timedelta(hours=24)
        for task in self.tasks:
            if task["deadline"] and not task["completed"]:
               time_until_deadline = task["deadline"] - current_time
               if timedelta(seconds=0) <=time_until_deadline <= timedelta(hours=24):
                  message = f"Deadline for task '{task['task']}' is approaching!"
                  messagebox.showwarning("Deadline Approaching", message)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks):
            status = "$" if task["completed"] else " "
            photo_indicator = "[Photo]" if "photo" in task else ""
            task_text = f"{status} {task['task']} - {task['deadline']}" if task['deadline'] else f"{status} {task['task']}"
            self.task_listbox.insert(idx, task_text)

    def show_task_photo(self, event=None):
        selected_idx = self.task_listbox.curselection()
        if selected_idx:
           idx = selected_idx[0]
           task = self.tasks[idx]
           if "photo" in task:
               photo_filename = task["photo"]
               try:
                  photo = Image.open(photo_filename)
                  photo.show()
               except Exception as e:
                  messagebox.showerror("Error", f"An error occurred while opening the photo: {e}")

           else:
               messagebox.showinfo("Info", "No photo attached to this task.") 

    def create_gui(self):
       self.root.geometry("500x400")

       top_frame = tk.Frame(self.root)
       top_frame.grid(row=0, column=0, padx=10, pady=10)

       middle_frame = tk.Frame(self.root)
       middle_frame.grid(row=1, column=0, padx=10, pady=10)

       bottom_frame = tk.Frame(self.root)
       bottom_frame.grid(row=2, column=0, padx=10, pady=10)

       self.task_entry = tk.Entry(top_frame)
       self.task_entry.grid(row=0, column=0, padx=2)

       self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
       self.add_button.grid(row=0, column=1, padx=3)

       self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
       self.task_listbox.grid(row=2, column=0, padx=5, pady=5)

       self.task_listbox.bind("<<ListboxSelect>>", self.show_task_photo)

       task_listbox_scroll_y = tk.Scrollbar(middle_frame, command=self.task_listbox.yview)
       task_listbox_scroll_y.grid(row=1, column=0)
       self.task_listbox.config(yscrollcommand=task_listbox_scroll_y.set)

       self.complete_button = tk.Button(self.root, text="Mark Complete", command=self.mark_complete)
       self.complete_button.grid(row=1, column=1, padx=5)

       self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
       self.delete_button.grid(row=0, column=3, padx=5)

       self.set_deadline_button = tk.Button(self.root, text="Set Deadline", command=self.set_deadline)
       self.set_deadline_button.grid(row=1, column=3, padx=5)

       self.save_button = tk.Button(self.root, text="save Tasks", command=self.save_tasks)
       self.save_button.grid(row=2, column=1, padx=5)

       self.load_button = tk.Button(self.root, text="Load Tasks", command=self.load_tasks)
       self.load_button.grid(row=2, column=2, padx=5)

       self.capture_button = tk.Button(self.root, text="Capture Photo", command=self.capture_photo)
       self.capture_button.grid(row=0, column=2, padx=5)

       self.notify_button = tk.Button(self.root, text="Notify", command=self.notify_deadlines)
       self.notify_button.grid(row=1, column=2, padx=5)

       self.root.mainloop()

def main():
    root = tk.Tk()
    app = DigitalTaskManager(root)
    app.create_gui()
    root.mainloop()

if __name__ == "__main__":
      main()
