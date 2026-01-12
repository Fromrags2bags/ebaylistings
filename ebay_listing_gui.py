#!/usr/bin/env python3
"""
eBay Listing Creator - GUI Application
User-friendly interface for creating eBay listings with automatic GitHub image hosting
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import base64
import requests
from datetime import datetime, timedelta
from pathlib import Path
import csv

class EbayListingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("eBay Listing Creator")
        self.root.geometry("800x700")
        
        # Configuration
        self.config_file = "ebay_config.json"
        self.config = self.load_config()
        
        # Variables
        self.images = []
        self.current_folder = None
        
        # Check if first run
        if not self.config.get('github_configured'):
            self.show_github_setup()
        else:
            self.show_main_window()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'github_configured': False,
            'github_username': '',
            'github_repo': '',
            'github_token': '',
            'default_location': 'New York',
            'default_shipping': '0.00'
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def show_github_setup(self):
        """Show GitHub setup screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="GitHub Setup (One-Time)", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Info text
        info = ttk.Label(main_frame, text="To upload images automatically, we need your GitHub information:",
                        wraplength=500)
        info.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="GitHub Username:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.github_username = ttk.Entry(main_frame, width=40)
        self.github_username.grid(row=2, column=1, pady=5)
        self.github_username.insert(0, self.config.get('github_username', ''))
        
        # Repository
        ttk.Label(main_frame, text="Repository Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.github_repo = ttk.Entry(main_frame, width=40)
        self.github_repo.grid(row=3, column=1, pady=5)
        self.github_repo.insert(0, self.config.get('github_repo', ''))
        
        # Token
        ttk.Label(main_frame, text="Personal Access Token:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.github_token = ttk.Entry(main_frame, width=40, show="*")
        self.github_token.grid(row=4, column=1, pady=5)
        
        # Help button
        help_btn = ttk.Button(main_frame, text="How to get a token?", 
                             command=self.show_token_help)
        help_btn.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Test Connection", 
                  command=self.test_github_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save & Continue", 
                  command=self.save_github_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Skip for now", 
                  command=self.skip_github_setup).pack(side=tk.LEFT, padx=5)
    
    def show_token_help(self):
        """Show help for getting GitHub token"""
        help_window = tk.Toplevel(self.root)
        help_window.title("How to Get GitHub Token")
        help_window.geometry("500x400")
        
        frame = ttk.Frame(help_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15)
        text.pack(fill=tk.BOTH, expand=True)
        
        instructions = """How to Get GitHub Personal Access Token:

1. Go to: https://github.com/settings/tokens

2. Click "Generate new token (classic)"

3. Name it: "eBay Image Upload"

4. Set expiration: No expiration (or your preference)

5. Check these permissions:
   ☑ repo (Full control of private repositories)

6. Scroll down and click "Generate token"

7. IMPORTANT: Copy the token immediately!
   (It starts with ghp_)

8. Paste it in the Token field

Note: Keep your token secure. Don't share it with anyone.
You can revoke it anytime from GitHub settings.
"""
        text.insert('1.0', instructions)
        text.config(state='disabled')
        
        ttk.Button(frame, text="Open GitHub Token Page", 
                  command=lambda: os.system('start https://github.com/settings/tokens')).pack(pady=10)
        ttk.Button(frame, text="Close", command=help_window.destroy).pack()
    
    def test_github_connection(self):
        """Test GitHub connection"""
        username = self.github_username.get().strip()
        repo = self.github_repo.get().strip()
        token = self.github_token.get().strip()
        
        if not all([username, repo, token]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            # Test API connection
            url = f"https://api.github.com/repos/{username}/{repo}"
            headers = {'Authorization': f'token {token}'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "✓ Connection successful!\nGitHub credentials are valid.")
            else:
                messagebox.showerror("Error", f"Connection failed: {response.status_code}\n{response.json().get('message', 'Unknown error')}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def save_github_config(self):
        """Save GitHub configuration"""
        username = self.github_username.get().strip()
        repo = self.github_repo.get().strip()
        token = self.github_token.get().strip()
        
        if not all([username, repo, token]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        self.config['github_username'] = username
        self.config['github_repo'] = repo
        self.config['github_token'] = token
        self.config['github_configured'] = True
        self.save_config()
        
        messagebox.showinfo("Success", "GitHub settings saved!")
        self.show_main_window()
    
    def skip_github_setup(self):
        """Skip GitHub setup"""
        result = messagebox.askyesno("Skip Setup", 
                                     "You can add image URLs manually later.\nContinue without GitHub setup?")
        if result:
            self.show_main_window()
    
    def show_main_window(self):
        """Show main application window"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Listing", command=self.new_listing)
        file_menu.add_command(label="Open Existing", command=self.open_existing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="GitHub Settings", command=self.show_github_setup)
        settings_menu.add_command(label="Default Values", command=self.show_defaults)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main content
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        # Clear content area
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Menu):
                continue
            widget.destroy()
        
        frame = ttk.Frame(self.root, padding="40")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="eBay Listing Creator", 
                         font=('Arial', 24, 'bold'))
        title.pack(pady=(0, 20))
        
        subtitle = ttk.Label(frame, text="Create professional eBay listings with ease", 
                            font=('Arial', 12))
        subtitle.pack(pady=(0, 40))
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        
        new_btn = ttk.Button(btn_frame, text="Create New Listing", 
                            command=self.new_listing, width=25)
        new_btn.pack(pady=10)
        
        open_btn = ttk.Button(btn_frame, text="Edit Existing Listing", 
                             command=self.open_existing, width=25)
        open_btn.pack(pady=10)
        
        # Status
        status_text = "✓ GitHub configured" if self.config.get('github_configured') else "⚠ GitHub not configured"
        status = ttk.Label(frame, text=status_text, font=('Arial', 10))
        status.pack(pady=(40, 0))
    
    def new_listing(self):
        """Create new listing"""
        # Prompt for folder name
        dialog = tk.Toplevel(self.root)
        dialog.title("New Listing")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Enter folder name for this listing:").pack(pady=(0, 10))
        ttk.Label(frame, text="(e.g., lululemon_hoodie_gray_xs)", 
                 font=('Arial', 9, 'italic')).pack()
        
        folder_entry = ttk.Entry(frame, width=40)
        folder_entry.pack(pady=10)
        folder_entry.focus()
        
        def create_folder():
            folder_name = folder_entry.get().strip()
            if not folder_name:
                messagebox.showerror("Error", "Please enter a folder name")
                return
            
            # Create folder
            folder_path = os.path.join('listings', folder_name)
            if os.path.exists(folder_path):
                messagebox.showerror("Error", f"Folder '{folder_name}' already exists")
                return
            
            os.makedirs(folder_path, exist_ok=True)
            self.current_folder = folder_path
            dialog.destroy()
            self.show_listing_form()
        
        ttk.Button(frame, text="Create", command=create_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        folder_entry.bind('<Return>', lambda e: create_folder())
    
    def open_existing(self):
        """Open existing listing folder"""
        listings_dir = 'listings'
        if not os.path.exists(listings_dir):
            messagebox.showerror("Error", "No listings folder found")
            return
        
        folders = [f for f in os.listdir(listings_dir) 
                  if os.path.isdir(os.path.join(listings_dir, f))]
        
        if not folders:
            messagebox.showinfo("Info", "No existing listings found")
            return
        
        # Show folder selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Listing")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Select a listing to edit:").pack(pady=(0, 10))
        
        listbox = tk.Listbox(frame, height=10)
        listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for folder in folders:
            listbox.insert(tk.END, folder)
        
        def select_folder():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a folder")
                return
            
            folder_name = listbox.get(selection[0])
            self.current_folder = os.path.join('listings', folder_name)
            dialog.destroy()
            self.show_listing_form()
        
        ttk.Button(frame, text="Open", command=select_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_listing_form(self):
        """Show listing creation form"""
        # Clear window
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Menu):
                continue
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main form frame
        form_frame = ttk.Frame(scrollable_frame, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(form_frame, text=f"Listing: {os.path.basename(self.current_folder)}",
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Form fields
        row = 1
        
        # Title
        ttk.Label(form_frame, text="*Title:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(form_frame, width=50)
        self.title_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Brand
        ttk.Label(form_frame, text="*Brand:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.brand_entry = ttk.Entry(form_frame, width=50)
        self.brand_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Price
        ttk.Label(form_frame, text="*Price:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.price_entry = ttk.Entry(form_frame, width=20)
        self.price_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Size
        ttk.Label(form_frame, text="*Size:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.size_entry = ttk.Entry(form_frame, width=20)
        self.size_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Color
        ttk.Label(form_frame, text="*Color:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.color_entry = ttk.Entry(form_frame, width=30)
        self.color_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Condition
        ttk.Label(form_frame, text="*Condition:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.condition_var = tk.StringVar(value="Used - Excellent")
        condition_combo = ttk.Combobox(form_frame, textvariable=self.condition_var, width=30)
        condition_combo['values'] = ('New with tags', 'New without tags', 'Used - Excellent',
                                     'Used - Good', 'Used - Acceptable')
        condition_combo.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.description_text = scrolledtext.ScrolledText(form_frame, width=50, height=5)
        self.description_text.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.quantity_entry = ttk.Entry(form_frame, width=10)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Shipping Cost
        ttk.Label(form_frame, text="Shipping Cost:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.shipping_entry = ttk.Entry(form_frame, width=10)
        self.shipping_entry.insert(0, self.config.get('default_shipping', '0.00'))
        self.shipping_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Location
        ttk.Label(form_frame, text="Location:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.location_entry = ttk.Entry(form_frame, width=30)
        self.location_entry.insert(0, self.config.get('default_location', 'New York'))
        self.location_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # SKU
        ttk.Label(form_frame, text="SKU:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.sku_entry = ttk.Entry(form_frame, width=30)
        self.sku_entry.grid(row=row, column=1, pady=5, sticky=tk.W)
        row += 1
        
        # Images section
        ttk.Label(form_frame, text="Images:", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        # Image list
        self.image_listbox = tk.Listbox(form_frame, height=5, width=50)
        self.image_listbox.grid(row=row, column=0, columnspan=2, pady=5, sticky=tk.W)
        row += 1
        
        # Image buttons
        img_btn_frame = ttk.Frame(form_frame)
        img_btn_frame.grid(row=row, column=0, columnspan=2, pady=5, sticky=tk.W)
        ttk.Button(img_btn_frame, text="Add Images", command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Remove Selected", command=self.remove_image).pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Action buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save Listing Data", command=self.save_listing_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate CSV (No Upload)", command=self.generate_csv_only).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.show_welcome_screen).pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load existing data if available
        self.load_existing_data()
    
    def add_images(self):
        """Add images to listing"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.images:
                self.images.append(file)
                self.image_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_image(self):
        """Remove selected image"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            self.images.pop(index)
            self.image_listbox.delete(index)
    
    def load_existing_data(self):
        """Load existing listing data if available"""
        listing_file = os.path.join(self.current_folder, 'listing_data.txt')
        if not os.path.exists(listing_file):
            return
        
        try:
            data = {}
            with open(listing_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line and not line.startswith('#'):
                        key, value = line.split(':', 1)
                        data[key.strip().lower()] = value.strip()
            
            # Populate fields
            if 'title' in data:
                self.title_entry.insert(0, data['title'])
            if 'brand' in data:
                self.brand_entry.insert(0, data['brand'])
            if 'price' in data:
                self.price_entry.insert(0, data['price'])
            if 'size' in data:
                self.size_entry.insert(0, data['size'])
            if 'color' in data:
                self.color_entry.insert(0, data['color'])
            if 'condition' in data:
                self.condition_var.set(data['condition'])
            if 'description' in data:
                self.description_text.insert('1.0', data['description'])
            if 'quantity' in data:
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, data['quantity'])
            if 'shipping_cost' in data:
                self.shipping_entry.delete(0, tk.END)
                self.shipping_entry.insert(0, data['shipping_cost'])
            if 'location' in data:
                self.location_entry.delete(0, tk.END)
                self.location_entry.insert(0, data['location'])
            if 'sku' in data:
                self.sku_entry.insert(0, data['sku'])
            
            # Load images from folder
            for file in os.listdir(self.current_folder):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    img_path = os.path.join(self.current_folder, file)
                    if img_path not in self.images:
                        self.images.append(img_path)
                        self.image_listbox.insert(tk.END, file)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_listing_data(self):
        """Save listing data to file"""
        # Validate required fields
        if not self.title_entry.get().strip():
            messagebox.showerror("Error", "Title is required")
            return
        if not self.brand_entry.get().strip():
            messagebox.showerror("Error", "Brand is required")
            return
        if not self.price_entry.get().strip():
            messagebox.showerror("Error", "Price is required")
            return
        
        # Create listing_data.txt
        listing_file = os.path.join(self.current_folder, 'listing_data.txt')
        
        with open(listing_file, 'w', encoding='utf-8') as f:
            f.write(f"title: {self.title_entry.get().strip()}\n")
            f.write(f"brand: {self.brand_entry.get().strip()}\n")
            f.write(f"price: {self.price_entry.get().strip()}\n")
            f.write(f"size: {self.size_entry.get().strip()}\n")
            f.write(f"color: {self.color_entry.get().strip()}\n")
            f.write(f"condition: {self.condition_var.get()}\n")
            f.write(f"description: {self.description_text.get('1.0', tk.END).strip()}\n")
            f.write(f"quantity: {self.quantity_entry.get().strip()}\n")
            f.write(f"shipping_cost: {self.shipping_entry.get().strip()}\n")
            f.write(f"location: {self.location_entry.get().strip()}\n")
            if self.sku_entry.get().strip():
                f.write(f"sku: {self.sku_entry.get().strip()}\n")
        
        # Copy images to folder
        for img_path in self.images:
            if not img_path.startswith(self.current_folder):
                import shutil
                dest = os.path.join(self.current_folder, os.path.basename(img_path))
                shutil.copy2(img_path, dest)
        
        messagebox.showinfo("Success", f"Listing data saved to:\n{listing_file}")
    
    def generate_csv_only(self):
        """Generate CSV without uploading images"""
        # First save the listing data
        self.save_listing_data()
        
        # Import the converter
        from convert_to_ebay_category_template import convert_to_ebay_category_template
        from datetime import datetime
        
        # Generate CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'ebay_category_upload_{timestamp}.csv'
        
        try:
            success = convert_to_ebay_category_template(self.current_folder, output_file)
            if success:
                messagebox.showinfo("Success",
                                  f"CSV file created successfully!\n\n"
                                  f"File: {output_file}\n\n"
                                  f"Note: Images are local file paths.\n"
                                  f"Upload to eBay and add images manually,\n"
                                  f"or use GitHub upload feature.")
            else:
                messagebox.showerror("Error", "Failed to generate CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate CSV:\n{str(e)}")
    
    def show_defaults(self):
        """Show default settings"""
        messagebox.showinfo("Coming Soon", "Default settings dialog coming soon...")
    
    def show_instructions(self):
        """Show instructions"""
        messagebox.showinfo("Instructions", 
                          "1. Click 'Create New Listing'\n"
                          "2. Enter a folder name\n"
                          "3. Fill in product details\n"
                          "4. Add images\n"
                          "5. Click 'Generate CSV'\n"
                          "6. Upload CSV to eBay")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "eBay Listing Creator v1.0\n\n"
                          "Automated eBay listing creation with\n"
                          "GitHub image hosting integration.\n\n"
                          "Created with Python & Tkinter")

def main():
    root = tk.Tk()
    app = EbayListingGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

# Made with Bob
