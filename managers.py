"""
Rimworld Mod Maker - Content and Asset Management Module
Contains all methods for managing mod content and assets.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import END
import os
import shutil


class ContentManager:
    def __init__(self, app):
        self.app = app
    
    def add_item(self):
        """Add a new item to the mod"""
        defname = self.app.item_defname.get().strip()
        label = self.app.item_label.get().strip()
        description = self.app.item_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for item in self.app.items:
            if item['defName'] == defname:
                messagebox.showerror("Error", f"Item with DefName '{defname}' already exists!")
                return
        
        try:
            market_value = float(self.app.item_market_value.get() or "10.0")
            mass = float(self.app.item_mass.get() or "0.1")
            stack_limit = int(self.app.item_stack_limit.get() or "75")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for market value, mass, and stack limit!")
            return
        
        category = self.app.item_category.get()
        
        item = {
            'defName': defname,
            'label': label,
            'description': description,
            'marketValue': market_value,
            'mass': mass,
            'stackLimit': stack_limit,
            'category': category,
            'texture': getattr(self.app, 'selected_item_texture', None),
            'sound': getattr(self.app, 'selected_item_sound', None)
        }
        
        self.app.items.append(item)
        self.app.items_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.item_defname.delete(0, END)
        self.app.item_label.delete(0, END)
        self.app.item_description.delete(0, END)
        self.app.item_market_value.delete(0, END)
        self.app.item_market_value.insert(0, "10.0")
        self.app.item_mass.delete(0, END)
        self.app.item_mass.insert(0, "0.1")
        self.app.item_stack_limit.delete(0, END)
        self.app.item_stack_limit.insert(0, "75")
        self.app.item_category.set("ResourcesRaw")
        self.app.item_texture_label.config(text="No texture selected")
        self.app.item_sound_label.config(text="No sound selected")
        self.app.selected_item_texture = None
        self.app.selected_item_sound = None
        
        messagebox.showinfo("Success", f"Item '{label}' added successfully!")
    
    def remove_item(self):
        """Remove selected item"""
        selection = self.app.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return
        
        index = selection[0]
        item = self.app.items[index]
        
        if messagebox.askyesno("Confirm", f"Remove item '{item['label']}'?"):
            del self.app.items[index]
            self.app.items_listbox.delete(index)
            messagebox.showinfo("Success", "Item removed successfully!")
    
    def add_weapon(self):
        """Add a new weapon to the mod"""
        defname = self.app.weapon_defname.get().strip()
        label = self.app.weapon_label.get().strip()
        description = self.app.weapon_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for weapon in self.app.weapons:
            if weapon['defName'] == defname:
                messagebox.showerror("Error", f"Weapon with DefName '{defname}' already exists!")
                return
        
        try:
            damage = int(self.app.weapon_damage.get() or "10")
            market_value = float(self.app.weapon_market_value.get() or "100.0")
            mass = float(self.app.weapon_mass.get() or "1.5")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for damage, market value, and mass!")
            return
        
        weapon_type = self.app.weapon_type.get()
        damage_type = self.app.weapon_damage_type.get()
        
        weapon = {
            'defName': defname,
            'label': label,
            'description': description,
            'weaponType': weapon_type,
            'damage': damage,
            'damageType': damage_type,
            'marketValue': market_value,
            'mass': mass,
            'texture': getattr(self.app, 'selected_weapon_texture', None),
            'sound': getattr(self.app, 'selected_weapon_sound', None)
        }
        
        self.app.weapons.append(weapon)
        self.app.weapons_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.weapon_defname.delete(0, END)
        self.app.weapon_label.delete(0, END)
        self.app.weapon_description.delete(0, END)
        self.app.weapon_damage.delete(0, END)
        self.app.weapon_damage.insert(0, "10")
        self.app.weapon_market_value.delete(0, END)
        self.app.weapon_market_value.insert(0, "100.0")
        self.app.weapon_mass.delete(0, END)
        self.app.weapon_mass.insert(0, "1.5")
        self.app.weapon_type.set("Melee")
        self.app.weapon_damage_type.set("Cut")
        self.app.weapon_texture_label.config(text="No texture selected")
        self.app.weapon_sound_label.config(text="No sound selected")
        self.app.selected_weapon_texture = None
        self.app.selected_weapon_sound = None
        
        messagebox.showinfo("Success", f"Weapon '{label}' added successfully!")
    
    def remove_weapon(self):
        """Remove selected weapon"""
        selection = self.app.weapons_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a weapon to remove!")
            return
        
        index = selection[0]
        weapon = self.app.weapons[index]
        
        if messagebox.askyesno("Confirm", f"Remove weapon '{weapon['label']}'?"):
            del self.app.weapons[index]
            self.app.weapons_listbox.delete(index)
            messagebox.showinfo("Success", "Weapon removed successfully!")
    
    def add_building(self):
        """Add a new building to the mod"""
        defname = self.app.building_defname.get().strip()
        label = self.app.building_label.get().strip()
        description = self.app.building_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for building in self.app.buildings:
            if building['defName'] == defname:
                messagebox.showerror("Error", f"Building with DefName '{defname}' already exists!")
                return
        
        try:
            hitpoints = int(self.app.building_hitpoints.get() or "100")
            work = int(self.app.building_work.get() or "500")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for hit points and work!")
            return
        
        size = self.app.building_size.get() or "1,1"
        
        building = {
            'defName': defname,
            'label': label,
            'description': description,
            'size': size,
            'hitPoints': hitpoints,
            'workToBuild': work,
            'texture': getattr(self.app, 'selected_building_texture', None),
            'sound': getattr(self.app, 'selected_building_sound', None)
        }
        
        self.app.buildings.append(building)
        self.app.buildings_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.building_defname.delete(0, END)
        self.app.building_label.delete(0, END)
        self.app.building_description.delete(0, END)
        self.app.building_size.delete(0, END)
        self.app.building_size.insert(0, "1,1")
        self.app.building_hitpoints.delete(0, END)
        self.app.building_hitpoints.insert(0, "100")
        self.app.building_work.delete(0, END)
        self.app.building_work.insert(0, "500")
        self.app.building_texture_label.config(text="No texture selected")
        self.app.building_sound_label.config(text="No sound selected")
        self.app.selected_building_texture = None
        self.app.selected_building_sound = None
        
        messagebox.showinfo("Success", f"Building '{label}' added successfully!")
    
    def remove_building(self):
        """Remove selected building"""
        selection = self.app.buildings_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a building to remove!")
            return
        
        index = selection[0]
        building = self.app.buildings[index]
        
        if messagebox.askyesno("Confirm", f"Remove building '{building['label']}'?"):
            del self.app.buildings[index]
            self.app.buildings_listbox.delete(index)
            messagebox.showinfo("Success", "Building removed successfully!")
    
    def add_cosmetic(self):
        """Add a new cosmetic/apparel to the mod"""
        defname = self.app.cosmetic_defname.get().strip()
        label = self.app.cosmetic_label.get().strip()
        description = self.app.cosmetic_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for cosmetic in self.app.cosmetics:
            if cosmetic['defName'] == defname:
                messagebox.showerror("Error", f"Cosmetic with DefName '{defname}' already exists!")
                return
        
        try:
            armor_sharp = float(self.app.cosmetic_armor_sharp.get() or "0.0")
            armor_blunt = float(self.app.cosmetic_armor_blunt.get() or "0.0")
            armor_heat = float(self.app.cosmetic_armor_heat.get() or "0.0")
            market_value = float(self.app.cosmetic_market_value.get() or "50.0")
            mass = float(self.app.cosmetic_mass.get() or "0.5")
            work = int(self.app.cosmetic_work.get() or "1000")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for armor ratings, market value, mass, and work!")
            return
        
        cosmetic_type = self.app.cosmetic_type.get()
        body_parts = self.app.cosmetic_body_parts.get()
        layer = self.app.cosmetic_layer.get()
        
        cosmetic = {
            'defName': defname,
            'label': label,
            'description': description,
            'apparelType': cosmetic_type,
            'bodyParts': body_parts,
            'layer': layer,
            'armorSharp': armor_sharp,
            'armorBlunt': armor_blunt,
            'armorHeat': armor_heat,
            'marketValue': market_value,
            'mass': mass,
            'workToMake': work,
            'texture': getattr(self.app, 'selected_cosmetic_texture', None),
            'sound': getattr(self.app, 'selected_cosmetic_sound', None)
        }
        
        self.app.cosmetics.append(cosmetic)
        self.app.cosmetics_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.cosmetic_defname.delete(0, END)
        self.app.cosmetic_label.delete(0, END)
        self.app.cosmetic_description.delete(0, END)
        self.app.cosmetic_type.set("Shirt")
        self.app.cosmetic_body_parts.delete(0, END)
        self.app.cosmetic_body_parts.insert(0, "Torso")
        self.app.cosmetic_layer.set("Middle")
        self.app.cosmetic_armor_sharp.delete(0, END)
        self.app.cosmetic_armor_sharp.insert(0, "0.0")
        self.app.cosmetic_armor_blunt.delete(0, END)
        self.app.cosmetic_armor_blunt.insert(0, "0.0")
        self.app.cosmetic_armor_heat.delete(0, END)
        self.app.cosmetic_armor_heat.insert(0, "0.0")
        self.app.cosmetic_market_value.delete(0, END)
        self.app.cosmetic_market_value.insert(0, "50.0")
        self.app.cosmetic_mass.delete(0, END)
        self.app.cosmetic_mass.insert(0, "0.5")
        self.app.cosmetic_work.delete(0, END)
        self.app.cosmetic_work.insert(0, "1000")
        self.app.cosmetic_texture_label.config(text="No texture selected")
        self.app.cosmetic_sound_label.config(text="No sound selected")
        self.app.selected_cosmetic_texture = None
        self.app.selected_cosmetic_sound = None
        
        messagebox.showinfo("Success", f"Cosmetic '{label}' added successfully!")
    
    def remove_cosmetic(self):
        """Remove selected cosmetic"""
        selection = self.app.cosmetics_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a cosmetic to remove!")
            return
        
        index = selection[0]
        cosmetic = self.app.cosmetics[index]
        
        if messagebox.askyesno("Confirm", f"Remove cosmetic '{cosmetic['label']}'?"):
            del self.app.cosmetics[index]
            self.app.cosmetics_listbox.delete(index)
            messagebox.showinfo("Success", "Cosmetic removed successfully!")
    
    def add_research(self):
        """Add a new research project to the mod"""
        defname = self.app.research_defname.get().strip()
        label = self.app.research_label.get().strip()
        description = self.app.research_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for research in self.app.research:
            if research['defName'] == defname:
                messagebox.showerror("Error", f"Research with DefName '{defname}' already exists!")
                return
        
        try:
            cost = int(self.app.research_cost.get() or "500")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for base cost!")
            return
        
        tech_level = self.app.research_tech_level.get()
        
        # Get unlocked items, weapons, buildings, cosmetics
        unlocked_items = [self.app.research_unlocked_items.get(i) for i in self.app.research_unlocked_items.curselection()]
        unlocked_weapons = [self.app.research_unlocked_weapons.get(i) for i in self.app.research_unlocked_weapons.curselection()]
        unlocked_buildings = [self.app.research_unlocked_buildings.get(i) for i in self.app.research_unlocked_buildings.curselection()]
        unlocked_cosmetics = [self.app.research_unlocked_cosmetics.get(i) for i in self.app.research_unlocked_cosmetics.curselection()]
        
        research = {
            'defName': defname,
            'label': label,
            'description': description,
            'baseCost': cost,
            'techLevel': tech_level,
            'unlockedItems': unlocked_items,
            'unlockedWeapons': unlocked_weapons,
            'unlockedBuildings': unlocked_buildings,
            'unlockedCosmetics': unlocked_cosmetics
        }
        
        self.app.research.append(research)
        self.app.research_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.research_defname.delete(0, END)
        self.app.research_label.delete(0, END)
        self.app.research_description.delete(0, END)
        self.app.research_cost.delete(0, END)
        self.app.research_cost.insert(0, "500")
        self.app.research_tech_level.set("Industrial")
        self.app.research_unlocked_items.selection_clear(0, END)
        self.app.research_unlocked_weapons.selection_clear(0, END)
        self.app.research_unlocked_buildings.selection_clear(0, END)
        self.app.research_unlocked_cosmetics.selection_clear(0, END)
        
        messagebox.showinfo("Success", f"Research '{label}' added successfully!")
    
    def remove_research(self):
        """Remove selected research"""
        selection = self.app.research_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a research to remove!")
            return
        
        index = selection[0]
        research = self.app.research[index]
        
        if messagebox.askyesno("Confirm", f"Remove research '{research['label']}'?"):
            del self.app.research[index]
            self.app.research_listbox.delete(index)
            messagebox.showinfo("Success", "Research removed successfully!")
    
    def add_recipe(self):
        """Add a new recipe to the mod"""
        defname = self.app.recipe_defname.get().strip()
        label = self.app.recipe_label.get().strip()
        description = self.app.recipe_description.get().strip()
        
        if not defname or not label:
            messagebox.showerror("Error", "DefName and Label are required!")
            return
        
        # Check for duplicate defnames
        for recipe in self.app.recipes:
            if recipe['defName'] == defname:
                messagebox.showerror("Error", f"Recipe with DefName '{defname}' already exists!")
                return
        
        try:
            work = int(self.app.recipe_work.get() or "100")
            product_count = int(self.app.recipe_product_count.get() or "1")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for work amount and product count!")
            return
        
        product = self.app.recipe_product.get().strip()
        ingredients = self.app.recipe_ingredients.get().strip()
        
        recipe = {
            'defName': defname,
            'label': label,
            'description': description,
            'workAmount': work,
            'product': product,
            'productCount': product_count,
            'ingredients': ingredients
        }
        
        self.app.recipes.append(recipe)
        self.app.recipes_listbox.insert(END, f"{defname} - {label}")
        
        # Clear form
        self.app.recipe_defname.delete(0, END)
        self.app.recipe_label.delete(0, END)
        self.app.recipe_description.delete(0, END)
        self.app.recipe_work.delete(0, END)
        self.app.recipe_work.insert(0, "100")
        self.app.recipe_product.delete(0, END)
        self.app.recipe_product_count.delete(0, END)
        self.app.recipe_product_count.insert(0, "1")
        self.app.recipe_ingredients.delete(0, END)
        self.app.recipe_ingredients.insert(0, "Steel:5")
        
        messagebox.showinfo("Success", f"Recipe '{label}' added successfully!")
    
    def remove_recipe(self):
        """Remove selected recipe"""
        selection = self.app.recipes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recipe to remove!")
            return
        
        index = selection[0]
        recipe = self.app.recipes[index]
        
        if messagebox.askyesno("Confirm", f"Remove recipe '{recipe['label']}'?"):
            del self.app.recipes[index]
            self.app.recipes_listbox.delete(index)
            messagebox.showinfo("Success", "Recipe removed successfully!")
    
    # Research unlock management methods
    def add_item_to_research(self):
        """Add an item to the research unlocks list"""
        if not self.app.items:
            messagebox.showwarning("Warning", "No items available! Create items first.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.app.root)
        selection_window.title("Select Item to Add")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select an item to add to research unlocks:", font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(selection_window, height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        for item in self.app.items:
            listbox.insert(END, f"{item['defName']} - {item['label']}")
        
        def add_selected():
            selection = listbox.curselection()
            if selection:
                item_text = listbox.get(selection[0])
                # Check if already in list
                current_items = [self.app.research_unlocked_items.get(i) for i in range(self.app.research_unlocked_items.size())]
                if item_text not in current_items:
                    self.app.research_unlocked_items.insert(END, item_text)
                selection_window.destroy()
        
        tk.Button(selection_window, text="Add Selected", command=add_selected, bg="#2196F3", fg="white").pack(pady=10)
    
    def remove_item_from_research(self):
        """Remove selected item from research unlocks"""
        selection = self.app.research_unlocked_items.curselection()
        if selection:
            self.app.research_unlocked_items.delete(selection[0])
    
    def add_weapon_to_research(self):
        """Add a weapon to the research unlocks list"""
        if not self.app.weapons:
            messagebox.showwarning("Warning", "No weapons available! Create weapons first.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.app.root)
        selection_window.title("Select Weapon to Add")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select a weapon to add to research unlocks:", font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(selection_window, height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        for weapon in self.app.weapons:
            listbox.insert(END, f"{weapon['defName']} - {weapon['label']}")
        
        def add_selected():
            selection = listbox.curselection()
            if selection:
                weapon_text = listbox.get(selection[0])
                # Check if already in list
                current_weapons = [self.app.research_unlocked_weapons.get(i) for i in range(self.app.research_unlocked_weapons.size())]
                if weapon_text not in current_weapons:
                    self.app.research_unlocked_weapons.insert(END, weapon_text)
                selection_window.destroy()
        
        tk.Button(selection_window, text="Add Selected", command=add_selected, bg="#2196F3", fg="white").pack(pady=10)
    
    def remove_weapon_from_research(self):
        """Remove selected weapon from research unlocks"""
        selection = self.app.research_unlocked_weapons.curselection()
        if selection:
            self.app.research_unlocked_weapons.delete(selection[0])
    
    def add_building_to_research(self):
        """Add a building to the research unlocks list"""
        if not self.app.buildings:
            messagebox.showwarning("Warning", "No buildings available! Create buildings first.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.app.root)
        selection_window.title("Select Building to Add")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select a building to add to research unlocks:", font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(selection_window, height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        for building in self.app.buildings:
            listbox.insert(END, f"{building['defName']} - {building['label']}")
        
        def add_selected():
            selection = listbox.curselection()
            if selection:
                building_text = listbox.get(selection[0])
                # Check if already in list
                current_buildings = [self.app.research_unlocked_buildings.get(i) for i in range(self.app.research_unlocked_buildings.size())]
                if building_text not in current_buildings:
                    self.app.research_unlocked_buildings.insert(END, building_text)
                selection_window.destroy()
        
        tk.Button(selection_window, text="Add Selected", command=add_selected, bg="#2196F3", fg="white").pack(pady=10)
    
    def remove_building_from_research(self):
        """Remove selected building from research unlocks"""
        selection = self.app.research_unlocked_buildings.curselection()
        if selection:
            self.app.research_unlocked_buildings.delete(selection[0])
    
    def add_cosmetic_to_research(self):
        """Add a cosmetic to the research unlocks list"""
        if not self.app.cosmetics:
            messagebox.showwarning("Warning", "No cosmetics available! Create cosmetics first.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.app.root)
        selection_window.title("Select Cosmetic to Add")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select a cosmetic to add to research unlocks:", font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(selection_window, height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        for cosmetic in self.app.cosmetics:
            listbox.insert(END, f"{cosmetic['defName']} - {cosmetic['label']}")
        
        def add_selected():
            selection = listbox.curselection()
            if selection:
                cosmetic_text = listbox.get(selection[0])
                # Check if already in list
                current_cosmetics = [self.app.research_unlocked_cosmetics.get(i) for i in range(self.app.research_unlocked_cosmetics.size())]
                if cosmetic_text not in current_cosmetics:
                    self.app.research_unlocked_cosmetics.insert(END, cosmetic_text)
                selection_window.destroy()
        
        tk.Button(selection_window, text="Add Selected", command=add_selected, bg="#2196F3", fg="white").pack(pady=10)
    
    def remove_cosmetic_from_research(self):
        """Remove selected cosmetic from research unlocks"""
        selection = self.app.research_unlocked_cosmetics.curselection()
        if selection:
            self.app.research_unlocked_cosmetics.delete(selection[0])


class AssetManager:
    def __init__(self, app):
        self.app = app
    
    def select_item_texture(self):
        """Select texture file for item"""
        filename = filedialog.askopenfilename(
            title="Select Item Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_item_texture = filename
            self.app.item_texture_label.config(text=os.path.basename(filename))
    
    def select_item_sound(self):
        """Select sound file for item"""
        filename = filedialog.askopenfilename(
            title="Select Item Sound",
            filetypes=[("Audio files", "*.wav *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_item_sound = filename
            self.app.item_sound_label.config(text=os.path.basename(filename))
    
    def select_weapon_texture(self):
        """Select texture file for weapon"""
        filename = filedialog.askopenfilename(
            title="Select Weapon Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_weapon_texture = filename
            self.app.weapon_texture_label.config(text=os.path.basename(filename))
    
    def select_weapon_sound(self):
        """Select sound file for weapon"""
        filename = filedialog.askopenfilename(
            title="Select Weapon Sound",
            filetypes=[("Audio files", "*.wav *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_weapon_sound = filename
            self.app.weapon_sound_label.config(text=os.path.basename(filename))
    
    def select_building_texture(self):
        """Select texture file for building"""
        filename = filedialog.askopenfilename(
            title="Select Building Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_building_texture = filename
            self.app.building_texture_label.config(text=os.path.basename(filename))
    
    def select_building_sound(self):
        """Select sound file for building"""
        filename = filedialog.askopenfilename(
            title="Select Building Sound",
            filetypes=[("Audio files", "*.wav *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_building_sound = filename
            self.app.building_sound_label.config(text=os.path.basename(filename))
    
    def select_cosmetic_texture(self):
        """Select texture file for cosmetic"""
        filename = filedialog.askopenfilename(
            title="Select Cosmetic Texture",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_cosmetic_texture = filename
            self.app.cosmetic_texture_label.config(text=os.path.basename(filename))
    
    def select_cosmetic_sound(self):
        """Select sound file for cosmetic"""
        filename = filedialog.askopenfilename(
            title="Select Cosmetic Sound",
            filetypes=[("Audio files", "*.wav *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.app.selected_cosmetic_sound = filename
            self.app.cosmetic_sound_label.config(text=os.path.basename(filename))
    
    def copy_assets(self, mod_folder):
        """Copy selected asset files to the mod folder"""
        copied_assets = []
        
        # Create textures and sounds directories
        textures_dir = os.path.join(mod_folder, "Textures", "Things")
        sounds_dir = os.path.join(mod_folder, "Sounds")
        
        os.makedirs(textures_dir, exist_ok=True)
        os.makedirs(sounds_dir, exist_ok=True)
        
        # Copy item assets
        for item in self.app.items:
            if item.get('texture'):
                try:
                    dest_path = os.path.join(textures_dir, f"{item['defName']}.png")
                    shutil.copy2(item['texture'], dest_path)
                    copied_assets.append(f"Item texture: {item['defName']}.png")
                except Exception as e:
                    print(f"Error copying item texture: {e}")
            
            if item.get('sound'):
                try:
                    ext = os.path.splitext(item['sound'])[1]
                    dest_path = os.path.join(sounds_dir, f"{item['defName']}{ext}")
                    shutil.copy2(item['sound'], dest_path)
                    copied_assets.append(f"Item sound: {item['defName']}{ext}")
                except Exception as e:
                    print(f"Error copying item sound: {e}")
        
        # Copy weapon assets
        for weapon in self.app.weapons:
            if weapon.get('texture'):
                try:
                    dest_path = os.path.join(textures_dir, f"{weapon['defName']}.png")
                    shutil.copy2(weapon['texture'], dest_path)
                    copied_assets.append(f"Weapon texture: {weapon['defName']}.png")
                except Exception as e:
                    print(f"Error copying weapon texture: {e}")
            
            if weapon.get('sound'):
                try:
                    ext = os.path.splitext(weapon['sound'])[1]
                    dest_path = os.path.join(sounds_dir, f"{weapon['defName']}{ext}")
                    shutil.copy2(weapon['sound'], dest_path)
                    copied_assets.append(f"Weapon sound: {weapon['defName']}{ext}")
                except Exception as e:
                    print(f"Error copying weapon sound: {e}")
        
        # Copy building assets
        for building in self.app.buildings:
            if building.get('texture'):
                try:
                    dest_path = os.path.join(textures_dir, f"{building['defName']}.png")
                    shutil.copy2(building['texture'], dest_path)
                    copied_assets.append(f"Building texture: {building['defName']}.png")
                except Exception as e:
                    print(f"Error copying building texture: {e}")
            
            if building.get('sound'):
                try:
                    ext = os.path.splitext(building['sound'])[1]
                    dest_path = os.path.join(sounds_dir, f"{building['defName']}{ext}")
                    shutil.copy2(building['sound'], dest_path)
                    copied_assets.append(f"Building sound: {building['defName']}{ext}")
                except Exception as e:
                    print(f"Error copying building sound: {e}")
        
        # Copy cosmetic assets
        for cosmetic in self.app.cosmetics:
            if cosmetic.get('texture'):
                try:
                    dest_path = os.path.join(textures_dir, f"{cosmetic['defName']}.png")
                    shutil.copy2(cosmetic['texture'], dest_path)
                    copied_assets.append(f"Cosmetic texture: {cosmetic['defName']}.png")
                except Exception as e:
                    print(f"Error copying cosmetic texture: {e}")
            
            if cosmetic.get('sound'):
                try:
                    ext = os.path.splitext(cosmetic['sound'])[1]
                    dest_path = os.path.join(sounds_dir, f"{cosmetic['defName']}{ext}")
                    shutil.copy2(cosmetic['sound'], dest_path)
                    copied_assets.append(f"Cosmetic sound: {cosmetic['defName']}{ext}")
                except Exception as e:
                    print(f"Error copying cosmetic sound: {e}")
        
        return copied_assets
