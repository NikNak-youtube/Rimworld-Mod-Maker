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
    
    def generate_drugs_xml(self, defs_folder):
        """Generate ThingDefs for drugs"""
        if not self.app.drugs:
            return
        
        root = ET.Element("Defs")
        
        for drug in self.app.drugs:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="DrugBase")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = drug['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = drug['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = drug['description']
            
            # Tech level
            tech_level = ET.SubElement(thing_def, "techLevel")
            tech_level.text = "Industrial"
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{drug['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_StackCount"
            
            # Social properness
            social_properness = ET.SubElement(thing_def, "socialProperness")
            social_properness.text = "Rude"
            
            # Use hit points
            use_hit_points = ET.SubElement(thing_def, "useHitPoints")
            use_hit_points.text = "true"
            
            # Stackable
            stackable = ET.SubElement(thing_def, "stackLimit")
            stackable.text = "75"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            max_hit_points = ET.SubElement(stat_bases, "MaxHitPoints")
            max_hit_points.text = "50"
            
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = str(drug['marketValue'])
            
            mass = ET.SubElement(stat_bases, "Mass")
            mass.text = str(drug['mass'])
            
            flammability = ET.SubElement(stat_bases, "Flammability")
            flammability.text = "1.0"
            
            deterioration_rate = ET.SubElement(stat_bases, "DeteriorationRate")
            deterioration_rate.text = "6.0"
            
            # Nutrition if it provides any
            if float(drug['nutrition']) > 0:
                nutrition = ET.SubElement(stat_bases, "Nutrition")
                nutrition.text = str(drug['nutrition'])
            
            # Thing categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            thing_category = ET.SubElement(thing_categories, "li")
            thing_category.text = "Drugs"
            
            # Ingestible properties
            ingestible = ET.SubElement(thing_def, "ingestible")
            
            food_type = ET.SubElement(ingestible, "foodType")
            food_type.text = "Processed"
            
            joy_kind = ET.SubElement(ingestible, "joyKind")
            joy_kind.text = "Chemical"
            
            joy_offset = ET.SubElement(ingestible, "joy")
            joy_offset.text = str(drug['joy'])
            
            base_ingestion_ticks = ET.SubElement(ingestible, "baseIngestTicks")
            base_ingestion_ticks.text = "240"
            
            chair_search_radius = ET.SubElement(ingestible, "chairSearchRadius")
            chair_search_radius.text = "4"
            
            nurseable = ET.SubElement(ingestible, "nurseable")
            nurseable.text = "true"
            
            # Drug category and addiction
            drug_category = ET.SubElement(ingestible, "drugCategory")
            drug_category.text = "Hard"
            
            addiction_chance = ET.SubElement(ingestible, "addictiveness")
            addiction_chance.text = str(drug['addictionChance'])
            
            min_tolerance = ET.SubElement(ingestible, "minToleranceToAddict")
            min_tolerance.text = "0.1"
            
            # Tolerance building
            tolerance_chemical = ET.SubElement(ingestible, "toleranceChemical")
            tolerance_chemical.text = drug['defName']
            
            # Outcome effects
            outcome_doers = ET.SubElement(ingestible, "outcomeDoers")
            
            # Main effect
            outcome = ET.SubElement(outcome_doers, "li", Class="IngestionOutcomeDoer_GiveHediff")
            hediff_def = ET.SubElement(outcome, "hediffDef")
            hediff_def.text = f"{drug['defName']}_Effect"
            severity = ET.SubElement(outcome, "severity")
            severity.text = "1.0"
            tolerance_chemical_outcome = ET.SubElement(outcome, "toleranceChemical")
            tolerance_chemical_outcome.text = drug['defName']
            divide_by_body_size = ET.SubElement(outcome, "divideByBodySize")
            divide_by_body_size.text = "true"
            
            # Tolerance effect
            tolerance_outcome = ET.SubElement(outcome_doers, "li", Class="IngestionOutcomeDoer_OffsetTolerance")
            tolerance_chemical_tolerance = ET.SubElement(tolerance_outcome, "toleranceChemical")
            tolerance_chemical_tolerance.text = drug['defName']
            tolerance_offset = ET.SubElement(tolerance_outcome, "offset")
            tolerance_offset.text = str(drug['toleranceGain'])
            
            # Trading tags
            trading_tags = ET.SubElement(thing_def, "tradeTags")
            trade_tag = ET.SubElement(trading_tags, "li")
            trade_tag.text = "ExoticMisc"
        
        # Generate the hediff (effect) def
        for drug in self.app.drugs:
            hediff_def = ET.SubElement(root, "HediffDef")
            
            # DefName
            hediff_defname = ET.SubElement(hediff_def, "defName")
            hediff_defname.text = f"{drug['defName']}_Effect"
            
            # Label
            hediff_label = ET.SubElement(hediff_def, "label")
            hediff_label.text = f"{drug['label']} effect"
            
            # Label noun
            label_noun = ET.SubElement(hediff_def, "labelNoun")
            label_noun.text = f"{drug['label']} effect"
            
            # Description
            hediff_description = ET.SubElement(hediff_def, "description")
            hediff_description.text = f"Active effects of {drug['label']}."
            
            # Hediff class
            hediff_class = ET.SubElement(hediff_def, "hediffClass")
            hediff_class.text = "HediffWithComps"
            
            # Default label color
            default_label_color = ET.SubElement(hediff_def, "defaultLabelColor")
            default_label_color.text = "(1,0,0.5)"
            
            # Scene overlay
            scene_overlay = ET.SubElement(hediff_def, "scenarioCanAdd")
            scene_overlay.text = "true"
            
            # Max severity
            max_severity = ET.SubElement(hediff_def, "maxSeverity")
            max_severity.text = "1.0"
            
            # Is bad
            is_bad = ET.SubElement(hediff_def, "isBad")
            is_bad.text = "false"
            
            # Comps
            comps = ET.SubElement(hediff_def, "comps")
            
            # Severity per day comp
            severity_comp = ET.SubElement(comps, "li", Class="HediffComp_SeverityPerDay")
            severity_per_day = ET.SubElement(severity_comp, "severityPerDay")
            severity_per_day.text = str(-24.0 / float(drug['duration']))  # Duration in hours to severity decay
            
            # Effects on different body parts
            stages = ET.SubElement(hediff_def, "stages")
            stage = ET.SubElement(stages, "li")
            
            # Stat offsets
            if float(drug['painReduction']) != 0 or float(drug['moodOffset']) != 0 or float(drug['consciousnessOffset']) != 0:
                stat_offsets = ET.SubElement(stage, "statOffsets")
                
                if float(drug['painReduction']) != 0:
                    pain_sensitivity = ET.SubElement(stat_offsets, "PainShockThreshold")
                    pain_sensitivity.text = str(drug['painReduction'])
                
                if float(drug['consciousnessOffset']) != 0:
                    consciousness = ET.SubElement(stat_offsets, "Consciousness")
                    consciousness.text = str(drug['consciousnessOffset'])
            
            # Mood offset
            if float(drug['moodOffset']) != 0:
                mood_offset = ET.SubElement(stage, "moodOffset")
                mood_offset.text = str(drug['moodOffset'])
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        drugs_path = os.path.join(defs_folder, "Drugs.xml")
        with open(drugs_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    def generate_workbenches_xml(self, defs_folder):
        """Generate ThingDefs for workbenches"""
        if not self.app.workbenches:
            return
        
        root = ET.Element("Defs")
        
        for workbench in self.app.workbenches:
            thing_def = ET.SubElement(root, "ThingDef", ParentName="BenchBase")
            
            # DefName
            defname = ET.SubElement(thing_def, "defName")
            defname.text = workbench['defName']
            
            # Label
            label = ET.SubElement(thing_def, "label")
            label.text = workbench['label']
            
            # Description
            description = ET.SubElement(thing_def, "description")
            description.text = workbench['description']
            
            # Tech level
            tech_level = ET.SubElement(thing_def, "techLevel")
            tech_level.text = "Industrial"
            
            # Graphic data
            graphic_data = ET.SubElement(thing_def, "graphicData")
            texture_path = ET.SubElement(graphic_data, "texPath")
            texture_path.text = f"Things/{workbench['defName']}"
            graphic_class = ET.SubElement(graphic_data, "graphicClass")
            graphic_class.text = "Graphic_Multi"
            draw_size = ET.SubElement(graphic_data, "drawSize")
            draw_size.text = f"({workbench['sizeX']},{workbench['sizeZ']})"
            
            # Cost list
            cost_list = ET.SubElement(thing_def, "costList")
            steel_cost = ET.SubElement(cost_list, "Steel")
            steel_cost.text = str(workbench['steelCost'])
            
            if int(workbench['componentCost']) > 0:
                component_cost = ET.SubElement(cost_list, "ComponentIndustrial")
                component_cost.text = str(workbench['componentCost'])
            
            # Alt building
            alt_building = ET.SubElement(thing_def, "altitudeLayer")
            alt_building.text = "Building"
            
            # Pass ability
            pass_ability = ET.SubElement(thing_def, "passability")
            pass_ability.text = "PassThroughOnly"
            
            # Path cost
            path_cost = ET.SubElement(thing_def, "pathCost")
            path_cost.text = "50"
            
            # Block wind
            block_wind = ET.SubElement(thing_def, "blockWind")
            block_wind.text = "true"
            
            # Fillage
            fillage = ET.SubElement(thing_def, "fillPercent")
            fillage.text = "0.5"
            
            # Use hit points
            use_hit_points = ET.SubElement(thing_def, "useHitPoints")
            use_hit_points.text = "true"
            
            # Size
            size = ET.SubElement(thing_def, "size")
            size.text = f"({workbench['sizeX']},{workbench['sizeZ']})"
            
            # Stats
            stat_bases = ET.SubElement(thing_def, "statBases")
            
            max_hit_points = ET.SubElement(stat_bases, "MaxHitPoints")
            max_hit_points.text = "180"
            
            market_value = ET.SubElement(stat_bases, "MarketValue")
            market_value.text = str(workbench['marketValue'])
            
            work_to_make = ET.SubElement(stat_bases, "WorkToBuild")
            work_to_make.text = str(workbench['workToBuild'])
            
            flammability = ET.SubElement(stat_bases, "Flammability")
            flammability.text = "1.0"
            
            work_table_work_speed = ET.SubElement(stat_bases, "WorkTableWorkSpeedFactor")
            work_table_work_speed.text = str(workbench['workSpeedFactor'])
            
            work_table_efficiency = ET.SubElement(stat_bases, "WorkTableEfficiencyFactor")
            work_table_efficiency.text = str(workbench['efficiencyFactor'])
            
            # Thing categories
            thing_categories = ET.SubElement(thing_def, "thingCategories")
            thing_category = ET.SubElement(thing_categories, "li")
            thing_category.text = "BuildingsProduction"
            
            # Building properties
            building = ET.SubElement(thing_def, "building")
            is_inert = ET.SubElement(building, "isInert")
            is_inert.text = "true"
            
            is_edifice = ET.SubElement(building, "isEdifice")
            is_edifice.text = "true"
            
            # Surface type
            surface_type = ET.SubElement(building, "surfaceType")
            surface_type.text = "Item"
            
            # Can place blueprints over
            can_place_over = ET.SubElement(building, "canPlaceOverImpassablePlant")
            can_place_over.text = "false"
            
            # AI destory holdable
            ai_destory = ET.SubElement(building, "ai_chillDestination")
            ai_destory.text = "false"
            
            # Designator dropdown group key
            designation_category = ET.SubElement(thing_def, "designationCategory")
            designation_category.text = "Production"
            
            # Inspectorstring extra
            has_interact_cell = ET.SubElement(thing_def, "hasInteractionCell")
            has_interact_cell.text = "true"
            
            interaction_cell_offset = ET.SubElement(thing_def, "interactionCellOffset")
            interaction_cell_offset.text = "(0,0,-1)"
            
            # Recipe users
            recipes = ET.SubElement(thing_def, "recipes")
            # Add some default recipes based on workbench type
            recipe = ET.SubElement(recipes, "li")
            recipe.text = "Make_Apparel_BasicShirt"
            
            # Skill requirements
            if workbench['skillRequired'] != "None":
                skill_requirements = ET.SubElement(thing_def, "skillRequirements")
                skill = ET.SubElement(skill_requirements, "li")
                skill_def = ET.SubElement(skill, "skill")
                skill_def.text = workbench['skillRequired']
                min_level = ET.SubElement(skill, "minLevel")
                min_level.text = str(workbench['skillLevel'])
            
            # Power consumption if needed
            if int(workbench['powerConsumption']) > 0:
                comp_power = ET.SubElement(thing_def, "comps")
                power_comp = ET.SubElement(comp_power, "li", Class="CompProperties_Power")
                comp_class = ET.SubElement(power_comp, "compClass")
                comp_class.text = "CompPowerTrader"
                base_power = ET.SubElement(power_comp, "basePowerConsumption")
                base_power.text = str(workbench['powerConsumption'])
                short_circuit = ET.SubElement(power_comp, "shortCircuitInRain")
                short_circuit.text = "true"
            
            # Research prerequisites
            research_prerequisites = ET.SubElement(thing_def, "researchPrerequisites")
            research_prereq = ET.SubElement(research_prerequisites, "li")
            research_prereq.text = "BasicFabrication"
            
            # Construction skill to build
            construction_skill = ET.SubElement(thing_def, "constructionSkillPrerequisite")
            construction_skill.text = "4"
            
            # Trading tags
            trading_tags = ET.SubElement(thing_def, "tradeTags")
            trade_tag = ET.SubElement(trading_tags, "li")
            trade_tag.text = "Building"
        
        # Write to file
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        
        workbenches_path = os.path.join(defs_folder, "Workbenches.xml")
        with open(workbenches_path, 'w', encoding='utf-8') as f:
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
            
            # Create patches for drugs
            for drug_text in research['unlockedDrugs']:
                if ' - ' in drug_text:
                    drug_defname = drug_text.split(' - ')[0]
                    patches.append(self._create_research_patch(drug_defname, research_defname))
            
            # Create patches for workbenches
            for workbench_text in research['unlockedWorkbenches']:
                if ' - ' in workbench_text:
                    workbench_defname = workbench_text.split(' - ')[0]
                    patches.append(self._create_research_patch(workbench_defname, research_defname))
        
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
