import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import tkinter as tk
import shutil

# A rimworld mod maker for creating mods with a simple interface.
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox, ttk
from tkinter import simpledialog, Frame, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH, END, BooleanVar, Checkbutton
from tkinter import StringVar, DoubleVar, IntVar, Listbox, SINGLE
from tkinter.ttk import Notebook

class ModMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rimworld Mod Maker")
        self.root.geometry("1000x700")
        
        # Variables to store mod information
        self.mod_name = ""
        self.mod_author = ""
        self.mod_description = ""
        self.mod_version = ""
        self.mod_directory = ""
        
        # Lists to store created items
        self.created_items = []
        self.created_weapons = []
        self.created_buildings = []
        self.created_research = []
        self.created_recipes = []
        
        # Lists to store file paths for assets
        self.item_textures = {}  # defName: texture_path
        self.item_sounds = {}    # defName: sound_path
        self.weapon_textures = {}
        self.weapon_sounds = {}
        self.building_textures = {}
        self.building_sounds = {}
        
        # Current asset paths (temporary storage)
        self.item_texture_path = None
        self.item_sound_path = None
        self.weapon_texture_path = None
        self.weapon_sound_path = None
        self.building_texture_path = None
        self.building_sound_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main scrollable frame
        main_canvas = tk.Canvas(self.root)
        main_scrollbar = Scrollbar(self.root, orient=VERTICAL, command=main_canvas.yview)
        scrollable_frame = Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(20, 0), pady=20)
        main_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Title
        title_label = Label(scrollable_frame, text="Rimworld Mod Maker", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = Notebook(scrollable_frame)
        self.notebook.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        # Mod Info Tab
        self.create_mod_info_tab()
        
        # Items Tab
        self.create_items_tab()
        
        # Weapons Tab
        self.create_weapons_tab()
        
        # Buildings Tab
        self.create_buildings_tab()
        
        # Research Tab
        self.create_research_tab()
        
        # Recipes Tab
        self.create_recipes_tab()
        
        # Final buttons
        button_frame = Frame(scrollable_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        Button(button_frame, text="Create Mod", command=self.create_mod, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 10))
        Button(button_frame, text="Clear All", command=self.clear_all).pack(side=LEFT)
        Button(button_frame, text="Exit", command=self.root.quit).pack(side=RIGHT)
    
    def create_mod_info_tab(self):
        # Mod Information Tab
        info_tab = Frame(self.notebook)
        self.notebook.add(info_tab, text="Mod Info")
        
        # Create scrollable frame for this tab
        info_canvas = tk.Canvas(info_tab)
        info_scrollbar = Scrollbar(info_tab, orient=VERTICAL, command=info_canvas.yview)
        info_scrollable_frame = Frame(info_canvas)
        
        info_scrollable_frame.bind(
            "<Configure>",
            lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all"))
        )
        
        info_canvas.create_window((0, 0), window=info_scrollable_frame, anchor="nw")
        info_canvas.configure(yscrollcommand=info_scrollbar.set)
        
        info_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        info_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        # Mod Information Section
        Label(info_scrollable_frame, text="Mod Information", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Mod Name
        Label(info_scrollable_frame, text="Mod Name:").pack(anchor="w", pady=(10, 0))
        self.name_entry = Entry(info_scrollable_frame, width=50)
        self.name_entry.pack(fill="x", pady=(5, 0))
        
        # Author
        Label(info_scrollable_frame, text="Author:").pack(anchor="w", pady=(10, 0))
        self.author_entry = Entry(info_scrollable_frame, width=50)
        self.author_entry.pack(fill="x", pady=(5, 0))
        
        # Version
        Label(info_scrollable_frame, text="Version:").pack(anchor="w", pady=(10, 0))
        self.version_entry = Entry(info_scrollable_frame, width=50)
        self.version_entry.insert(0, "1.0.0")
        self.version_entry.pack(fill="x", pady=(5, 0))
        
        # Description
        Label(info_scrollable_frame, text="Description:").pack(anchor="w", pady=(10, 0))
        desc_frame = Frame(info_scrollable_frame)
        desc_frame.pack(fill="x", pady=(5, 0))
        
        self.description_text = Text(desc_frame, height=4, width=50)
        desc_scrollbar = Scrollbar(desc_frame, orient=VERTICAL, command=self.description_text.yview)
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        self.description_text.pack(side=LEFT, fill=BOTH, expand=True)
        desc_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Directory Selection
        Label(info_scrollable_frame, text="Output Directory", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))
        
        dir_select_frame = Frame(info_scrollable_frame)
        dir_select_frame.pack(fill="x", pady=(0, 20))
        
        self.directory_label = Label(dir_select_frame, text="No directory selected", bg="white", relief="sunken", anchor="w")
        self.directory_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 10))
        
        Button(dir_select_frame, text="Browse", command=self.select_directory).pack(side=RIGHT)
        
        # Mod Components Section
        Label(info_scrollable_frame, text="Mod Components", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Checkboxes for different mod components
        self.include_defs = BooleanVar(value=True)
        self.include_patches = BooleanVar(value=False)
        self.include_assemblies = BooleanVar(value=False)
        self.include_textures = BooleanVar(value=False)
        self.include_sounds = BooleanVar(value=False)
        self.include_languages = BooleanVar(value=False)
        
        Checkbutton(info_scrollable_frame, text="Defs (XML definitions)", variable=self.include_defs).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Patches (XML patches)", variable=self.include_patches).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Assemblies (C# code)", variable=self.include_assemblies).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Textures", variable=self.include_textures).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Sounds", variable=self.include_sounds).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Languages", variable=self.include_languages).pack(anchor="w", pady=2)
    
    def create_items_tab(self):
        # Items Tab
        items_tab = Frame(self.notebook)
        self.notebook.add(items_tab, text="Items")
        
        # Create scrollable frame
        items_canvas = tk.Canvas(items_tab)
        items_scrollbar = Scrollbar(items_tab, orient=VERTICAL, command=items_canvas.yview)
        items_scrollable_frame = Frame(items_canvas)
        
        items_scrollable_frame.bind(
            "<Configure>",
            lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all"))
        )
        
        items_canvas.create_window((0, 0), window=items_scrollable_frame, anchor="nw")
        items_canvas.configure(yscrollcommand=items_scrollbar.set)
        
        items_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        items_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(items_scrollable_frame, text="Create Items", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Item form
        form_frame = Frame(items_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.item_defname = Entry(form_frame, width=30)
        self.item_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.item_label = Entry(form_frame, width=30)
        self.item_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.item_description = Entry(form_frame, width=30)
        self.item_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=3, column=0, sticky="w", pady=5)
        self.item_market_value = Entry(form_frame, width=30)
        self.item_market_value.insert(0, "10.0")
        self.item_market_value.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=4, column=0, sticky="w", pady=5)
        self.item_mass = Entry(form_frame, width=30)
        self.item_mass.insert(0, "0.1")
        self.item_mass.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Stack Limit
        Label(form_frame, text="Stack Limit:").grid(row=5, column=0, sticky="w", pady=5)
        self.item_stack_limit = Entry(form_frame, width=30)
        self.item_stack_limit.insert(0, "75")
        self.item_stack_limit.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Category
        Label(form_frame, text="Category:").grid(row=6, column=0, sticky="w", pady=5)
        self.item_category = ttk.Combobox(form_frame, width=27, values=[
            "ResourcesRaw", "Items", "Medicine", "Foods", "Manufactured", "Art"
        ])
        self.item_category.set("ResourcesRaw")
        self.item_category.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=7, column=0, sticky="w", pady=5)
        texture_frame = Frame(form_frame)
        texture_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.item_texture_label = Label(texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.item_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(texture_frame, text="Browse", command=self.select_item_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=8, column=0, sticky="w", pady=5)
        sound_frame = Frame(form_frame)
        sound_frame.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.item_sound_label = Label(sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.item_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(sound_frame, text="Browse", command=self.select_item_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(items_scrollable_frame, text="Add Item", command=self.add_item, bg="#2196F3", fg="white").pack(pady=10)
        
        # Items list
        Label(items_scrollable_frame, text="Created Items:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        items_list_frame = Frame(items_scrollable_frame)
        items_list_frame.pack(fill="both", expand=True)
        
        self.items_listbox = Listbox(items_list_frame, height=10)
        items_list_scrollbar = Scrollbar(items_list_frame, orient=VERTICAL, command=self.items_listbox.yview)
        self.items_listbox.configure(yscrollcommand=items_list_scrollbar.set)
        
        self.items_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        items_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(items_scrollable_frame, text="Remove Selected Item", command=self.remove_item, bg="#f44336", fg="white").pack(pady=10)
    
    def create_weapons_tab(self):
        # Weapons Tab
        weapons_tab = Frame(self.notebook)
        self.notebook.add(weapons_tab, text="Weapons")
        
        # Create scrollable frame
        weapons_canvas = tk.Canvas(weapons_tab)
        weapons_scrollbar = Scrollbar(weapons_tab, orient=VERTICAL, command=weapons_canvas.yview)
        weapons_scrollable_frame = Frame(weapons_canvas)
        
        weapons_scrollable_frame.bind(
            "<Configure>",
            lambda e: weapons_canvas.configure(scrollregion=weapons_canvas.bbox("all"))
        )
        
        weapons_canvas.create_window((0, 0), window=weapons_scrollable_frame, anchor="nw")
        weapons_canvas.configure(yscrollcommand=weapons_scrollbar.set)
        
        weapons_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        weapons_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(weapons_scrollable_frame, text="Create Weapons", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Weapon form
        form_frame = Frame(weapons_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.weapon_defname = Entry(form_frame, width=30)
        self.weapon_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.weapon_label = Entry(form_frame, width=30)
        self.weapon_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.weapon_description = Entry(form_frame, width=30)
        self.weapon_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Weapon Type
        Label(form_frame, text="Weapon Type:").grid(row=3, column=0, sticky="w", pady=5)
        self.weapon_type = ttk.Combobox(form_frame, width=27, values=[
            "Melee", "Ranged"
        ])
        self.weapon_type.set("Melee")
        self.weapon_type.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Damage
        Label(form_frame, text="Damage:").grid(row=4, column=0, sticky="w", pady=5)
        self.weapon_damage = Entry(form_frame, width=30)
        self.weapon_damage.insert(0, "10")
        self.weapon_damage.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Damage Type
        Label(form_frame, text="Damage Type:").grid(row=5, column=0, sticky="w", pady=5)
        self.weapon_damage_type = ttk.Combobox(form_frame, width=27, values=[
            "Blunt", "Cut", "Bullet", "Bomb", "Flame"
        ])
        self.weapon_damage_type.set("Cut")
        self.weapon_damage_type.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=6, column=0, sticky="w", pady=5)
        self.weapon_market_value = Entry(form_frame, width=30)
        self.weapon_market_value.insert(0, "100.0")
        self.weapon_market_value.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=7, column=0, sticky="w", pady=5)
        self.weapon_mass = Entry(form_frame, width=30)
        self.weapon_mass.insert(0, "1.5")
        self.weapon_mass.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=8, column=0, sticky="w", pady=5)
        weapon_texture_frame = Frame(form_frame)
        weapon_texture_frame.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.weapon_texture_label = Label(weapon_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.weapon_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(weapon_texture_frame, text="Browse", command=self.select_weapon_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=9, column=0, sticky="w", pady=5)
        weapon_sound_frame = Frame(form_frame)
        weapon_sound_frame.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.weapon_sound_label = Label(weapon_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.weapon_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(weapon_sound_frame, text="Browse", command=self.select_weapon_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(weapons_scrollable_frame, text="Add Weapon", command=self.add_weapon, bg="#2196F3", fg="white").pack(pady=10)
        
        # Weapons list
        Label(weapons_scrollable_frame, text="Created Weapons:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        weapons_list_frame = Frame(weapons_scrollable_frame)
        weapons_list_frame.pack(fill="both", expand=True)
        
        self.weapons_listbox = Listbox(weapons_list_frame, height=10)
        weapons_list_scrollbar = Scrollbar(weapons_list_frame, orient=VERTICAL, command=self.weapons_listbox.yview)
        self.weapons_listbox.configure(yscrollcommand=weapons_list_scrollbar.set)
        
        self.weapons_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        weapons_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(weapons_scrollable_frame, text="Remove Selected Weapon", command=self.remove_weapon, bg="#f44336", fg="white").pack(pady=10)
    
    def create_buildings_tab(self):
        # Buildings Tab
        buildings_tab = Frame(self.notebook)
        self.notebook.add(buildings_tab, text="Buildings")
        
        # Create scrollable frame
        buildings_canvas = tk.Canvas(buildings_tab)
        buildings_scrollbar = Scrollbar(buildings_tab, orient=VERTICAL, command=buildings_canvas.yview)
        buildings_scrollable_frame = Frame(buildings_canvas)
        
        buildings_scrollable_frame.bind(
            "<Configure>",
            lambda e: buildings_canvas.configure(scrollregion=buildings_canvas.bbox("all"))
        )
        
        buildings_canvas.create_window((0, 0), window=buildings_scrollable_frame, anchor="nw")
        buildings_canvas.configure(yscrollcommand=buildings_scrollbar.set)
        
        buildings_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        buildings_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(buildings_scrollable_frame, text="Create Buildings", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Building form
        form_frame = Frame(buildings_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.building_defname = Entry(form_frame, width=30)
        self.building_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.building_label = Entry(form_frame, width=30)
        self.building_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.building_description = Entry(form_frame, width=30)
        self.building_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Size
        Label(form_frame, text="Size (e.g., 1,1):").grid(row=3, column=0, sticky="w", pady=5)
        self.building_size = Entry(form_frame, width=30)
        self.building_size.insert(0, "1,1")
        self.building_size.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Hit Points
        Label(form_frame, text="Hit Points:").grid(row=4, column=0, sticky="w", pady=5)
        self.building_hitpoints = Entry(form_frame, width=30)
        self.building_hitpoints.insert(0, "100")
        self.building_hitpoints.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work to Make
        Label(form_frame, text="Work to Make:").grid(row=5, column=0, sticky="w", pady=5)
        self.building_work = Entry(form_frame, width=30)
        self.building_work.insert(0, "500")
        self.building_work.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=6, column=0, sticky="w", pady=5)
        building_texture_frame = Frame(form_frame)
        building_texture_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.building_texture_label = Label(building_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.building_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(building_texture_frame, text="Browse", command=self.select_building_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=7, column=0, sticky="w", pady=5)
        building_sound_frame = Frame(form_frame)
        building_sound_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.building_sound_label = Label(building_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.building_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(building_sound_frame, text="Browse", command=self.select_building_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(buildings_scrollable_frame, text="Add Building", command=self.add_building, bg="#2196F3", fg="white").pack(pady=10)
        
        # Buildings list
        Label(buildings_scrollable_frame, text="Created Buildings:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        buildings_list_frame = Frame(buildings_scrollable_frame)
        buildings_list_frame.pack(fill="both", expand=True)
        
        self.buildings_listbox = Listbox(buildings_list_frame, height=10)
        buildings_list_scrollbar = Scrollbar(buildings_list_frame, orient=VERTICAL, command=self.buildings_listbox.yview)
        self.buildings_listbox.configure(yscrollcommand=buildings_list_scrollbar.set)
        
        self.buildings_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        buildings_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(buildings_scrollable_frame, text="Remove Selected Building", command=self.remove_building, bg="#f44336", fg="white").pack(pady=10)
    
    def create_research_tab(self):
        # Research Tab
        research_tab = Frame(self.notebook)
        self.notebook.add(research_tab, text="Research")
        
        # Create scrollable frame
        research_canvas = tk.Canvas(research_tab)
        research_scrollbar = Scrollbar(research_tab, orient=VERTICAL, command=research_canvas.yview)
        research_scrollable_frame = Frame(research_canvas)
        
        research_scrollable_frame.bind(
            "<Configure>",
            lambda e: research_canvas.configure(scrollregion=research_canvas.bbox("all"))
        )
        
        research_canvas.create_window((0, 0), window=research_scrollable_frame, anchor="nw")
        research_canvas.configure(yscrollcommand=research_scrollbar.set)
        
        research_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        research_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(research_scrollable_frame, text="Create Research Projects", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Research form
        form_frame = Frame(research_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.research_defname = Entry(form_frame, width=30)
        self.research_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.research_label = Entry(form_frame, width=30)
        self.research_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.research_description = Entry(form_frame, width=30)
        self.research_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Base Cost
        Label(form_frame, text="Base Cost:").grid(row=3, column=0, sticky="w", pady=5)
        self.research_cost = Entry(form_frame, width=30)
        self.research_cost.insert(0, "500")
        self.research_cost.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Tech Level
        Label(form_frame, text="Tech Level:").grid(row=4, column=0, sticky="w", pady=5)
        self.research_tech_level = ttk.Combobox(form_frame, width=27, values=[
            "Neolithic", "Medieval", "Industrial", "Spacer", "Ultra"
        ])
        self.research_tech_level.set("Industrial")
        self.research_tech_level.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(research_scrollable_frame, text="Add Research", command=self.add_research, bg="#2196F3", fg="white").pack(pady=10)
        
        # Research list
        Label(research_scrollable_frame, text="Created Research:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        research_list_frame = Frame(research_scrollable_frame)
        research_list_frame.pack(fill="both", expand=True)
        
        self.research_listbox = Listbox(research_list_frame, height=10)
        research_list_scrollbar = Scrollbar(research_list_frame, orient=VERTICAL, command=self.research_listbox.yview)
        self.research_listbox.configure(yscrollcommand=research_list_scrollbar.set)
        
        self.research_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        research_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(research_scrollable_frame, text="Remove Selected Research", command=self.remove_research, bg="#f44336", fg="white").pack(pady=10)
    
    def create_recipes_tab(self):
        # Recipes Tab
        recipes_tab = Frame(self.notebook)
        self.notebook.add(recipes_tab, text="Recipes")
        
        # Create scrollable frame
        recipes_canvas = tk.Canvas(recipes_tab)
        recipes_scrollbar = Scrollbar(recipes_tab, orient=VERTICAL, command=recipes_canvas.yview)
        recipes_scrollable_frame = Frame(recipes_canvas)
        
        recipes_scrollable_frame.bind(
            "<Configure>",
            lambda e: recipes_canvas.configure(scrollregion=recipes_canvas.bbox("all"))
        )
        
        recipes_canvas.create_window((0, 0), window=recipes_scrollable_frame, anchor="nw")
        recipes_canvas.configure(yscrollcommand=recipes_scrollbar.set)
        
        recipes_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        recipes_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(recipes_scrollable_frame, text="Create Recipes", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Recipe form
        form_frame = Frame(recipes_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.recipe_defname = Entry(form_frame, width=30)
        self.recipe_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.recipe_label = Entry(form_frame, width=30)
        self.recipe_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.recipe_description = Entry(form_frame, width=30)
        self.recipe_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work Amount
        Label(form_frame, text="Work Amount:").grid(row=3, column=0, sticky="w", pady=5)
        self.recipe_work = Entry(form_frame, width=30)
        self.recipe_work.insert(0, "100")
        self.recipe_work.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Product Def Name
        Label(form_frame, text="Product Def Name:").grid(row=4, column=0, sticky="w", pady=5)
        self.recipe_product = Entry(form_frame, width=30)
        self.recipe_product.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Product Count
        Label(form_frame, text="Product Count:").grid(row=5, column=0, sticky="w", pady=5)
        self.recipe_product_count = Entry(form_frame, width=30)
        self.recipe_product_count.insert(0, "1")
        self.recipe_product_count.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Ingredients (simplified)
        Label(form_frame, text="Ingredients (format: DefName:Count):").grid(row=6, column=0, sticky="w", pady=5)
        self.recipe_ingredients = Entry(form_frame, width=30)
        self.recipe_ingredients.insert(0, "Steel:5")
        self.recipe_ingredients.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(recipes_scrollable_frame, text="Add Recipe", command=self.add_recipe, bg="#2196F3", fg="white").pack(pady=10)
        
        # Recipes list
        Label(recipes_scrollable_frame, text="Created Recipes:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        recipes_list_frame = Frame(recipes_scrollable_frame)
        recipes_list_frame.pack(fill="both", expand=True)
        
        self.recipes_listbox = Listbox(recipes_list_frame, height=10)
        recipes_list_scrollbar = Scrollbar(recipes_list_frame, orient=VERTICAL, command=self.recipes_listbox.yview)
        self.recipes_listbox.configure(yscrollcommand=recipes_list_scrollbar.set)
        
        self.recipes_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        recipes_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(recipes_scrollable_frame, text="Remove Selected Recipe", command=self.remove_recipe, bg="#f44336", fg="white").pack(pady=10)
        directory = filedialog.askdirectory(title="Select output directory for mod")
        if directory:
            self.mod_directory = directory
            self.directory_label.config(text=directory)
    
    def clear_form(self):
        self.name_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.version_entry.delete(0, END)
        self.version_entry.insert(0, "1.0.0")
        self.description_text.delete(1.0, END)
        self.directory_label.config(text="No directory selected")
        self.mod_directory = ""

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select output directory for mod")
        if directory:
            self.mod_directory = directory
            self.directory_label.config(text=directory)
    
    # Asset selection methods
    def select_item_texture(self):
        file_path = filedialog.askopenfilename(
            title="Select Item Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.item_texture_path = file_path
            self.item_texture_label.config(text=os.path.basename(file_path))
    
    def select_item_sound(self):
        file_path = filedialog.askopenfilename(
            title="Select Item Sound",
            filetypes=[("Audio files", "*.wav *.ogg *.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.item_sound_path = file_path
            self.item_sound_label.config(text=os.path.basename(file_path))
    
    def select_weapon_texture(self):
        file_path = filedialog.askopenfilename(
            title="Select Weapon Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.weapon_texture_path = file_path
            self.weapon_texture_label.config(text=os.path.basename(file_path))
    
    def select_weapon_sound(self):
        file_path = filedialog.askopenfilename(
            title="Select Weapon Sound",
            filetypes=[("Audio files", "*.wav *.ogg *.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.weapon_sound_path = file_path
            self.weapon_sound_label.config(text=os.path.basename(file_path))
    
    def select_building_texture(self):
        file_path = filedialog.askopenfilename(
            title="Select Building Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.building_texture_path = file_path
            self.building_texture_label.config(text=os.path.basename(file_path))
    
    def select_building_sound(self):
        file_path = filedialog.askopenfilename(
            title="Select Building Sound",
            filetypes=[("Audio files", "*.wav *.ogg *.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.building_sound_path = file_path
            self.building_sound_label.config(text=os.path.basename(file_path))
    
    def clear_all(self):
        self.clear_form()
        self.created_items.clear()
        self.created_weapons.clear()
        self.created_buildings.clear()
        self.created_research.clear()
        self.created_recipes.clear()
        
        # Clear asset dictionaries
        self.item_textures.clear()
        self.item_sounds.clear()
        self.weapon_textures.clear()
        self.weapon_sounds.clear()
        self.building_textures.clear()
        self.building_sounds.clear()
        
        # Clear listboxes
        if hasattr(self, 'items_listbox'):
            self.items_listbox.delete(0, END)
        if hasattr(self, 'weapons_listbox'):
            self.weapons_listbox.delete(0, END)
        if hasattr(self, 'buildings_listbox'):
            self.buildings_listbox.delete(0, END)
        if hasattr(self, 'research_listbox'):
            self.research_listbox.delete(0, END)
        if hasattr(self, 'recipes_listbox'):
            self.recipes_listbox.delete(0, END)
    
    def clear_form(self):
        self.name_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.version_entry.delete(0, END)
        self.version_entry.insert(0, "1.0.0")
        self.description_text.delete(1.0, END)
        self.directory_label.config(text="No directory selected")
        self.mod_directory = ""
    
    # Item management methods
    def add_item(self):
        item_data = {
            'defName': self.item_defname.get().strip(),
            'label': self.item_label.get().strip(),
            'description': self.item_description.get().strip(),
            'marketValue': self.item_market_value.get().strip(),
            'mass': self.item_mass.get().strip(),
            'stackLimit': self.item_stack_limit.get().strip(),
            'category': self.item_category.get()
        }
        
        if not item_data['defName'] or not item_data['label']:
            messagebox.showerror("Error", "Def Name and Label are required!")
            return
        
        self.created_items.append(item_data)
        self.items_listbox.insert(END, f"{item_data['defName']} - {item_data['label']}")
        
        # Store asset paths if selected
        if hasattr(self, 'item_texture_path') and self.item_texture_path:
            self.item_textures[item_data['defName']] = self.item_texture_path
        if hasattr(self, 'item_sound_path') and self.item_sound_path:
            self.item_sounds[item_data['defName']] = self.item_sound_path
        
        # Clear form
        self.item_defname.delete(0, END)
        self.item_label.delete(0, END)
        self.item_description.delete(0, END)
        self.item_market_value.delete(0, END)
        self.item_market_value.insert(0, "10.0")
        self.item_mass.delete(0, END)
        self.item_mass.insert(0, "0.1")
        self.item_stack_limit.delete(0, END)
        self.item_stack_limit.insert(0, "75")
        
        # Clear asset selections
        self.item_texture_path = None
        self.item_sound_path = None
        self.item_texture_label.config(text="No texture selected")
        self.item_sound_label.config(text="No sound selected")
    
    def remove_item(self):
        selection = self.items_listbox.curselection()
        if selection:
            index = selection[0]
            self.created_items.pop(index)
            self.items_listbox.delete(index)
    
    # Weapon management methods
    def add_weapon(self):
        weapon_data = {
            'defName': self.weapon_defname.get().strip(),
            'label': self.weapon_label.get().strip(),
            'description': self.weapon_description.get().strip(),
            'weaponType': self.weapon_type.get(),
            'damage': self.weapon_damage.get().strip(),
            'damageType': self.weapon_damage_type.get(),
            'marketValue': self.weapon_market_value.get().strip(),
            'mass': self.weapon_mass.get().strip()
        }
        
        if not weapon_data['defName'] or not weapon_data['label']:
            messagebox.showerror("Error", "Def Name and Label are required!")
            return
        
        self.created_weapons.append(weapon_data)
        self.weapons_listbox.insert(END, f"{weapon_data['defName']} - {weapon_data['label']}")
        
        # Store asset paths if selected
        if hasattr(self, 'weapon_texture_path') and self.weapon_texture_path:
            self.weapon_textures[weapon_data['defName']] = self.weapon_texture_path
        if hasattr(self, 'weapon_sound_path') and self.weapon_sound_path:
            self.weapon_sounds[weapon_data['defName']] = self.weapon_sound_path
        
        # Clear form
        self.weapon_defname.delete(0, END)
        self.weapon_label.delete(0, END)
        self.weapon_description.delete(0, END)
        self.weapon_damage.delete(0, END)
        self.weapon_damage.insert(0, "10")
        self.weapon_market_value.delete(0, END)
        self.weapon_market_value.insert(0, "100.0")
        self.weapon_mass.delete(0, END)
        self.weapon_mass.insert(0, "1.5")
        
        # Clear asset selections
        self.weapon_texture_path = None
        self.weapon_sound_path = None
        self.weapon_texture_label.config(text="No texture selected")
        self.weapon_sound_label.config(text="No sound selected")
    
    def remove_weapon(self):
        selection = self.weapons_listbox.curselection()
        if selection:
            index = selection[0]
            self.created_weapons.pop(index)
            self.weapons_listbox.delete(index)
    
    # Building management methods
    def add_building(self):
        building_data = {
            'defName': self.building_defname.get().strip(),
            'label': self.building_label.get().strip(),
            'description': self.building_description.get().strip(),
            'size': self.building_size.get().strip(),
            'hitpoints': self.building_hitpoints.get().strip(),
            'work': self.building_work.get().strip()
        }
        
        if not building_data['defName'] or not building_data['label']:
            messagebox.showerror("Error", "Def Name and Label are required!")
            return
        
        self.created_buildings.append(building_data)
        self.buildings_listbox.insert(END, f"{building_data['defName']} - {building_data['label']}")
        
        # Store asset paths if selected
        if hasattr(self, 'building_texture_path') and self.building_texture_path:
            self.building_textures[building_data['defName']] = self.building_texture_path
        if hasattr(self, 'building_sound_path') and self.building_sound_path:
            self.building_sounds[building_data['defName']] = self.building_sound_path
        
        # Clear form
        self.building_defname.delete(0, END)
        self.building_label.delete(0, END)
        self.building_description.delete(0, END)
        self.building_size.delete(0, END)
        self.building_size.insert(0, "1,1")
        self.building_hitpoints.delete(0, END)
        self.building_hitpoints.insert(0, "100")
        self.building_work.delete(0, END)
        self.building_work.insert(0, "500")
        
        # Clear asset selections
        self.building_texture_path = None
        self.building_sound_path = None
        self.building_texture_label.config(text="No texture selected")
        self.building_sound_label.config(text="No sound selected")
    
    def remove_building(self):
        selection = self.buildings_listbox.curselection()
        if selection:
            index = selection[0]
            self.created_buildings.pop(index)
            self.buildings_listbox.delete(index)
    
    # Research management methods
    def add_research(self):
        research_data = {
            'defName': self.research_defname.get().strip(),
            'label': self.research_label.get().strip(),
            'description': self.research_description.get().strip(),
            'cost': self.research_cost.get().strip(),
            'techLevel': self.research_tech_level.get()
        }
        
        if not research_data['defName'] or not research_data['label']:
            messagebox.showerror("Error", "Def Name and Label are required!")
            return
        
        self.created_research.append(research_data)
        self.research_listbox.insert(END, f"{research_data['defName']} - {research_data['label']}")
        
        # Clear form
        self.research_defname.delete(0, END)
        self.research_label.delete(0, END)
        self.research_description.delete(0, END)
        self.research_cost.delete(0, END)
        self.research_cost.insert(0, "500")
    
    def remove_research(self):
        selection = self.research_listbox.curselection()
        if selection:
            index = selection[0]
            self.created_research.pop(index)
            self.research_listbox.delete(index)
    
    # Recipe management methods
    def add_recipe(self):
        recipe_data = {
            'defName': self.recipe_defname.get().strip(),
            'label': self.recipe_label.get().strip(),
            'description': self.recipe_description.get().strip(),
            'work': self.recipe_work.get().strip(),
            'product': self.recipe_product.get().strip(),
            'productCount': self.recipe_product_count.get().strip(),
            'ingredients': self.recipe_ingredients.get().strip()
        }
        
        if not recipe_data['defName'] or not recipe_data['label']:
            messagebox.showerror("Error", "Def Name and Label are required!")
            return
        
        self.created_recipes.append(recipe_data)
        self.recipes_listbox.insert(END, f"{recipe_data['defName']} - {recipe_data['label']}")
        
        # Clear form
        self.recipe_defname.delete(0, END)
        self.recipe_label.delete(0, END)
        self.recipe_description.delete(0, END)
        self.recipe_work.delete(0, END)
        self.recipe_work.insert(0, "100")
        self.recipe_product.delete(0, END)
        self.recipe_product_count.delete(0, END)
        self.recipe_product_count.insert(0, "1")
        self.recipe_ingredients.delete(0, END)
        self.recipe_ingredients.insert(0, "Steel:5")
    
    def remove_recipe(self):
        selection = self.recipes_listbox.curselection()
        if selection:
            index = selection[0]
            self.created_recipes.pop(index)
            self.recipes_listbox.delete(index)

    def validate_inputs(self):
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Mod name is required!")
            return False
        
        if not self.author_entry.get().strip():
            messagebox.showerror("Error", "Author name is required!")
            return False
        
        if not self.mod_directory:
            messagebox.showerror("Error", "Please select an output directory!")
            return False
        
        return True
    
    def create_mod(self):
        if not self.validate_inputs():
            return
        
        # Get values from form
        self.mod_name = self.name_entry.get().strip()
        self.mod_author = self.author_entry.get().strip()
        self.mod_version = self.version_entry.get().strip()
        self.mod_description = self.description_text.get(1.0, END).strip()
        
        try:
            # Create mod directory structure
            mod_path = os.path.join(self.mod_directory, self.mod_name)
            os.makedirs(mod_path, exist_ok=True)
            
            # Create About folder and About.xml
            self.create_about_xml(mod_path)
            
            # Create Defs folder if selected and generate XMLs for created items
            if self.include_defs.get():
                self.create_defs_folder(mod_path)
                self.generate_item_xmls(mod_path)
                self.generate_weapon_xmls(mod_path)
                self.generate_building_xmls(mod_path)
                self.generate_research_xmls(mod_path)
                self.generate_recipe_xmls(mod_path)
            
            # Create Patches folder if selected
            if self.include_patches.get():
                self.create_patches_folder(mod_path)
            
            # Create Assemblies folder if selected
            if self.include_assemblies.get():
                self.create_assemblies_folder(mod_path)
            
            # Create Textures folder if selected
            if self.include_textures.get():
                self.create_textures_folder(mod_path)
            
            # Create Sounds folder if selected
            if self.include_sounds.get():
                self.create_sounds_folder(mod_path)
            
            # Create Languages folder if selected
            if self.include_languages.get():
                self.create_languages_folder(mod_path)
            
            # Copy assets to mod directory
            self.copy_assets_to_mod(mod_path)
            
            messagebox.showinfo("Success", f"Mod '{self.mod_name}' created successfully at:\n{mod_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create mod: {str(e)}")
    
    def copy_assets_to_mod(self, mod_path):
        """Copy all selected assets to the appropriate mod directories"""
        try:
            # Copy item textures
            for def_name, texture_path in self.item_textures.items():
                if os.path.exists(texture_path):
                    dest_dir = os.path.join(mod_path, "Textures", "Things", "Item")
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_file = os.path.join(dest_dir, f"{def_name}.png")
                    shutil.copy2(texture_path, dest_file)
            
            # Copy item sounds
            for def_name, sound_path in self.item_sounds.items():
                if os.path.exists(sound_path):
                    dest_dir = os.path.join(mod_path, "Sounds", "Items")
                    os.makedirs(dest_dir, exist_ok=True)
                    file_ext = os.path.splitext(sound_path)[1]
                    dest_file = os.path.join(dest_dir, f"{def_name}{file_ext}")
                    shutil.copy2(sound_path, dest_file)
            
            # Copy weapon textures
            for def_name, texture_path in self.weapon_textures.items():
                if os.path.exists(texture_path):
                    dest_dir = os.path.join(mod_path, "Textures", "Things", "Item", "Equipment", "WeaponMelee")
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_file = os.path.join(dest_dir, f"{def_name}.png")
                    shutil.copy2(texture_path, dest_file)
            
            # Copy weapon sounds
            for def_name, sound_path in self.weapon_sounds.items():
                if os.path.exists(sound_path):
                    dest_dir = os.path.join(mod_path, "Sounds", "Weapons")
                    os.makedirs(dest_dir, exist_ok=True)
                    file_ext = os.path.splitext(sound_path)[1]
                    dest_file = os.path.join(dest_dir, f"{def_name}{file_ext}")
                    shutil.copy2(sound_path, dest_file)
            
            # Copy building textures
            for def_name, texture_path in self.building_textures.items():
                if os.path.exists(texture_path):
                    dest_dir = os.path.join(mod_path, "Textures", "Things", "Building")
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_file = os.path.join(dest_dir, f"{def_name}.png")
                    shutil.copy2(texture_path, dest_file)
            
            # Copy building sounds
            for def_name, sound_path in self.building_sounds.items():
                if os.path.exists(sound_path):
                    dest_dir = os.path.join(mod_path, "Sounds", "Buildings")
                    os.makedirs(dest_dir, exist_ok=True)
                    file_ext = os.path.splitext(sound_path)[1]
                    dest_file = os.path.join(dest_dir, f"{def_name}{file_ext}")
                    shutil.copy2(sound_path, dest_file)
                    
        except Exception as e:
            print(f"Warning: Failed to copy some assets: {str(e)}")
    
    def generate_item_xmls(self, mod_path):
        if not self.created_items:
            return
        
        defs_path = os.path.join(mod_path, "Defs")
        
        # Create XML structure
        root = ET.Element("Defs")
        
        for item in self.created_items:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="ResourceBase")
            
            # Basic info
            def_name = ET.SubElement(thing_def, "defName")
            def_name.text = item['defName']
            
            label = ET.SubElement(thing_def, "label")
            label.text = item['label']
            
            description = ET.SubElement(thing_def, "description")
            description.text = item['description']
            
            # Graphics
            graphic_data = ET.SubElement(thing_def, "graphicData")
            tex_path = ET.SubElement(graphic_data, "texPath")
            tex_path.text = f"Things/Item/{item['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_StackCount"
            
            # Stack limit
            stack_limit = ET.SubElement(thing_def, "stackLimit")
            stack_limit.text = item['stackLimit']
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = item['marketValue']
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = item['mass']
            
            # Categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            category = ET.SubElement(thing_categories, "li")
            category.text = item['category']
        
        # Save XML
        self.save_xml_file(root, os.path.join(defs_path, "Items.xml"))
    
    def generate_weapon_xmls(self, mod_path):
        if not self.created_weapons:
            return
        
        defs_path = os.path.join(mod_path, "Defs")
        
        # Create XML structure
        root = ET.Element("Defs")
        
        for weapon in self.created_weapons:
            parent_name = "BaseMeleeWeapon_Sharp" if weapon['weaponType'] == "Melee" else "BaseGun"
            thing_def = ET.SubElement(root, "ThingDef", ParentName=parent_name)
            
            # Basic info
            def_name = ET.SubElement(thing_def, "defName")
            def_name.text = weapon['defName']
            
            label = ET.SubElement(thing_def, "label")
            label.text = weapon['label']
            
            description = ET.SubElement(thing_def, "description")
            description.text = weapon['description']
            
            # Graphics
            graphic_data = ET.SubElement(thing_def, "graphicData")
            tex_path = ET.SubElement(graphic_data, "texPath")
            tex_path.text = f"Things/Item/Equipment/WeaponMelee/{weapon['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Single"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = weapon['marketValue']
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = weapon['mass']
            
            # Weapon stats (for melee weapons)
            if weapon['weaponType'] == "Melee":
                melee_damage_base_amount = ET.SubElement(stat_bases, "MeleeWeapon_DamageMultiplier")
                melee_damage_base_amount.text = "1.0"
        
        # Save XML
        self.save_xml_file(root, os.path.join(defs_path, "Weapons.xml"))
    
    def generate_building_xmls(self, mod_path):
        if not self.created_buildings:
            return
        
        defs_path = os.path.join(mod_path, "Defs")
        
        # Create XML structure
        root = ET.Element("Defs")
        
        for building in self.created_buildings:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="BuildingBase")
            
            # Basic info
            def_name = ET.SubElement(thing_def, "defName")
            def_name.text = building['defName']
            
            label = ET.SubElement(thing_def, "label")
            label.text = building['label']
            
            description = ET.SubElement(thing_def, "description")
            description.text = building['description']
            
            # Graphics
            graphic_data = ET.SubElement(thing_def, "graphicData")
            tex_path = ET.SubElement(graphic_data, "texPath")
            tex_path.text = f"Things/Building/{building['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Single"
            
            # Size
            size_parts = building['size'].split(',')
            size_elem = ET.SubElement(thing_def, "size")
            size_elem.text = f"({size_parts[0]},{size_parts[1]})"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            max_hit_points = ET.SubElement(stat_bases, "MaxHitPoints")
            max_hit_points.text = building['hitpoints']
            work_to_make = ET.SubElement(stat_bases, "WorkToBuild")
            work_to_make.text = building['work']
        
        # Save XML
        self.save_xml_file(root, os.path.join(defs_path, "Buildings.xml"))
    
    def generate_research_xmls(self, mod_path):
        if not self.created_research:
            return
        
        defs_path = os.path.join(mod_path, "Defs")
        
        # Create XML structure
        root = ET.Element("Defs")
        
        for research in self.created_research:
            research_def = ET.SubElement(root, "ResearchProjectDef")
            
            # Basic info
            def_name = ET.SubElement(research_def, "defName")
            def_name.text = research['defName']
            
            label = ET.SubElement(research_def, "label")
            label.text = research['label']
            
            description = ET.SubElement(research_def, "description")
            description.text = research['description']
            
            # Cost
            base_cost = ET.SubElement(research_def, "baseCost")
            base_cost.text = research['cost']
            
            # Tech level
            tech_level = ET.SubElement(research_def, "techLevel")
            tech_level.text = research['techLevel']
        
        # Save XML
        self.save_xml_file(root, os.path.join(defs_path, "Research.xml"))
    
    def generate_recipe_xmls(self, mod_path):
        if not self.created_recipes:
            return
        
        defs_path = os.path.join(mod_path, "Defs")
        
        # Create XML structure
        root = ET.Element("Defs")
        
        for recipe in self.created_recipes:
            recipe_def = ET.SubElement(root, "RecipeDef")
            
            # Basic info
            def_name = ET.SubElement(recipe_def, "defName")
            def_name.text = recipe['defName']
            
            label = ET.SubElement(recipe_def, "label")
            label.text = recipe['label']
            
            description = ET.SubElement(recipe_def, "description")
            description.text = recipe['description']
            
            # Work amount
            work_amount = ET.SubElement(recipe_def, "workAmount")
            work_amount.text = recipe['work']
            
            # Ingredients
            ingredients = ET.SubElement(recipe_def, "ingredients")
            ingredient_parts = recipe['ingredients'].split(':')
            if len(ingredient_parts) == 2:
                ingredient = ET.SubElement(ingredients, "li")
                filter_elem = ET.SubElement(ingredient, "filter")
                thing_defs = ET.SubElement(filter_elem, "thingDefs")
                li_elem = ET.SubElement(thing_defs, "li")
                li_elem.text = ingredient_parts[0]
                count_elem = ET.SubElement(ingredient, "count")
                count_elem.text = ingredient_parts[1]
            
            # Products
            products = ET.SubElement(recipe_def, "products")
            product = ET.SubElement(products, recipe['product'])
            product.text = recipe['productCount']
        
        # Save XML
        self.save_xml_file(root, os.path.join(defs_path, "Recipes.xml"))
    
    def save_xml_file(self, root, file_path):
        # Format and save XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(xml_str.split('\n', 1)[1])  # Remove the first XML declaration line
    
    def create_about_xml(self, mod_path):
        about_path = os.path.join(mod_path, "About")
        os.makedirs(about_path, exist_ok=True)
        
        # Create About.xml
        root = ET.Element("ModMetaData")
        
        name_elem = ET.SubElement(root, "name")
        name_elem.text = self.mod_name
        
        author_elem = ET.SubElement(root, "author")
        author_elem.text = self.mod_author
        
        version_elem = ET.SubElement(root, "packageId")
        version_elem.text = f"{self.mod_author.lower().replace(' ', '')}.{self.mod_name.lower().replace(' ', '')}"
        
        supported_versions = ET.SubElement(root, "supportedVersions")
        version_li = ET.SubElement(supported_versions, "li")
        version_li.text = "1.4"
        version_li2 = ET.SubElement(supported_versions, "li")
        version_li2.text = "1.5"
        
        description_elem = ET.SubElement(root, "description")
        description_elem.text = self.mod_description if self.mod_description else f"A mod created with Rimworld Mod Maker."
        
        # Format and save XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])
        
        with open(os.path.join(about_path, "About.xml"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(xml_str.split('\n', 1)[1])  # Remove the first XML declaration line
    
    def create_defs_folder(self, mod_path):
        defs_path = os.path.join(mod_path, "Defs")
        os.makedirs(defs_path, exist_ok=True)
        
        # Create example ThingDef
        example_def = '''<?xml version="1.0" encoding="utf-8"?>
<Defs>
  <!-- Example ThingDef - Remove or modify as needed -->
  <!--
  <ThingDef ParentName="ResourceBase">
    <defName>ExampleResource</defName>
    <label>example resource</label>
    <description>An example resource created by the mod maker.</description>
    <graphicData>
      <texPath>Things/Item/Resource/ExampleResource</texPath>
      <graphicClass>Graphic_StackCount</graphicClass>
    </graphicData>
    <stackLimit>75</stackLimit>
    <statBases>
      <MarketValue>2.0</MarketValue>
      <Mass>0.1</Mass>
    </statBases>
    <thingCategories>
      <li>ResourcesRaw</li>
    </thingCategories>
  </ThingDef>
  -->
</Defs>'''
        
        with open(os.path.join(defs_path, "ExampleDefs.xml"), "w", encoding="utf-8") as f:
            f.write(example_def)
    
    def create_patches_folder(self, mod_path):
        patches_path = os.path.join(mod_path, "Patches")
        os.makedirs(patches_path, exist_ok=True)
        
        # Create example patch
        example_patch = '''<?xml version="1.0" encoding="utf-8"?>
<Patch>
  <!-- Example patch - Remove or modify as needed -->
  <!--
  <Operation Class="PatchOperationAdd">
    <xpath>/Defs</xpath>
    <value>
      <ThingDef ParentName="ResourceBase">
        <defName>PatchedResource</defName>
        <label>patched resource</label>
        <description>A resource added via patch.</description>
      </ThingDef>
    </value>
  </Operation>
  -->
</Patch>'''
        
        with open(os.path.join(patches_path, "ExamplePatch.xml"), "w", encoding="utf-8") as f:
            f.write(example_patch)
    
    def create_assemblies_folder(self, mod_path):
        assemblies_path = os.path.join(mod_path, "Assemblies")
        os.makedirs(assemblies_path, exist_ok=True)
        
        # Create a readme for assemblies
        readme_content = '''# Assemblies Folder

This folder contains compiled .NET assemblies (DLL files) for your mod.

To add C# code to your mod:
1. Create a new C# project targeting .NET Framework 4.7.2 or .NET Standard 2.0
2. Reference the RimWorld and UnityEngine assemblies
3. Compile your code and place the resulting DLL files in this folder

Example references needed:
- RimWorld.exe (from RimWorld installation)
- Assembly-CSharp.dll (from RimWorld_Data/Managed/)
- UnityEngine.CoreModule.dll (from RimWorld_Data/Managed/)
'''
        
        with open(os.path.join(assemblies_path, "README.txt"), "w", encoding="utf-8") as f:
            f.write(readme_content)
    
    def create_textures_folder(self, mod_path):
        textures_path = os.path.join(mod_path, "Textures")
        os.makedirs(textures_path, exist_ok=True)
        
        # Create common texture subfolders
        os.makedirs(os.path.join(textures_path, "Things", "Item"), exist_ok=True)
        os.makedirs(os.path.join(textures_path, "Things", "Building"), exist_ok=True)
        os.makedirs(os.path.join(textures_path, "Things", "Pawn"), exist_ok=True)
        os.makedirs(os.path.join(textures_path, "UI"), exist_ok=True)
        
        # Create readme
        readme_content = '''# Textures Folder

Place your mod's texture files (.png) in this folder structure:

Things/Item/ - Item textures
Things/Building/ - Building textures  
Things/Pawn/ - Pawn-related textures
UI/ - User interface textures

Texture requirements:
- Use PNG format
- Power-of-2 dimensions recommended (64x64, 128x128, 256x256, etc.)
- Keep file sizes reasonable for performance
'''
        
        with open(os.path.join(textures_path, "README.txt"), "w", encoding="utf-8") as f:
            f.write(readme_content)
    
    def create_sounds_folder(self, mod_path):
        sounds_path = os.path.join(mod_path, "Sounds")
        os.makedirs(sounds_path, exist_ok=True)
        
        # Create readme
        readme_content = '''# Sounds Folder

Place your mod's sound files in this folder.

Supported formats:
- .wav (recommended)
- .ogg
- .mp3

Organization suggestions:
- Create subfolders for different sound categories
- Use descriptive filenames
- Keep file sizes reasonable
'''
        
        with open(os.path.join(sounds_path, "README.txt"), "w", encoding="utf-8") as f:
            f.write(readme_content)
    
    def create_languages_folder(self, mod_path):
        languages_path = os.path.join(mod_path, "Languages")
        os.makedirs(languages_path, exist_ok=True)
        
        # Create English language folder
        english_path = os.path.join(languages_path, "English")
        os.makedirs(english_path, exist_ok=True)
        
        keyed_path = os.path.join(english_path, "Keyed")
        os.makedirs(keyed_path, exist_ok=True)
        
        # Create example language file
        example_lang = '''<?xml version="1.0" encoding="utf-8"?>
<LanguageData>
  <!-- Example language keys - Remove or modify as needed -->
  <!--
  <ExampleKey>Example text</ExampleKey>
  <AnotherKey>Another example text</AnotherKey>
  -->
</LanguageData>'''
        
        with open(os.path.join(keyed_path, "ExampleKeys.xml"), "w", encoding="utf-8") as f:
            f.write(example_lang)


def main():
    root = Tk()
    app = ModMakerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()