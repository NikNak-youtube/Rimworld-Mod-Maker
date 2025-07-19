"""
Rimworld Mod Maker - XML Generation Module
Contains all methods for generating RimWorld-compatible XML files.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os


class XMLGenerator:
    def __init__(self, app):
        self.app = app
    
    def generate_about_xml(self, mod_folder):
        """Generate About.xml file"""
        root = ET.Element("ModMetaData")
        
        # Basic mod information
        name = ET.SubElement(root, "name")
        name.text = self.app.name_entry.get() or "My Rimworld Mod"
        
        author = ET.SubElement(root, "author")
        author.text = self.app.author_entry.get() or "Unknown Author"
        
        version = ET.SubElement(root, "version")
        version.text = self.app.version_entry.get() or "1.0.0"
        
        description = ET.SubElement(root, "description")
        description.text = self.app.description_text.get("1.0", "end-1c") or "A custom Rimworld mod."
        
        # Target version
        target_version = ET.SubElement(root, "targetVersion")
        target_version.text = "1.4"
        
        # Dependencies (if any)
        dependencies = ET.SubElement(root, "modDependencies")
        
        # Package ID
        package_id = ET.SubElement(root, "packageId")
        package_id.text = f"modmaker.{(self.app.name_entry.get() or 'mymod').lower().replace(' ', '')}"
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        about_path = os.path.join(mod_folder, "About", "About.xml")
        os.makedirs(os.path.dirname(about_path), exist_ok=True)
        
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_items_xml(self, defs_folder):
        """Generate ThingDefs for items"""
        if not self.app.items:
            return
        
        root = ET.Element("Defs")
        
        for item in self.app.items:
            thing_def = ET.SubElement(root, "ThingDef")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = item['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = item['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = item['description']
            
            # Category
            category = ET.SubElement(thing_def, "category")
            category.text = item['category']
            
            # Thing class
            thing_class = ET.SubElement(thing_def, "thingClass")
            thing_class.text = "ThingWithComps"
            
            # Drawertype
            drawer_type = ET.SubElement(thing_def, "drawerType")
            drawer_type.text = "MapMeshOnly"
            
            # Use hit points
            use_hit_points = ET.SubElement(thing_def, "useHitPoints")
            use_hit_points.text = "false"
            
            # Selectable
            selectable = ET.SubElement(thing_def, "selectable")
            selectable.text = "true"
            
            # Rotatable
            rotatable = ET.SubElement(thing_def, "rotatable")
            rotatable.text = "false"
            
            # Stack limit
            stack_limit = ET.SubElement(thing_def, "stackLimit")
            stack_limit.text = str(item['stackLimit'])
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{item['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_StackCount"
            
            # Sound interact
            if item.get('sound'):
                sound_interact = ET.SubElement(thing_def, "soundInteract")
                sound_interact.text = f"Standard_Drop"  # Default RimWorld sound
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = str(item['marketValue'])
            
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = str(item['mass'])
            
            # Thing categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            thing_category = ET.SubElement(thing_categories, "li")
            thing_category.text = item['category']
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        items_path = os.path.join(defs_folder, "Items.xml")
        with open(items_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_weapons_xml(self, defs_folder):
        """Generate ThingDefs for weapons"""
        if not self.app.weapons:
            return
        
        root = ET.Element("Defs")
        
        for weapon in self.app.weapons:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="BaseWeapon")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = weapon['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = weapon['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = weapon['description']
            
            # Thing class
            if weapon['weaponType'] == "Melee":
                thing_class = ET.SubElement(thing_def, "thingClass")
                thing_class.text = "ThingWithComps"
                weapon_class = "Melee"
            else:
                thing_class = ET.SubElement(thing_def, "thingClass")
                thing_class.text = "ThingWithComps"
                weapon_class = "Ranged"
            
            # Category
            category = ET.SubElement(thing_def, "category")
            category.text = "Item"
            
            # Tech level
            tech_level = ET.SubElement(thing_def, "techLevel")
            tech_level.text = "Industrial"
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{weapon['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Single"
            
            # Sound interact
            if weapon.get('sound'):
                sound_interact = ET.SubElement(thing_def, "soundInteract")
                sound_interact.text = f"Interact_BeatFire"  # Default weapon sound
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = str(weapon['marketValue'])
            
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = str(weapon['mass'])
            
            # Weapon specific stats
            if weapon['weaponType'] == "Melee":
                melee_weapon_damage_multiplier = ET.SubElement(stat_bases, "MeleeWeapon_DamageMultiplier")
                melee_weapon_damage_multiplier.text = "1.0"
                
                melee_weapon_cooldown = ET.SubElement(stat_bases, "MeleeWeapon_CooldownMultiplier")
                melee_weapon_cooldown.text = "1.0"
            
            # Tools (for melee weapons)
            if weapon['weaponType'] == "Melee":
                tools = ET.SubElement(thing_def, "tools")
                tool = ET.SubElement(tools, "li")
                
                tool_label = ET.SubElement(tool, "label")
                tool_label.text = f"{weapon['label']} blade"
                
                capacities = ET.SubElement(tool, "capacities")
                capacity = ET.SubElement(capacities, "li")
                capacity.text = "Cut" if weapon['damageType'] == "Cut" else "Blunt"
                
                power = ET.SubElement(tool, "power")
                power.text = str(weapon['damage'])
                
                cooldown = ET.SubElement(tool, "cooldownTime")
                cooldown.text = "2.0"
            
            # Verbs (for ranged weapons)
            if weapon['weaponType'] == "Ranged":
                verbs = ET.SubElement(thing_def, "verbs")
                verb = ET.SubElement(verbs, "li")
                
                verb_class = ET.SubElement(verb, "verbClass")
                verb_class.text = "Verb_Shoot"
                
                has_standard_command = ET.SubElement(verb, "hasStandardCommand")
                has_standard_command.text = "true"
                
                default_projectile = ET.SubElement(verb, "defaultProjectile")
                default_projectile.text = "Bullet_Rifle"
                
                warmup_time = ET.SubElement(verb, "warmupTime")
                warmup_time.text = "1.0"
                
                range_value = ET.SubElement(verb, "range")
                range_value.text = "25"
                
                sound_cast = ET.SubElement(verb, "soundCast")
                sound_cast.text = "Shot_AssaultRifle"
            
            # Equipment type
            equipment_type = ET.SubElement(thing_def, "equipmentType")
            equipment_type.text = "Primary"
            
            # Thing categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            thing_category = ET.SubElement(thing_categories, "li")
            thing_category.text = "WeaponsRanged" if weapon['weaponType'] == "Ranged" else "WeaponsMelee"
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        weapons_path = os.path.join(defs_folder, "Weapons.xml")
        with open(weapons_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_buildings_xml(self, defs_folder):
        """Generate ThingDefs for buildings"""
        if not self.app.buildings:
            return
        
        root = ET.Element("Defs")
        
        for building in self.app.buildings:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="BuildingBase")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = building['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = building['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = building['description']
            
            # Thing class
            thing_class = ET.SubElement(thing_def, "thingClass")
            thing_class.text = "Building"
            
            # Category
            category = ET.SubElement(thing_def, "category")
            category.text = "Building"
            
            # Building properties
            building_props = ET.SubElement(thing_def, "building")
            building_props.set("Class", "Building")
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{building['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Single"
            
            # Size
            size_parts = building['size'].split(',')
            if len(size_parts) == 2:
                size_elem = ET.SubElement(thing_def, "size")
                size_elem.text = f"({size_parts[0].strip()},{size_parts[1].strip()})"
            
            # Altitudes
            altitude_layer = ET.SubElement(thing_def, "altitudeLayer")
            altitude_layer.text = "Building"
            
            # Passability
            passability = ET.SubElement(thing_def, "passability")
            passability.text = "PassThroughOnly"
            
            # Block wind
            block_wind = ET.SubElement(thing_def, "blockWind")
            block_wind.text = "true"
            
            # Fillage
            fillage = ET.SubElement(thing_def, "fillage")
            fillage.text = "Partial"
            
            # Coversleepers
            cover_sleepers = ET.SubElement(thing_def, "coversleepers")
            cover_sleepers.text = "true"
            
            # Blocking sleep
            blocking_sleep_is_fire = ET.SubElement(thing_def, "blockLight")
            blocking_sleep_is_fire.text = "true"
            
            # Rotatable
            rotatable = ET.SubElement(thing_def, "rotatable")
            rotatable.text = "false"
            
            # Selectable
            selectable = ET.SubElement(thing_def, "selectable")
            selectable.text = "true"
            
            # Drawertype
            drawer_type = ET.SubElement(thing_def, "drawerType")
            drawer_type.text = "MapMeshAndRealTime"
            
            # Repairability
            repairability = ET.SubElement(thing_def, "repairability")
            repairability.text = "Repairability_Normal"
            
            # Terrain affordance needed
            terrain_affordance_needed = ET.SubElement(thing_def, "terrainAffordanceNeeded")
            terrain_affordance_needed.text = "Light"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            max_hit_points = ET.SubElement(stat_bases, "MaxHitPoints")
            max_hit_points.text = str(building['hitPoints'])
            
            work_to_build = ET.SubElement(stat_bases, "WorkToBuild")
            work_to_build.text = str(building['workToBuild'])
            
            flammability = ET.SubElement(stat_bases, "Flammability")
            flammability.text = "1.0"
            
            # Building
            building_elem = ET.SubElement(thing_def, "building")
            is_inert = ET.SubElement(building_elem, "isInert")
            is_inert.text = "true"
            
            # Cost list (basic materials)
            cost_list = ET.SubElement(thing_def, "costList")
            steel_cost = ET.SubElement(cost_list, "Steel")
            steel_cost.text = "25"
            
            # Research prerequisites (empty for now)
            research_prerequisites = ET.SubElement(thing_def, "researchPrerequisites")
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        buildings_path = os.path.join(defs_folder, "Buildings.xml")
        with open(buildings_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_cosmetics_xml(self, defs_folder):
        """Generate ThingDefs for cosmetics/apparel"""
        if not self.app.cosmetics:
            return
        
        root = ET.Element("Defs")
        
        for cosmetic in self.app.cosmetics:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="ApparelBase")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = cosmetic['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = cosmetic['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = cosmetic['description']
            
            # Tech level
            tech_level = ET.SubElement(thing_def, "techLevel")
            tech_level.text = "Industrial"
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{cosmetic['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Single"
            
            # Generate wearable
            generate_allowable_designators = ET.SubElement(thing_def, "generateAllowableDesignators")
            generate_allowable_designators.text = "true"
            
            # Use hit points
            use_hit_points = ET.SubElement(thing_def, "useHitPoints")
            use_hit_points.text = "true"
            
            # Path cost
            path_cost = ET.SubElement(thing_def, "pathCost")
            path_cost.text = "15"
            
            # Selectable
            selectable = ET.SubElement(thing_def, "selectable")
            selectable.text = "true"
            
            # Apparel
            apparel = ET.SubElement(thing_def, "apparel")
            
            # Body part groups
            body_part_groups = ET.SubElement(apparel, "bodyPartGroups")
            for part in cosmetic['bodyParts'].split(','):
                part = part.strip()
                if part:
                    part_elem = ET.SubElement(body_part_groups, "li")
                    part_elem.text = part
            
            # Worngrafix
            worn_graphic = ET.SubElement(apparel, "wornGraphicPath")
            worn_graphic.text = f"Things/Apparel/{cosmetic['defName']}"
            
            # Layers
            layers = ET.SubElement(apparel, "layers")
            layer_elem = ET.SubElement(layers, "li")
            layer_elem.text = cosmetic['layer']
            
            # Default outfit tags
            default_outfit_tags = ET.SubElement(apparel, "defaultOutfitTags")
            tag = ET.SubElement(default_outfit_tags, "li")
            tag.text = "Worker"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            max_hit_points = ET.SubElement(stat_bases, "MaxHitPoints")
            max_hit_points.text = "100"
            
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = str(cosmetic['marketValue'])
            
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = str(cosmetic['mass'])
            
            work_to_make = ET.SubElement(stat_bases, "WorkToMake")
            work_to_make.text = str(cosmetic['workToMake'])
            
            # Armor ratings if any
            if float(cosmetic['armorSharp']) > 0:
                armor_sharp = ET.SubElement(stat_bases, "ArmorRating_Sharp")
                armor_sharp.text = str(cosmetic['armorSharp'])
            
            if float(cosmetic['armorBlunt']) > 0:
                armor_blunt = ET.SubElement(stat_bases, "ArmorRating_Blunt")
                armor_blunt.text = str(cosmetic['armorBlunt'])
            
            if float(cosmetic['armorHeat']) > 0:
                armor_heat = ET.SubElement(stat_bases, "ArmorRating_Heat")
                armor_heat.text = str(cosmetic['armorHeat'])
            
            # Equip delay
            equip_delay = ET.SubElement(stat_bases, "EquipDelay")
            equip_delay.text = "1.5"
            
            # Thing categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            thing_category = ET.SubElement(thing_categories, "li")
            thing_category.text = "Apparel"
            
            # Trading tags
            trading_tags = ET.SubElement(thing_def, "tradeTags")
            trade_tag = ET.SubElement(trading_tags, "li")
            trade_tag.text = "Clothing"
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        cosmetics_path = os.path.join(defs_folder, "Apparel.xml")
        with open(cosmetics_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_research_xml(self, defs_folder):
        """Generate ResearchProjectDefs for research"""
        if not self.app.research:
            return
        
        root = ET.Element("Defs")
        
        for research in self.app.research:
            research_def = ET.SubElement(root, "ResearchProjectDef")
            
            # DefName
            defname = ET.SubElement(research_def, "defName")
            defname.text = research['defName']
            
            # Label
            label = ET.SubElement(research_def, "label")
            label.text = research['label']
            
            # Description
            description = ET.SubElement(research_def, "description")
            description.text = research['description']
            
            # Base cost
            base_cost = ET.SubElement(research_def, "baseCost")
            base_cost.text = str(research['baseCost'])
            
            # Tech level
            tech_level = ET.SubElement(research_def, "techLevel")
            tech_level.text = research['techLevel']
            
            # Research tab
            tab = ET.SubElement(research_def, "tab")
            tab.text = "Main"
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        research_path = os.path.join(defs_folder, "Research.xml")
        with open(research_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_recipes_xml(self, defs_folder):
        """Generate RecipeDefs for recipes"""
        if not self.app.recipes:
            return
        
        root = ET.Element("Defs")
        
        for recipe in self.app.recipes:
            recipe_def = ET.SubElement(root, "RecipeDef")
            
            # DefName
            defname = ET.SubElement(recipe_def, "defName")
            defname.text = recipe['defName']
            
            # Label
            label = ET.SubElement(recipe_def, "label")
            label.text = recipe['label']
            
            # Description
            description = ET.SubElement(recipe_def, "description")
            description.text = recipe['description']
            
            # Job string
            job_string = ET.SubElement(recipe_def, "jobString")
            job_string.text = f"Making {recipe['label']}."
            
            # Work amount
            work_amount = ET.SubElement(recipe_def, "workAmount")
            work_amount.text = str(recipe['workAmount'])
            
            # Work skill
            work_skill = ET.SubElement(recipe_def, "workSkill")
            work_skill.text = "Crafting"
            
            # Effect working
            effect_working = ET.SubElement(recipe_def, "effectWorking")
            effect_working.text = "Cook"
            
            # Sound working
            sound_working = ET.SubElement(recipe_def, "soundWorking")
            sound_working.text = "Recipe_CookMeal"
            
            # Ingredients
            ingredients = ET.SubElement(recipe_def, "ingredients")
            
            # Parse ingredient string (format: DefName:Count)
            for ingredient_str in recipe['ingredients'].split(','):
                ingredient_str = ingredient_str.strip()
                if ':' in ingredient_str:
                    ing_name, ing_count = ingredient_str.split(':', 1)
                    ing_name = ing_name.strip()
                    ing_count = ing_count.strip()
                    
                    ingredient = ET.SubElement(ingredients, "li")
                    filter_elem = ET.SubElement(ingredient, "filter")
                    things_defs = ET.SubElement(filter_elem, "thingDefs")
                    thing_def = ET.SubElement(things_defs, "li")
                    thing_def.text = ing_name
                    
                    count = ET.SubElement(ingredient, "count")
                    count.text = ing_count
            
            # Products
            products = ET.SubElement(recipe_def, "products")
            product = ET.SubElement(products, recipe['product'])
            product.text = str(recipe['productCount'])
            
            # Default ingredient filter
            default_ingredient_filter = ET.SubElement(recipe_def, "defaultIngredientFilter")
            categories = ET.SubElement(default_ingredient_filter, "categories")
            category = ET.SubElement(categories, "li")
            category.text = "Root"
            
            # Recipe users (what workbenches can use this recipe)
            recipe_users = ET.SubElement(recipe_def, "recipeUsers")
            user = ET.SubElement(recipe_users, "li")
            user.text = "CraftingSpot"  # Basic crafting spot
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        recipes_path = os.path.join(defs_folder, "Recipes.xml")
        with open(recipes_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_research_unlock_patches(self, patches_folder):
        """Generate patches to add research prerequisites to items/weapons/buildings/cosmetics"""
        if not self.app.research:
            return
        
        patches = []
        
        for research in self.app.research:
            research_defname = research['defName']
            
            # Create patches for items
            for item_text in research['unlockedItems']:
                if ' - ' in item_text:
                    item_defname = item_text.split(' - ')[0]
                    patches.append(self._create_research_patch(item_defname, research_defname))
            
            # Create patches for weapons
            for weapon_text in research['unlockedWeapons']:
                if ' - ' in weapon_text:
                    weapon_defname = weapon_text.split(' - ')[0]
                    patches.append(self._create_research_patch(weapon_defname, research_defname))
            
            # Create patches for buildings
            for building_text in research['unlockedBuildings']:
                if ' - ' in building_text:
                    building_defname = building_text.split(' - ')[0]
                    patches.append(self._create_research_patch(building_defname, research_defname))
            
            # Create patches for cosmetics
            for cosmetic_text in research['unlockedCosmetics']:
                if ' - ' in cosmetic_text:
                    cosmetic_defname = cosmetic_text.split(' - ')[0]
                    patches.append(self._create_research_patch(cosmetic_defname, research_defname))
        
        if patches:
            # Write patches to file
            root = ET.Element("Patch")
            
            for patch in patches:
                root.append(patch)
            
            rough_string = ET.tostring(root, 'unicode')
            reparsed = minidom.parseString(rough_string)
            
            patch_path = os.path.join(patches_folder, "ResearchUnlocks.xml")
            with open(patch_path, 'w', encoding='utf-8') as f:
                f.write(reparsed.toprettyxml(indent="  "))
    
    def _create_research_patch(self, def_name, research_defname):
        """Create a research prerequisite patch for a specific def"""
        operation = ET.Element("Operation", Class="PatchOperationAdd")
        
        xpath = ET.SubElement(operation, "xpath")
        xpath.text = f"Defs/ThingDef[defName='{def_name}']"
        
        value = ET.SubElement(operation, "value")
        research_prerequisites = ET.SubElement(value, "researchPrerequisites")
        prerequisite = ET.SubElement(research_prerequisites, "li")
        prerequisite.text = research_defname
        
        return operation
