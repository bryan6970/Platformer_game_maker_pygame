import math
import tkinter as tk
import json
import os

def save_to_config_file(new_obstacle_post):
    config_path = "config.json"
    
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.json not found")
    
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
    
    config_data["OBSTACLE_POST"] = new_obstacle_post
    
    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    
    storage_path = "config_storage.json"
    
    if not os.path.exists(storage_path):
        with open(storage_path, "w") as storage_file:
            json.dump({}, storage_file)
    
    with open(storage_path, "r") as storage_file:
        storage_data = json.load(storage_file)

    post_keys = [key for key in storage_data.keys() if key.startswith("OBSTACLE_POST_")]
    if post_keys:
        post_numbers = [int(key.split("_")[-1]) for key in post_keys]
        next_key_number = max(post_numbers) + 1
    else:
        next_key_number = 1
    
    new_key = f"OBSTACLE_POST_{next_key_number}"

    storage_data[new_key] = config_data["OBSTACLE_POST"]

    with open(storage_path, "w") as storage_file:
        json.dump(storage_data, storage_file, indent=4)

    print(f"Added OBSTACLE_POST to {new_key} in config_storage.json and updated config.json.")

class GridApp:
    def __init__(self, root, size):
        self.root = root
        self.root.title("Grid App")
        self.cols, self.rows = size

        self.btn_color = "forestgreen"
        self.selected_key = None
        
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Frame for the grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure the rows and columns of the grid frame
        for i in range(self.rows):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.cols):
            self.grid_frame.grid_columnconfigure(j, weight=1)

        for i in range(self.rows):
            for j in range(self.cols):
                btn = tk.Button(self.grid_frame, bg="white", relief="flat", activebackground="white", 
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j, sticky="nsew")
                self.buttons[i][j] = btn
        
        # Frame for buttons
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Configure the grid to maintain an aspect ratio of 16:9
        self.grid_frame.grid_rowconfigure(0, weight=9)
        self.grid_frame.grid_columnconfigure(0, weight=16)


     

        self.save_button = tk.Button(self.buttons_frame, text="Save to Config", command=self.save_highlighted)
        self.save_button.pack(fill=tk.X, pady=5)
        
        self.save_to_storage_button = tk.Button(self.buttons_frame, text="Save to Storage", command=self.save_highlighted_to_storage)
        self.save_to_storage_button.pack(fill=tk.X, pady=5)
        
        self.create_new_key_button = tk.Button(self.buttons_frame, text="Create New Key", command=self.create_new_key)
        self.create_new_key_button.pack(fill=tk.X, pady=5)
        
        self.delete_key_button = tk.Button(self.buttons_frame, text="Delete Selected Key", command=self.delete_selected_key)
        self.delete_key_button.pack(fill=tk.X, pady=5)

        # Frame for the listbox
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

        self.listbox_label = tk.Label(self.listbox_frame, text="Select Obstacle Post:")
        self.listbox_label.pack(pady=(0, 5))

        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.listbox.bind('<<ListboxSelect>>', self.load_selected_list)

        self.root.bind('<Control-s>', self.save_highlighted)
        
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        self.load_obstacle_posts()

    def on_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["bg"] == "white":
            btn["bg"] = self.btn_color
            btn["activebackground"] = self.btn_color
        elif btn["bg"] == self.btn_color:
            btn["bg"] = "white"
            btn["activebackground"] = "white"

    def save_highlighted(self, event=None):
        highlighted = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j]["bg"] == self.btn_color:
                    highlighted.append((j, i))
        
        save_to_config_file(highlighted)
        print("Highlighted cells:", highlighted)

    def save_highlighted_to_storage(self):
        if self.selected_key is None:
            print("No list selected for saving.")
            return
        
        highlighted = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j]["bg"] == self.btn_color:
                    highlighted.append((j, i))
        
        storage_path = "config_storage.json"
        
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as storage_file:
                json.dump({}, storage_file)
        
        with open(storage_path, "r") as storage_file:
            storage_data = json.load(storage_file)
        
        highlighted_set = set(highlighted)
        if self.selected_key in storage_data:
            existing_set = set(storage_data[self.selected_key])
            if existing_set == highlighted_set:
                print(f"Exact same list already exists under key: {self.selected_key}")
                return
        
        storage_data[self.selected_key] = highlighted

        with open(storage_path, "w") as storage_file:
            json.dump(storage_data, storage_file, indent=4)

        print(f"Updated highlighted cells in {self.selected_key} in config_storage.json.")

    def load_obstacle_posts(self):
        storage_path = "config_storage.json"
        
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as storage_file:
                json.dump({}, storage_file)
        
        with open(storage_path, "r") as storage_file:
            storage_data = json.load(storage_file)
        
        self.listbox.delete(0, tk.END)
        for key in storage_data.keys():
            if key.startswith("OBSTACLE_POST_"):
                self.listbox.insert(tk.END, key)

    def load_selected_list(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        self.selected_key = self.listbox.get(selected_index)
        
        storage_path = "config_storage.json"
        
        with open(storage_path, "r") as storage_file:
            storage_data = json.load(storage_file)
        
        if self.selected_key in storage_data:
            obstacle_post = storage_data[self.selected_key]
            for i in range(self.rows):
                for j in range(self.cols):
                    self.buttons[i][j].config(bg="white", activebackground="white")
            for x, y in obstacle_post:
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    self.buttons[y][x].config(bg=self.btn_color, activebackground=self.btn_color)
        else:
            print(f"{self.selected_key} not found in config_storage.json.")

    def create_new_key(self):
        storage_path = "config_storage.json"
        
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as storage_file:
                json.dump({}, storage_file)
        
        with open(storage_path, "r") as storage_file:
            storage_data = json.load(storage_file)
        
        post_keys = [key for key in storage_data.keys() if key.startswith("OBSTACLE_POST_")]
        if post_keys:
            post_numbers = [int(key.split("_")[-1]) for key in post_keys]
            next_key_number = max(post_numbers) + 1
        else:
            next_key_number = 1
        
        new_key = f"OBSTACLE_POST_{next_key_number}"
        
        storage_data[new_key] = []

        with open(storage_path, "w") as storage_file:
            json.dump(storage_data, storage_file, indent=4)

        self.listbox.insert(tk.END, new_key)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(tk.END)
        self.listbox.event_generate('<<ListboxSelect>>')

        print(f"Created new key {new_key} with a blank list in config_storage.json.")

    def delete_selected_key(self):
        if self.selected_key is None:
            print("No key selected for deletion.")
            return
        
        storage_path = "config_storage.json"
        
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as storage_file:
                json.dump({}, storage_file)
        
        with open(storage_path, "r") as storage_file:
            storage_data = json.load(storage_file)
        
        if self.selected_key in storage_data:
            del storage_data[self.selected_key]
            
            with open(storage_path, "w") as storage_file:
                json.dump(storage_data, storage_file, indent=4)
            
            self.listbox.delete(self.listbox.curselection())
            self.selected_key = None
            
            print(f"Deleted key {self.selected_key} from config_storage.json.")
        else:
            print(f"{self.selected_key} not found in config_storage.json.")

# Create the main window
root = tk.Tk()

if not os.path.exists("config.json"):
    raise FileNotFoundError("config.json not found")

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

grid_size = (math.ceil(1920 / config_data["TERRAIN_SIZE"][0]), math.ceil(1080 / config_data["TERRAIN_SIZE"][1]))
app = GridApp(root, grid_size)

root.mainloop()
