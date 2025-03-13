#import necessary libraries
import sqlite3
import tkinter as tk
import sys
import logging

#Even though you import tkinter, ttk is a separate submodule that won’t be accessible unless you import it explicitly like from tkinter import ttk.
from tkinter import ttk #is this not already included in tkinter?

#If you do import datetime, you’d have to write datetime.datetime.now() every time. By doing from datetime import datetime, you can just call datetime.now(), which is cleaner.
from datetime import datetime

#save entry
def save_entry():

    conn = sqlite3.connect('gratitude-journal.db')
    cur = conn.cursor()

    #Retrieves text from the text box starting from line 1, character 0 to the end.    
    #It is a constant, the literal string "end". In this context it represents the point immediately after the last character entered by the user. The function get on a text widget requires two values: a starting position and an ending position.
    entry = text_box.get("1.0", tk.END).strip() #Remove spaces at the beginning and at the end of the string

    if entry:
        now = datetime.now()
        date_val = now.strftime('%Y-%m-%d')  # Formats as 'YYYY-MM-DD'
        time_val = now.strftime('%H:%M:%S')

        cur.execute("INSERT INTO entries (date, time, entry) VALUES (?, ?, ?)",
                    (date_val, time_val, entry))
        
            # Load existing entries
        cur.execute("SELECT * FROM entries")
        rows = cur.fetchall()

        for row in rows:
            with open("gratitude.txt","a") as f:
                rowstr = " ".join(str(row))
                f.write(rowstr)

        load_entries()
        conn.commit()
        conn.close()

#load entries
def load_entries():
    #Opens gratitude.txt in read mode ("r") and stores its contents in journal_text. If the file doesn’t exist yet, it sets "no entries yet!".
    try:
        with open("gratitude.txt","r") as f:
            journal_text.set(f.read())
        logging.info("entries loaded")
    except FileNotFoundError:
        logging.error("no entries while displaying")
        journal_text.set("no entries yet!")

#delete all entries
def del_all_entries():
    try:
        open("gratitude.txt","w").close()
        load_entries()
        logging.info("delete all entries by writing to file")
    except FileNotFoundError:
        journal_text.set("no entries yet!")
        logging.error("no entries while trying to delete all")



# create log file to track info, errors, etc
logging.basicConfig(level=logging.DEBUG, filename="mini-journal.log", filemode="w")

try:   
    # connect to sqlite db
    conn = sqlite3.connect('gratitude-journal.db')
    # create cursor object from cursor class
    cur = conn.cursor()
    # check if entries table exists, if not create it
    cur.execute('''CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date TEXT, 
                time TEXT, 
                entry TEXT
                )
                ''')
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(res.fetchall())
    res2 = cur.execute("PRAGMA table_info(entries);")
    print(res2.fetchall())
except Exception as e:
    logging.error(f"something went wrong, error: {e}")
    print(f"something went wrong, error:{e}")


#create main window
root = tk.Tk()
root.title("⋆˚࿔ mini gratitude journal ⋆˚࿔")
root.geometry("420x420")
root.configure(bg="#fcebf3")

#custom styling
font_style = ("Arial",12)
button_style = {"font":("Arial",11), "fg": "white", "padx": 10, "pady": 5}

# Create widgets with styles
label = tk.Label(root, text="What are you grateful for today? 😊", font=font_style, bg="#fefae0", fg="#283618")
label.pack(pady=10)

text_box = tk.Text(root, height=5, width=50, font=("Arial", 10), bg="#faedcd", fg="#283618")
text_box.pack(pady=5)

save_button = tk.Button(root, text="Save Entry", command=save_entry, bg="#6a994e", **button_style)
save_button.pack(pady=5)

del_all_button = tk.Button(root, text="Delete All", command=del_all_entries, bg="#b51d22", **button_style)
del_all_button.pack(pady=5)

journal_text = tk.StringVar()
journal_label = tk.Label(root, textvariable=journal_text, wraplength=400, justify="left", font=("Arial", 10), bg="#fefae0", fg="#606c38")
journal_label.pack(pady=10)

# Load existing entries
cur.execute("SELECT date, time, entry FROM entries")
rows = cur.fetchall()

for row in rows:
    with open("gratitude.txt","a") as f:
        rowstr = " ".join(str(row))
        f.write(rowstr)
        load_entries()



# Run the app
root.mainloop()

# commit and close connection
conn.commit()
conn.close()

