from tkinter import *
from tkinter import filedialog
import smtplib
from email.message import EmailMessage

#Global Variables
attachments = []

#Main Screen
master = Tk()
master.title("Email App")

#Functions
def attachFile():
    filename = filedialog.askopenfilename(initialdir="C:/", title="Select a File")
    attachments.append(filename)
    notif.config(text="Attached" + str(len(attachments)) + " files.")
def send():
    try:
        msg = EmailMessage()
        email = temp_email.get()
        password = temp_password.get()
        recvEmail = temp_recvEmail.get()
        subject = temp_Subject.get()
        body = temp_Body.get()
        msg["subject"] = subject
        msg["from"] = email
        msg["to"] = recvEmail
        msg.set_content(body)

        filename = attachments[0]
        filetype = filename.split(".")
        filetype = filetype[1]
        print(filetype)
        if filetype == "jpg" or filetype == "JPG" or filetype == "png" or filetype == "PNG":
            import imghdr
            with open(filename, "rb") as f:
                file_data = f.read()
                image_type = imghdr.what(filename)
            msg.add_attachment(file_data, maintype="image", subtype=image_type, filename=f.name)

        else:
            with open(filename, "rb") as f:
                file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=f.name)


        if(email == "" or password == "" or recvEmail == "" or subject == "" or body == ""):
            notif.config(text="All fields required", fg="red")
            return
        else: 
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            notif.config(text="Email has been sent.", fg="green")

    except Exception as e:
        notif.config(text="Error sending email", fg="red")
        print(e)

def reset():
    emailEntry.delete(0, "end")
    passwordEntry.delete(0, "end")
    recvEmailEntry.delete(0, "end")
    subjectEntry.delete(0, "end")
    bodyEntry.delete(0, "end")

#Graphics
Label(master, text="Custom Email App", font=("Calibri", 15)).grid(row=0, sticky=N)
Label(master, text="Use the form below to send an email", font=("Calibri", 11)).grid(row=1, sticky=W, padx=5)

Label(master, text="Email:", font=("Calibri", 11)).grid(row=2, sticky=W, padx=5)
Label(master, text="Password:", font=("Calibri", 11)).grid(row=3, sticky=W, padx=5)
Label(master, text="Receiver's Email: ", font=("Calibri", 11)).grid(row=4, sticky=W, padx=5)
Label(master, text="Subject: ", font=("Calibri", 11)).grid(row=5, sticky=W, padx=5)
Label(master, text="Body: ", font=("Calibri", 11)).grid(row=6, sticky=W, padx=5)
notif = Label(master, text="", font=("Calibri", 11))
notif.grid(row=8, sticky=W, padx=5)

#Storage
temp_email = StringVar()
temp_password = StringVar()
temp_recvEmail = StringVar()
temp_Subject = StringVar()
temp_Body = StringVar()

#Entries
emailEntry = Entry(master, textvariable=temp_email)
emailEntry.grid(row=2, column=0)
passwordEntry = Entry(master, show="*", textvariable=temp_password)
passwordEntry.grid(row=3, column=0)
recvEmailEntry = Entry(master, textvariable=temp_recvEmail)
recvEmailEntry.grid(row=4, column=0)
subjectEntry = Entry(master, textvariable=temp_Subject)
subjectEntry.grid(row=5, column=0)
bodyEntry = Entry(master, textvariable=temp_Body)
bodyEntry.grid(row=6, column=0)

#Buttons
Button(master, text="Send", command=send).grid(row=7, sticky=W, pady=15, padx=5)
Button(master, text="Reset", command=reset).grid(row=7, sticky=W, pady=45, padx=45)
Button(master, text="Attachments", command=attachFile).grid(row=7, sticky=W, pady=90, padx=90)


master.mainloop()