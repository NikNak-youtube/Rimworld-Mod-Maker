#!/usr/bin/env python3
"""
Rimworld Mod Maker - Main Application Entry Point
A comprehensive tool for creating RimWorld mods with GUI interface.
"""

import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
import tkinter as tk
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox, ttk
from tkinter import simpledialog, Frame, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH, END, BooleanVar, Checkbutton
from tkinter import StringVar, DoubleVar, IntVar, Listbox, SINGLE
from tkinter.ttk import Notebook

from tabs import TabCreator
from managers import ContentManager, AssetManager
from generators import XMLGenerator
from utils import FileUtils


class ModMakerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Rimworld Mod Maker")
        self.root.geometry("900x700")
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Mod Data...", command=self.export_mod_data)
        file_menu.add_command(label="Import Mod Data...", command=self.import_mod_data)
        file_menu.add_separator()
        file_menu.add_command(label="Clear All Data", command=self.clear_all_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Initialize component managers
        self.content_manager = ContentManager(self)
        self.asset_manager = AssetManager(self)
        self.xml_generator = XMLGenerator(self)
        self.file_utils = FileUtils(self)
        self.tab_creator = TabCreator(self)
        
        # Initialize data storage
        self.items = []
        self.weapons = []
        self.buildings = []
        self.cosmetics = []
        self.drugs = []
        self.workbenches = []
        self.research = []
        self.recipes = []
        
        # Initialize asset tracking
        self.selected_item_texture = None
        self.selected_item_sound = None
        self.selected_weapon_texture = None
        self.selected_weapon_sound = None
        self.selected_building_texture = None
        self.selected_building_sound = None
        self.selected_cosmetic_texture = None
        self.selected_cosmetic_sound = None
        self.selected_drug_texture = None
        self.selected_drug_sound = None
        self.selected_workbench_texture = None
        self.selected_workbench_sound = None
        self.selected_directory = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook for tabs
        self.notebook = Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.tab_creator.create_all_tabs()
        
        # Create main control panel
        control_frame = Frame(self.root)
        control_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create Mod button
        Button(control_frame, text="Create Mod", command=self.create_mod, 
               bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
               height=2).pack(side=RIGHT, padx=(10, 0))
        
        # Directory display
        Label(control_frame, text="Output Directory:", font=("Arial", 10, "bold")).pack(side=LEFT)
        self.directory_label = Label(control_frame, text="No directory selected", 
                                   bg="white", relief="sunken", anchor="w")
        self.directory_label.pack(side=LEFT, fill="x", expand=True, padx=(10, 10))
        Button(control_frame, text="Browse", command=self.select_directory).pack(side=LEFT)
    
    def select_directory(self):
        """Wrapper method for file_utils.select_directory"""
        self.file_utils.select_directory()
    
    def create_mod(self):
        """Wrapper method for file_utils.create_mod"""
        self.file_utils.create_mod()
    
    def export_mod_data(self):
        """Wrapper method for file_utils.export_mod_data"""
        self.file_utils.export_mod_data()
    
    def import_mod_data(self):
        """Wrapper method for file_utils.import_mod_data"""
        self.file_utils.import_mod_data()
    
    def clear_all_data(self):
        """Wrapper method for file_utils.clear_all_data"""
        if messagebox.askyesno("Confirm", "This will clear all mod data. Continue?"):
            self.file_utils.clear_all_data()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Rimworld Mod Maker v2.0

A comprehensive tool for creating RimWorld mods with a user-friendly GUI interface.

Features:
• Create items, weapons, buildings, cosmetics, research, and recipes
• Asset management for textures and sounds
• Research unlock system
• XML generation for RimWorld compatibility
• Export/Import mod data

Created with Python and Tkinter
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main application entry point"""
    app = ModMakerApp()
    app.run()


if __name__ == "__main__":
    main()
