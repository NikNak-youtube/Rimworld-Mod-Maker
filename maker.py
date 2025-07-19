import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import tkinter as tk

# A rimworld mod maker for creating mods with a simple interface.
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox, ttk
from tkinter import simpledialog, Frame, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH, END, BooleanVar, Checkbutton

class ModMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rimworld Mod Maker")
        self.root.geometry("800x600")
        
        # Variables to store mod information
        self.mod_name = ""
        self.mod_author = ""
        self.mod_description = ""
        self.mod_version = ""
        self.mod_directory = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Title
        title_label = Label(main_frame, text="Rimworld Mod Maker", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Mod Information Section
        info_frame = Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        Label(info_frame, text="Mod Information", font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Mod Name
        Label(info_frame, text="Mod Name:").pack(anchor="w", pady=(10, 0))
        self.name_entry = Entry(info_frame, width=50)
        self.name_entry.pack(fill="x", pady=(5, 0))
        
        # Author
        Label(info_frame, text="Author:").pack(anchor="w", pady=(10, 0))
        self.author_entry = Entry(info_frame, width=50)
        self.author_entry.pack(fill="x", pady=(5, 0))
        
        # Version
        Label(info_frame, text="Version:").pack(anchor="w", pady=(10, 0))
        self.version_entry = Entry(info_frame, width=50)
        self.version_entry.insert(0, "1.0.0")
        self.version_entry.pack(fill="x", pady=(5, 0))
        
        # Description
        Label(info_frame, text="Description:").pack(anchor="w", pady=(10, 0))
        desc_frame = Frame(info_frame)
        desc_frame.pack(fill="x", pady=(5, 0))
        
        self.description_text = Text(desc_frame, height=4, width=50)
        desc_scrollbar = Scrollbar(desc_frame, orient=VERTICAL, command=self.description_text.yview)
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        self.description_text.pack(side=LEFT, fill=BOTH, expand=True)
        desc_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Directory Selection
        dir_frame = Frame(main_frame)
        dir_frame.pack(fill="x", pady=(0, 20))
        
        Label(dir_frame, text="Output Directory", font=("Arial", 12, "bold")).pack(anchor="w")
        
        dir_select_frame = Frame(dir_frame)
        dir_select_frame.pack(fill="x", pady=(10, 0))
        
        self.directory_label = Label(dir_select_frame, text="No directory selected", bg="white", relief="sunken", anchor="w")
        self.directory_label.pack(side=LEFT, fill="x", expand=True, padx=(0, 10))
        
        Button(dir_select_frame, text="Browse", command=self.select_directory).pack(side=RIGHT)
        
        # Mod Components Section
        components_frame = Frame(main_frame)
        components_frame.pack(fill="x", pady=(0, 20))
        
        Label(components_frame, text="Mod Components", font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Checkboxes for different mod components
        self.include_defs = BooleanVar(value=True)
        self.include_patches = BooleanVar(value=False)
        self.include_assemblies = BooleanVar(value=False)
        self.include_textures = BooleanVar(value=False)
        self.include_sounds = BooleanVar(value=False)
        self.include_languages = BooleanVar(value=False)
        
        Checkbutton(components_frame, text="Defs (XML definitions)", variable=self.include_defs).pack(anchor="w", pady=2)
        Checkbutton(components_frame, text="Patches (XML patches)", variable=self.include_patches).pack(anchor="w", pady=2)
        Checkbutton(components_frame, text="Assemblies (C# code)", variable=self.include_assemblies).pack(anchor="w", pady=2)
        Checkbutton(components_frame, text="Textures", variable=self.include_textures).pack(anchor="w", pady=2)
        Checkbutton(components_frame, text="Sounds", variable=self.include_sounds).pack(anchor="w", pady=2)
        Checkbutton(components_frame, text="Languages", variable=self.include_languages).pack(anchor="w", pady=2)
        
        # Buttons
        button_frame = Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        Button(button_frame, text="Create Mod", command=self.create_mod, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=LEFT, padx=(0, 10))
        Button(button_frame, text="Clear", command=self.clear_form).pack(side=LEFT)
        Button(button_frame, text="Exit", command=self.root.quit).pack(side=RIGHT)
    
    def select_directory(self):
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
            
            # Create Defs folder if selected
            if self.include_defs.get():
                self.create_defs_folder(mod_path)
            
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
            
            messagebox.showinfo("Success", f"Mod '{self.mod_name}' created successfully at:\n{mod_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create mod: {str(e)}")
    
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