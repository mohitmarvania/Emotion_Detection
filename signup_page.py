from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyDaJgPhHB7Js_TZbSdQj2Ryc7u_7zZZtHU",
    'authDomain': "emotiondetection-ae64e.firebaseapp.com",
    'projectId': "emotiondetection-ae64e",
    'databaseURL': "https://emotiondetection-ae64e-default-rtdb.firebaseio.com",
    'storageBucket': "emotiondetection-ae64e.appspot.com",
    'messagingSenderId': "698314744650",
    'appId': "1:698314744650:web:1491fc313462e36c2a17b3",
    'measurementId': "G-1XB1D32RE8"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()


def go_to_main_gui():
    signup_window.destroy()
    import main_gui


def signup_task():
    usernameData = username.get()
    emailData = Email_signup.get()
    semesterData = semesters_var.get()
    passwordData = password_signup.get()

    try:
        user = auth.create_user_with_email_and_password(emailData, passwordData)
        # Store user data in the Realtime Database
        user_data = {
            'username': usernameData,
            'email': emailData,
            'semester': semesterData
        }
        # Use the user's unique ID as the key
        database.child('users').child(user['localId']).set(user_data)

        # USER IS CREATED AND DATA IS STORED IN THE FIREBASE REALTIME DATABASE.
        # Call the main GUI function
        go_to_main_gui()

        messagebox.showinfo("Sign up", "User created successfully!!")
    except Exception as e:
        error_message = str(e)
        print(error_message)
        messagebox.showerror("Sign up", "Unable to create user!")
    return


def go_to_login_page():
    signup_window.destroy()
    import login_page


signup_window = Tk()
signup_window.title("Sign Up")
signup_window.configure(bg="#fff")
signup_window.geometry("925x500+300+200")
signup_window.resizable(False, False)

img_signup = PhotoImage(file='/Users/mohit/PycharmProjects/login_signup_gui/cspit.png')
img1_signup = PhotoImage(file='/Users/mohit/PycharmProjects/login_signup_gui/login.png')
Label(signup_window, image=img_signup, bg="white").place(x=820, y=-2)
Label(signup_window, image=img1_signup, bg="white").place(x=500, y=50)

frame_signup = Frame(signup_window, width=350, height=350, bg="white")
frame_signup.place(x=60, y=70)

heading_signup = Label(signup_window, text="Sign Up", fg="#57a1f8", bg="white",
                       font=("Microsoft YaHei UI Light", 23,
                             "bold"))
heading_signup.place(x=170, y=50)


# FUNCTION WHICH HANDLES THE SIGNUP DETAILS.
def signedUp():
    usernameData = username.get()
    emailData = Email_signup.get()
    semesterData = semesters_var.get()
    passwordData = password_signup.get()
    repasswordData = repassword_signup.get()

    if '@' in emailData or 'charusat' in emailData:
        print("Email is correct at signup!")
    else:
        messagebox.showerror("Sign up", "Email is not correct!")
        return

    if passwordData == repasswordData:
        print("Password matched at signup!")
    else:
        messagebox.showerror("Sign up", "Password didn't matched!")
        return

    if usernameData == "":
        messagebox.showerror("Sign up", "Please enter valid username!")
        return

    if semesterData == "":
        messagebox.showerror("Sign up", "Please select valid semester!")
        return

    signup_task()


##---------------------------------------------------------------------------------------------------
def on_enter_username(e):
    username.delete(0, 'end')


def on_leave_username(e):
    usernameInput = username.get()
    if usernameInput == "" or len(usernameInput) > 30:
        username.insert(0, "Username")


username = Entry(signup_window, width=36, fg='black', border=0, bg="white", font=("Microsoft YaHei UI Light", 12),
                 highlightthickness=0, highlightbackground="white", insertbackground="black")
username.place(x=80, y=120)
username.insert(0, "Username")
username.bind('<FocusIn>', on_enter_username)
username.bind('<FocusOut>', on_leave_username)
Frame(frame_signup, width=295, height=2, bg='black').place(x=16, y=75)


##---------------------------------------------------------------------------------------------------
def on_enter_email_signup(e):
    Email_signup.delete(0, 'end')


def on_leave_email_signup(e):
    Email_signup_input = Email_signup.get()
    if Email_signup_input == "":
        Email_signup.insert(0, 'Email')


Email_signup = Entry(signup_window, width=36, fg='black', border=0, bg="white",
                     font=("Microsoft YaHei UI Light", 12),
                     highlightthickness=0, highlightbackground="white", insertbackground="black")
Email_signup.place(x=80, y=170)
Email_signup.insert(0, "Email")
Email_signup.bind('<FocusIn>', on_enter_email_signup)
Email_signup.bind('<FocusOut>', on_leave_email_signup)
Frame(frame_signup, width=295, height=2, bg='black').place(x=16, y=125)

##---------------------------------------------------------------------------------------------------
Label(signup_window, text="Current semester :", fg='black', bg='white').place(x=75, y=218)
semesters = ["Sem - " + str(i) for i in range(1, 8)]  # List of semester options

semesters_var = StringVar(signup_window)
semesters_var.set(semesters[0])  # Set the default semester

# Dropdown menu for semesters
semester_dropdown = OptionMenu(signup_window, semesters_var, *semesters)
semester_dropdown.configure(bg="#fff", fg="black", bd=2, highlightthickness=1, highlightcolor="black")
semester_dropdown.place(x=208, y=218)


def on_semester_select(event):
    print(f"Selected Semester: {semesters_var.get()}")


semester_dropdown.bind("<Button-1>", on_semester_select)


##---------------------------------------------------------------------------------------------------
def on_enter_password_signup(e):
    password_signup.delete(0, 'end')
    password_signup.config(show='*')  # Set show option to '*' for password entry
    # --------------- CONVERT THE ENTERED PASSWORD INTO HASH CODE HERE AND CAPUTRE THE HASH CODE AND SALT -------


def on_leave_password_signup(e):
    password_signup_input = password_signup.get()
    if password_signup_input == "":
        password_signup.insert(0, "New password")
        password_signup.config(show='')


password_signup = Entry(signup_window, width=36, fg="black", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 12),
                        highlightthickness=0, highlightbackground="white", insertbackground="black")
password_signup.place(x=80, y=265)
password_signup.insert(0, "New password")
password_signup.bind('<FocusIn>', on_enter_password_signup)
password_signup.bind('<FocusOut>', on_leave_password_signup)
Frame(frame_signup, width=295, height=2, bg='black').place(x=16, y=220)


##---------------------------------------------------------------------------------------------------
def on_enter_repassword_signup(e):
    repassword_signup.delete(0, 'end')
    repassword_signup.config(show='*')


def on_leave_repassword_signup(e):
    repassword_signup_input = repassword_signup.get()
    if repassword_signup_input == "":
        repassword_signup.insert(0, "Re-enter password")
        repassword_signup.config(show='')


repassword_signup = Entry(signup_window, width=36, fg="black", border=0, bg="white",
                          font=("Microsoft YaHei UI Light", 12),
                          highlightthickness=0, highlightbackground="white", insertbackground="black")
repassword_signup.place(x=80, y=315)
repassword_signup.insert(0, "Re-enter password")
repassword_signup.bind('<FocusIn>', on_enter_repassword_signup)
repassword_signup.bind('<FocusOut>', on_leave_repassword_signup)
Frame(frame_signup, width=295, height=2, bg="black").place(x=16, y=270)

##---------------------------------------------------------------------------------------------------
# color code of blue = #57a1f8
signup_button = Button(signup_window, width="24", pady="7", text="Sign Up",
                       font=("Microsoft YaHei UI Light", 16, "bold"), command=signedUp)
signup_button.configure(fg="#57a1f8", bg="white", bd=0, highlightthickness=0,  highlightbackground="white")
signup_button.place(x=75, y=360)

label = Label(signup_window, text="Already have an account ?", fg='black', bg='white',
              font=("Microsoft YaHei UI Light", 12))
label.place(x=110, y=410)

login_btn = Button(signup_window, width=4, text="Login", cursor='hand',
                   font=("Microsoft YaHei UI Light", 12), fg='#57a1f8', command=go_to_login_page)
login_btn.configure(bg="white", fg="#57a1f8", bd=0, highlightthickness=0,  highlightbackground="white")
login_btn.place(x=270, y=410)

signup_window.mainloop()
