import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk
import winsound
from io import BytesIO
import urllib.request

NUM_NOTEPADS = 4  # Variable to control how many notepads spawn
IMAGE_WIDTH = 300  # Adjust this to change image width in pixels
IMAGE_HEIGHT = 300  # Adjust this to change image height in pixels

class BouncingNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("hi i am spongebob :D")
        
        # Load and display image from GitHub
        github_url = "https://raw.githubusercontent.com/gaers-svg/idk/main/spong.jpg"  # Replace with your raw GitHub URL
        try:
            with urllib.request.urlopen(github_url) as response:
                image_data = response.read()
            self.pil_image = Image.open(BytesIO(image_data)).convert('RGBA')
        except Exception as e:
            print(f"Could not load image from GitHub: {e}")
            # Fallback to local image
            self.pil_image = Image.open("C:\\Users\\Grays\\Downloads\\spong.jpg").convert('RGBA')
        self.pil_image = self.pil_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.pil_image)
        self.label = tk.Label(root, image=self.photo)
        self.label.pack()
        
        self.root.geometry(f"{self.pil_image.width}x{self.pil_image.height}")
        
        # Window position and velocity
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x = random.randint(0, screen_width - self.pil_image.width)
        self.y = random.randint(0, screen_height - self.pil_image.height)
        self.vx = random.randint(35, 35)
        self.vy = random.randint(35, 35)
        
        self.root.geometry(f"+{self.x}+{self.y}")
        self.bounce()
    
    def bounce(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = self.pil_image.width
        window_height = self.pil_image.height
        
        self.x += self.vx
        self.y += self.vy
        
        if self.x <= 0 or self.x + window_width >= screen_width:
            self.vx = -self.vx
        if self.y <= 0 or self.y + window_height >= screen_height:
            self.vy = -self.vy
        
        self.root.geometry(f"+{self.x}+{self.y}")
        self.root.after(4, self.bounce)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show message popup with username
    username = os.getenv('USERNAME')
    messagebox.showinfo("SPONGEBOB IS COMING FOR YOU", f"spong is coming for you, {username}.")
    
    # Play music from GitHub (after notification closes)
    try:
        music_url = "https://raw.githubusercontent.com/gaers-svg/idk/main/spongebob-krusty-krab-trap-remix-_LOUD_.wav"  # Raw GitHub URL
        music_file = "spong.wav"
        urllib.request.urlretrieve(music_url, music_file)
        winsound.PlaySound(music_file, winsound.SND_ASYNC)
    except Exception as e:
        print(f"Could not play music: {e}")
    
    apps = []  # Keep references to prevent garbage collection
    for i in range(NUM_NOTEPADS):
        if i == 0:
            # First window uses the main root
            window = root
            window.deiconify()  # Show the main window
        else:
            # Additional windows use Toplevel
            window = tk.Toplevel(root)
        
        app = BouncingNotepad(window)
        apps.append(app)  # Store reference to keep app alive
    
    tk.mainloop()