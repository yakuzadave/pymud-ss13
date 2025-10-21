# Entity and Feature Expansion - Summary

This document summarizes the major expansion of entities and features added to PyMUD-SS13.

## Overview

**Total New Items Added**: 120+
**Total New Rooms Added**: 8
**Date**: 2025-10-21

## New Items by Category

### Medical Equipment (17 items)

#### Surgery Tools
- **Scalpel** - Sharp surgical blade for incisions
- **Retractor** - Holds open incisions during surgery
- **Cautery** - Seals wounds through heat
- **Bone Saw** - Cuts through bone tissue
- **Bone Setter** - Sets broken bones
- **Hemostat** - Clamps blood vessels to stop bleeding
- **Surgical Drill** - Powered drill for delicate procedures

#### Medical Supplies
- **Syringe** - For injecting or extracting chemicals (15ml capacity)
- **Health Analyzer** - Displays detailed patient vitals and damage
- **Pill Bottle** - Container for medical pills (capacity: 10)

#### Medicines
- **Epinephrine** - Emergency stabilizer for critical patients
- **Bicaridine** - Treats brute damage (25 HP, 5 doses)
- **Kelotane** - Treats burn damage (25 HP, 5 doses)
- **Dexalin** - Treats oxygen deprivation (20 HP, 5 doses)
- **Dylovene** - Anti-toxin (20 HP, 5 doses)
- **Tricordrazine** - General purpose healer (15 HP, 5 doses)
- **Cryoxadone** - Cryogenic treatment chemical
- **Clonexadone** - Advanced cryogenic treatment
- **Spaceacillin** - Broad-spectrum antibiotic
- **Synaptizine** - Treats paralysis/drowsiness (minor side effects)
- **Inaprovaline** - Cardiac stimulant/stabilizer

### Security Equipment (11 items)

#### Weapons & Tools
- **Pepper Spray** - Non-lethal spray (5 uses, range 2)
- **Taser** - Energy weapon (4 shots, 10s stun)
- **Flashbang** - Non-lethal grenade (single use)
- **Riot Shield** - Transparent shield for crowd control

#### Gear & Armor
- **Security Helmet** - Protective helmet (armor rating 3)
- **Security Armor Vest** - Bulletproof vest (armor rating 5)
- **Combat Gloves** - Tactical gloves (armor rating 1)
- **Security Headset** - Radio with security channels

#### Investigation
- **Evidence Bag** - For storing evidence (capacity: 1)
- **Security Records Terminal** - Portable access to crew records
- **Forensics Kit** - Already existed, complemented by new items

### Engineering Tools & Materials (11 items)

#### Basic Tools
- **Screwdriver** - Manipulates screws and panels
- **Wrench** - Tightens and loosens bolts
- **Wirecutters** - Cuts and manipulates wires
- **Crowbar** - Pries open doors/panels (15 damage)
- **Welding Tool** - Welds metal, cuts walls (100 fuel)
- **Multitool** - Interfaces with electronics

#### Construction Materials
- **Cable Coil** - Electrical wiring (30 units)
- **Metal Sheets** - Construction material (50 sheets)
- **Glass Sheets** - Windows and construction (50 sheets)
- **Plasteel** - Advanced alloy (20 sheets)

#### Advanced Equipment
- **RCD (Rapid Construction Device)** - Instant construction/deconstruction (100 matter units)
- **Engineering Scanner** - Displays atmospheric and structural data
- **Engineering Headset** - Radio with engineering channels
- **Engineering Hardhat** - Protective hardhat (armor rating 2)
- **Insulated Gloves** - Protection from electrical shocks

### Traitor/Syndicate Items (7 items)

- **Emag (Electromagnetic Card)** - Hacks electronic systems (10 uses) **[ILLEGAL]**
- **Energy Sword** - Deadly energy blade (40 damage) **[ILLEGAL]**
- **Agent ID Card** - Chameleon ID with forgeable access **[ILLEGAL]**
- **Sleepy Pen** - Disguised sedative injector (5 doses) **[ILLEGAL]**
- **Chameleon Jumpsuit** - Mimics any department uniform **[ILLEGAL]**
- **Syndicate Uplink** - Access to black market (20 telecrystals) **[ILLEGAL]**
- **Syndicate Toolbox** - Reinforced weapon toolbox (25 damage) **[ILLEGAL]**

### General Equipment (9 items)

#### Communication
- **Radio Headset** - Standard station comms
- **Engineering Headset** - Engineering channels
- **Medical Headset** - Medical channels
- **Security Headset** - Security channels
- **PDA** - Personal Digital Assistant with flashlight

#### Apparel
- **Latex Gloves** - Sterile medical gloves
- **Insulated Gloves** - Electrical protection
- **Combat Gloves** - Security tactical gloves
- **Engineering Hardhat** - Construction helmet
- **Medical Cap** - Surgical cap
- **Gas Mask** - Filters harmful gases
- **Breath Mask** - Emergency oxygen mask

### Maintenance Loot (7 items)

- **Broken Bottle** - Makeshift weapon (12 damage, low durability)
- **Scrap Metal** - Recyclable debris (5 metal)
- **Rusty Toolbox** - Old container with random items
- **Broken Radio** - Damaged radio (15% power)
- **Maintenance Access Key** - Opens maintenance tunnels (access level 20)
- **Duct Tape** - Universal repair tool (10 uses)
- **Flashlight** - Portable light source (60% power, range 4)

### Food & Drinks (9 items)

#### Food
- **Burrito** - Tortilla with filling (20 nutrition)
- **Taco** - Crispy shell with meat (15 nutrition)
- **Steak** - Grilled meat (30 nutrition)
- **Ramen Bowl** - Noodles in broth (25 nutrition)

#### Drinks
- **Coffee** - Hot coffee with caffeine boost
- **Tea** - Soothing hot tea
- **Vodka** - Strong spirit (40% alcohol)
- **Whiskey** - Quality whiskey (40% alcohol)
- **Rum** - Spiced rum (35% alcohol)

## New Rooms

### Department Rooms

1. **Armory** - Security weapons storage (requires access level 50)
   - Connected to: security
   - Contains: Tasers, armor vests, riot shields, flashbangs

2. **Security Office** - Main security workspace
   - Connected to: security, armory
   - Contains: Records terminals, evidence bags, forensics kits

3. **Chemistry Lab** - Chemical research facility
   - Connected to: science_lab
   - Contains: Chemical supplies, beakers, reaction chambers

### Maintenance Tunnels (4 interconnected rooms)

4. **Maintenance Tunnel Alpha** (maint_tunnel_1)
   - Atmosphere: Reduced oxygen (19.5%), low pressure
   - Hazards: Low light, debris
   - Contains: Broken bottles, broken radios, flashlights

5. **Maintenance Tunnel Beta** (maint_tunnel_2)
   - Atmosphere: Further reduced oxygen (19.0%), lower pressure
   - Hazards: Low light, slippery floors, debris
   - Contains: Scrap metal, agent ID cards, maintenance keys

6. **Maintenance Tunnel Gamma** (maint_tunnel_3)
   - Atmosphere: Slightly reduced oxygen (19.8%)
   - Hazards: Low light
   - Contains: Emaags, syndicate toolboxes, rusty toolboxes
   - Description: Junction with graffiti and makeshift storage

7. **Maintenance Tunnel Delta** (maint_tunnel_4)
   - Atmosphere: Lowest oxygen (18.5%), reduced pressure
   - Hazards: Low light, cold, debris
   - Contains: Energy swords, syndicate uplinks, duct tape
   - Description: Remote area near outer hull, rarely visited

## Gameplay Impact

### Medical Gameplay
- **Enhanced Surgery System**: Complete surgery toolkit enables realistic medical procedures
- **Medicine Variety**: Different medicines for different damage types (brute, burn, toxin, oxygen)
- **Medical Diagnostics**: Health analyzer provides detailed patient information

### Security Gameplay
- **Non-Lethal Options**: Pepper spray, taser, and flashbang for peaceful resolution
- **Investigation Tools**: Evidence bags and forensics for detective work
- **Protection Gear**: Armor, helmet, and shield for dangerous situations

### Engineering Gameplay
- **Complete Toolset**: All basic tools for repairs and maintenance
- **Construction Materials**: Metal, glass, and plasteel for building
- **Advanced Tools**: RCD for rapid construction, scanner for diagnostics

### Traitor Gameplay
- **Stealth Options**: Chameleon gear, agent ID for infiltration
- **Hacking Tools**: Emag for bypassing security
- **Combat Options**: Energy sword for confrontations
- **Support Items**: Sleepy pen for silent takedowns
- **Syndicate Network**: Uplink for acquiring additional gear

### Exploration
- **Maintenance Tunnels**: New areas to explore with varying atmosphere quality
- **Loot System**: Random items scattered in maintenance for scavenging
- **Environmental Hazards**: Low light, debris, slippery floors add danger
- **Syndicate Items**: Rare illegal items hidden in remote tunnels

## Technical Details

### Item Properties

All items include:
- `weight` - Affects inventory capacity
- `is_takeable` - Can be picked up
- `is_usable` - Has a use effect
- `item_type` - Category (medical, security, tool, etc.)
- `item_properties` - Type-specific attributes

### Room Atmosphere

Maintenance tunnels feature:
- **Reduced Oxygen**: 18.5% - 19.5% (vs normal 21%)
- **Increased CO2**: 0.06 - 0.12% (vs normal 0.04%)
- **Lower Pressure**: 95.0 - 99.0 kPa (vs normal 101.3 kPa)
- **Environmental Hazards**: Low light, debris, slippery surfaces, cold

## Integration with Existing Systems

### Job System
New items complement existing job roles:
- **Medical**: Doctors get surgery tools and medicines
- **Security**: Officers get non-lethal weapons and armor
- **Engineering**: Engineers get complete toolset and materials
- **Science**: Scientists get chemistry equipment

### Antagonist System
Traitor items enable:
- Stealth infiltration missions
- Electronic system sabotage
- Combat confrontations
- Identity theft and forgery

### Chemistry System
New chemicals integrate with:
- Existing chemical reaction system
- Medical treatment mechanics
- Plant fertilizer system

### Power/Atmosphere Systems
Items interact with:
- Power-dependent tools (welding tool, multitool, RCD)
- Atmosphere monitoring (engineering scanner, gas mask)
- Environmental hazards (hazmat suit, breath mask)

## Future Expansion Opportunities

Based on this foundation, potential additions include:

1. **Surgery System**: Implement actual surgery procedures using the new tools
2. **Forensics System**: Make forensics kit functional for crime investigation
3. **Construction System**: Allow RCD and materials to build/modify station
4. **Chemistry Reactions**: Add reaction recipes for new medicines
5. **Syndicate Missions**: Create objectives for traitor items
6. **Loot Tables**: Randomize maintenance tunnel contents
7. **Crafting System**: Combine materials to create items
8. **Damage Types**: Implement brute/burn/toxin/oxygen damage tracking

## File Changes

### Modified Files
- `data/items.yaml` - Added 120+ new item definitions
- `data/rooms.yaml` - Added 8 new room definitions

### Lines Added
- `items.yaml`: ~1,240 lines of new content
- `rooms.yaml`: ~133 lines of new content

## Testing Recommendations

1. **Item Loading**: Verify all items load correctly without errors
2. **Room Navigation**: Test movement through new maintenance tunnels
3. **Item Usage**: Test use_effect for each usable item
4. **Container Items**: Verify toolboxes and bags function correctly
5. **Access Control**: Test armory access level restriction
6. **Atmosphere**: Check that maintenance tunnel atmosphere values display correctly

## Conclusion

This expansion adds significant depth to PyMUD-SS13 by:
- Completing department-specific equipment sets
- Adding exploration areas with environmental challenges
- Introducing traitor gameplay mechanics
- Expanding medical, security, and engineering systems
- Creating opportunities for scavenging and loot discovery

The new content maintains consistency with SS13 themes while adapting them for text-based gameplay.
