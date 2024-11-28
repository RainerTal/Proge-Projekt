import tkinter
from tkinter import Tk, PhotoImage, Label, filedialog
from tkinter import ttk
import os

def faili_asukoht(fail):
    faili_asukoht = os.path.dirname(fail)
    return faili_asukoht

def avafail():
    return filedialog.askopenfilename(title="Vali CSV fail", 
                                        filetypes=[("CSV files", "*.csv"), 
                                                    ("All files", "*.*")])

root = Tk()

root.title("Finantside Jälgija")
root.configure(background="black")
root.eval('tk::PlaceWindow . center')
root.minsize(600,350)
root.resizable(False, False)

canvas = tkinter.Canvas(root, width=600, height=350, highlightthickness=0)
canvas.grid(column=1, row=1, padx=0, pady=0)

taust = PhotoImage(file="dimtaust.png")
canvas.create_image(0, 0, anchor="nw", image=taust)

canvas.create_text(90, 100, text="Sisesta oma panga (SEB, Revolut) kontoväljavõtte fail", 
                   font=("Helvetica", 12, "bold"), fill="white", anchor="nw")

# Create a button on the canvas
button_x1, button_y1 = 250, 150  # Top-left corner
button_x2, button_y2 = 350, 180  # Bottom-right corner
button = canvas.create_rectangle(button_x1, button_y1, button_x2, button_y2, fill="cyan", outline="white")

# Create text for the button
canvas.create_text((button_x1 + button_x2) / 2, (button_y1 + button_y2) / 2, text="Ava fail", 
                   font=("Helvetica", 14), fill="black")

# Function to handle button click
def on_button_click(event):
    faili_asukoht(avafail())

# Bind mouse click event to the button
canvas.tag_bind(button, "<Button-1>", on_button_click)

root.mainloop()