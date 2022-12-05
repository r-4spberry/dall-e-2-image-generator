import openai 
import tkinter
import tkinter.filedialog
import requests
from PIL import Image, ImageTk
import threading
import config

openai.api_key = config.api_key

last_image = None
def get_openai_credits():
    return openai.C
# get an DALL-E image from prompt
def get_image_openai(prompt, size=1024):
    response = openai.Image.create(
        prompt = prompt,
        size = f"{size}x{size}"
    )
    print(response['data'][0]['url'])
    image  = Image.open(requests.get(response['data'][0]['url'], stream=True).raw)
    return image

def thread(prompt, canvas:tkinter.Canvas, button, save_button, size=256):
    def update_image():
        global last_image
        try:
            button.config(state="disabled")
            save_button.config(state="disabled")
            image = get_image_openai(prompt, size).resize((512, 512))
            last_image = image.copy()
            image = ImageTk.PhotoImage(image)
            canvas.image = image
            canvas.create_image(0, 0, anchor="nw", image=image)
            button.config(state="normal")
            save_button.config(state="normal")
        except Exception as e:
            print(e)
            button.config(state="normal")
            save_button.config(state="normal")
            popup = tkinter.Tk()
            popup.wm_title("!")
            label = tkinter.Label(popup, text=f"Some problem with your prompt:\n{e}", font=("Verdana", 10))
            label.pack(side="top", fill="x", pady=10)
            B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
            B1.pack()
            popup.mainloop()
    
    threading.Thread(target=update_image).start()

def save():
    global last_image
    if last_image is not None:
        #open a save file dialog
        filename = tkinter.filedialog.asksaveasfilename(initialdir = "/", title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        if filename is not None:
            last_image.save(filename)
            return
    popup = tkinter.Tk()
    popup.wm_title("!")
    label = tkinter.Label(popup, text="Error when saving the image.", font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
        
def main():
    #create a tkinter window.
    window = tkinter.Tk()
    #set the title.
    window.title("DALL-E")
    #set the size.
    window.geometry("1024x600")
    #set the background color.
    window.config(background = "white")
    #create a tkinter canvas to draw on
    canvas = tkinter.Canvas(window, width = 512, height = 512)
    #pack the canvas into a frame/form
    canvas.pack(side="left", padx=64, pady=64)
    prompt_field = tkinter.Text(window, width=40, height=3, wrap = "word")
    prompt_field.pack(anchor="w", side = "top", pady=64)
    #save button
    save_button = tkinter.Button(window, text = "Save Image",
                            command = save,
                            width=37)
    #create a button
    button = tkinter.Button(window, text = "Generate Image",
                            command = lambda: thread(prompt_field.get("1.0", "end-1c"), canvas, button, save_button),
                            width=37)
    #pack the button into the window
    button.pack(anchor="w", side = "top", pady=3)
    #pack the button into the window
    save_button.pack(anchor="w", side = "top", pady=3)
    #start the window's main loop
    window.mainloop()
if __name__ == "__main__":
    main()