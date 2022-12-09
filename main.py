#!/usr/bin/env python3.10
import os
import time
import openai 
import tkinter
import requests
import threading
import customtkinter
import tkinter.filedialog
from PIL import Image, ImageTk


import config
openai.api_key = config.api_key # "your Secret API Key" must be here


def get_time_str():
    t = time.localtime()
    return f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}"


last_image = None
def get_openai_credits():
    return openai.C


#########################################
#                                       #
#    get an DALL-E image from prompt    #
#                                       #
#########################################
def get_image_openai(prompt, size_=1024):
    response = openai.Image.create(
        prompt = prompt,
        n = 1,
        size = f"{size_}x{size_}"
    )
    print(size_)
    print(response['data'][0]['url'])
    return Image.open(requests.get(response['data'][0]['url'], stream=True).raw)


########################
#                      #
#    generate image    #
#                      #
########################
def thread(prompt, canvas:customtkinter.CTkCanvas, button_gen:customtkinter.CTkButton, button_save:customtkinter.CTkButton, comboBox_res:customtkinter.CTkComboBox):
    def update_image():
        global last_image
        size = comboBox_res._variable.get()
        try:
            button_gen.configure(state="disabled")
            button_save.configure(state="disabled")
            comboBox_res.configure(state="disabled")
            image = get_image_openai(prompt, size)
            last_image = image.copy()
            image = ImageTk.PhotoImage(image.resize((512, 512)))
            canvas.image = image
            canvas.create_image(0, 0, anchor="nw", image=image)
            button_gen.configure(state="normal")
            button_save.configure(state="normal")
            comboBox_res.configure(state="normal")
        except Exception as e:
            print(e)
            button_gen.configure(state="normal")
            button_save.configure(state="normal")
            comboBox_res.configure(state="normal")
            popup = tkinter.Tk()
            popup.wm_title("!")
            label = tkinter.Label(popup, text=f"There is a problem with your prompt:\n{e}", font=("Verdana", 10))
            label.pack(side="top", fill="x", pady=10)
            B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
            B1.pack()
            popup.mainloop()
    threading.Thread(target=update_image).start()


##############################
#                            #
#    save generated image    #
#                            #
##############################
def save():
    global last_image
    if last_image is not None:
        #open save file dialog
        filename = tkinter.filedialog.asksaveasfilename(initialfile = f"{get_time_str()}.png", initialdir = os.path.expanduser("~/Desktop"), title = "Select file", filetypes = (("png files","*.png"),("all files","*.*")))
        if filename is not None:
            last_image.save(filename)
            return
    popup = tkinter.Tk()
    popup.wm_title("!")
    label = tkinter.Label(popup, text="An error occurred while saving the image!", font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


#####################
#                   #
#    create gui     #
#                   #
#####################
def main():
    #creating a winwdow
    window = customtkinter.CTk()
    window.title("DALL-E 2 image")
    window.geometry("900x540")
    window.resizable(False, False)
    #theme
    fontStyle = tkinter.font.NORMAL
    #creating gui elements
    variable = customtkinter.IntVar(window) 
    variable.set(1024)
    comboBoxResolution = customtkinter.CTkOptionMenu(master=window, hover=True, variable=variable, width=350, height=50, font=(fontStyle, 18), values=["256","512","1024"])
    imageCanvas = customtkinter.CTkCanvas(master=window, width = 510, height = 510, background="Black")
    # labelPrompt = customtkinter.CTkLabel(master=window, text="Enter your prompt here:", font=(fontStyle, 18))
    # textBoxPrompt = customtkinter.CTkTextbox(master=window, width=350, height=200, font=(fontStyle, 16), wrap="word")
    entryPrompt = customtkinter.CTkEntry(master=window, width=880, height=50, font=(fontStyle, 16), placeholder_text="Enter your prompt here")
    buttonSaveImage= customtkinter.CTkButton(master=window, text = "Save Image", width=350, height=50, font=(fontStyle, 18), command = save)
    buttonGenerateImage = customtkinter.CTkButton(master=window, text = "Generate Image", width=350, height=50, font=(fontStyle, 18), 
            command = lambda: thread(entryPrompt.get(), imageCanvas, buttonGenerateImage, buttonSaveImage, comboBoxResolution))
    #packing gui elements
    entryPrompt.pack(anchor="w", side = "top", pady=10, padx = 10)
    imageCanvas.pack(side="left", pady=10, padx = 10)
    # labelPrompt.pack(anchor="w", side = "top", pady=10, padx = 0)
    # textBoxPrompt.pack(anchor="w", side = "top", pady=10, padx = 0)
    comboBoxResolution.pack(anchor="w", side = "top", pady=10, padx = 0)
    buttonGenerateImage.pack(anchor="w", side = "top", pady=10, padx = 0)
    buttonSaveImage.pack(anchor="w", side = "top", pady=10, padx = 0)
    window.mainloop()


##################
#                #
#    app init    #
#                #
##################
if __name__ == "__main__":
    main()
