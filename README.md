# 🎮 RimWorld Mod Maker

A comprehensive Python GUI application for creating custom RimWorld mods with ease. This tool provides an intuitive interface for creating items, weapons, buildings, cosmetics, drugs, workbenches, research projects, and recipes without needing to manually write XML files.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [How to Use](#-how-to-use)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Features

### Content Creation

- **Items**: Create consumables, materials, and misc items with custom properties
- **Weapons**: Design melee and ranged weapons with damage, accuracy, and material settings
- **Buildings**: Build structures with size, hitpoints, beauty, and construction requirements
- **Cosmetics/Apparel**: Create clothing and armor with protection values and body coverage
- **Drugs**: Design custom drugs with addiction mechanics, tolerance, and effects
- **Workbenches**: Create production buildings with power requirements and skill prerequisites
- **Research**: Set up research projects with costs and tech levels
- **Recipes**: Define crafting recipes with ingredients and skill requirements

### Advanced Features

- **Research Integration**: Lock content behind research prerequisites
- **Asset Management**: Import custom textures and sounds for your content
- **XML Generation**: Automatically generates RimWorld-compatible XML files
- **Project Management**: Save and load your mod projects as JSON files
- **Language Support**: Auto-generates localization files
- **Mod Structure**: Creates complete mod folder structure with all necessary files

### Quality of Life

- **Validation**: Built-in validation for defNames and numeric values
- **Preview**: Real-time preview of mod content
- **Export/Import**: Share mod projects with other creators
- **Batch Operations**: Manage multiple content items efficiently

## 📋 Requirements

- **Python 3.7 or higher**
- **tkinter** (usually included with Python)
- **Standard Python libraries**: `os`, `shutil`, `xml.etree.ElementTree`, `json`

### Operating System Support

- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, other distributions)

## 🚀 Installation

### Option 1: Direct Download

1. Download or clone this repository:

   ```bash
   git clone https://github.com/YourUsername/Rimworld-Mod-Maker.git
   cd Rimworld-Mod-Maker
   ```

2. Ensure Python 3.7+ is installed:

   ```bash
   python --version
   ```

3. No additional dependencies needed! All required libraries are part of Python's standard library.

### Option 2: Virtual Environment (Recommended for Development)

```bash
git clone https://github.com/YourUsername/Rimworld-Mod-Maker.git
cd Rimworld-Mod-Maker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 🎯 Quick Start

### Running the Application

**Modern Version (Recommended):**

```bash
python main.py
```

**Legacy Version:**

```bash
python maker.py
```

### Creating Your First Mod

1. **Launch the application**
2. **Fill in mod details** in the "Mod Info" tab:
   - Mod Name: "My Awesome Mod"
   - Author: "Your Name"
   - Version: "1.0.0"
   - Description: Brief description of your mod

3. **Create content** using the tabs:
   - Navigate to "Items", "Weapons", "Buildings", etc.
   - Fill out the forms with your content details
   - Add custom textures/sounds if desired

4. **Set up research** (optional):
   - Go to "Research" tab
   - Create research projects
   - Link content to research prerequisites

5. **Generate your mod**:
   - Click "Select Output Directory"
   - Choose where to save your mod
   - Click "Create Mod"

6. **Install in RimWorld**:
   - Copy the generated mod folder to your RimWorld mods directory
   - Enable the mod in RimWorld's mod manager

## 📖 How to Use

### Creating Different Content Types

#### Items

Create consumables, materials, and miscellaneous items:

- Set basic properties (name, description, market value)
- Configure stack limits and mass
- Add custom graphics and sounds
- Set item categories and trading tags

#### Weapons

Design both melee and ranged weapons:

- Configure damage values and accuracy
- Set weapon classes and materials
- Define sounds and animations
- Add special properties like armor penetration

#### Buildings

Create structures and furniture:

- Set building size and hitpoints
- Configure beauty and comfort values
- Define construction requirements and costs
- Add power consumption or generation

#### Drugs

Design custom pharmaceutical items:

- Set addiction chance and tolerance mechanics
- Configure mood, pain, and consciousness effects
- Define duration and withdrawal symptoms
- Add custom drug categories

#### Workbenches

Create production buildings:

- Set power requirements and skill prerequisites
- Configure work speed and efficiency factors
- Define building size and construction costs
- Add custom recipe support

### Asset Management

1. **Adding Textures**:
   - Click "Select Texture" button in any content tab
   - Choose a PNG file (recommended: 64x64 or 128x128 pixels)
   - File will be automatically copied to mod structure

2. **Adding Sounds**:
   - Click "Select Sound" button
   - Choose WAV or OGG files
   - Sounds will be integrated into the mod

### Research Integration

1. **Create Research Projects**:
   - Go to "Research" tab
   - Define research cost and tech level
   - Set prerequisites if needed

2. **Lock Content Behind Research**:
   - In any research project, use "Add [Content]" buttons
   - Select items/weapons/buildings to unlock
   - Generate mod with automatic prerequisite patches

### Project Management

**Saving Projects**:

- File → Export Mod Data
- Choose location for JSON file
- All content and settings are saved

**Loading Projects**:

- File → Import Mod Data
- Select previously saved JSON file
- All content will be restored

## 🏗️ Project Structure

### Modern Architecture (main.py)

```text
Rimworld-Mod-Maker/
├── main.py              # Application entry point
├── tabs.py              # UI tab creation and management
├── managers.py          # Content and asset management
├── generators.py        # XML file generation
├── utils.py             # File operations and utilities
├── README.md            # This file
└── README_Architecture.md # Detailed architecture docs
```

### Legacy Version

```text
├── maker.py             # Complete application in single file
```

### Generated Mod Structure

```text
YourMod/
├── About/
│   └── About.xml        # Mod metadata
├── Defs/
│   ├── Items.xml        # Item definitions
│   ├── Weapons.xml      # Weapon definitions
│   ├── Buildings.xml    # Building definitions
│   ├── Apparel.xml      # Cosmetic/apparel definitions
│   ├── Drugs.xml        # Drug definitions
│   ├── Workbenches.xml  # Workbench definitions
│   ├── Research.xml     # Research definitions
│   └── Recipes.xml      # Recipe definitions
├── Patches/
│   └── ResearchUnlocks.xml # Research prerequisite patches
├── Textures/Things/     # Custom textures
├── Sounds/              # Custom sounds
└── Languages/English/Keyed/
    └── ModLanguage.xml  # Localization keys
```

## 🛠️ Development

### Code Architecture

The application follows a modular architecture:

- **`main.py`**: Entry point and main application class
- **`tabs.py`**: UI components and tab management
- **`managers.py`**: Business logic for content and asset management
- **`generators.py`**: XML generation for RimWorld compatibility
- **`utils.py`**: File operations and utility functions

### Adding New Content Types

1. **Update `tabs.py`**:
   - Create new tab creation method
   - Add UI form elements
   - Integrate with existing tab structure

2. **Update `managers.py`**:
   - Add content management methods
   - Add research integration
   - Add asset management

3. **Update `generators.py`**:
   - Add XML generation method
   - Update research unlock patches

4. **Update `utils.py`**:
   - Add to export/import functionality
   - Update language file generation

### Customizing the Interface

The application uses `tkinter` for the GUI. Key customization points:

- **Colors**: Modify color schemes in tab creation methods
- **Layout**: Adjust grid layouts in `tabs.py`
- **Validation**: Update validation logic in `managers.py`
- **File Formats**: Modify XML templates in `generators.py`

### Testing

1. **Manual Testing**:
   - Create content in each tab
   - Generate mods and test in RimWorld
   - Verify XML structure and game compatibility

2. **Edge Cases**:
   - Test with special characters in names
   - Test with very large/small numeric values
   - Test asset loading with various file formats

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the existing code style
4. **Test your changes** thoroughly
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Add docstrings to new functions and classes
- Test with multiple content types before submitting
- Update this README if adding new features

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**

- Ensure you're running from the correct directory
- Check that all required files are present
- Verify Python version is 3.7+

**Generated mod doesn't work in RimWorld:**

- Check mod folder is in correct RimWorld mods directory
- Verify mod is enabled in RimWorld mod manager
- Check RimWorld logs for XML errors

**Texture/Sound files not appearing:**

- Ensure files are PNG (textures) or WAV/OGG (sounds)
- Check file permissions
- Verify assets were copied to mod folder

**Application crashes:**

- Check Python console for error messages
- Ensure all required fields are filled
- Try creating a minimal mod first

### Performance Issues

- Large numbers of content items may slow the interface
- Consider breaking large mods into multiple smaller mods
- Asset files should be reasonably sized (textures <1MB recommended)

### Getting Help

1. **Check the console output** for error messages
2. **Review RimWorld logs** after enabling your mod
3. **Test with minimal content** to isolate issues
4. **Check RimWorld modding documentation** for XML requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Planned Features

- [ ] Visual recipe editor
- [ ] Mod compatibility checker
- [ ] Advanced texture management
- [ ] Batch content import from CSV
- [ ] Mod packaging and distribution tools
- [ ] Real-time RimWorld integration
- [ ] Template system for common content types

### Suggestions Welcome

Have ideas for new features? Open an issue or submit a pull request!

---

## 🙏 Acknowledgments

- **RimWorld Community** for extensive modding documentation
- **Ludeon Studios** for creating RimWorld
- **Python tkinter community** for GUI development resources

---

## Happy Modding! 🚀

For detailed architecture information, see [README_Architecture.md](README_Architecture.md)