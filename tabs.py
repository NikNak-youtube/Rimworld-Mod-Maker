"""
Rimworld Mod Maker - Tab Creation Module
Contains all methods for creating UI tabs and their components.
"""

import tkinter as tk
from tkinter import Label, Button, Entry, Text, Frame, Scrollbar, BooleanVar, Checkbutton, Listbox, ttk
from tkinter import VERTICAL, RIGHT, Y, LEFT, BOTH, END


class TabCreator:
    def __init__(self, app):
        self.app = app
    
    def create_all_tabs(self):
        """Create all tabs in the notebook"""
        # Mod Info Tab
        self.create_mod_info_tab()
        
        # Items Tab
        self.create_items_tab()
        
        # Weapons Tab
        self.create_weapons_tab()
        
        # Buildings Tab
        self.create_buildings_tab()
        
        # Cosmetics Tab
        self.create_cosmetics_tab()
        
        # Drugs Tab
        self.create_drugs_tab()
        
        # Workbenches Tab
        self.create_workbenches_tab()
        
        # Research Tab
        self.create_research_tab()
        
        # Recipes Tab
        self.create_recipes_tab()
    
    def create_mod_info_tab(self):
        # Mod Information Tab
        info_tab = Frame(self.app.notebook)
        self.app.notebook.add(info_tab, text="Mod Info")
        
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
        self.app.name_entry = Entry(info_scrollable_frame, width=50)
        self.app.name_entry.pack(fill="x", pady=(5, 0))
        
        # Author
        Label(info_scrollable_frame, text="Author:").pack(anchor="w", pady=(10, 0))
        self.app.author_entry = Entry(info_scrollable_frame, width=50)
        self.app.author_entry.pack(fill="x", pady=(5, 0))
        
        # Version
        Label(info_scrollable_frame, text="Version:").pack(anchor="w", pady=(10, 0))
        self.app.version_entry = Entry(info_scrollable_frame, width=50)
        self.app.version_entry.insert(0, "1.0.0")
        self.app.version_entry.pack(fill="x", pady=(5, 0))
        
        # Description
        Label(info_scrollable_frame, text="Description:").pack(anchor="w", pady=(10, 0))
        desc_frame = Frame(info_scrollable_frame)
        desc_frame.pack(fill="x", pady=(5, 0))
        
        self.app.description_text = Text(desc_frame, height=4, width=50)
        desc_scrollbar = Scrollbar(desc_frame, orient=VERTICAL, command=self.app.description_text.yview)
        self.app.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        self.app.description_text.pack(side=LEFT, fill=BOTH, expand=True)
        desc_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Directory Selection
        Label(info_scrollable_frame, text="Output Directory", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))
        
        dir_select_frame = Frame(info_scrollable_frame)
        dir_select_frame.pack(fill="x", pady=(0, 20))
        
        self.app.directory_label = Label(dir_select_frame, text="No directory selected", bg="white", relief="sunken", anchor="w")
        self.app.directory_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 10))
        
        Button(dir_select_frame, text="Browse", command=self.app.select_directory).pack(side=RIGHT)
        
        # Mod Components Section
        Label(info_scrollable_frame, text="Mod Components", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Checkboxes for different mod components
        self.app.include_defs = BooleanVar(value=True)
        self.app.include_patches = BooleanVar(value=False)
        self.app.include_assemblies = BooleanVar(value=False)
        self.app.include_textures = BooleanVar(value=False)
        self.app.include_sounds = BooleanVar(value=False)
        self.app.include_languages = BooleanVar(value=False)
        
        Checkbutton(info_scrollable_frame, text="Defs (XML definitions)", variable=self.app.include_defs).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Patches (XML patches)", variable=self.app.include_patches).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Assemblies (C# code)", variable=self.app.include_assemblies).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Textures", variable=self.app.include_textures).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Sounds", variable=self.app.include_sounds).pack(anchor="w", pady=2)
        Checkbutton(info_scrollable_frame, text="Languages", variable=self.app.include_languages).pack(anchor="w", pady=2)
    
    def create_items_tab(self):
        # Items Tab
        items_tab = Frame(self.app.notebook)
        self.app.notebook.add(items_tab, text="Items")
        
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
        self.app.item_defname = Entry(form_frame, width=30)
        self.app.item_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.item_label = Entry(form_frame, width=30)
        self.app.item_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.item_description = Entry(form_frame, width=30)
        self.app.item_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.item_market_value = Entry(form_frame, width=30)
        self.app.item_market_value.insert(0, "10.0")
        self.app.item_market_value.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=4, column=0, sticky="w", pady=5)
        self.app.item_mass = Entry(form_frame, width=30)
        self.app.item_mass.insert(0, "0.1")
        self.app.item_mass.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Stack Limit
        Label(form_frame, text="Stack Limit:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.item_stack_limit = Entry(form_frame, width=30)
        self.app.item_stack_limit.insert(0, "75")
        self.app.item_stack_limit.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Category
        Label(form_frame, text="Category:").grid(row=6, column=0, sticky="w", pady=5)
        self.app.item_category = ttk.Combobox(form_frame, width=27, values=[
            "ResourcesRaw", "Items", "Medicine", "Foods", "Manufactured", "Art"
        ])
        self.app.item_category.set("ResourcesRaw")
        self.app.item_category.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=7, column=0, sticky="w", pady=5)
        texture_frame = Frame(form_frame)
        texture_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.item_texture_label = Label(texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.item_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(texture_frame, text="Browse", command=self.app.asset_manager.select_item_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=8, column=0, sticky="w", pady=5)
        sound_frame = Frame(form_frame)
        sound_frame.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.item_sound_label = Label(sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.item_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(sound_frame, text="Browse", command=self.app.asset_manager.select_item_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(items_scrollable_frame, text="Add Item", command=self.app.content_manager.add_item, bg="#2196F3", fg="white").pack(pady=10)
        
        # Items list
        Label(items_scrollable_frame, text="Created Items:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        items_list_frame = Frame(items_scrollable_frame)
        items_list_frame.pack(fill="both", expand=True)
        
        self.app.items_listbox = Listbox(items_list_frame, height=10)
        items_list_scrollbar = Scrollbar(items_list_frame, orient=VERTICAL, command=self.app.items_listbox.yview)
        self.app.items_listbox.configure(yscrollcommand=items_list_scrollbar.set)
        
        self.app.items_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        items_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(items_scrollable_frame, text="Remove Selected Item", command=self.app.content_manager.remove_item, bg="#f44336", fg="white").pack(pady=10)
    
    def create_weapons_tab(self):
        # Weapons Tab
        weapons_tab = Frame(self.app.notebook)
        self.app.notebook.add(weapons_tab, text="Weapons")
        
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
        self.app.weapon_defname = Entry(form_frame, width=30)
        self.app.weapon_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.weapon_label = Entry(form_frame, width=30)
        self.app.weapon_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.weapon_description = Entry(form_frame, width=30)
        self.app.weapon_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Weapon Type
        Label(form_frame, text="Weapon Type:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.weapon_type = ttk.Combobox(form_frame, width=27, values=[
            "Melee", "Ranged"
        ])
        self.app.weapon_type.set("Melee")
        self.app.weapon_type.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Damage
        Label(form_frame, text="Damage:").grid(row=4, column=0, sticky="w", pady=5)
        self.app.weapon_damage = Entry(form_frame, width=30)
        self.app.weapon_damage.insert(0, "10")
        self.app.weapon_damage.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Damage Type
        Label(form_frame, text="Damage Type:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.weapon_damage_type = ttk.Combobox(form_frame, width=27, values=[
            "Blunt", "Cut", "Bullet", "Bomb", "Flame"
        ])
        self.app.weapon_damage_type.set("Cut")
        self.app.weapon_damage_type.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=6, column=0, sticky="w", pady=5)
        self.app.weapon_market_value = Entry(form_frame, width=30)
        self.app.weapon_market_value.insert(0, "100.0")
        self.app.weapon_market_value.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=7, column=0, sticky="w", pady=5)
        self.app.weapon_mass = Entry(form_frame, width=30)
        self.app.weapon_mass.insert(0, "1.5")
        self.app.weapon_mass.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=8, column=0, sticky="w", pady=5)
        weapon_texture_frame = Frame(form_frame)
        weapon_texture_frame.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.weapon_texture_label = Label(weapon_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.weapon_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(weapon_texture_frame, text="Browse", command=self.app.asset_manager.select_weapon_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=9, column=0, sticky="w", pady=5)
        weapon_sound_frame = Frame(form_frame)
        weapon_sound_frame.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.weapon_sound_label = Label(weapon_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.weapon_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(weapon_sound_frame, text="Browse", command=self.app.asset_manager.select_weapon_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(weapons_scrollable_frame, text="Add Weapon", command=self.app.content_manager.add_weapon, bg="#2196F3", fg="white").pack(pady=10)
        
        # Weapons list
        Label(weapons_scrollable_frame, text="Created Weapons:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        weapons_list_frame = Frame(weapons_scrollable_frame)
        weapons_list_frame.pack(fill="both", expand=True)
        
        self.app.weapons_listbox = Listbox(weapons_list_frame, height=10)
        weapons_list_scrollbar = Scrollbar(weapons_list_frame, orient=VERTICAL, command=self.app.weapons_listbox.yview)
        self.app.weapons_listbox.configure(yscrollcommand=weapons_list_scrollbar.set)
        
        self.app.weapons_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        weapons_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(weapons_scrollable_frame, text="Remove Selected Weapon", command=self.app.content_manager.remove_weapon, bg="#f44336", fg="white").pack(pady=10)
    
    def create_buildings_tab(self):
        # Buildings Tab
        buildings_tab = Frame(self.app.notebook)
        self.app.notebook.add(buildings_tab, text="Buildings")
        
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
        self.app.building_defname = Entry(form_frame, width=30)
        self.app.building_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.building_label = Entry(form_frame, width=30)
        self.app.building_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.building_description = Entry(form_frame, width=30)
        self.app.building_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Size
        Label(form_frame, text="Size (e.g., 1,1):").grid(row=3, column=0, sticky="w", pady=5)
        self.app.building_size = Entry(form_frame, width=30)
        self.app.building_size.insert(0, "1,1")
        self.app.building_size.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Hit Points
        Label(form_frame, text="Hit Points:").grid(row=4, column=0, sticky="w", pady=5)
        self.app.building_hitpoints = Entry(form_frame, width=30)
        self.app.building_hitpoints.insert(0, "100")
        self.app.building_hitpoints.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work to Make
        Label(form_frame, text="Work to Make:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.building_work = Entry(form_frame, width=30)
        self.app.building_work.insert(0, "500")
        self.app.building_work.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=6, column=0, sticky="w", pady=5)
        building_texture_frame = Frame(form_frame)
        building_texture_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.building_texture_label = Label(building_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.building_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(building_texture_frame, text="Browse", command=self.app.asset_manager.select_building_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=7, column=0, sticky="w", pady=5)
        building_sound_frame = Frame(form_frame)
        building_sound_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.building_sound_label = Label(building_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.building_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(building_sound_frame, text="Browse", command=self.app.asset_manager.select_building_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(buildings_scrollable_frame, text="Add Building", command=self.app.content_manager.add_building, bg="#2196F3", fg="white").pack(pady=10)
        
        # Buildings list
        Label(buildings_scrollable_frame, text="Created Buildings:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        buildings_list_frame = Frame(buildings_scrollable_frame)
        buildings_list_frame.pack(fill="both", expand=True)
        
        self.app.buildings_listbox = Listbox(buildings_list_frame, height=10)
        buildings_list_scrollbar = Scrollbar(buildings_list_frame, orient=VERTICAL, command=self.app.buildings_listbox.yview)
        self.app.buildings_listbox.configure(yscrollcommand=buildings_list_scrollbar.set)
        
        self.app.buildings_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        buildings_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(buildings_scrollable_frame, text="Remove Selected Building", command=self.app.content_manager.remove_building, bg="#f44336", fg="white").pack(pady=10)
    
    def create_cosmetics_tab(self):
        # Cosmetics Tab
        cosmetics_tab = Frame(self.app.notebook)
        self.app.notebook.add(cosmetics_tab, text="Cosmetics")
        
        # Create scrollable frame
        cosmetics_canvas = tk.Canvas(cosmetics_tab)
        cosmetics_scrollbar = Scrollbar(cosmetics_tab, orient=VERTICAL, command=cosmetics_canvas.yview)
        cosmetics_scrollable_frame = Frame(cosmetics_canvas)
        
        cosmetics_scrollable_frame.bind(
            "<Configure>",
            lambda e: cosmetics_canvas.configure(scrollregion=cosmetics_canvas.bbox("all"))
        )
        
        cosmetics_canvas.create_window((0, 0), window=cosmetics_scrollable_frame, anchor="nw")
        cosmetics_canvas.configure(yscrollcommand=cosmetics_scrollbar.set)
        
        cosmetics_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        cosmetics_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(cosmetics_scrollable_frame, text="Create Cosmetics & Apparel", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Cosmetic form
        form_frame = Frame(cosmetics_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.app.cosmetic_defname = Entry(form_frame, width=30)
        self.app.cosmetic_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.cosmetic_label = Entry(form_frame, width=30)
        self.app.cosmetic_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.cosmetic_description = Entry(form_frame, width=30)
        self.app.cosmetic_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Apparel Type
        Label(form_frame, text="Apparel Type:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.cosmetic_type = ttk.Combobox(form_frame, width=27, values=[
            "Headwear", "Shirt", "Pants", "Jacket", "Belt", "Shoes", "Gloves", "Accessory", "Armor"
        ])
        self.app.cosmetic_type.set("Shirt")
        self.app.cosmetic_type.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Body Parts Covered
        Label(form_frame, text="Body Parts (comma-separated):").grid(row=4, column=0, sticky="w", pady=5)
        self.app.cosmetic_body_parts = Entry(form_frame, width=30)
        self.app.cosmetic_body_parts.insert(0, "Torso")
        self.app.cosmetic_body_parts.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Layers
        Label(form_frame, text="Apparel Layer:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.cosmetic_layer = ttk.Combobox(form_frame, width=27, values=[
            "OnSkin", "Middle", "Shell", "Overhead", "EyeCover", "StrappedHead", "Belt"
        ])
        self.app.cosmetic_layer.set("Middle")
        self.app.cosmetic_layer.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Armor Rating (if armor)
        Label(form_frame, text="Armor Rating (Sharp):").grid(row=6, column=0, sticky="w", pady=5)
        self.app.cosmetic_armor_sharp = Entry(form_frame, width=30)
        self.app.cosmetic_armor_sharp.insert(0, "0.0")
        self.app.cosmetic_armor_sharp.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        Label(form_frame, text="Armor Rating (Blunt):").grid(row=7, column=0, sticky="w", pady=5)
        self.app.cosmetic_armor_blunt = Entry(form_frame, width=30)
        self.app.cosmetic_armor_blunt.insert(0, "0.0")
        self.app.cosmetic_armor_blunt.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        Label(form_frame, text="Armor Rating (Heat):").grid(row=8, column=0, sticky="w", pady=5)
        self.app.cosmetic_armor_heat = Entry(form_frame, width=30)
        self.app.cosmetic_armor_heat.insert(0, "0.0")
        self.app.cosmetic_armor_heat.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=9, column=0, sticky="w", pady=5)
        self.app.cosmetic_market_value = Entry(form_frame, width=30)
        self.app.cosmetic_market_value.insert(0, "50.0")
        self.app.cosmetic_market_value.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=10, column=0, sticky="w", pady=5)
        self.app.cosmetic_mass = Entry(form_frame, width=30)
        self.app.cosmetic_mass.insert(0, "0.5")
        self.app.cosmetic_mass.grid(row=10, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work to Make
        Label(form_frame, text="Work to Make:").grid(row=11, column=0, sticky="w", pady=5)
        self.app.cosmetic_work = Entry(form_frame, width=30)
        self.app.cosmetic_work.insert(0, "1000")
        self.app.cosmetic_work.grid(row=11, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=12, column=0, sticky="w", pady=5)
        cosmetic_texture_frame = Frame(form_frame)
        cosmetic_texture_frame.grid(row=12, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.cosmetic_texture_label = Label(cosmetic_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.cosmetic_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(cosmetic_texture_frame, text="Browse", command=self.app.asset_manager.select_cosmetic_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=13, column=0, sticky="w", pady=5)
        cosmetic_sound_frame = Frame(form_frame)
        cosmetic_sound_frame.grid(row=13, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.cosmetic_sound_label = Label(cosmetic_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.cosmetic_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(cosmetic_sound_frame, text="Browse", command=self.app.asset_manager.select_cosmetic_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(cosmetics_scrollable_frame, text="Add Cosmetic", command=self.app.content_manager.add_cosmetic, bg="#2196F3", fg="white").pack(pady=10)
        
        # Cosmetics list
        Label(cosmetics_scrollable_frame, text="Created Cosmetics:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        cosmetics_list_frame = Frame(cosmetics_scrollable_frame)
        cosmetics_list_frame.pack(fill="both", expand=True)
        
        self.app.cosmetics_listbox = Listbox(cosmetics_list_frame, height=10)
        cosmetics_list_scrollbar = Scrollbar(cosmetics_list_frame, orient=VERTICAL, command=self.app.cosmetics_listbox.yview)
        self.app.cosmetics_listbox.configure(yscrollcommand=cosmetics_list_scrollbar.set)
        
        self.app.cosmetics_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        cosmetics_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(cosmetics_scrollable_frame, text="Remove Selected Cosmetic", command=self.app.content_manager.remove_cosmetic, bg="#f44336", fg="white").pack(pady=10)
    
    def create_drugs_tab(self):
        # Drugs Tab
        drugs_tab = Frame(self.app.notebook)
        self.app.notebook.add(drugs_tab, text="Drugs")
        
        # Create scrollable frame
        drugs_canvas = tk.Canvas(drugs_tab)
        drugs_scrollbar = Scrollbar(drugs_tab, orient=VERTICAL, command=drugs_canvas.yview)
        drugs_scrollable_frame = Frame(drugs_canvas)
        
        drugs_scrollable_frame.bind(
            "<Configure>",
            lambda e: drugs_canvas.configure(scrollregion=drugs_canvas.bbox("all"))
        )
        
        drugs_canvas.create_window((0, 0), window=drugs_scrollable_frame, anchor="nw")
        drugs_canvas.configure(yscrollcommand=drugs_scrollbar.set)
        
        drugs_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        drugs_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(drugs_scrollable_frame, text="Create Drugs", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Drug form
        form_frame = Frame(drugs_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.app.drug_defname = Entry(form_frame, width=30)
        self.app.drug_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.drug_label = Entry(form_frame, width=30)
        self.app.drug_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.drug_description = Entry(form_frame, width=30)
        self.app.drug_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Drug Category
        Label(form_frame, text="Drug Category:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.drug_category = ttk.Combobox(form_frame, width=27, values=[
            "Medical", "Social", "Combat", "Production", "Psychic"
        ])
        self.app.drug_category.set("Medical")
        self.app.drug_category.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Addiction Chance
        Label(form_frame, text="Addiction Chance (%):").grid(row=4, column=0, sticky="w", pady=5)
        self.app.drug_addiction_chance = Entry(form_frame, width=30)
        self.app.drug_addiction_chance.insert(0, "0.0")
        self.app.drug_addiction_chance.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Tolerance Gain
        Label(form_frame, text="Tolerance Gain:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.drug_tolerance_gain = Entry(form_frame, width=30)
        self.app.drug_tolerance_gain.insert(0, "0.0")
        self.app.drug_tolerance_gain.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # High Duration (hours)
        Label(form_frame, text="High Duration (hours):").grid(row=6, column=0, sticky="w", pady=5)
        self.app.drug_high_duration = Entry(form_frame, width=30)
        self.app.drug_high_duration.insert(0, "8.0")
        self.app.drug_high_duration.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Market Value
        Label(form_frame, text="Market Value:").grid(row=7, column=0, sticky="w", pady=5)
        self.app.drug_market_value = Entry(form_frame, width=30)
        self.app.drug_market_value.insert(0, "25.0")
        self.app.drug_market_value.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mass
        Label(form_frame, text="Mass:").grid(row=8, column=0, sticky="w", pady=5)
        self.app.drug_mass = Entry(form_frame, width=30)
        self.app.drug_mass.insert(0, "0.05")
        self.app.drug_mass.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Stack Limit
        Label(form_frame, text="Stack Limit:").grid(row=9, column=0, sticky="w", pady=5)
        self.app.drug_stack_limit = Entry(form_frame, width=30)
        self.app.drug_stack_limit.insert(0, "150")
        self.app.drug_stack_limit.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Effects Section
        Label(form_frame, text="Effects:", font=("Arial", 10, "bold")).grid(row=10, column=0, columnspan=2, sticky="w", pady=(15, 5))
        
        # Mood Effect
        Label(form_frame, text="Mood Effect:").grid(row=11, column=0, sticky="w", pady=5)
        self.app.drug_mood_effect = Entry(form_frame, width=30)
        self.app.drug_mood_effect.insert(0, "0")
        self.app.drug_mood_effect.grid(row=11, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Pain Effect
        Label(form_frame, text="Pain Effect:").grid(row=12, column=0, sticky="w", pady=5)
        self.app.drug_pain_effect = Entry(form_frame, width=30)
        self.app.drug_pain_effect.insert(0, "0.0")
        self.app.drug_pain_effect.grid(row=12, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Consciousness Effect
        Label(form_frame, text="Consciousness Effect:").grid(row=13, column=0, sticky="w", pady=5)
        self.app.drug_consciousness_effect = Entry(form_frame, width=30)
        self.app.drug_consciousness_effect.insert(0, "0.0")
        self.app.drug_consciousness_effect.grid(row=13, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Moving Effect
        Label(form_frame, text="Moving Effect:").grid(row=14, column=0, sticky="w", pady=5)
        self.app.drug_moving_effect = Entry(form_frame, width=30)
        self.app.drug_moving_effect.insert(0, "0.0")
        self.app.drug_moving_effect.grid(row=14, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=15, column=0, sticky="w", pady=5)
        drug_texture_frame = Frame(form_frame)
        drug_texture_frame.grid(row=15, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.drug_texture_label = Label(drug_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.drug_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(drug_texture_frame, text="Browse", command=self.app.asset_manager.select_drug_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=16, column=0, sticky="w", pady=5)
        drug_sound_frame = Frame(form_frame)
        drug_sound_frame.grid(row=16, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.drug_sound_label = Label(drug_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.drug_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(drug_sound_frame, text="Browse", command=self.app.asset_manager.select_drug_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(drugs_scrollable_frame, text="Add Drug", command=self.app.content_manager.add_drug, bg="#2196F3", fg="white").pack(pady=10)
        
        # Drugs list
        Label(drugs_scrollable_frame, text="Created Drugs:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        drugs_list_frame = Frame(drugs_scrollable_frame)
        drugs_list_frame.pack(fill="both", expand=True)
        
        self.app.drugs_listbox = Listbox(drugs_list_frame, height=10)
        drugs_list_scrollbar = Scrollbar(drugs_list_frame, orient=VERTICAL, command=self.app.drugs_listbox.yview)
        self.app.drugs_listbox.configure(yscrollcommand=drugs_list_scrollbar.set)
        
        self.app.drugs_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        drugs_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(drugs_scrollable_frame, text="Remove Selected Drug", command=self.app.content_manager.remove_drug, bg="#f44336", fg="white").pack(pady=10)
    
    def create_workbenches_tab(self):
        # Workbenches Tab
        workbenches_tab = Frame(self.app.notebook)
        self.app.notebook.add(workbenches_tab, text="Workbenches")
        
        # Create scrollable frame
        workbenches_canvas = tk.Canvas(workbenches_tab)
        workbenches_scrollbar = Scrollbar(workbenches_tab, orient=VERTICAL, command=workbenches_canvas.yview)
        workbenches_scrollable_frame = Frame(workbenches_canvas)
        
        workbenches_scrollable_frame.bind(
            "<Configure>",
            lambda e: workbenches_canvas.configure(scrollregion=workbenches_canvas.bbox("all"))
        )
        
        workbenches_canvas.create_window((0, 0), window=workbenches_scrollable_frame, anchor="nw")
        workbenches_canvas.configure(yscrollcommand=workbenches_scrollbar.set)
        
        workbenches_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        workbenches_scrollbar.pack(side=RIGHT, fill=Y, pady=20)
        
        Label(workbenches_scrollable_frame, text="Create Workbenches", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Workbench form
        form_frame = Frame(workbenches_scrollable_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # DefName
        Label(form_frame, text="Def Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.app.workbench_defname = Entry(form_frame, width=30)
        self.app.workbench_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.workbench_label = Entry(form_frame, width=30)
        self.app.workbench_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.workbench_description = Entry(form_frame, width=30)
        self.app.workbench_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Workbench Type
        Label(form_frame, text="Workbench Type:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.workbench_type = ttk.Combobox(form_frame, width=27, values=[
            "Crafting", "Production", "Research", "Cooking", "Smithing", "Tailoring", "Art"
        ])
        self.app.workbench_type.set("Crafting")
        self.app.workbench_type.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Size
        Label(form_frame, text="Size (e.g., 3,1):").grid(row=4, column=0, sticky="w", pady=5)
        self.app.workbench_size = Entry(form_frame, width=30)
        self.app.workbench_size.insert(0, "3,1")
        self.app.workbench_size.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Hit Points
        Label(form_frame, text="Hit Points:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.workbench_hitpoints = Entry(form_frame, width=30)
        self.app.workbench_hitpoints.insert(0, "180")
        self.app.workbench_hitpoints.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work to Make
        Label(form_frame, text="Work to Make:").grid(row=6, column=0, sticky="w", pady=5)
        self.app.workbench_work = Entry(form_frame, width=30)
        self.app.workbench_work.insert(0, "3000")
        self.app.workbench_work.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work Speed Factor
        Label(form_frame, text="Work Speed Factor:").grid(row=7, column=0, sticky="w", pady=5)
        self.app.workbench_speed_factor = Entry(form_frame, width=30)
        self.app.workbench_speed_factor.insert(0, "1.0")
        self.app.workbench_speed_factor.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Power Consumption
        Label(form_frame, text="Power Consumption:").grid(row=8, column=0, sticky="w", pady=5)
        self.app.workbench_power = Entry(form_frame, width=30)
        self.app.workbench_power.insert(0, "0")
        self.app.workbench_power.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Skill Requirements
        Label(form_frame, text="Required Skill:").grid(row=9, column=0, sticky="w", pady=5)
        self.app.workbench_skill = ttk.Combobox(form_frame, width=27, values=[
            "None", "Crafting", "Construction", "Cooking", "Artistic", "Intellectual", "Medicine"
        ])
        self.app.workbench_skill.set("Crafting")
        self.app.workbench_skill.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Skill Level
        Label(form_frame, text="Required Skill Level:").grid(row=10, column=0, sticky="w", pady=5)
        self.app.workbench_skill_level = Entry(form_frame, width=30)
        self.app.workbench_skill_level.insert(0, "0")
        self.app.workbench_skill_level.grid(row=10, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Texture selection
        Label(form_frame, text="Texture (PNG):").grid(row=11, column=0, sticky="w", pady=5)
        workbench_texture_frame = Frame(form_frame)
        workbench_texture_frame.grid(row=11, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.workbench_texture_label = Label(workbench_texture_frame, text="No texture selected", bg="white", relief="sunken", anchor="w")
        self.app.workbench_texture_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(workbench_texture_frame, text="Browse", command=self.app.asset_manager.select_workbench_texture).pack(side=RIGHT)
        
        # Sound selection
        Label(form_frame, text="Sound (WAV/OGG):").grid(row=12, column=0, sticky="w", pady=5)
        workbench_sound_frame = Frame(form_frame)
        workbench_sound_frame.grid(row=12, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.workbench_sound_label = Label(workbench_sound_frame, text="No sound selected", bg="white", relief="sunken", anchor="w")
        self.app.workbench_sound_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 5))
        Button(workbench_sound_frame, text="Browse", command=self.app.asset_manager.select_workbench_sound).pack(side=RIGHT)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(workbenches_scrollable_frame, text="Add Workbench", command=self.app.content_manager.add_workbench, bg="#2196F3", fg="white").pack(pady=10)
        
        # Workbenches list
        Label(workbenches_scrollable_frame, text="Created Workbenches:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        workbenches_list_frame = Frame(workbenches_scrollable_frame)
        workbenches_list_frame.pack(fill="both", expand=True)
        
        self.app.workbenches_listbox = Listbox(workbenches_list_frame, height=10)
        workbenches_list_scrollbar = Scrollbar(workbenches_list_frame, orient=VERTICAL, command=self.app.workbenches_listbox.yview)
        self.app.workbenches_listbox.configure(yscrollcommand=workbenches_list_scrollbar.set)
        
        self.app.workbenches_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        workbenches_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(workbenches_scrollable_frame, text="Remove Selected Workbench", command=self.app.content_manager.remove_workbench, bg="#f44336", fg="white").pack(pady=10)
    
    def create_research_tab(self):
        # Research Tab
        research_tab = Frame(self.app.notebook)
        self.app.notebook.add(research_tab, text="Research")
        
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
        self.app.research_defname = Entry(form_frame, width=30)
        self.app.research_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.research_label = Entry(form_frame, width=30)
        self.app.research_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.research_description = Entry(form_frame, width=30)
        self.app.research_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Base Cost
        Label(form_frame, text="Base Cost:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.research_cost = Entry(form_frame, width=30)
        self.app.research_cost.insert(0, "500")
        self.app.research_cost.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Tech Level
        Label(form_frame, text="Tech Level:").grid(row=4, column=0, sticky="w", pady=5)
        self.app.research_tech_level = ttk.Combobox(form_frame, width=27, values=[
            "Neolithic", "Medieval", "Industrial", "Spacer", "Ultra"
        ])
        self.app.research_tech_level.set("Industrial")
        self.app.research_tech_level.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Research Unlocks Section
        Label(form_frame, text="Unlocked Things:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(15, 5))
        
        # Items unlocked
        Label(form_frame, text="Unlocked Items:").grid(row=6, column=0, sticky="w", pady=5)
        unlocked_items_frame = Frame(form_frame)
        unlocked_items_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_items = Listbox(unlocked_items_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_items.pack(side=LEFT, fill="both", expand=True)
        
        items_buttons_frame = Frame(unlocked_items_frame)
        items_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(items_buttons_frame, text="Add Item", command=self.app.content_manager.add_item_to_research, width=8).pack(pady=1)
        Button(items_buttons_frame, text="Remove", command=self.app.content_manager.remove_item_from_research, width=8).pack(pady=1)
        
        # Weapons unlocked
        Label(form_frame, text="Unlocked Weapons:").grid(row=7, column=0, sticky="w", pady=5)
        unlocked_weapons_frame = Frame(form_frame)
        unlocked_weapons_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_weapons = Listbox(unlocked_weapons_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_weapons.pack(side=LEFT, fill="both", expand=True)
        
        weapons_buttons_frame = Frame(unlocked_weapons_frame)
        weapons_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(weapons_buttons_frame, text="Add Weapon", command=self.app.content_manager.add_weapon_to_research, width=8).pack(pady=1)
        Button(weapons_buttons_frame, text="Remove", command=self.app.content_manager.remove_weapon_from_research, width=8).pack(pady=1)
        
        # Buildings unlocked
        Label(form_frame, text="Unlocked Buildings:").grid(row=8, column=0, sticky="w", pady=5)
        unlocked_buildings_frame = Frame(form_frame)
        unlocked_buildings_frame.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_buildings = Listbox(unlocked_buildings_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_buildings.pack(side=LEFT, fill="both", expand=True)
        
        buildings_buttons_frame = Frame(unlocked_buildings_frame)
        buildings_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(buildings_buttons_frame, text="Add Building", command=self.app.content_manager.add_building_to_research, width=8).pack(pady=1)
        Button(buildings_buttons_frame, text="Remove", command=self.app.content_manager.remove_building_from_research, width=8).pack(pady=1)
        
        # Cosmetics unlocked
        Label(form_frame, text="Unlocked Cosmetics:").grid(row=9, column=0, sticky="w", pady=5)
        unlocked_cosmetics_frame = Frame(form_frame)
        unlocked_cosmetics_frame.grid(row=9, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_cosmetics = Listbox(unlocked_cosmetics_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_cosmetics.pack(side=LEFT, fill="both", expand=True)
        
        cosmetics_buttons_frame = Frame(unlocked_cosmetics_frame)
        cosmetics_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(cosmetics_buttons_frame, text="Add Cosmetic", command=self.app.content_manager.add_cosmetic_to_research, width=8).pack(pady=1)
        Button(cosmetics_buttons_frame, text="Remove", command=self.app.content_manager.remove_cosmetic_from_research, width=8).pack(pady=1)
        
        # Drugs unlocked
        Label(form_frame, text="Unlocked Drugs:").grid(row=10, column=0, sticky="w", pady=5)
        unlocked_drugs_frame = Frame(form_frame)
        unlocked_drugs_frame.grid(row=10, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_drugs = Listbox(unlocked_drugs_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_drugs.pack(side=LEFT, fill="both", expand=True)
        
        drugs_buttons_frame = Frame(unlocked_drugs_frame)
        drugs_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(drugs_buttons_frame, text="Add Drug", command=self.app.content_manager.add_drug_to_research, width=8).pack(pady=1)
        Button(drugs_buttons_frame, text="Remove", command=self.app.content_manager.remove_drug_from_research, width=8).pack(pady=1)
        
        # Workbenches unlocked
        Label(form_frame, text="Unlocked Workbenches:").grid(row=11, column=0, sticky="w", pady=5)
        unlocked_workbenches_frame = Frame(form_frame)
        unlocked_workbenches_frame.grid(row=11, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        self.app.research_unlocked_workbenches = Listbox(unlocked_workbenches_frame, height=3, selectmode="multiple")
        self.app.research_unlocked_workbenches.pack(side=LEFT, fill="both", expand=True)
        
        workbenches_buttons_frame = Frame(unlocked_workbenches_frame)
        workbenches_buttons_frame.pack(side=RIGHT, fill="y", padx=(5, 0))
        Button(workbenches_buttons_frame, text="Add Workbench", command=self.app.content_manager.add_workbench_to_research, width=8).pack(pady=1)
        Button(workbenches_buttons_frame, text="Remove", command=self.app.content_manager.remove_workbench_from_research, width=8).pack(pady=1)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(research_scrollable_frame, text="Add Research", command=self.app.content_manager.add_research, bg="#2196F3", fg="white").pack(pady=10)
        
        # Research list
        Label(research_scrollable_frame, text="Created Research:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        research_list_frame = Frame(research_scrollable_frame)
        research_list_frame.pack(fill="both", expand=True)
        
        self.app.research_listbox = Listbox(research_list_frame, height=10)
        research_list_scrollbar = Scrollbar(research_list_frame, orient=VERTICAL, command=self.app.research_listbox.yview)
        self.app.research_listbox.configure(yscrollcommand=research_list_scrollbar.set)
        
        self.app.research_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        research_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(research_scrollable_frame, text="Remove Selected Research", command=self.app.content_manager.remove_research, bg="#f44336", fg="white").pack(pady=10)
    
    def create_recipes_tab(self):
        # Recipes Tab
        recipes_tab = Frame(self.app.notebook)
        self.app.notebook.add(recipes_tab, text="Recipes")
        
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
        self.app.recipe_defname = Entry(form_frame, width=30)
        self.app.recipe_defname.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Label
        Label(form_frame, text="Label:").grid(row=1, column=0, sticky="w", pady=5)
        self.app.recipe_label = Entry(form_frame, width=30)
        self.app.recipe_label.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Description
        Label(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.app.recipe_description = Entry(form_frame, width=30)
        self.app.recipe_description.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Work Amount
        Label(form_frame, text="Work Amount:").grid(row=3, column=0, sticky="w", pady=5)
        self.app.recipe_work = Entry(form_frame, width=30)
        self.app.recipe_work.insert(0, "100")
        self.app.recipe_work.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Product Def Name
        Label(form_frame, text="Product Def Name:").grid(row=4, column=0, sticky="w", pady=5)
        self.app.recipe_product = Entry(form_frame, width=30)
        self.app.recipe_product.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Product Count
        Label(form_frame, text="Product Count:").grid(row=5, column=0, sticky="w", pady=5)
        self.app.recipe_product_count = Entry(form_frame, width=30)
        self.app.recipe_product_count.insert(0, "1")
        self.app.recipe_product_count.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Ingredients (simplified)
        Label(form_frame, text="Ingredients (format: DefName:Count):").grid(row=6, column=0, sticky="w", pady=5)
        self.app.recipe_ingredients = Entry(form_frame, width=30)
        self.app.recipe_ingredients.insert(0, "Steel:5")
        self.app.recipe_ingredients.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        Button(recipes_scrollable_frame, text="Add Recipe", command=self.app.content_manager.add_recipe, bg="#2196F3", fg="white").pack(pady=10)
        
        # Recipes list
        Label(recipes_scrollable_frame, text="Created Recipes:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        
        recipes_list_frame = Frame(recipes_scrollable_frame)
        recipes_list_frame.pack(fill="both", expand=True)
        
        self.app.recipes_listbox = Listbox(recipes_list_frame, height=10)
        recipes_list_scrollbar = Scrollbar(recipes_list_frame, orient=VERTICAL, command=self.app.recipes_listbox.yview)
        self.app.recipes_listbox.configure(yscrollcommand=recipes_list_scrollbar.set)
        
        self.app.recipes_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        recipes_list_scrollbar.pack(side=RIGHT, fill=Y)
        
        Button(recipes_scrollable_frame, text="Remove Selected Recipe", command=self.app.content_manager.remove_recipe, bg="#f44336", fg="white").pack(pady=10)
