from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import *
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


def go_to_main_gui():
    root.destroy()
    import main_gui


def login_task():
    emailData = Email.get()
    passwordData = code.get()

    try:
        Login = auth.sign_in_with_email_and_password(emailData, passwordData)
        # USER HAS SUCCESSFULLY LOGGED IN.
        # Call the main gui here.
        go_to_main_gui()
        messagebox.showinfo("Login", "Login successfully!")
    except Exception as e:
        error_message = str(e)
        print(error_message)
        messagebox.showerror("Login", "Invalid email or password!!")
    return


def go_to_signup_page():
    root.destroy()
    import signup_page


# FUNCTION WHICH HANDLES THE LOGIN DETAILS.
def login():
    emailId = Email.get()
    password = code.get()

    if '@' in emailId and 'charusat' in emailId:
        print("Email is correct!")
    else:
        messagebox.showerror("Login", "Email is not correct!\n Please enter charusat email")
        return

    if password == "":
        messagebox.showerror("Login", "Please enter valid password!")
        return

    login_task()


root = Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(bg="#fff")
root.resizable(False, False)
img = PhotoImage(file='cspit.png')
img1 = PhotoImage(file='login.png')
Label(root, image=img, bg="white").place(x=820, y=-2)
Label(root, image=img1, bg="white").place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text="Login", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=150, y=5)


##---------------------------------------------------------------------------------------------------
def on_enter(e):
    Email.delete(0, 'end')


def on_leave(e):
    emailInput = Email.get()
    if emailInput == "":
        Email.insert(0, 'Email')


Email = Entry(frame, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 12),
              highlightthickness=0, highlightbackground="white", insertbackground="black")
Email.place(x=30, y=80)
Email.insert(0, 'Email')
Email.bind('<FocusIn>', on_enter)
Email.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


##---------------------------------------------------------------------------------------------------
def on_enter(e):
    code.delete(0, 'end')
    code.config(show='*')  # Set show option to '*' for password entry


def on_leave(e):
    passwordInput = code.get()
    if passwordInput == "":
        code.insert(0, 'Password')
        code.config(show='')  # Set show option to '' for regular entry


code = Entry(frame, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 12),
             highlightthickness=0, highlightbackground="white", insertbackground="black")
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

##---------------------------------------------------------------------------------------------------
login_button = Button(frame, width="24", pady="7", text="Login", fg="white", bg='red', bd=0,
                      font=("Microsoft YaHei UI Light", 16,
                            "bold"), command=login)
login_button.configure(fg="#57a1f8", bg="white", bd=0, highlightthickness=0,  highlightbackground="white")
login_button.place(x=25, y=204)

label = Label(frame, text="Don't have an account ?", fg='black', bg='white', font=("Microsoft YaHei UI Light", 12))
label.place(x=75, y=270)

sign_up = Button(frame, width=4, text="Sign Up", bg='white', cursor='hand',
                 font=("Microsoft YaHei UI Light", 12), fg='white', command=go_to_signup_page)
sign_up.configure(bg="white", fg="#57a1f8", bd=0, highlightthickness=0,  highlightbackground="white")
sign_up.place(x=218, y=270)

root.mainloop()
