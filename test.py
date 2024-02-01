import tkinter as tk

def button_clicked():
    button.config(image=clicked_image)

root = tk.Tk()

default_image = tk.PhotoImage(file="default_image.png")
clicked_image = tk.PhotoImage(file="clicked_image.png")

button = tk.Button(root, image=default_image, command=button_clicked)
button.pack()

root.mainloop()
