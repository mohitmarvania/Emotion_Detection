import os.path
from pathlib import Path
from tkinter import *
from tkcalendar import DateEntry
import testing_emotions
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from PIL import ImageTk, Image

"""
THIS IS THE MAIN GUI WHICH CONTROLS EVERYTHING AND WHICH IS SHOWN TO THE USER.
ALSO IT HAS ALL THE BELOW MENTIONS FEATURES : 
1. Faculty selection dropdown menu.
2. Automatically takes current date.
3. Without selecting any faculty feedback cannot be taken.
4. Directly clicking on submit button will not do anything to the excel file and closes the GUI.
"""

# Global variable to store the emotion value
emotion_result = ""


def run_main_feedback_program():
    # Function which calls the main feedback program when feedback button is clicked
    global emotion_result

    # Check if a faculty is selected.
    if dropdown.get() == "":
        messagebox.showwarning("Warning", "Please select faculty first !")
        return

    emotion_result = testing_emotions.test_emotion()


# FUNCTION WHICH IS CALLED WHEN DATA IS SUBMITTED AND ALSO THE EXCEL SHEET IS GENERATED.
def submit_feedback():
    # Function to handle the Submit button click event
    global emotion_result

    # Get the current date and time
    current_date = date.today().strftime("%Y-%m-%d")

    # Get the selected faculty
    selected_faculty_final = dropdown.get()

    # Check if a faculty is selected
    if dropdown.get() == "":
        root.destroy()
        return

    # Create a DataFrame with the data
    feedback_data = pd.DataFrame({
        'Time': [pd.Timestamp.now()],
        'Faculty': [selected_faculty_final],
        'Emotion': [emotion_result]
    })

    # Set the file name for the Excel file
    excel_file_name = f"feedback_data_{current_date}.xlsx"

    # Set the path for the Excel file
    downloads_folder = Path.home() / "Downloads"
    excel_file_path = downloads_folder / excel_file_name

    # Check if the file already exists
    if os.path.isfile(excel_file_path):
        # If the file exists, append the data to the existing file
        existing_data = pd.read_excel(excel_file_path)
        updated_data = pd.concat([existing_data, feedback_data], ignore_index=True)
        updated_data.to_excel(excel_file_path, index=False)
    else:
        # If the file does not exists, create a new file with the data
        feedback_data.to_excel(excel_file_path, index=False)

    # Close the tkinter window.
    root.destroy()


def get_selected_faculty(event):
    # Function to handle the dropdown selection event
    selected_faculty = dropdown.get()
    selected_faculty_label.config(text=selected_faculty)


# Create the main Tkinter window
root = tk.Tk()
root.title("Charusat Live Feedback App")
root.geometry("925x500+300+200")
root.resizable(False, False)

# Load the image
image = Image.open("/Users/mohit/PycharmProjects/Emotion_detection/cspit.jpg")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)

# Create a label to display image
image_label = tk.Label(root, image=photo)
image_label.place(x=10, y=10)

# Centered text label
welcome_label = tk.Label(root, text="WELCOME TO CHARUSAT LIVE FEEDBACK APP", font=("Times New Roman", 24))
welcome_label.place(relx=0.5, rely=0.2, anchor="center")

# Separator line≤
separator = ttk.Separator(root, orient="horizontal")
separator.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8)

# Dropdown menu
faculty_label = tk.Label(root, text="Please select faculty : ", font=("Arial", 16))
faculty_label.place(relx=0.4, rely=0.35, anchor="e")
faculty_names = ["Dr. Amit Thakkar",
                 "Prof. Hemang Thakar",
                 "Prof. Pinal shah",
                 "Prof. Dharmendrasinh Rathod",
                 "Prof. Brinda Patel",
                 "Prof. Bela Shah",
                 "Prof. Spandan Joshi"]
selected_faculty = tk.StringVar()
dropdown = ttk.Combobox(root, values=faculty_names, textvariable=selected_faculty, state="readonly")
dropdown.place(relx=0.6, rely=0.35, anchor="w")
dropdown.bind("<<ComboboxSelected>>", get_selected_faculty)

# Label to display selected faculty
selected_faculty_label = tk.Label(root, text="", font=("Arial", 16))
selected_faculty_label.place(relx=0.5, rely=0.4, anchor="center")

# Date Label
data_label = tk.Label(root, text="Date : ", font=("Arial", 14))
data_label.place(relx=0.4, rely=0.45, anchor="e")
today = date.today().strftime("%d/%m/%Y")
data_value_label = tk.Label(root, text=today, font=("Arial", 16))
data_value_label.place(relx=0.6, rely=0.45, anchor="w")

# Take feedback button
feedback_button = tk.Button(root, text="Take Feedback", font=("Arial", 16), width=20, height=2,
                            command=run_main_feedback_program)
feedback_button.place(relx=0.5, rely=0.55, anchor="center")

# Submit button
submit_button = tk.Button(root, text="Submit", font=("Arial", 16), width=20, height=2, command=submit_feedback)
submit_button.place(relx=0.5, rely=0.65, anchor="center")

# Start the tkinter event loop
root.mainloop()