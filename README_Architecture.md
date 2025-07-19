# Rimworld Mod Maker - Refactored Architecture

## File Structure

The Rimworld Mod Maker has been successfully split into 5 organized modules for better maintainability and code organization:

### 1. main.py (127 lines)
- **Purpose**: Entry point and main application class
- **Contains**: ModMakerApp class, UI setup, menu bar, application initialization
- **Key Methods**: `__init__()`, `setup_ui()`, `run()`, menu command wrappers
- **Dependencies**: All other modules (tabs, managers, generators, utils)

### 2. tabs.py (640+ lines)
- **Purpose**: All GUI tab creation and layout
- **Contains**: TabCreator class with methods for each tab
- **Key Methods**: 
  - `create_all_tabs()` - Creates all 7 tabs
  - `create_mod_info_tab()` - Basic mod information
  - `create_items_tab()` - Item creation interface
  - `create_weapons_tab()` - Weapon creation interface
  - `create_buildings_tab()` - Building creation interface
  - `create_cosmetics_tab()` - Apparel/cosmetics interface
  - `create_research_tab()` - Research project interface
  - `create_recipes_tab()` - Recipe creation interface
- **UI Components**: Forms, listboxes, scrollable frames, asset selection

### 3. managers.py (750+ lines)
- **Purpose**: Content and asset management
- **Contains**: ContentManager and AssetManager classes
- **Key Components**:
  - **ContentManager**: Add/remove items, weapons, buildings, cosmetics, research, recipes
  - **AssetManager**: Handle texture and sound file selection and copying
- **Key Methods**:
  - `add_item()`, `add_weapon()`, `add_building()`, `add_cosmetic()`, `add_research()`, `add_recipe()`
  - `remove_*()` methods for each content type
  - Research unlock management methods
  - Asset selection and copying methods

### 4. generators.py (520+ lines)
- **Purpose**: XML generation for RimWorld compatibility
- **Contains**: XMLGenerator class
- **Key Methods**:
  - `generate_about_xml()` - Mod metadata
  - `generate_items_xml()` - ThingDefs for items
  - `generate_weapons_xml()` - ThingDefs for weapons
  - `generate_buildings_xml()` - ThingDefs for buildings
  - `generate_cosmetics_xml()` - ThingDefs for apparel
  - `generate_research_xml()` - ResearchProjectDefs
  - `generate_recipes_xml()` - RecipeDefs
  - `generate_research_unlock_patches()` - Research prerequisite patches
- **XML Features**: Proper RimWorld XML structure, minidom formatting

### 5. utils.py (290+ lines)
- **Purpose**: File operations and utility functions
- **Contains**: FileUtils and ValidationUtils classes
- **Key Methods**:
  - `create_mod()` - Main mod creation workflow
  - `create_mod_structure()` - Directory creation
  - `export_mod_data()` / `import_mod_data()` - JSON backup/restore
  - `create_preview_image()` - Placeholder creation
  - `create_language_files()` - Language key generation
  - `clear_all_data()` - Data reset
  - Validation utilities

## Benefits of Refactoring

### 1. **Improved Maintainability**
- Each file has a single, clear responsibility
- Easier to locate and modify specific functionality
- Reduced risk of unintended side effects when making changes

### 2. **Better Code Organization**
- Related functionality grouped together
- Clear separation of concerns (UI, data management, file operations, XML generation)
- Easier for new developers to understand the codebase

### 3. **Enhanced Testability**
- Individual components can be tested in isolation
- Mock objects can be easily substituted for testing
- Clearer interfaces between components

### 4. **Scalability**
- Easy to add new content types (just extend the appropriate manager and generator)
- New UI components can be added to tabs.py without affecting other functionality
- Additional utility functions can be added to utils.py

### 5. **Reusability**
- Components can be reused or extended for similar projects
- Clear APIs make it easy to build upon existing functionality

## Key Features Preserved

All original functionality has been preserved in the refactored version:

- ✅ Complete GUI with 7 tabs (Mod Info, Items, Weapons, Buildings, Cosmetics, Research, Recipes)
- ✅ Asset management for textures and sounds
- ✅ Research unlock system with prerequisites
- ✅ Full RimWorld-compatible XML generation
- ✅ Export/Import mod data functionality
- ✅ File menu with data management options
- ✅ Comprehensive apparel/cosmetics system
- ✅ Recipe creation with ingredient management
- ✅ Scrollable interfaces for large content lists

## Usage

To run the application:
```bash
python main.py
```

The refactored architecture maintains full backward compatibility while providing a much cleaner, more maintainable codebase for future development.
