import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from script_builder import ScriptBuilder

class CardMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yu-Gi-Oh! Card Maker")
        self.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create left frame for card details
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Create right frame for image and script
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Create and pack frames
        self.card_details_frame = self.create_card_details_frame(left_frame)
        self.card_details_frame.pack(fill="both", expand=True)
        
        # Create notebook for image and script
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create image frame
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="Card Image")
        
        # Image contents
        self.image_label = ttk.Label(image_frame, text="No image selected")
        self.image_label.pack(pady=10)
        ttk.Button(image_frame, text="Select Image", command=self.select_image).pack(pady=5)
        
        # Create script frame
        script_frame = self.create_script_tab(self.notebook)
        
        # Create buttons frame at the bottom
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(side="bottom", fill="x", pady=10)
        
        # Add buttons
        ttk.Button(self.buttons_frame, text="Load Card", command=self.load_card).pack(side="left", padx=5)
        ttk.Button(self.buttons_frame, text="Save Card", command=self.save_card).pack(side="left", padx=5)
        ttk.Button(self.buttons_frame, text="Clear", command=self.clear_form).pack(side="left", padx=5)

    def create_card_details_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Card Details")
        
        # Card ID with Browse button
        id_frame = ttk.Frame(frame)
        id_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(id_frame, text="Card ID:").pack(side="left")
        self.id_entry = ttk.Entry(id_frame, width=20)
        self.id_entry.pack(side="left", padx=5)
        ttk.Button(id_frame, text="Browse", command=self.browse_cards).pack(side="left")
        
        # Card Name
        name_frame = ttk.Frame(frame)
        name_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(name_frame, text="Card Name:").pack(side="left")
        self.name_entry = ttk.Entry(name_frame, width=40)
        self.name_entry.pack(side="left", padx=5)
        
        # Card Type
        type_frame = ttk.LabelFrame(frame, text="Card Type")
        type_frame.pack(fill="x", padx=5, pady=5)
        
        # Type checkboxes
        self.type_vars = {
            "Effect": tk.BooleanVar(),
            "Fusion": tk.BooleanVar(),
            "Ritual": tk.BooleanVar(),
            "Synchro": tk.BooleanVar(),
            "Xyz": tk.BooleanVar(),
            "Pendulum": tk.BooleanVar(),
            "Link": tk.BooleanVar(),
            "Tuner": tk.BooleanVar(),
            "Gemini": tk.BooleanVar(),
            "Flip": tk.BooleanVar(),
            "Spirit": tk.BooleanVar(),
            "Union": tk.BooleanVar(),
            "Toon": tk.BooleanVar()
        }
        
        type_grid = ttk.Frame(type_frame)
        type_grid.pack(fill="x", padx=5, pady=5)
        
        row = 0
        col = 0
        for type_name, var in self.type_vars.items():
            ttk.Checkbutton(type_grid, text=type_name, variable=var, 
                          command=self.on_type_changed).grid(row=row, column=col, sticky="w", padx=5)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Card Stats
        stats_frame = ttk.LabelFrame(frame, text="Card Stats")
        stats_frame.pack(fill="x", padx=5, pady=5)
        
        # Attribute
        attr_frame = ttk.Frame(stats_frame)
        attr_frame.pack(fill="x")
        ttk.Label(attr_frame, text="Attribute:").pack(side="left")
        self.attribute = tk.StringVar()
        self.attribute_map = {
            "EARTH": 0x01,
            "WATER": 0x02, 
            "FIRE": 0x04,
            "WIND": 0x08,
            "LIGHT": 0x10,
            "DARK": 0x20,
            "DIVINE": 0x40
        }
        self.reverse_attribute_map = {v: k for k, v in self.attribute_map.items()}
        attributes = list(self.attribute_map.keys())
        self.attribute_combo = ttk.Combobox(attr_frame, values=attributes, textvariable=self.attribute)
        self.attribute_combo.pack(side="left", padx=5)
        self.attribute_combo.set(attributes[0])
        
        # Level/Rank
        level_frame = ttk.Frame(stats_frame)
        level_frame.pack(fill="x")
        ttk.Label(level_frame, text="Level/Rank:").pack(side="left")
        self.level = tk.StringVar()
        self.level_combo = ttk.Combobox(level_frame, values=[str(i) for i in range(1, 13)], textvariable=self.level)
        self.level_combo.pack(side="left", padx=5)
        self.level_combo.set("4")  # Default to level 4
        
        # ATK/DEF
        stats_frame2 = ttk.Frame(stats_frame)
        stats_frame2.pack(fill="x")
        ttk.Label(stats_frame2, text="ATK:").pack(side="left")
        self.atk = ttk.Entry(stats_frame2, width=10)
        self.atk.pack(side="left", padx=5)
        ttk.Label(stats_frame2, text="DEF:").pack(side="left")
        self.def_ = ttk.Entry(stats_frame2, width=10)
        self.def_.pack(side="left", padx=5)
        
        # Setcode
        setcode_frame = ttk.Frame(stats_frame)
        setcode_frame.pack(fill="x")
        ttk.Label(setcode_frame, text="Setcode:").pack(side="left")
        self.setcode = ttk.Entry(setcode_frame)
        self.setcode.pack(side="left", padx=5, fill="x", expand=True)
        
        # Link Properties
        self.link_frame = ttk.LabelFrame(frame, text="Link Properties")
        
        # Link Rating
        rating_frame = ttk.Frame(self.link_frame)
        rating_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(rating_frame, text="Link Rating:").pack(side="left")
        self.link_rating = ttk.Combobox(rating_frame, values=[str(i) for i in range(1, 9)])
        self.link_rating.pack(side="left", padx=5)
        self.link_rating.set("1")
        
        # Link Arrows
        arrows_frame = ttk.Frame(self.link_frame)
        arrows_frame.pack(fill="x", padx=5, pady=5)
        
        # Create Link Marker checkboxes and preview
        self.link_vars = {
            "Top-Left": tk.BooleanVar(),
            "Top": tk.BooleanVar(),
            "Top-Right": tk.BooleanVar(),
            "Left": tk.BooleanVar(),
            "Right": tk.BooleanVar(),
            "Bottom-Left": tk.BooleanVar(),
            "Bottom": tk.BooleanVar(),
            "Bottom-Right": tk.BooleanVar()
        }
        
        # Create Link Marker preview canvas
        self.link_canvas = tk.Canvas(arrows_frame, width=150, height=150)
        self.link_canvas.pack(side="left", padx=5)
        
        # Create Link Marker checkboxes
        checkbox_frame = ttk.Frame(arrows_frame)
        checkbox_frame.pack(side="left", fill="y", padx=5)
        
        for marker, var in self.link_vars.items():
            ttk.Checkbutton(checkbox_frame, text=marker, variable=var,
                          command=self.update_link_preview).pack(anchor="w")
        
        # Pendulum Scales
        self.pendulum_frame = ttk.LabelFrame(frame, text="Pendulum Scales")
        self.pendulum_frame.pack(fill="x", padx=5, pady=5)
        
        scales_frame = ttk.Frame(self.pendulum_frame)
        scales_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(scales_frame, text="Left Scale:").pack(side="left")
        self.scale_left_var = tk.StringVar()
        scales = list(range(0, 14))
        self.scale_left_combo = ttk.Combobox(scales_frame, values=scales, textvariable=self.scale_left_var)
        self.scale_left_combo.pack(side="left", padx=5)
        self.scale_left_combo.set("1")
        
        ttk.Label(scales_frame, text="Right Scale:").pack(side="left", padx=5)
        self.scale_right_var = tk.StringVar()
        self.scale_right_combo = ttk.Combobox(scales_frame, values=scales, textvariable=self.scale_right_var)
        self.scale_right_combo.pack(side="left", padx=5)
        self.scale_right_combo.set("1")
        
        # Card Text
        text_frame = ttk.LabelFrame(frame, text="Card Text")
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_text = tk.Text(text_frame, height=4, width=60)
        self.text_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initially hide Link and Pendulum frames
        self.link_frame.pack_forget()
        self.pendulum_frame.pack_forget()
        
        return frame

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                # Open and resize image
                image = Image.open(file_path)
                image = image.resize((400, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Update image label
                self.image_label.configure(image=photo)
                self.image_label.image = photo  # Keep a reference
                
                # Store the original file path
                self.image_path = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def find_image(self, card_id):
        image_name = f"{card_id}.jpg"  # Try jpg first
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Debug print
        print(f"Looking for image: {image_name}")
        print(f"Base path: {base_path}")
        
        # Search recursively through all subdirectories
        for root, dirs, files in os.walk(base_path):
            # Check for both .jpg and .png
            for ext in ['.jpg', '.png']:
                image_name = f"{card_id}{ext}"
                if image_name in files:
                    full_path = os.path.join(root, image_name)
                    print(f"Found image at: {full_path}")
                    return full_path
                    
        print(f"No image found for card {card_id}")
        return None

    def load_card(self, card_id):
        try:
            # Connect to cards.cdb
            conn = sqlite3.connect('cards.cdb')
            c = conn.cursor()
            
            # Query both datas and texts tables
            c.execute('''
                SELECT d.*, t.name, t.desc 
                FROM datas d 
                LEFT JOIN texts t ON d.id = t.id 
                WHERE d.id = ?
            ''', (card_id,))
            
            result = c.fetchone()
            if result:
                # Unpack the results
                id, ot, alias, setcode, type, atk, def_, level, race, attribute, category, name, desc = result
                
                # Debug prints for attribute
                print(f"Raw attribute value from DB: {attribute}")
                print(f"Attribute map: {self.attribute_map}")
                print(f"Reverse attribute map: {self.reverse_attribute_map}")
                
                # Update the form fields
                self.id_entry.delete(0, tk.END)
                self.id_entry.insert(0, str(id))
                
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)
                
                # Set attribute
                if attribute in self.reverse_attribute_map:
                    attr_name = self.reverse_attribute_map[attribute]
                    print(f"Setting attribute to: {attr_name}")  # Debug print
                    self.attribute.set(attr_name)
                else:
                    print(f"Attribute {attribute} not found in map")  # Debug print
                    # Try to find the closest match
                    for k, v in self.attribute_map.items():
                        print(f"Checking {k}: {v} (binary: {bin(v)})")
                    # Default to DARK if not found
                    self.attribute.set("DARK")
                
                # Set level/rank
                self.level.set(str(level & 0xff))  # Get the level value
                
                # Set ATK/DEF
                self.atk.delete(0, tk.END)
                self.atk.insert(0, str(atk))
                
                self.def_.delete(0, tk.END)
                self.def_.insert(0, str(def_))
                
                # Set setcode
                self.setcode.delete(0, tk.END)
                self.setcode.insert(0, str(setcode))
                
                # Set card text
                self.text_text.delete("1.0", tk.END)
                self.text_text.insert("1.0", desc)
                
                # Update card types
                self.update_card_types(type)
                
                # Set Link Rating if it's a Link monster
                if type & 0x4000000:  # Link monster
                    # Extract Link Rating from level field
                    link_rating = (level >> 24) & 0xFF
                    print(f"Link Rating: {link_rating}")  # Debug print
                    
                    # Make sure the Link frame is visible first
                    self.link_frame.pack(fill="x", padx=5, pady=5)
                    
                    # Force update the Link Rating combobox
                    self.link_rating.set("")  # Clear first
                    self.link_rating.set(str(link_rating))  # Then set new value
                    
                    # Set Link Markers
                    link_markers = level & 0xFF
                    self.link_vars["Bottom-Left"].set(bool(link_markers & 0x01))
                    self.link_vars["Bottom"].set(bool(link_markers & 0x02))
                    self.link_vars["Bottom-Right"].set(bool(link_markers & 0x04))
                    self.link_vars["Left"].set(bool(link_markers & 0x08))
                    self.link_vars["Right"].set(bool(link_markers & 0x20))
                    self.link_vars["Top-Left"].set(bool(link_markers & 0x40))
                    self.link_vars["Top"].set(bool(link_markers & 0x80))
                    self.link_vars["Top-Right"].set(bool(link_markers & 0x100))
                    
                    # Update the link preview
                    self.update_link_preview()
                    
                    # Set DEF to "-" for Link monsters
                    self.def_.configure(state="normal")
                    self.def_.delete(0, tk.END)
                    self.def_.insert(0, "-")
                    self.def_.configure(state="disabled")
                
                # Try to load image
                image_path = self.find_image(card_id)
                if image_path:
                    try:
                        # Open and resize image
                        image = Image.open(image_path)
                        image = image.resize((400, 400), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        
                        # Update image label
                        self.image_label.configure(image=photo, text="")
                        self.image_label.image = photo  # Keep a reference
                        
                        # Store the original file path
                        self.image_path = image_path
                    except Exception as e:
                        print(f"Failed to load image: {str(e)}")
                
                # Try to load script
                script_content = self.find_script(card_id)
                if script_content:
                    self.script_text.delete("1.0", tk.END)
                    self.script_text.insert("1.0", script_content)
                else:
                    # Set default script template
                    self.script_text.delete("1.0", tk.END)
                    self.script_text.insert("1.0", f"--Card Script\nlocal s,id=GetID()\nfunction s.initial_effect(c)\n\nend")
                
            conn.close()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load card: {str(e)}")
            
    def find_script(self, card_id):
        script_name = f"c{card_id}.lua"
        script_paths = [
            os.path.join("script", "official", script_name),
            os.path.join("script", script_name),
            os.path.join("expansions", "script", script_name),
            os.path.join("custom_cards", "scripts", script_name)
        ]
        
        # Debug print
        print(f"Looking for script: {script_name}")
        print(f"Base path: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # First try specific paths
        for path in script_paths:
            full_path = os.path.join(base_path, path)
            print(f"Checking path: {full_path}")
            if os.path.exists(full_path):
                print(f"Found script at: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        # If not found, search recursively
        for root, dirs, files in os.walk(base_path):
            if script_name in files:
                full_path = os.path.join(root, script_name)
                print(f"Found script at: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        print(f"No script found for card {card_id}")
        return None

    def save_card(self):
        try:
            # Get values from form
            card_id = int(self.id_entry.get())
            name = self.name_entry.get()
            attribute_name = self.attribute.get()
            attribute = self.attribute_map.get(attribute_name, 0)
            level = int(self.level.get())
            atk = int(self.atk.get() or 0)
            def_ = int(self.def_.get() or 0) if self.def_.get() != '-' else 0
            setcode = int(self.setcode.get() or 0)
            desc = self.text_text.get("1.0", tk.END).strip()
            
            # Calculate type value based on constant.lua values
            type_value = 0x1  # Monster type
            if self.type_vars["Effect"].get():
                type_value |= 0x20
            if self.type_vars["Fusion"].get():
                type_value |= 0x40
            if self.type_vars["Ritual"].get():
                type_value |= 0x80
            if self.type_vars["Spirit"].get():
                type_value |= 0x200
            if self.type_vars["Union"].get():
                type_value |= 0x400
            if self.type_vars["Gemini"].get():
                type_value |= 0x800
            if self.type_vars["Tuner"].get():
                type_value |= 0x1000
            if self.type_vars["Synchro"].get():
                type_value |= 0x2000
            if self.type_vars["Xyz"].get():
                type_value |= 0x800000
            if self.type_vars["Pendulum"].get():
                type_value |= 0x1000000
            if self.type_vars["Link"].get():
                type_value |= 0x4000000
            if self.type_vars["Flip"].get():
                type_value |= 0x2000000
            if self.type_vars["Toon"].get():
                type_value |= 0x4000
            
            # Calculate Link Rating and Markers for Link monsters
            if self.type_vars["Link"].get():
                link_rating = int(self.link_rating.get())
                link_markers = 0
                if self.link_vars["Bottom-Left"].get(): link_markers |= 0x01
                if self.link_vars["Bottom"].get(): link_markers |= 0x02
                if self.link_vars["Bottom-Right"].get(): link_markers |= 0x04
                if self.link_vars["Left"].get(): link_markers |= 0x08
                if self.link_vars["Right"].get(): link_markers |= 0x20
                if self.link_vars["Top-Left"].get(): link_markers |= 0x40
                if self.link_vars["Top"].get(): link_markers |= 0x80
                if self.link_vars["Top-Right"].get(): link_markers |= 0x100
                
                # Combine Link Rating and Markers into level field
                level = (link_rating << 24) | (link_markers & 0xFF)  # Changed back to << 24
                print(f"Saving Link Rating: {link_rating}, Level: {level}")  # Debug print
                
            # Connect to database
            conn = sqlite3.connect('cards.cdb')
            c = conn.cursor()
            
            # Update datas table
            c.execute('''
                INSERT OR REPLACE INTO datas 
                (id, ot, alias, setcode, type, atk, def, level, race, attribute)
                VALUES (?, 0, 0, ?, ?, ?, ?, ?, 0, ?)
            ''', (card_id, setcode, type_value, atk, def_, level, attribute))
            
            # Update texts table
            c.execute('''
                INSERT OR REPLACE INTO texts 
                (id, name, desc)
                VALUES (?, ?, ?)
            ''', (card_id, name, desc))
            
            conn.commit()
            conn.close()
            
            tk.messagebox.showinfo("Success", "Card saved successfully!")
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save card: {str(e)}")

    def clear_form(self):
        # Clear all form fields
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        
        # Reset type checkboxes
        for var in self.type_vars.values():
            var.set(False)
        
        # Reset other fields
        self.attribute.set("DARK")
        self.level.set("4")
        self.atk.delete(0, tk.END)
        self.atk.insert(0, "0")
        self.def_.delete(0, tk.END)
        self.def_.insert(0, "0")
        self.setcode.delete(0, tk.END)
        self.text_text.delete("1.0", tk.END)
        
        # Reset image
        self.image_label.configure(image="", text="No image selected")
        if hasattr(self, 'image_path'):
            del self.image_path
        
        # Clear script
        self.script_text.delete("1.0", tk.END)
        self.script_text.insert("1.0", "--Card Script\nlocal s,id=GetID()\nfunction s.initial_effect(c)\n\nend")
        
        # Update UI
        self.on_type_changed()

    def on_type_changed(self):
        # Show/hide Link elements
        if self.type_vars["Link"].get():
            self.link_frame.pack(fill="x", padx=5, pady=5)
            self.def_.delete(0, tk.END)
            self.def_.insert(0, "-")
            self.def_.configure(state="disabled")
        else:
            self.link_frame.pack_forget()
            self.def_.configure(state="normal")
        
        # Show/hide Pendulum elements
        if self.type_vars["Pendulum"].get():
            self.pendulum_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.pendulum_frame.pack_forget()
            
        # Update link arrows if needed
        if hasattr(self, 'link_canvas'):
            self.update_link_preview()

    def update_link_preview(self):
        # Clear canvas
        self.link_canvas.delete("all")
        
        # Draw card outline
        self.link_canvas.create_rectangle(30, 30, 120, 120, outline="black")
        
        # Draw arrows for selected markers
        if self.link_vars["Top-Left"].get():
            self.draw_arrow(30, 30, 45, "northwest")
        if self.link_vars["Top"].get():
            self.draw_arrow(75, 30, 0, "north")
        if self.link_vars["Top-Right"].get():
            self.draw_arrow(120, 30, -45, "northeast")
        if self.link_vars["Left"].get():
            self.draw_arrow(30, 75, 90, "west")
        if self.link_vars["Right"].get():
            self.draw_arrow(120, 75, -90, "east")
        if self.link_vars["Bottom-Left"].get():
            self.draw_arrow(30, 120, 135, "southwest")
        if self.link_vars["Bottom"].get():
            self.draw_arrow(75, 120, 180, "south")
        if self.link_vars["Bottom-Right"].get():
            self.draw_arrow(120, 120, -135, "southeast")

    def draw_arrow(self, x, y, angle, direction):
        # Arrow dimensions
        arrow_length = 20
        arrow_width = 10
        
        # Calculate arrow points based on direction
        if direction == "northwest":
            points = [x, y, x-arrow_length, y-arrow_length, x-arrow_width, y-arrow_length+arrow_width]
        elif direction == "north":
            points = [x, y, x, y-arrow_length, x-arrow_width, y-arrow_length+arrow_width, x+arrow_width, y-arrow_length+arrow_width]
        elif direction == "northeast":
            points = [x, y, x+arrow_length, y-arrow_length, x+arrow_width, y-arrow_length+arrow_width]
        elif direction == "west":
            points = [x, y, x-arrow_length, y, x-arrow_length+arrow_width, y-arrow_width, x-arrow_length+arrow_width, y+arrow_width]
        elif direction == "east":
            points = [x, y, x+arrow_length, y, x+arrow_length-arrow_width, y-arrow_width, x+arrow_length-arrow_width, y+arrow_width]
        elif direction == "southwest":
            points = [x, y, x-arrow_length, y+arrow_length, x-arrow_width, y+arrow_length-arrow_width]
        elif direction == "south":
            points = [x, y, x, y+arrow_length, x-arrow_width, y+arrow_length-arrow_width, x+arrow_width, y+arrow_length-arrow_width]
        else:  # southeast
            points = [x, y, x+arrow_length, y+arrow_length, x+arrow_width, y+arrow_length-arrow_width]
        
        # Draw arrow
        self.link_canvas.create_polygon(points, fill="red", outline="black") 

    def browse_cards(self):
        dialog = CardBrowser(self)
        self.wait_window(dialog)
        if dialog.selected_card:
            self.load_card(dialog.selected_card)

    def update_card_types(self, type_value):
        # Clear existing types
        for var in self.type_vars.values():
            var.set(False)
            
        # Check each type bit based on constant.lua values
        if type_value & 0x20:     # Effect
            self.type_vars["Effect"].set(True)
        if type_value & 0x40:     # Fusion
            self.type_vars["Fusion"].set(True)
        if type_value & 0x80:     # Ritual
            self.type_vars["Ritual"].set(True)
        if type_value & 0x200:    # Spirit
            self.type_vars["Spirit"].set(True)
        if type_value & 0x400:    # Union
            self.type_vars["Union"].set(True)
        if type_value & 0x800:    # Gemini
            self.type_vars["Gemini"].set(True)
        if type_value & 0x1000:   # Tuner
            self.type_vars["Tuner"].set(True)
        if type_value & 0x2000:   # Synchro
            self.type_vars["Synchro"].set(True)
        if type_value & 0x800000: # Xyz
            self.type_vars["Xyz"].set(True)
        if type_value & 0x1000000: # Pendulum
            self.type_vars["Pendulum"].set(True)
        if type_value & 0x4000000: # Link
            self.type_vars["Link"].set(True)
        if type_value & 0x2000000: # Flip
            self.type_vars["Flip"].set(True)
        if type_value & 0x4000:    # Toon
            self.type_vars["Toon"].set(True)
            
        # Update UI based on type changes
        self.on_type_changed()

    def create_script_tab(self, notebook):
        # Create script frame
        script_frame = ttk.Frame(notebook)
        notebook.add(script_frame, text="Script")
        
        # Create paned window for script
        script_paned = ttk.PanedWindow(script_frame, orient=tk.HORIZONTAL)
        script_paned.pack(fill="both", expand=True)
        
        # Create script text area with label frame
        script_text_frame = ttk.LabelFrame(script_paned, text="Card Script")
        script_paned.add(script_text_frame)
        
        # Add scrollbars
        script_scroll_y = ttk.Scrollbar(script_text_frame)
        script_scroll_y.pack(side="right", fill="y")
        
        script_scroll_x = ttk.Scrollbar(script_text_frame, orient="horizontal")
        script_scroll_x.pack(side="bottom", fill="x")
        
        # Create text widget with scrollbars
        self.script_text = tk.Text(script_text_frame, wrap="none", 
                                 yscrollcommand=script_scroll_y.set,
                                 xscrollcommand=script_scroll_x.set,
                                 width=60, height=20)
        self.script_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        script_scroll_y.config(command=self.script_text.yview)
        script_scroll_x.config(command=self.script_text.xview)
        
        # Add default script template
        self.script_text.insert("1.0", "--Card Script\nlocal s,id=GetID()\nfunction s.initial_effect(c)\n\nend")
        
        # Create script builder frame
        builder_frame = ttk.LabelFrame(script_paned, text="Script Builder")
        script_paned.add(builder_frame)
        
        # Initialize script builder
        self.script_builder = ScriptBuilder(builder_frame, self.script_text)
        self.script_builder.pack(fill="both", expand=True)
        
        return script_frame

class CardBrowser(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Card Browser")
        self.selected_card = None
        
        # Create search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<Return>", self.search_cards)
        ttk.Button(search_frame, text="Search", command=self.search_cards).pack(side="left")
        
        # Create treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Type", "ATK", "DEF"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("ATK", text="ATK")
        self.tree.heading("DEF", text="DEF")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Load initial data
        self.search_cards()
        
    def search_cards(self, event=None):
        search_term = self.search_entry.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Connect to database
            conn = sqlite3.connect("cards.cdb")
            cursor = conn.cursor()
            
            # Search cards
            if search_term:
                cursor.execute("""
                    SELECT d.id, t.name, d.type, d.atk, d.def
                    FROM datas d
                    LEFT JOIN texts t ON d.id = t.id
                    WHERE t.name LIKE ? OR d.id LIKE ?
                    LIMIT 100
                """, (f"%{search_term}%", f"%{search_term}%"))
            else:
                cursor.execute("""
                    SELECT d.id, t.name, d.type, d.atk, d.def
                    FROM datas d
                    LEFT JOIN texts t ON d.id = t.id
                    LIMIT 100
                """)
            
            # Add results to treeview
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
            conn.close()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to search cards: {str(e)}")
            
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            card_id = item["values"][0]  # Get the card ID from the selected row
            self.selected_card = card_id
            self.destroy()  # Close the browser window

if __name__ == "__main__":
    app = CardMaker()
    app.mainloop() 