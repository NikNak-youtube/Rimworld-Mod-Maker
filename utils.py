"""
Rimworld Mod Maker - Utility Functions Module
Contains file operations, mod creation, and utility functions.
"""

import os
import shutil
from tkinter import filedialog, messagebox


class FileUtils:
    def __init__(self, app):
        self.app = app
    
    def select_directory(self):
        """Select output directory for the mod"""
        directory = filedialog.askdirectory(title="Select output directory for your mod")
        if directory:
            self.app.selected_directory = directory
            self.app.directory_label.config(text=directory)
    
    def create_mod_structure(self, mod_folder):
        """Create the basic mod folder structure"""
        # Create basic directories
        directories = [
            "About",
            "Defs",
            "Textures/Things",
            "Sounds",
            "Patches",
            "Assemblies",
            "Languages/English/Keyed"
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(mod_folder, directory), exist_ok=True)
    
    def create_mod(self):
        """Create the complete mod with all files and structure"""
        # Validate required fields
        mod_name = self.app.name_entry.get().strip()
        if not mod_name:
            messagebox.showerror("Error", "Mod name is required!")
            return
        
        if not hasattr(self.app, 'selected_directory') or not self.app.selected_directory:
            messagebox.showerror("Error", "Please select an output directory!")
            return
        
        try:
            # Create mod folder
            mod_folder = os.path.join(self.app.selected_directory, mod_name)
            
            # Check if folder already exists
            if os.path.exists(mod_folder):
                if not messagebox.askyesno("Folder Exists", 
                    f"The folder '{mod_name}' already exists. Do you want to overwrite it?"):
                    return
                # Remove existing folder
                shutil.rmtree(mod_folder)
            
            # Create folder structure
            self.create_mod_structure(mod_folder)
            
            # Generate XML files
            defs_folder = os.path.join(mod_folder, "Defs")
            patches_folder = os.path.join(mod_folder, "Patches")
            
            # Generate About.xml
            self.app.xml_generator.generate_about_xml(mod_folder)
            
            # Generate content XML files
            if self.app.items:
                self.app.xml_generator.generate_items_xml(defs_folder)
            
            if self.app.weapons:
                self.app.xml_generator.generate_weapons_xml(defs_folder)
            
            if self.app.buildings:
                self.app.xml_generator.generate_buildings_xml(defs_folder)
            
            if self.app.cosmetics:
                self.app.xml_generator.generate_cosmetics_xml(defs_folder)
            
            if self.app.drugs:
                self.app.xml_generator.generate_drugs_xml(defs_folder)
            
            if self.app.workbenches:
                self.app.xml_generator.generate_workbenches_xml(defs_folder)
            
            if self.app.research:
                self.app.xml_generator.generate_research_xml(defs_folder)
                # Generate research unlock patches
                self.app.xml_generator.generate_research_unlock_patches(patches_folder)
            
            if self.app.recipes:
                self.app.xml_generator.generate_recipes_xml(defs_folder)
            
            # Copy assets
            copied_assets = self.app.asset_manager.copy_assets(mod_folder)
            
            # Create preview image placeholder
            self.create_preview_image(mod_folder)
            
            # Create language files
            self.create_language_files(mod_folder)
            
            # Show success message
            message = f"Mod '{mod_name}' created successfully!\n\nLocation: {mod_folder}\n\n"
            
            if copied_assets:
                message += f"Copied {len(copied_assets)} asset files:\n"
                for asset in copied_assets[:5]:  # Show first 5 assets
                    message += f"- {asset}\n"
                if len(copied_assets) > 5:
                    message += f"... and {len(copied_assets) - 5} more"
            else:
                message += "No custom assets were copied."
            
            messagebox.showinfo("Success", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the mod:\n{str(e)}")
    
    def create_preview_image(self, mod_folder):
        """Create a placeholder preview image for the mod"""
        about_folder = os.path.join(mod_folder, "About")
        preview_path = os.path.join(about_folder, "Preview.png")
        
        # Create a simple text file explaining how to add a preview
        readme_path = os.path.join(about_folder, "README_Preview.txt")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("To add a preview image for your mod:\n")
            f.write("1. Create or find a 512x512 pixel PNG image\n")
            f.write("2. Name it 'Preview.png'\n")
            f.write("3. Replace this file with your preview image\n")
            f.write("4. Delete this README_Preview.txt file\n")
    
    def create_language_files(self, mod_folder):
        """Create basic language files for the mod"""
        lang_folder = os.path.join(mod_folder, "Languages", "English", "Keyed")
        
        # Create a basic language file with keys for custom content
        lang_content = []
        lang_content.append('<?xml version="1.0" encoding="utf-8" ?>')
        lang_content.append('<LanguageData>')
        lang_content.append('')
        lang_content.append('  <!-- Mod-specific translations can be added here -->')
        
        # Add language keys for items
        if self.app.items:
            lang_content.append('')
            lang_content.append('  <!-- Items -->')
            for item in self.app.items:
                safe_name = item['defName'].replace(' ', '_')
                if item.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{item["description"]}</{safe_name}.description>')
        
        # Add language keys for weapons
        if self.app.weapons:
            lang_content.append('')
            lang_content.append('  <!-- Weapons -->')
            for weapon in self.app.weapons:
                safe_name = weapon['defName'].replace(' ', '_')
                if weapon.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{weapon["description"]}</{safe_name}.description>')
        
        # Add language keys for buildings
        if self.app.buildings:
            lang_content.append('')
            lang_content.append('  <!-- Buildings -->')
            for building in self.app.buildings:
                safe_name = building['defName'].replace(' ', '_')
                if building.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{building["description"]}</{safe_name}.description>')
        
        # Add language keys for cosmetics
        if self.app.cosmetics:
            lang_content.append('')
            lang_content.append('  <!-- Cosmetics -->')
            for cosmetic in self.app.cosmetics:
                safe_name = cosmetic['defName'].replace(' ', '_')
                if cosmetic.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{cosmetic["description"]}</{safe_name}.description>')
        
        # Add language keys for drugs
        if self.app.drugs:
            lang_content.append('')
            lang_content.append('  <!-- Drugs -->')
            for drug in self.app.drugs:
                safe_name = drug['defName'].replace(' ', '_')
                if drug.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{drug["description"]}</{safe_name}.description>')
        
        # Add language keys for workbenches
        if self.app.workbenches:
            lang_content.append('')
            lang_content.append('  <!-- Workbenches -->')
            for workbench in self.app.workbenches:
                safe_name = workbench['defName'].replace(' ', '_')
                if workbench.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{workbench["description"]}</{safe_name}.description>')
        
        # Add language keys for research
        if self.app.research:
            lang_content.append('')
            lang_content.append('  <!-- Research -->')
            for research in self.app.research:
                safe_name = research['defName'].replace(' ', '_')
                if research.get('description'):
                    lang_content.append(f'  <{safe_name}.description>{research["description"]}</{safe_name}.description>')
        
        lang_content.append('')
        lang_content.append('</LanguageData>')
        
        # Write language file
        lang_file_path = os.path.join(lang_folder, "ModLanguage.xml")
        with open(lang_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lang_content))
    
    def export_mod_data(self):
        """Export all mod data to a JSON file for backup/sharing"""
        import json
        from tkinter import filedialog
        
        if not any([self.app.items, self.app.weapons, self.app.buildings, 
                   self.app.cosmetics, self.app.drugs, self.app.workbenches, 
                   self.app.research, self.app.recipes]):
            messagebox.showwarning("Warning", "No mod content to export!")
            return
        
        # Prepare data for export
        export_data = {
            'mod_info': {
                'name': self.app.name_entry.get(),
                'author': self.app.author_entry.get(),
                'version': self.app.version_entry.get(),
                'description': self.app.description_text.get("1.0", "end-1c")
            },
            'items': self.app.items,
            'weapons': self.app.weapons,
            'buildings': self.app.buildings,
            'cosmetics': self.app.cosmetics,
            'drugs': self.app.drugs,
            'workbenches': self.app.workbenches,
            'research': self.app.research,
            'recipes': self.app.recipes,
            'settings': {
                'include_defs': self.app.include_defs.get(),
                'include_patches': self.app.include_patches.get(),
                'include_assemblies': self.app.include_assemblies.get(),
                'include_textures': self.app.include_textures.get(),
                'include_sounds': self.app.include_sounds.get(),
                'include_languages': self.app.include_languages.get()
            }
        }
        
        # Select save location
        filename = filedialog.asksaveasfilename(
            title="Export Mod Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Mod data exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export mod data:\n{str(e)}")
    
    def import_mod_data(self):
        """Import mod data from a JSON file"""
        import json
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Import Mod Data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Confirm import
            if not messagebox.askyesno("Confirm Import", 
                "This will replace all current mod data. Continue?"):
                return
            
            # Clear existing data
            self.clear_all_data()
            
            # Import mod info
            if 'mod_info' in import_data:
                mod_info = import_data['mod_info']
                self.app.name_entry.delete(0, 'end')
                self.app.name_entry.insert(0, mod_info.get('name', ''))
                self.app.author_entry.delete(0, 'end')
                self.app.author_entry.insert(0, mod_info.get('author', ''))
                self.app.version_entry.delete(0, 'end')
                self.app.version_entry.insert(0, mod_info.get('version', '1.0.0'))
                self.app.description_text.delete("1.0", 'end')
                self.app.description_text.insert("1.0", mod_info.get('description', ''))
            
            # Import content
            self.app.items = import_data.get('items', [])
            self.app.weapons = import_data.get('weapons', [])
            self.app.buildings = import_data.get('buildings', [])
            self.app.cosmetics = import_data.get('cosmetics', [])
            self.app.drugs = import_data.get('drugs', [])
            self.app.workbenches = import_data.get('workbenches', [])
            self.app.research = import_data.get('research', [])
            self.app.recipes = import_data.get('recipes', [])
            
            # Import settings
            if 'settings' in import_data:
                settings = import_data['settings']
                self.app.include_defs.set(settings.get('include_defs', True))
                self.app.include_patches.set(settings.get('include_patches', False))
                self.app.include_assemblies.set(settings.get('include_assemblies', False))
                self.app.include_textures.set(settings.get('include_textures', False))
                self.app.include_sounds.set(settings.get('include_sounds', False))
                self.app.include_languages.set(settings.get('include_languages', False))
            
            # Refresh all listboxes
            self.refresh_all_listboxes()
            
            messagebox.showinfo("Success", f"Mod data imported from:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import mod data:\n{str(e)}")
    
    def clear_all_data(self):
        """Clear all mod data"""
        # Clear lists
        self.app.items.clear()
        self.app.weapons.clear()
        self.app.buildings.clear()
        self.app.cosmetics.clear()
        self.app.drugs.clear()
        self.app.workbenches.clear()
        self.app.research.clear()
        self.app.recipes.clear()
        
        # Clear listboxes
        self.refresh_all_listboxes()
    
    def refresh_all_listboxes(self):
        """Refresh all content listboxes"""
        # Clear and populate items listbox
        self.app.items_listbox.delete(0, 'end')
        for item in self.app.items:
            self.app.items_listbox.insert('end', f"{item['defName']} - {item['label']}")
        
        # Clear and populate weapons listbox
        self.app.weapons_listbox.delete(0, 'end')
        for weapon in self.app.weapons:
            self.app.weapons_listbox.insert('end', f"{weapon['defName']} - {weapon['label']}")
        
        # Clear and populate buildings listbox
        self.app.buildings_listbox.delete(0, 'end')
        for building in self.app.buildings:
            self.app.buildings_listbox.insert('end', f"{building['defName']} - {building['label']}")
        
        # Clear and populate cosmetics listbox
        self.app.cosmetics_listbox.delete(0, 'end')
        for cosmetic in self.app.cosmetics:
            self.app.cosmetics_listbox.insert('end', f"{cosmetic['defName']} - {cosmetic['label']}")
        
        # Clear and populate drugs listbox
        self.app.drugs_listbox.delete(0, 'end')
        for drug in self.app.drugs:
            self.app.drugs_listbox.insert('end', f"{drug['defName']} - {drug['label']}")
        
        # Clear and populate workbenches listbox
        self.app.workbenches_listbox.delete(0, 'end')
        for workbench in self.app.workbenches:
            self.app.workbenches_listbox.insert('end', f"{workbench['defName']} - {workbench['label']}")
        
        # Clear and populate research listbox
        self.app.research_listbox.delete(0, 'end')
        for research in self.app.research:
            self.app.research_listbox.insert('end', f"{research['defName']} - {research['label']}")
        
        # Clear and populate recipes listbox
        self.app.recipes_listbox.delete(0, 'end')
        for recipe in self.app.recipes:
            self.app.recipes_listbox.insert('end', f"{recipe['defName']} - {recipe['label']}")
        
        # Clear and populate research unlock listboxes
        self.app.research_unlocked_items.delete(0, 'end')
        self.app.research_unlocked_weapons.delete(0, 'end')
        self.app.research_unlocked_buildings.delete(0, 'end')
        self.app.research_unlocked_cosmetics.delete(0, 'end')
        self.app.research_unlocked_drugs.delete(0, 'end')
        self.app.research_unlocked_workbenches.delete(0, 'end')


class ValidationUtils:
    """Utility functions for validating mod content"""
    
    @staticmethod
    def validate_defname(defname):
        """Validate that a defname follows RimWorld conventions"""
        if not defname:
            return False, "DefName cannot be empty"
        
        # Check for invalid characters
        invalid_chars = [' ', '-', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=']
        for char in invalid_chars:
            if char in defname:
                return False, f"DefName cannot contain '{char}'"
        
        # Check length
        if len(defname) > 50:
            return False, "DefName is too long (max 50 characters)"
        
        return True, ""
    
    @staticmethod
    def validate_numeric_field(value, field_name, min_val=None, max_val=None):
        """Validate numeric input fields"""
        try:
            num_val = float(value)
            if min_val is not None and num_val < min_val:
                return False, f"{field_name} must be at least {min_val}"
            if max_val is not None and num_val > max_val:
                return False, f"{field_name} must be at most {max_val}"
            return True, ""
        except ValueError:
            return False, f"{field_name} must be a valid number"
