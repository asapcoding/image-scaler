import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from ttkthemes import ThemedTk
from datetime import datetime
from PIL import Image, ImageTk
import numpy as np
import math
import os
import cv2

class ImageScaler:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Scaler")
        self.master.iconbitmap("scaler.ico")
        self.master.geometry("1080x620")
        
        # Erstellen des Frames, in dem die Buttons und Eingabefelder angeordnet werden
        # flat, groove, raised, ridge, solid, or sunken
        self.main_frame = ttk.Frame(master, relief="raised")
        self.main_frame.place(relwidth = 1, relheight = 1)
        
        self.control_frame = ttk.Frame(self.main_frame, relief="raised")
        self.control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)

        self.loadsave_frame = ttk.Frame(self.control_frame)
        self.loadsave_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        
        self.control_frame0 = ttk.Frame(self.control_frame)
        self.control_frame0.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.control_frame1 = ttk.Frame(self.control_frame, relief="ridge")
        self.control_frame1.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.control_frame2 = ttk.Frame(self.control_frame)
        self.control_frame2.grid(row=3, column=0, padx=5, pady=5)
        
        self.image_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Dateiname
        self.file_label = ttk.Label(self.control_frame0, text="file:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.file_name = ttk.Label(self.control_frame0, text="")
        self.file_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Pixelmaße Originalbild
        self.px_label = ttk.Label(self.control_frame0, text="size[px]:")
        self.px_label.grid(row=1, column=0, padx=5, pady=5)

        self.px_name = ttk.Label(self.control_frame0, text="")
        self.px_name.grid(row=1, column=1, padx=5, pady=5)
        
        # Breiten-Eingabefeld
        self.width_label = ttk.Label(self.control_frame1, text="width:")
        self.width_label.grid(row=0, column=0, padx=5, pady=5)

        self.width_var = tk.StringVar(value="800")
        self.width_entry = ttk.Entry(self.control_frame1, textvariable=self.width_var)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)

        # Höhen-Eingabefeld
        self.height_label = ttk.Label(self.control_frame1, text="height:")
        self.height_label.grid(row=1, column=0, padx=5, pady=5)

        self.height_var = tk.StringVar(value="600")
        self.height_entry = ttk.Entry(self.control_frame1, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        # Seitenverhältnis-Label aspect ratio
        self.aspect_ratio_name = ttk.Label(self.control_frame1, text="aspect ratio:", width=10)
        self.aspect_ratio_name.grid(row=2, column=0, padx=5, pady=5)
        
        self.aspect_ratio_label = ttk.Label(self.control_frame1, text="4/3", width=10)
        self.aspect_ratio_label.grid(row=2, column=1, padx=5, pady=5)

        #Originalbild Skalierung
        self.spin_label = ttk.Label(self.control_frame1, text="image scaling:")
        self.spin_label.grid(row=3, column=0, padx=5, pady=5)
        
        self.spin_var = tk.StringVar(value="100")
        self.spin_entry = ttk.Spinbox(self.control_frame1, from_=1.0, to=200.0, textvariable=self.spin_var, command=self.redraw_image)
        self.spin_entry.grid(row=3, column=1, padx=5, pady=5)

        # Contrast scaling
        self.spin_contrast_label = ttk.Label(self.control_frame1, text="contrast:")
        self.spin_contrast_label.grid(row=4, column=0, padx=5, pady=5)

        self.spin_contrast_var = tk.StringVar(value="1")
        self.spin_contrast_entry = ttk.Spinbox(self.control_frame1, from_=0.0, to=127.0, increment=.1, textvariable=self.spin_contrast_var, command=self.redraw_image) #(0-127)
        self.spin_contrast_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # brightness scaling
        self.spin_brightness_label = ttk.Label(self.control_frame1, text="brightness:")
        self.spin_brightness_label.grid(row=5, column=0, padx=5, pady=5)

        self.spin_brightness_var = tk.StringVar(value="0")
        self.spin_brightness_entry = ttk.Spinbox(self.control_frame1, from_=0.0, to=100.0, increment=1, textvariable=self.spin_brightness_var, command=self.redraw_image) #(0-100)
        self.spin_brightness_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Color-Button
        self.change_background_color_button = ttk.Button(self.control_frame2, text="change background color", command=self.change_background_color)
        self.change_background_color_button.grid(row=0, column=0, padx=1, pady=5)
        
        # Load-Button
        self.load_button = ttk.Button(self.loadsave_frame, text="load image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Save-Button
        self.save_button = ttk.Button(self.loadsave_frame, text="save image", command=self.save_image)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        # Image Canvas
        self.canvas = tk.Canvas(self.image_frame, width=int(self.width_var.get()), height=int(self.height_var.get()), bg="white")
        self.canvas.pack(fill="both", expand=False)

        # Image Variable set none
        self.photo = None
        self.original_image = None
        self.file_path = None
        self.paste_x = None
        self.paste_y = None
        self.target_width = None
        self.target_height = None
        self.resized_image = None
  
    # CheckBox für Rahmen um das Orignalbild mit Strichstärke und Farbe des Rahmens
    
    
    # Load Image by dialog window
    def load_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Bilder", "*.jpg;*.jpeg;*.png;*.bmp")])
        self.file_path
        if self.file_path:
            self.original_image = Image.open(self.file_path)

            #get filename
            path = self.original_image.filename
            filename = path.split("/")[-1]
            self.file_name.config(text=filename)

            #get original image size
            image_shapes = self.original_image.size
            self.px_name.config(text=(str(image_shapes[0]) + " x " + str(image_shapes[1])))
            #self.master.geometry(str(image_shapes[0]) + "x" + str(image_shapes[1]))
            #call function
            self.redraw_image()
            

    # Save Image by dialog window
    def save_image(self):
        if hasattr(self, "image"):
            if self.file_path is None:
                file = datetime.now().strftime("%d-%m-%Y_%H-%M-%S_")
            else:
                file = os.path.splitext(self.file_path)[0]
            file = file + "_" + self.width_var.get() + "x" + self.height_var.get()
            file_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=file)
            if file_path:
                self.image.save(file_path)

    # if width in edit field change redraw the image            
    def on_width_change(self, *args):
        try:
            self.canvas.config(width=int(self.width_var.get()))
            self.redraw_image()
            self.on_size_change()
        except:
            pass

    # if height in edit field change redraw the image
    def on_height_change(self, *args):
        try:
            self.canvas.config(height=int(self.height_var.get()))
            self.redraw_image()
            self.on_size_change()
        except:
            pass

    # Calculate and output aspect ratio 
    def on_size_change(self):
        width = int(self.width_var.get())
        height = int(self.height_var.get())
        gcd = math.gcd(width, height)
        aspect_width = width // gcd
        aspect_height = height // gcd
        result = f"{aspect_width}/{aspect_height}"
        self.aspect_ratio_label.config(text=result)

    # when the color change
    def change_background_color(self):
        (triple, hexstr) = colorchooser.askcolor()
        self.canvas.configure(bg=hexstr)
        self.redraw_image()

    def change_contrast_brightness(self):
        # define the alpha and beta
        alpha = float(self.spin_contrast_var.get())  # 1.0 # Contrast control   (0-127)
        beta = float(self.spin_brightness_var.get()) #10   # Brightness control (0-100)

        cv2_img = np.array(self.resized_image)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        
        cv2_img = cv2.convertScaleAbs(cv2_img, alpha=alpha, beta=beta)

        top = int(0.002 * cv2_img.shape[0]) # shape[0] = rows
        bottom = top
        left = int(0.002 * cv2_img.shape[1]) # shape[1] = cols
        right = left
        
        borderType = cv2.BORDER_CONSTANT
        value = [1, 1, 1, 1]
        
        cv2_img = cv2.copyMakeBorder(cv2_img, top, bottom, left, right, borderType, None, value)

        
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        self.resized_image = Image.fromarray(cv2_img)
        
    # calculates image size via choosen GUI settings
    def get_new_image_size(self):

        if self.original_image is not None:
            image_width, image_height = self.original_image.size
        else:
            image_width, image_height = int(self.width_var.get()), int(self.height_var.get())
                
        self.target_width, self.target_height = int(self.width_var.get()), int(self.height_var.get())
                    
        target_ratio = self.target_width / self.target_height
        image_ratio = image_width / image_height

        if (image_width > self.target_width) or (image_height > self.target_height):
            if target_ratio > image_ratio:
                # Ziel-Verhältnis ist breiter als das Verhältnis des Originalbildes
                new_width = int(self.target_height * image_ratio)
                new_height = self.target_height
            else:
                # Ziel-Verhältnis ist schmaler als das Verhältnis des Originalbildes
                new_width = self.target_width
                new_height = int(self.target_width / image_ratio)
        else:
            new_height = image_height
            new_width = image_width

        new_height = int(float(new_height / 100)*float(self.spin_var.get()))
        new_width = int(float(new_width / 100)*float(self.spin_var.get())) 

        if self.original_image is not None:        
            self.resized_image = self.original_image.resize((new_width, new_height), resample=Image.LANCZOS)
                
        self.paste_x = int((self.target_width - new_width) / 2)
        self.paste_y = int((self.target_height - new_height) / 2)

    # Resizes the image while maintaining the aspect ratio of the original image
    def redraw_image(self):
        #try:
            # The hasattr() method returns true if an object has the given named attribute "original_image" and false if it does not.
            if hasattr(self, "original_image") and self.original_image is not None:

                # Determining the size via the GUI settings
                self.get_new_image_size()

                # Creates a new image instance // monochrome image
                self.image = Image.new("RGB", (self.target_width, self.target_height), color=self.canvas.cget("bg"))

                self.change_contrast_brightness()

                # Sets the scaled main image to the monochrome image
                self.image.paste(self.resized_image, (self.paste_x, self.paste_y))           
                
                # Creates a Tk Image photo from the adjusted image
                self.photo = ImageTk.PhotoImage(self.image)

                # Puts the photo on the GUI picture frame
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            else:

                # Creates a new image instance
                self.image = Image.new("RGB", (int(self.width_var.get()), int(self.height_var.get())), color=self.canvas.cget("bg"))

                # Creates a Tk Image photo from the, in this case, not adjusted image
                self.photo = ImageTk.PhotoImage(self.image)

                # Puts the photo on the GUI picture frame
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        #except:
            #pass

if __name__ == '__main__':
    # Erstellen des Hauptfensters und des ImageScaler-Objekts
    root = ThemedTk(theme="black")
    app = ImageScaler(master=root)

    # Binden der Funktionen on_width_change und on_height_change an Änderungen in den Eingabefeldern
    app.width_var.trace("w", app.on_width_change)
    app.height_var.trace("w", app.on_height_change)

    # Starten der Hauptloop des Fensters
    root.mainloop()
