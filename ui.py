from tkinter import *

root = Tk()
root.title("Finantside Jälgija")
root.configure(background="grey")
root.eval('tk::PlaceWindow . center')
root.minsize(300,200)
root.resizable(False, False)

text = Label(root, text="Sisesta oma panga (SEB, Revolut) kontoväljavõtte fail.")
text.configure(background="grey")

text.pack()

root.mainloop()