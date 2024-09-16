import tkinter as tk
import qrcode, random
from PIL import ImageTk

# GUI for Command Generation
class CommandGeneratorGUI:
    def __init__(self, root, generator):
        self.root = root
        self.root.title("Command Generator")

        # Command Generators
        self.generator = generator

        # Create a frame to contain the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Create command options
        self.user_prompt_label = tk.Label(root, text="Select Command Option:")
        self.user_prompt_label.pack()

        # Arrange buttons side by side using grid
        self.btn_any_command = tk.Button(self.button_frame, text="Any Command", command=self.generate_any_command)
        self.btn_any_command.grid(row=0, column=0, padx=5, pady=5)

        # Display area for commands
        self.command_display = tk.Text(root, height=10, width=100)
        self.command_display.pack(pady=5)

        # Frame to hold QR codes
        self.qr_frame = tk.Frame(root)
        self.qr_frame.pack(pady=10)

        self.command = ""
        self.command_list = []


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

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((300, 300))  # Resize to fit the window

            # Convert the image to PhotoImage for displaying in Tkinter
            img_tk = ImageTk.PhotoImage(img)

            # Create a label to hold each QR code and display it in the grid
            qr_label = tk.Label(self.qr_frame, image=img_tk)
            qr_label.image = img_tk  # Keep a reference to avoid garbage collection
            qr_label.pack(side=tk.LEFT, padx=10)  # Align QR codes horizontally


