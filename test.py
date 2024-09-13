import math
import tkinter as tk

import json
import os


import json
import os

import json
import os

import json
import os

def update_obstacle_post(new_obstacle_post):
    # Step 1: Open config.json and overwrite OBSTACLE_POST with new_obstacle_post
    config_path = "config.json"
    
    # Check if the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.json not found")
    
    # Load existing data from config.json
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
    
    # Update the OBSTACLE_POST key with the new list
    config_data["OBSTACLE_POST"] = new_obstacle_post
    
    # Save the updated config data back to config.json
    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    
    # Step 2: Open config_storage.json
    storage_path = "config_storage.json"
    
    # Check if the storage file exists; create an empty one if not
    if not os.path.exists(storage_path):
        with open(storage_path, "w") as storage_file:
            json.dump({}, storage_file)
    
    with open(storage_path, "r") as storage_file:
        storage_data = json.load(storage_file)

    # Step 3: Find the next available key following the pattern OBSTACLE_POST_#
    post_keys = [key for key in storage_data.keys() if key.startswith("OBSTACLE_POST_")]
    if post_keys:
        # Extract numbers and find the next available
        post_numbers = [int(key.split("_")[-1]) for key in post_keys]
        next_key_number = max(post_numbers) + 1
    else:
        next_key_number = 1
    
    new_key = f"OBSTACLE_POST_{next_key_number}"

    # Step 4: Append the value from the new list to the new key in config_storage.json
    storage_data[new_key] = config_data["OBSTACLE_POST"]

    # Step 5: Write the updated storage data back to config_storage.json
    with open(storage_path, "w") as storage_file:
        json.dump(storage_data, storage_file, indent=4)

    print(f"Added OBSTACLE_POST to {new_key} in config_storage.json and updated config.json.")




class GridApp:
    def __init__(self, root, size):
        self.root = root
        self.root.title("Grid App")
        self.cols  , self.rows,= size

        self.btn_color = "forestgreen"
        
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Configure the rows and columns to expand and fill the window dynamically
        for i in range(self.rows):
            self.root.grid_rowconfigure(i, weight=1)  # Allow rows to stretch
        for j in range(self.cols):
            self.root.grid_columnconfigure(j, weight=1)  # Allow columns to stretch
        
        # Create the grid of buttons
        for i in range(self.rows):
            for j in range(self.cols):
                btn = tk.Button(self.root, bg="white", relief="flat", activebackground="white", 
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j, sticky="nsew")  # sticky="nsew" ensures the button fills the cell
                self.buttons[i][j] = btn
        
        # Create Save button below the grid
         
        # Bind Ctrl + S to the save function
        self.root.bind('<Control-s>', self.save_highlighted)
    

    def on_click(self, row, col):
        # Change the color of the clicked button
        btn = self.buttons[row][col]
        if btn["bg"] == "white":
            btn["bg"] = self.btn_color
            btn["activebackground"] = self.btn_color  # Update activebackground to match
        elif btn["bg"] == self.btn_color:
            btn["bg"] = "white"
            btn["activebackground"] = "white"  # Update activebackground to match
    
   
    def save_highlighted(self, key = None):
        # key is from the control + s key bind
        # Collect the coordinates of highlighted self.btn_color cells (green)
        highlighted = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j]["bg"] == self.btn_color:  # Check if the button is highlighted self.btn_color (green)
                    highlighted.append((j, i))  # Store the coordinates as a tuple
        


        update_obstacle_post(highlighted)
        print("Highlighted cells:", highlighted)  # Print the result to the console (or process as needed)

# Create the main window
root = tk.Tk()




# load terrain size into editor
if not os.path.exists("config.json"):
    raise FileNotFoundError("config.json not found")

# Load existing data from config.json
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Create the grid with size (x, y)
grid_size = (math.ceil(1920 / config_data["TERRAIN_SIZE"][0]), math.ceil(1080 / config_data["TERRAIN_SIZE"][1]))
app = GridApp(root, grid_size)

# Start the application
root.mainloop()
