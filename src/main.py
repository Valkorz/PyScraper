import tkinter 
import customtkinter
from PIL import Image, ImageTk
import build
import scraper
import json
import os 

with open("config/webConfig.json") as f:
        sourceData = json.load(f)

root_window = tkinter.Tk()
root_window.geometry("720x720")
root_window.title("Price scraper")

label = customtkinter.CTkLabel(root_window, text="Price scraper", font=("arial bold", 42))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

label_2 = customtkinter.CTkLabel(root_window, text="Search term: ", font=("arial bold", 18))
label_2.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

textbox = tkinter.Entry(root_window, font=("arial", 16))
textbox.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

label_2 = customtkinter.CTkLabel(root_window, text="Blacklisted words: ", font=("arial bold", 18))
label_2.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

textbox_2 = tkinter.Entry(root_window, font=("arial", 16))
textbox_2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

textboxPath = tkinter.Entry(root_window, textvariable="file name", font=("arial", 16))
textboxPath.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

textBoxVal = customtkinter.CTkLabel(root_window, text=f"Query: {textbox.get()}", font=("arial bold", 28))
textBoxVal.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

label_avg = customtkinter.CTkLabel(root_window, text=f"Average price: R$ {0}", font=("arial bold", 28))
label_avg.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

label_target = customtkinter.CTkLabel(root_window, text=f"Source: {0}", font=("arial bold", 22))
label_target.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


def update():
    textBoxVal.configure(text=f"Query: {textbox.get()}")
    data = build.scrapeFrom(textbox.get(), False)
    listFiltered = build.avg(data, textbox.get(), separate(textbox_2.get()))
    label_avg.configure(text=f"Average price: R$ {sum(listFiltered) / len(listFiltered)}")
    label_target.configure(text=f"Source: {sourceData["Websites"]["MercadoLivre"]["Url"]}")
    build.toSheet(textboxPath.get(), listFiltered, textbox.get())
    
def view():
    os.startfile(f"data\\{textboxPath.get()}.xlsx")
    
def separate(text : str):
    terms = []
    characters = ""
    for i in range(len(text)):
        if text[i] == ',':
            terms.append(characters)
            characters = ""
        else:
            characters += text[i]
            
    return terms
    
button = customtkinter.CTkButton(master=root_window, corner_radius=10, 
                                  command=update, 
                                  text="Search")
button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

button2 = customtkinter.CTkButton(master=root_window, corner_radius=10, 
                                  command=view, 
                                  text="View history")
button2.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

root_window.mainloop()
