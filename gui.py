import tkinter as tk
import qrcode
from PIL import Image, ImageTk
from utils.utils import *

# GUI for Command Generation
class CommandGeneratorGUI:
    def __init__(self, root, generator, league):
        # Variables
        # Load parameters from YAML
        self.config_file = "./params/frontend/params.yaml"
        self.load_config(self.config_file)

        # Get title
        try:
            self.title = self.league_names[league]
        except:
            print("Could not get league name in GUI!")
            exit(1)

        self.root = root
        self.root.title(self.window_title)

        # Maximize the window on launch
        try:
            # For Windows and Linux
            self.root.state('zoomed')
        except:
            # For macOS, manually set the window size to the screen resolution
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        # Set the background color of the GUI
        self.root.configure(bg=self.primary_base)

        # Command Generators
        self.generator = generator

        # Add titles at the top-left corner
        self.load_titles()

        # Create a frame to contain the buttons
        self.button_frame = tk.Frame(root, bg=self.primary_base)
        self.button_frame.pack(pady=10)

        # Create command options
        self.user_prompt_label = tk.Label(root, text=self.label_txt, bg=self.primary_base, fg='white')
        self.user_prompt_label.pack()

        # Arrange buttons side by side using grid
        self.btn_any_command = tk.Button(self.button_frame, text=self.button_title, command=self.generate_any_command,
                                         bg=self.secondary_base, fg=self.primary_base, activebackground='#005e33')
        self.btn_any_command.grid(row=0, column=0, padx=5, pady=5)

        # Display area for commands
        self.command_display = tk.Text(root, height=10, width=100, bg='white', fg=self.primary_base)
        self.command_display.pack(pady=5)

        # Frame to hold QR codes
        self.qr_frame = tk.Frame(root, bg=self.primary_base)
        self.qr_frame.pack(pady=10)

        # Add image at the bottom-left corner
        self.load_image()

        self.command = ""
        self.command_list = []

    
    def load_config(self, config_file):
        # Load configuration from the YAML file
        config = read_yaml_file(config_file)
        
        # Assign variables from YAML file
        self.window_title = config['window_title']
        self.image_path = config['image_path']
        self.title_font_size = config['title_font_size']
        self.subtitle = config['subtitle']
        self.subtitle_font_size = config['subtitle_font_size']
        self.font_type = config['font_type']
        self.primary_base = config['primary_base']
        self.secondary_base = config['secondary_base']
        self.button_title = config['button_title']
        self.label_txt = config['label_txt']
        self.qrcode_fill_color = config['qrcode_fill_color']
        self.qrcode_back_color = config['qrcode_back_color']
        self.league_names = config['league_names']


    def load_titles(self):
        # Add the larger "Service Robots League" title at the top-left
        title_label = tk.Label(self.root, text=self.title, 
                               font=(self.font_type, self.title_font_size, "bold"), 
                               bg=self.primary_base, fg='white')
        title_label.pack(anchor="nw", padx=10, pady=10)  # Align to top-left with padding

        # Add the smaller "Nancy euRobin Coopetition" subtitle below the main title
        subtitle_label = tk.Label(self.root, text=self.subtitle, 
                                  font=(self.font_type, self.subtitle_font_size), 
                                  bg=self.primary_base, fg='white')
        subtitle_label.pack(anchor="nw", padx=10)  # Align below the main title

    def load_image(self):
        # Load the image (replace 'your_image.png' with the path to your image)
        image_path = self.image_path
        img = Image.open(image_path).convert("RGBA")  # Ensure image is RGBA for transparency

        # Get the original dimensions
        original_width, original_height = img.size

        # Define the maximum width and height while maintaining the aspect ratio
        max_size = 200  # Max width or height

        # Calculate the scaling factor to keep the aspect ratio
        if original_width > original_height:
            new_width = max_size
            new_height = int((max_size / original_width) * original_height)
        else:
            new_height = max_size
            new_width = int((max_size / original_height) * original_width)

        # Resize the image with the new dimensions
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Create a background image (solid color) to replace transparency
        background = Image.new("RGBA", img.size, self.primary_base)

        # Paste the original image onto the background
        background.paste(img, (0, 0), img)

        # Convert to a format Tkinter can display
        img_tk = ImageTk.PhotoImage(background.convert("RGB"))

        # Create a label to display the image in the bottom-left corner
        self.image_label = tk.Label(self.root, image=img_tk, bg=self.primary_base)  # Set label background
        self.image_label.image = img_tk  # Keep a reference to avoid garbage collection
        self.image_label.pack(side="left", anchor="sw", padx=10, pady=10)  # Anchor to bottom-left corner

    def display_command(self, command):
        self.command_display.delete(1.0, tk.END)
        self.command_display.insert(tk.END, command)

        # Automatically generate and display a single QR code
        self.generate_qr_code([command])

    def generate_any_command(self):
        self.command = self.generator.generate_command_start(cmd_category="")
        self.command = self.command[0].upper() + self.command[1:]
        self.display_command(self.command)

    def generate_qr_code(self, command_list):
        # Clear the previous QR codes
        for widget in self.qr_frame.winfo_children():
            widget.destroy()

        # Generate and display QR code for each command in the list
        for command_text in command_list:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
            qr.add_data(command_text)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.qrcode_fill_color, back_color=self.qrcode_back_color)
            img = img.resize((300, 300))  # Resize to fit the window

            # Convert the image to PhotoImage for displaying in Tkinter
            img_tk = ImageTk.PhotoImage(img)

            # Create a label to hold each QR code and display it in the grid
            qr_label = tk.Label(self.qr_frame, image=img_tk, bg=self.primary_base)
            qr_label.image = img_tk  # Keep a reference to avoid garbage collection
            qr_label.pack(side=tk.LEFT, padx=10)  # Align QR codes horizontally
