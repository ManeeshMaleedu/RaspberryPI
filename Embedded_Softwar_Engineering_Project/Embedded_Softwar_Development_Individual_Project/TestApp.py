import tkinter as tk
from tkinter import simpledialog
import sys
sys.path.append('/usr/lib/python3/dist-packages')
from digital_task_manager import DigitalTaskManager
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
from CameraModule import CameraModule

class TestApp:
     def __init__(self,root):
          self.root = root
          self.root.title("Test App")

          self.dtm = DigitalTaskManager(root)
          self.dtm.create_gui()

          self.button_frame = tk.Frame(root)
          self.button_frame.pack()

          self.add_task_button = tk.Button(root, text="Add Task", command=self.dtm.add_task)
          self.add_task_button.grid(row=0, column=0, padx=10, pady=10)

          self.set_deadline_button = tk.Button(root, text="Set Deadline", command=self.dtm.set_deadline)
          self.set_deadline_button.grid(row=0,column=1, padx=10, pady=10)

          self.mark_complete_button = tk.Button(root, text="Mark Complete", command=self.dtm.mark_complete)
          self.mark_complete_button.grid(row=0,column=2, padx=10, pady=10)

          self.delete_task_button = tk.Button(root, text="Delete Task", command=self.dtm.delete_task)
          self.delete_task_button.grid(row=0,column=3, padx=10, pady=10)

          self.load_tasks_button = tk.Button(root, text="Load Tasks", command=self.dtm.load_tasks)
          self.load_tasks_button.grid(row=0, column=4, padx=10, pady=10)

          self.save_tasks_button = tk.Button(root, text="Save Tasks", command=self.dtm.save_tasks)
          self.save_tasks_button.grid(row=0, column=5, padx=10, pady=10)

          self.notify_button = tk.Button(root, text="Notify", command=self.dtm.notify_deadlines)
          self.notify_button.grid(row=0, column=6, padx=10, pady=10)

          self.capture_photo_button = tk.Button(root, text="Capture Photo", command=self.capture_photo)
          self.capture_photo_buttongrid(row=0, column=7, padx=10, pady=10)



     def add_task(self):
         task = simpledialog.askstring("Add Task", "Enter task:")
         if task:
              self.dtm.tasks.append({"name": task, "completed": False, "deadline": None})
              self.dtm.update_task_listbox()
              self.dtm.notify_deadlines()

     def capture_photo(self):
       selected_idx = self.dtm.task_listbox.curselection()
       if selected_idx:
         idx = selected_idx[0]
         task = self.dtm.tasks[idx]
         if "task" in task:
            filename = f"{task['task']}_photo.jpg"
            try:
                self.dtm.camera_module.capture_photo(filename + ".jpg")
                task['photo'] = filename
                self.dtm.update_task_listbox()
                messagebox.showinfo("Photo Captured", "photocaptured and linked to task successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occured: {str(e)}")
         else:
             messagebox.showwarning("No Task Selected", "Please select a task before capturing a photo.")

     def set_deadline(self):
          selected_idx = self.dtm.task_listbox.curselection()
          if selected_idx:
             idx = selected_idx[0]
             deadline_input = simpledialog.askstring("Set Deadline", "Enter Deadline (YYYY-MM-DD):")
             if deadline_input:
                try:
                    deadline = datetime.strptime(deadline_input, "%Y-%m-%d")
                    self.dtm.tasks[idx]["deadline"] = deadline
                    self.dtm.update_task_listbox()
                    self.dtm.notify_deadlines()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. please use YYYY-MM-DD.")

     def mark_completed(self):
         selected_idx = self.dtm.task_listbox.curselection()
         if selected_idx:
            idx = selected_idx[0]
            self.dtm.tasks[idx]["completed"] = True
            self.dtm.update_task_listbox()
            self.dtm.notify_deadlines()

     def delete_task(self):
         selected_idx = self.dtm.task_listbox.curselection()
         if selected_idx:
             idx = selected_idx[0]
             del self.dtm.tasks[idx]
             self.dtm.update_task_listbox()
             self.dtm.save_tasks()
             self.dtm.notify_deadlines()

     def load_tasks(self):
         self.dtm.load_tasks()

     def save_tasks(self):
         self.dtm.save_tasks()

def main():
    root = tk.Tk()
    test_app = TestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

