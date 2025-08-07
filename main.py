import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = None
        self.watermark_path = None
        self.original_image = None
        self.displayed_image = None
        self.watermarked_image = None
        self.watermark_text = tk.StringVar(value="Your Watermark Text")
        self.watermark_type = tk.StringVar(value="text")
        self.watermark_position = tk.StringVar(value="bottom-right")
        self.watermark_opacity = tk.IntVar(value=50)
        self.watermark_size = tk.IntVar(value=30)
        self.watermark_color = "#ffffff"  # Default white
        
        # Create UI Elements
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = ttk.LabelFrame(main_frame, text="Controls")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Image upload button
        ttk.Button(left_panel, text="Upload Image", command=self.upload_image).pack(fill=tk.X, padx=5, pady=5)
        
        # Watermark type selection
        watermark_type_frame = ttk.LabelFrame(left_panel, text="Watermark Type")
        watermark_type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(watermark_type_frame, text="Text", variable=self.watermark_type, value="text", 
                       command=self.update_watermark_options).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(watermark_type_frame, text="Logo/Image", variable=self.watermark_type, value="image", 
                       command=self.update_watermark_options).pack(anchor=tk.W, padx=5, pady=2)
        
        # Text watermark options
        self.text_options_frame = ttk.LabelFrame(left_panel, text="Text Watermark Options")
        self.text_options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.text_options_frame, text="Watermark Text:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Entry(self.text_options_frame, textvariable=self.watermark_text).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(self.text_options_frame, text="Text Size:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Scale(self.text_options_frame, from_=10, to=100, variable=self.watermark_size, 
                 orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(self.text_options_frame, text="Select Text Color", command=self.choose_color).pack(fill=tk.X, padx=5, pady=5)
        
        # Image watermark options
        self.image_options_frame = ttk.LabelFrame(left_panel, text="Image Watermark Options")
        ttk.Button(self.image_options_frame, text="Upload Logo/Image", command=self.upload_watermark_image).pack(fill=tk.X, padx=5, pady=5)
        
        # Common watermark options
        common_options_frame = ttk.LabelFrame(left_panel, text="Watermark Settings")
        common_options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(common_options_frame, text="Position:").pack(anchor=tk.W, padx=5, pady=2)
        positions = ["top-left", "top-right", "center", "bottom-left", "bottom-right"]
        position_dropdown = ttk.Combobox(common_options_frame, textvariable=self.watermark_position, values=positions, state="readonly")
        position_dropdown.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(common_options_frame, text="Opacity:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Scale(common_options_frame, from_=0, to=100, variable=self.watermark_opacity, 
                 orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=2)
        
        # Apply watermark button
        ttk.Button(left_panel, text="Apply Watermark", command=self.apply_watermark).pack(fill=tk.X, padx=5, pady=10)
        
        # Save image button
        ttk.Button(left_panel, text="Save Image", command=self.save_image).pack(fill=tk.X, padx=5, pady=5)
        
        # Right panel for image preview
        right_panel = ttk.LabelFrame(main_frame, text="Image Preview")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for image display
        self.canvas = tk.Canvas(right_panel, bg="#dcdcdc")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initial watermark type is text, so hide image options
        self.update_watermark_options()
        
    def update_watermark_options(self):
        if self.watermark_type.get() == "text":
            self.text_options_frame.pack(fill=tk.X, padx=5, pady=5)
            self.image_options_frame.pack_forget()
        else:
            self.text_options_frame.pack_forget()
            self.image_options_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)
    
    def upload_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if file_path:
            self.watermark_path = file_path
            messagebox.showinfo("Success", "Watermark image uploaded successfully!")
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.watermark_color)
        if color[1]:
            self.watermark_color = color[1]
    
    def display_image(self, image):
        # Resize image to fit canvas while preserving aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Ensure canvas dimensions are positive (might be 1 during initialization)
        if canvas_width < 10:
            canvas_width = 800
        if canvas_height < 10:
            canvas_height = 500
        
        # Calculate new dimensions
        img_width, img_height = image.size
        ratio = min(canvas_width/img_width, canvas_height/img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to PhotoImage
        self.displayed_image = ImageTk.PhotoImage(resized_image)
        
        # Update canvas
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width // 2, new_height // 2, image=self.displayed_image, anchor=tk.CENTER)
        
    def apply_watermark(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please upload an image first!")
            return
            
        # Create a copy of the original image
        result_image = self.original_image.copy()
        
        if self.watermark_type.get() == "text":
            # Apply text watermark
            if not self.watermark_text.get():
                messagebox.showerror("Error", "Please enter watermark text!")
                return
                
            # Create transparent layer for the watermark
            txt_layer = Image.new("RGBA", result_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            # Calculate font size based on image dimensions
            img_width, img_height = result_image.size
            font_size = int((img_width + img_height) / 50 * (self.watermark_size.get() / 30))
            
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                # Fall back to default font
                font = ImageFont.load_default()
            
            # Get text size
            text = self.watermark_text.get()
            text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font_size * len(text) // 2, font_size)
            
            # Calculate position
            position = self.calculate_position(result_image.size, (text_width, text_height))
            
            # Convert hex color to RGB
            r, g, b = tuple(int(self.watermark_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            # Draw text
            opacity = self.watermark_opacity.get() / 100 * 255
            draw.text(position, text, fill=(r, g, b, int(opacity)), font=font)
            
            # Combine images
            if result_image.mode != 'RGBA':
                result_image = result_image.convert('RGBA')
            
            self.watermarked_image = Image.alpha_composite(result_image, txt_layer).convert('RGB')
            
        else:
            # Apply image watermark
            if not self.watermark_path:
                messagebox.showerror("Error", "Please upload a watermark image!")
                return
                
            watermark = Image.open(self.watermark_path).convert('RGBA')
            
            # Resize watermark if needed
            img_width, img_height = result_image.size
            wm_width, wm_height = watermark.size
            
            # Scale watermark to a reasonable size (25% of the image by default)
            scale_factor = (img_width + img_height) / (wm_width + wm_height) * (self.watermark_size.get() / 60)
            new_wm_width = int(wm_width * scale_factor)
            new_wm_height = int(wm_height * scale_factor)
            watermark = watermark.resize((new_wm_width, new_wm_height), Image.LANCZOS)
            
            # Calculate position
            position = self.calculate_position(result_image.size, watermark.size)
            
            # Adjust opacity
            opacity = self.watermark_opacity.get() / 100
            watermark = self.adjust_opacity(watermark, opacity)
            
            # Ensure result_image is in RGBA mode
            if result_image.mode != 'RGBA':
                result_image = result_image.convert('RGBA')
            
            # Create a transparent layer for watermark placement
            transparent = Image.new('RGBA', result_image.size, (0, 0, 0, 0))
            transparent.paste(watermark, position, watermark)
            
            # Combine images
            self.watermarked_image = Image.alpha_composite(result_image, transparent).convert('RGB')
        
        # Display the watermarked image
        self.display_image(self.watermarked_image)
        messagebox.showinfo("Success", "Watermark applied successfully!")
    
    def calculate_position(self, img_size, watermark_size):
        img_width, img_height = img_size
        wm_width, wm_height = watermark_size
        padding = 20  # Padding from the edges
        
        position = self.watermark_position.get()
        
        if position == "top-left":
            return (padding, padding)
        elif position == "top-right":
            return (img_width - wm_width - padding, padding)
        elif position == "center":
            return ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
        elif position == "bottom-left":
            return (padding, img_height - wm_height - padding)
        else:  # bottom-right is the default
            return (img_width - wm_width - padding, img_height - wm_height - padding)
    
    def adjust_opacity(self, image, opacity):
        # Adjust the alpha channel of the image
        data = image.getdata()
        new_data = []
        for item in data:
            # Keep RGB values the same but adjust alpha
            new_data.append((item[0], item[1], item[2], int(item[3] * opacity)))
        
        image.putdata(new_data)
        return image
    
    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("Error", "Please apply a watermark first!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            self.watermarked_image.save(file_path)
            messagebox.showinfo("Success", f"Image saved successfully to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()