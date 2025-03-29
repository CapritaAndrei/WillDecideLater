import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re
import random
import requests
from time import sleep

# Before running, do these once:
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# Actualizează aceste constante la începutul fișierului cu rutele oferite
BASE_URL = "http://172.18.4.158:8000"
get_url = f"{BASE_URL}/get-word"  # Notă: este "get-word" nu "get_word"
post_url = f"{BASE_URL}/submit-word"  # Notă: este "submit-word" nu "submit_word"
status_url = f"{BASE_URL}/status"
NUM_ROUNDS = 20  # Ajustează acest număr la numărul real de runde din competiție
PLAYER_ID = "Llwr60Mns2"  # Player ID-ul tău specific

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Player words dictionary with "text" instead of "word"
PLAYER_WORDS = {
    1: {"text": "Feather", "cost": 1},
    2: {"text": "Coal", "cost": 1},
    3: {"text": "Pebble", "cost": 1},
    4: {"text": "Leaf", "cost": 2},
    5: {"text": "Paper", "cost": 2},
    6: {"text": "Rock", "cost": 2},
    7: {"text": "Water", "cost": 3},
    8: {"text": "Twig", "cost": 3},
    9: {"text": "Sword", "cost": 4},
    10: {"text": "Shield", "cost": 4},
    11: {"text": "Gun", "cost": 5},
    12: {"text": "Flame", "cost": 5},
    13: {"text": "Rope", "cost": 5},
    14: {"text": "Disease", "cost": 6},
    15: {"text": "Cure", "cost": 6},
    16: {"text": "Bacteria", "cost": 6},
    17: {"text": "Shadow", "cost": 7},
    18: {"text": "Light", "cost": 7},
    19: {"text": "Virus", "cost": 7},
    20: {"text": "Sound", "cost": 8},
    21: {"text": "Time", "cost": 8},
    22: {"text": "Fate", "cost": 8},
    23: {"text": "Earthquake", "cost": 9},
    24: {"text": "Storm", "cost": 9},
    25: {"text": "Vaccine", "cost": 9},
    26: {"text": "Logic", "cost": 10},
    27: {"text": "Gravity", "cost": 10},
    28: {"text": "Robots", "cost": 10},
    29: {"text": "Stone", "cost": 11},
    30: {"text": "Echo", "cost": 11},
    31: {"text": "Thunder", "cost": 12},
    32: {"text": "Karma", "cost": 12},
    33: {"text": "Wind", "cost": 13},
    34: {"text": "Ice", "cost": 13},
    35: {"text": "Sandstorm", "cost": 13},
    36: {"text": "Laser", "cost": 14},
    37: {"text": "Magma", "cost": 14},
    38: {"text": "Peace", "cost": 14},
    39: {"text": "Explosion", "cost": 15},
    40: {"text": "War", "cost": 15},
    41: {"text": "Enlightenment", "cost": 15},
    42: {"text": "Nuclear Bomb", "cost": 16},
    43: {"text": "Volcano", "cost": 16},
    44: {"text": "Whale", "cost": 17},
    45: {"text": "Earth", "cost": 17},
    46: {"text": "Moon", "cost": 17},
    47: {"text": "Star", "cost": 18},
    48: {"text": "Tsunami", "cost": 18},
    49: {"text": "Supernova", "cost": 19},
    50: {"text": "Antimatter", "cost": 19},
    51: {"text": "Plague", "cost": 20},
    52: {"text": "Rebirth", "cost": 20},
    53: {"text": "Tectonic Shift", "cost": 21},
    54: {"text": "Gamma-Ray Burst", "cost": 22},
    55: {"text": "Human Spirit", "cost": 23},
    56: {"text": "Apocalyptic Meteor", "cost": 24},
    57: {"text": "Earth's Core", "cost": 25},
    58: {"text": "Neutron Star", "cost": 26},
    59: {"text": "Supermassive Black Hole", "cost": 35},
    60: {"text": "Entropy", "cost": 45},
}

# Cost tiers for words
COST_TIERS = {
    "very_cheap": [1, 2, 3],  # $1-3
    "cheap": [4, 5, 6],       # $4-6
    "moderate": [7, 8, 9, 10, 11, 12, 13, 14, 15],  # $7-15 (expanded middle tier)
    "expensive": [16, 17, 18, 19, 20],  # $16-20
    "very_expensive": [21, 22, 23, 24, 25, 26, 35, 45]  # $21+
}

# Dictionary of category counters (what beats each category)
CATEGORY_COUNTERS = {
    # Natural Elements & Phenomena
    "atmospheric_phenomenon": ["Gravity", "Storm", "Laser", "Earth"],
    "body_of_water": ["Ice", "Earth", "Earthquake", "Drought"],
    "celestial_body": ["Supermassive Black Hole", "Supernova", "Neutron Star", "Gamma-Ray Burst"],
    "coldness": ["Flame", "Magma", "Heat"],
    "fire": ["Water", "Ice", "Earth", "Vacuum"],
    "geological_phenomenon": ["Earthquake", "Water", "Tectonic Shift", "Time"],
    "light": ["Shadow", "Supermassive Black Hole", "Darkness"],
    "liquid": ["Ice", "Heat", "Container", "Drought"],
    "mountain": ["Earthquake", "Tectonic Shift", "Volcano", "Water"],
    "natural_object": ["Earthquake", "Water", "Time", "Erosion"],
    "rock": ["Water", "Earthquake", "Paper", "Time"],
    "star": ["Supernova", "Supermassive Black Hole", "Neutron Star", "Time"],
    "stone": ["Water", "Time", "Earthquake", "Erosion"],
    "storm": ["Mountain", "Gravity", "Earth", "Time"],
    "weather": ["Gravity", "Climate Control", "Indoor Location"],
    "windstorm": ["Mountain", "Gravity", "Building"],
    "wave": ["Rock", "Shore", "Barrier", "Calm"],
    
    # Life Forms & Biology
    "animal_material": ["Fire", "Water", "Decay", "Time"],
    "cetacean": ["Gun", "Harpoon", "Pollution", "Shark"],
    "microorganism": ["Cure", "Vaccine", "Antibiotic", "Heat"],
    "infectious_agent": ["Vaccine", "Cure", "Isolation", "Heat"],
    "epidemic_disease": ["Vaccine", "Cure", "Quarantine", "Time"],
    "illness": ["Cure", "Vaccine", "Medicine", "Time"],
    
    # Abstract Concepts
    "blessedness": ["Corruption", "Darkness", "Evil", "Reality"],
    "destiny": ["Free Will", "Human Spirit", "Time", "Chaos"],
    "ethical_motive": ["Corruption", "Logic", "Selfishness"],
    "harmony": ["Chaos", "Discord", "War", "Noise"],
    "philosophy": ["Logic", "Science", "Empiricism", "Reality"],
    "principle": ["Corruption", "Chaos", "Reality", "Necessity"],
    "time_period": ["Entropy", "Infinity", "Timelessness", "Relativity"],
    "tranquillity": ["War", "Noise", "Chaos", "Explosion"],
    
    # Physical Actions & Forces
    "assault": ["Shield", "Armor", "Peace", "Law"],
    "attack": ["Shield", "Defense", "Evasion", "Counter-attack"],
    "blow": ["Shield", "Armor", "Distance", "Evasion"],
    "burn": ["Water", "Ice", "Fire Extinguisher", "Sand"],
    "combustion": ["Water", "Vacuum", "Explosion Suppression"],
    "conflict": ["Peace", "Diplomacy", "Resolution", "Enlightenment"],
    "discharge": ["Insulation", "Ground", "Containment"],
    "disturbance": ["Peace", "Order", "Calm", "Control"],
    "explosion": ["Containment", "Water", "Distance", "Time"],
    
    # Materials & Objects
    "armor": ["Laser", "Armor Piercing", "Heat", "Time"],
    "armament": ["Peace", "Shield", "Disarmament", "EMP"],
    "building_material": ["Water", "Fire", "Time", "Earthquake"],
    "device": ["Water", "EMP", "Disruption", "Time"],
    "element": ["Neutralizing Element", "Chemical Reaction", "Containment"],
    "fossil_fuel": ["Water", "Sand", "Containment", "Alternative Energy"],
    "material": ["Appropriate Solvent", "Heat", "Cold", "Time"],
    "matter": ["Antimatter", "Energy", "Supermassive Black Hole", "Entropy"],
    "weapon": ["Shield", "Peace", "Disarmament", "Distance"],
    
    # Additional categories
    "entity": ["Logic", "Time", "Entropy"],
    "object": ["Destruction", "Earthquake", "Time"],
    "abstemious": ["Temptation", "Pleasure", "Abundance"],
    "act": ["Inaction", "Opposition", "Prevention"],
    "actinic_radiation": ["Shield", "Lead", "Distance"],
    "actor": ["Critic", "Reality", "Obscurity"],
    "adjust": ["Fixation", "Rigidity", "Permanence"],
    "afflict": ["Peace", "Cure", "Protection"],
    "amphetamine": ["Sedative", "Sleep", "Calm"],
    "analogue": ["Digital", "Exact", "Precision"],
    "animal": ["Gun", "Predator", "Disease"],
    "announce": ["Silence", "Secrecy", "Censorship"],
    "annoy": ["Patience", "Tolerance", "Calm"],
    "annoyance": ["Peace", "Tranquility", "Pleasure"],
    "article": ["Censorship", "Destruction", "Suppression"],
    "attribute": ["Removal", "Nullification", "Absence"],
    "auditory_communication": ["Silence", "Deafness", "Noise"],
    "binary_compound": ["Separation", "Chemical Reaction", "Heat"],
    "birth": ["Death", "Prevention", "Sterilization"],
    "blast": ["Shield", "Distance", "Containment"],
    "calamity": ["Preparation", "Prevention", "Recovery"],
    "campaign": ["Opposition", "Failure", "Apathy"],
    "causal_agent": ["Effect", "Prevention", "Resistance"],
    "change_of_integrity": ["Preservation", "Protection", "Reinforcement"],
    "character": ["Transformation", "Development", "Exposure"],
    "chastise": ["Forgiveness", "Acceptance", "Tolerance"],
    "clean": ["Dirt", "Contamination", "Use"],
    "connect": ["Separation", "Isolation", "Break"],
    "connection": ["Isolation", "Barrier", "Distance"],
    "contend": ["Agreement", "Peace", "Surrender"],
    "controlled_substance": ["Law", "Rehabilitation", "Control"],
    "cover": ["Exposure", "Transparency", "Revelation"],
    "crack": ["Repair", "Reinforcement", "Prevention"],
    "crystal": ["Pressure", "Heat", "Dissolution"],
    "darken": ["Light", "Illumination", "Exposure"],
    "descend": ["Ascend", "Levitation", "Flight"],
    "determine": ["Chance", "Chaos", "Uncertainty"],
    "dimension": ["Reduction", "Contraction", "Limitation"],
    "displease": ["Pleasure", "Satisfaction", "Delight"],
    "dominate": ["Resistance", "Freedom", "Equality"],
    "education": ["Ignorance", "Censorship", "Misinformation"],
    "element": ["Compound", "Reaction", "Combination"],
    "expert": ["Novice", "Ignorance", "Error"],
    "express": ["Suppress", "Censor", "Hide"],
    "facility": ["Difficulty", "Obstacle", "Complexity"],
    "feeling": ["Numbness", "Logic", "Indifference"],
    "fill": ["Empty", "Vacuum", "Hole"],
    "flunitrazepan": ["Stimulant", "Awareness", "Consciousness"],
    "follower": ["Leader", "Independence", "Original"],
    "food": ["Starvation", "Poison", "Inedible"],
    "foreboding": ["Hope", "Optimism", "Certainty"],
    "fragment": ["Whole", "Unity", "Repair"],
    "freeze": ["Heat", "Flame", "Magma"],
    "friend": ["Enemy", "Betrayal", "Solitude"],
    "guidance": ["Confusion", "Misdirection", "Abandonment"],
    "happening": ["Prevention", "Avoidance", "Interruption"],
    "harden": ["Soften", "Melt", "Dissolve"],
    "have": ["Lack", "Loss", "Poverty"],
    "healthy": ["Disease", "Injury", "Poison"],
    "heat_engine": ["Cold", "Freezing", "Shutdown"],
    "heavy": ["Light", "Levitation", "Antigravity"],
    "help": ["Harm", "Hindrance", "Abandonment"],
    "hide": ["Expose", "Reveal", "Discover"],
    "hostility": ["Peace", "Friendship", "Harmony"],
    "idle": ["Work", "Activity", "Productivity"],
    "ignite": ["Extinguish", "Smother", "Wet"],
    "illusion": ["Reality", "Truth", "Clarity"],
    "insight": ["Blindness", "Ignorance", "Delusion"],
    "intertwine": ["Separate", "Unravel", "Divide"],
    "join": ["Separate", "Divide", "Isolate"],
    "kill": ["Life", "Protection", "Resurrection"],
    "land": ["Water", "Air", "Space"],
    "lighten": ["Darken", "Shadow", "Blackout"],
    "lurch": ["Stability", "Balance", "Smoothness"],
    "make": ["Destroy", "Undo", "Prevent"],
    "malevolent_program": ["Antivirus", "Firewall", "Security"],
    "mark": ["Erase", "Clean", "Remove"],
    "move": ["Stop", "Immobilize", "Paralyze"],
    "noise": ["Silence", "Peace", "Quiet"],
    "nymph": ["Age", "Time", "Reality"],
    "ordain": ["Cancel", "Prevent", "Nullify"],
    "prevent": ["Enable", "Allow", "Facilitate"],
    "product": ["Destruction", "Consumption", "Recycling"],
    "protect": ["Attack", "Expose", "Penetrate"],
    "quantify": ["Unquantified", "Immeasurable", "Quality"],
    "raise": ["Lower", "Decrease", "Sink"],
    "release": ["Capture", "Contain", "Imprison"],
    "remove": ["Attach", "Preserve", "Maintain"],
    "reply": ["Silence", "Ignore", "End"],
    "resemble": ["Differ", "Contrast", "Unique"],
    "rotation": ["Stillness", "Stop", "Fixation"],
    "row": ["Stillness", "Peace", "Stop"],
    "satellite": ["Gravity", "Collision", "Descent"],
    "scute": ["Softness", "Vulnerability", "Exposure"],
    "secrete": ["Absorb", "Contain", "Retain"],
    "security": ["Vulnerability", "Danger", "Breach"],
    "sensation": ["Numbness", "Unconsciousness", "Isolation"],
    "shoot": ["Shield", "Dodge", "Protection"],
    "smell": ["Scentless", "Olfactory Fatigue", "Nose Plug"],
    "spy": ["Counter-Intelligence", "Security", "Privacy"],
    "supply": ["Demand", "Shortage", "Consumption"],
    "system": ["Chaos", "Breakdown", "Disruption"],
    "take": ["Give", "Leave", "Return"],
    "tighten": ["Loosen", "Release", "Expand"],
    "transfer": ["Keep", "Retain", "Fix"],
    "travel": ["Stay", "Immobility", "Barrier"],
    "utter": ["Silence", "Muteness", "Censorship"],
    "visual_property": ["Blindness", "Darkness", "Invisibility"],
    "weapon": ["Shield", "Peace", "Disarmament"],
    "wet": ["Dry", "Desiccate", "Absorb"]
}

# Strength multipliers for our words when countering these categories
WORD_STRENGTH = {
    # Elemental counters
    "Water": {
        "fire": 5.0,
        "burn": 4.0, 
        "heat": 3.5,
        "combustion": 4.0,
        "stone": 2.0,
        "rock": 2.0
    },
    "Ice": {
        "fire": 3.0,
        "heat": 4.0,
        "water": 2.0,
        "liquid": 3.0,
        "body_of_water": 2.5
    },
    "Flame": {
        "coldness": 5.0,
        "freeze": 4.0,
        "paper": 4.0,
        "plant_organ": 3.0,
        "microorganism": 3.0
    },
    "Earth": {
        "atmospheric_phenomenon": 3.0,
        "storm": 2.5,
        "windstorm": 3.0,
        "wave": 2.0
    },
    "Wind": {
        "light": 1.5,
        "paper": 3.0,
        "lightweight": 3.5
    },
    "Fire": {
        "coldness": 5.0,
        "microorganism": 4.0,
        "infectious_agent": 3.5,
        "animal_material": 3.0
    },
    
    # Weapons & Tools
    "Sword": {
        "animal_material": 3.0,
        "cetacean": 2.0,
        "armor": 1.5,
        "plant_organ": 3.0
    },
    "Shield": {
        "attack": 4.0,
        "assault": 3.5,
        "blow": 4.0,
        "weapon": 2.5
    },
    "Gun": {
        "cetacean": 4.0,
        "animal": 4.5,
        "armor": 2.0,
        "attack": 3.0
    },
    "Nuclear Bomb": {
        "armor": 5.0,
        "building_material": 5.0,
        "city": 5.0,
        "army": 5.0
    },
    
    # Abstract & Conceptual
    "Logic": {
        "philosophy": 4.0,
        "ethical_motive": 3.0,
        "principle": 3.0,
        "belief": 3.5
    },
    "Time": {
        "material": 3.0,
        "stone": 4.0,
        "mountain": 3.0,
        "illness": 2.0,
        "epidemic_disease": 2.5
    },
    "Fate": {
        "free_will": 3.0,
        "destiny": 4.0,
        "chance": 3.5
    },
    "Enlightenment": {
        "darkness": 4.0,
        "ignorance": 5.0,
        "conflict": 3.0,
        "ethical_motive": 3.0
    },
    "Peace": {
        "conflict": 4.5,
        "war": 4.0,
        "assault": 3.0,
        "attack": 3.0,
        "armament": 2.5
    },
    
    # Cosmic-scale
    "Supermassive Black Hole": {
        "matter": 5.0,
        "light": 5.0,
        "celestial_body": 5.0,
        "star": 5.0
    },
    "Neutron Star": {
        "star": 4.0,
        "celestial_body": 3.5
    },
    "Supernova": {
        "star": 5.0,
        "celestial_body": 4.0
    },
    
    # Power adjustments for specific/specialized
    "Vaccine": {
        "infectious_agent": 5.0,
        "epidemic_disease": 5.0,
        "illness": 4.0
    },
    "Cure": {
        "illness": 5.0,
        "epidemic_disease": 4.0,
        "infectious_agent": 4.0
    },
    "Earthquake": {
        "mountain": 4.0,
        "building_material": 4.5,
        "stone": 4.0,
        "geological_phenomenon": 4.0
    },
    "Storm": {
        "light": 2.5,
        "paper": 3.0,
        "fragile": 3.5
    },
    "Gravity": {
        "atmospheric_phenomenon": 4.0,
        "storm": 3.0,
        "flight": 5.0,
        "windstorm": 3.5
    }
}

# Words that are weak against certain categories (negative adjustment)
WORD_WEAKNESS = {
    "Feather": {
        "wind": -4.0,
        "storm": -4.0,
        "fire": -4.0,
        "large": -4.0
    },
    "Paper": {
        "fire": -5.0,
        "water": -4.0,
        "wind": -3.0
    },
    "Leaf": {
        "fire": -4.0,
        "wind": -3.5,
        "herbivore": -4.0
    },
    "Coal": {
        "fire": -3.0,
    },
    "Twig": {
        "fire": -4.0,
        "strong_force": -4.0,
        "pressure": -3.0
    },
    "Ice": {
        "heat": -4.0,
        "fire": -5.0
    }
}

# Material classification for various objects
MATERIALS = {
    "wood": ["Tree", "Stick", "Twig", "Wood", "Log", "Timber", "Chair", "Table", "Furniture", "Door", "House"],
    "paper": ["Paper", "Book", "Document", "Letter", "Card", "Newspaper", "Page"],
    "metal": ["Metal", "Iron", "Steel", "Aluminum", "Copper", "Silver", "Gold", "Sword", "Shield", "Armor", "Gun", "Tank"],
    "stone": ["Stone", "Rock", "Pebble", "Mountain", "Cliff", "Boulder", "Gravel"],
    "water": ["Water", "Ocean", "Sea", "Lake", "River", "Stream", "Flood", "Rain"],
    "flesh": ["Flesh", "Body", "Human", "Animal", "Bird", "Whale", "Lion", "Tiger", "Bear", "Shark", "Snake"],
    "plant": ["Plant", "Tree", "Flower", "Grass", "Bush", "Leaf", "Forest", "Jungle"],
    "electronic": ["Computer", "Robot", "Machine", "Device", "Phone", "Television", "Radio", "Circuit"],
    "cloth": ["Cloth", "Fabric", "Clothing", "Shirt", "Pants", "Dress", "Jacket", "Textile", "Cotton", "Silk"],
    "plastic": ["Plastic", "Polymer", "Synthetic"]
}

# Hard counters for materials
MATERIAL_COUNTERS = {
    "wood": {
        "Flame": 200,
        "Fire": 200,
        "Magma": 150,
        "Lava": 150,
        "Sword": 100,
        "Axe": 150
    },
    "paper": {
        "Flame": 250,
        "Fire": 250,
        "Water": 150,
        "Wind": 130,
        "Scissor": 200
    },
    "metal": {
        "Magma": 180,
        "Acid": 150,
        "Rust": 130,
        "Water": 80,
        "Electricity": 100
    },
    "stone": {
        "Earthquake": 150,
        "Water": 100,
        "Ice": 120,
        "Erosion": 130
    },
    "water": {
        "Ice": 140,
        "Cold": 130,
        "Drought": 200,
        "Sun": 120,
        "Heat": 100
    },
    "flesh": {
        "Sword": 180,
        "Gun": 200,
        "Disease": 150,
        "Virus": 140,
        "Bacteria": 130,
        "Flame": 120
    },
    "plant": {
        "Flame": 190,
        "Fire": 190,
        "Drought": 150,
        "Disease": 120,
        "Insects": 100
    },
    "electronic": {
        "Water": 200,
        "Electricity": 150,
        "Magnet": 130,
        "Virus": 150,
        "Hacker": 140
    },
    "cloth": {
        "Flame": 180,
        "Fire": 180,
        "Scissor": 150,
        "Water": 100
    },
    "plastic": {
        "Flame": 150,
        "Heat": 130,
        "Sun": 80
    }
}

# Size classification
SIZE_CATEGORIES = {
    "tiny": ["Ant", "Insect", "Dust", "Atom", "Molecule", "Cell", "Microbe", "Bacteria", "Virus"],
    "small": ["Feather", "Leaf", "Twig", "Pebble", "Mouse", "Rat", "Squirrel", "Coin", "Key", "Phone", "Cat", "Small Dog"],
    "medium": ["Human", "Wolf", "Dog", "Furniture", "Bicycle", "Machine", "Computer", "Rock", "Tree", "Car", "Tiger", "Lion", "Bear"],
    "large": ["Elephant", "Whale", "House", "Building", "Ship", "Truck", "Plane", "Tank", "Mountain", "Hill"],
    "huge": ["Skyscraper", "Mountain", "Volcano", "Island", "Iceberg", "Aircraft Carrier"],
    "enormous": ["City", "Country", "Continent", "Moon", "Planet", "Star", "Meteor", "Ocean", "Sea"],
    "cosmic": ["Planet", "Star", "Sun", "Moon", "Galaxy", "Universe", "Supernova", "Black Hole"]
}

# Size based hard counters
SIZE_ADJUSTMENTS = {
    "tiny_vs_enormous": -200,  # Tiny things are ineffective against enormous things
    "tiny_vs_large": -150,     # Tiny things are weak against large things
    "small_vs_enormous": -150, # Small things are very weak against enormous things
    "small_vs_large": -100,    # Small things are weak against large things
    "medium_vs_enormous": -50, # Medium things are somewhat weak against enormous
    "large_vs_tiny": 150,      # Large things easily defeat tiny things
    "enormous_vs_tiny": 200,   # Enormous things easily defeat tiny things
    "enormous_vs_small": 150,  # Enormous things easily defeat small things
}

# Global dictionary to track word usage
WORD_USAGE_COUNT = {}

# Initialize categories for each word
def categorize_player_words():
    """Categorize all player words for later matching"""
    # Main categories with associated words
    categories = {
        # Elemental categories
        "water": ["Water", "Ice", "Tsunami"],
        "earth": ["Earth", "Rock", "Stone", "Earthquake", "Tectonic Shift", "Volcano", "Pebble"],
        "fire": ["Flame", "Magma", "Coal"],
        "air": ["Wind", "Storm", "Sandstorm", "Echo", "Sound", "Thunder"],
        
        # Material properties
        "light": ["Light", "Star", "Sun", "Supernova", "Laser"],
        "dark": ["Shadow", "Supermassive Black Hole"],
        "cold": ["Ice"],
        "heat": ["Flame", "Magma", "Volcano", "Star", "Supernova"],
        
        # Size/scale categories
        "small": ["Feather", "Coal", "Pebble", "Leaf", "Paper", "Twig"],
        "medium": ["Rock", "Water", "Shield", "Sword", "Gun"],
        "large": ["Whale", "Earth", "Moon", "Star"],
        "cosmic": ["Star", "Moon", "Supernova", "Neutron Star", "Supermassive Black Hole", "Earth's Core", "Gamma-Ray Burst", "Entropy"],
        
        # Abstract concepts
        "abstract": ["Time", "Fate", "Logic", "Karma", "Enlightenment", "Peace", "War", "Rebirth", "Entropy"],
        "time": ["Time", "Entropy", "Fate"],
        "mind": ["Logic", "Enlightenment", "Human Spirit", "Fate", "Karma"],
        "peace": ["Peace", "Cure", "Enlightenment"],
        "war": ["War", "Nuclear Bomb", "Explosion"],
        
        # Scientific concepts
        "physics": ["Gravity", "Antimatter", "Gamma-Ray Burst", "Light", "Sound", "Echo", "Time"],
        "biology": ["Disease", "Bacteria", "Virus", "Plague", "Vaccine", "Cure"],
        "disease": ["Disease", "Bacteria", "Virus", "Plague"],
        "medicine": ["Vaccine", "Cure"],
        
        # Weapons & tools
        "weapon": ["Sword", "Gun", "Nuclear Bomb", "Laser", "Explosion"],
        "protection": ["Shield"],
        "destructive": ["Explosion", "Nuclear Bomb", "Volcano", "Earthquake", "Tsunami", "Tectonic Shift", "Apocalyptic Meteor", "Gamma-Ray Burst"],
        
        # Entities
        "animal": ["Whale"],
        "machine": ["Robots", "Laser"],
        
        # Forces
        "force": ["Gravity", "Wind", "Earthquake", "Explosion", "Tsunami"],
        "natural_force": ["Wind", "Earthquake", "Storm", "Tsunami", "Volcano"],
        "supernatural_force": ["Fate", "Karma", "Human Spirit", "Enlightenment"]
    }
    
    # Size categories
    size_map = {
        "tiny": ["Feather", "Pebble", "Leaf"],
        "small": ["Coal", "Twig", "Paper", "Rock"],
        "medium": ["Water", "Sword", "Shield", "Gun", "Flame", "Rope", "Disease", "Bacteria", "Virus", "Shadow", "Light"],
        "large": ["Earthquake", "Storm", "Thunder", "Wind", "Ice", "Sandstorm", "Robots", "Explosion", "Volcano", "Whale", "Earth", "Moon"],
        "enormous": ["Star", "Tsunami", "Supernova", "Neutron Star", "Supermassive Black Hole"],
        "cosmic": ["Gamma-Ray Burst", "Apocalyptic Meteor", "Earth's Core", "Entropy"]
    }
    
    # Assign categories to each word
    for word_id, info in PLAYER_WORDS.items():
        word = info["text"]
        # Initialize categories
        info["categories"] = []
        info["size"] = None
        info["materials"] = []
        info["wordnet_categories"] = []
        
        # Assign categories from our mapping
        for category, words in categories.items():
            if word in words:
                info["categories"].append(category)
        
        # Assign size category
        for size, words in size_map.items():
            if word in words:
                info["size"] = size
                break
        
        # If no size assigned, determine by cost
        if not info["size"]:
            if info["cost"] <= 3:
                info["size"] = "small"
            elif info["cost"] <= 10:
                info["size"] = "medium"
            elif info["cost"] <= 18:
                info["size"] = "large"
            else:
                info["size"] = "enormous"
        
        # Assign material categories
        for material, items in MATERIALS.items():
            if word in items or any(item.lower() in word.lower() for item in items):
                info["materials"].append(material)
        
        # Add WordNet derived categories
        add_wordnet_categories(info)
        
        # If still no category, add defaults based on cost
        if not info["categories"]:
            if info["cost"] < 5:
                info["categories"].append("small")
            elif info["cost"] < 15:
                info["categories"].append("medium")
            else:
                info["categories"].append("large")
                
        # Add power level based on cost (adjusted to favor middle words)
        if info["cost"] <= 3:  # very cheap
            info["power"] = 2
        elif info["cost"] <= 6:  # cheap
            info["power"] = 4
        elif info["cost"] <= 15:  # middle (favored)
            info["power"] = 8
        elif info["cost"] <= 20:  # expensive
            info["power"] = 6
        else:  # very expensive
            info["power"] = 5
        
        # Add cost tier
        for tier, costs in COST_TIERS.items():
            if info["cost"] in costs:
                info["cost_tier"] = tier
                break

def add_wordnet_categories(word_info):
    """Add WordNet derived categories to a word"""
    word = word_info["text"].lower()
    synsets = wn.synsets(word)
    
    if not synsets:
        return
    
    # Check the top synsets for categories
    for synset in synsets[:2]:
        # Get hypernyms (broader categories)
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            category = hypernym.name().split('.')[0]
            if category not in word_info["categories"]:
                word_info["categories"].append(category)
            if category not in word_info["wordnet_categories"]:
                word_info["wordnet_categories"].append(category)

def analyze_system_word(sys_word):
    """Analyze a system word and return its categories and properties"""
    # Preprocess the word
    sys_word_lower = sys_word.lower()
    lemmatized = lemmatizer.lemmatize(sys_word_lower)
    
    categories = []
    materials = []
    size = None
    wordnet_categories = []
    
    # Check for size category
    for size_category, words in SIZE_CATEGORIES.items():
        if sys_word in words or any(word.lower() in sys_word_lower for word in words):
            size = size_category
            break
    
    # If no size found, determine by word length
    if not size:
        if len(sys_word) <= 4:
            size = "small"
        elif len(sys_word) <= 7:
            size = "medium"
        else:
            size = "large"
    
    # Check for material type
    for material, items in MATERIALS.items():
        if sys_word in items or any(item.lower() in sys_word_lower for item in items):
            materials.append(material)
    
    # Check WordNet for categories
    synsets = wn.synsets(lemmatized)
    if synsets:
        # Get the most common definitions
        for synset in synsets[:2]:
            # Extract hypernyms (categories)
            for hypernym in synset.hypernyms():
                category = hypernym.name().split('.')[0]
                categories.append(category)
                wordnet_categories.append(category)
            
            # Look for keywords in the definition
            definition = synset.definition().lower()
            if any(word in definition for word in ["animal", "creature", "beast", "bird", "fish"]):
                categories.append("animal")
            if any(word in definition for word in ["weapon", "gun", "sword", "bomb"]):
                categories.append("weapon")
            if any(word in definition for word in ["water", "liquid", "ocean", "sea"]):
                categories.append("water")
            if any(word in definition for word in ["fire", "flame", "burn", "heat"]):
                categories.append("fire")
            if any(word in definition for word in ["earth", "ground", "soil", "rock"]):
                categories.append("earth")
            if any(word in definition for word in ["air", "wind", "atmosphere", "sky"]):
                categories.append("air")
    
    # Check for common categories in the word itself
    if "animal" in sys_word_lower or any(animal in sys_word_lower for animal in ["lion", "tiger", "bear", "wolf", "snake", "shark", "dragon"]):
        categories.append("animal")
    if "water" in sys_word_lower or any(water in sys_word_lower for water in ["ocean", "sea", "lake", "river", "flood"]):
        categories.append("water")
    if "fire" in sys_word_lower or "flame" in sys_word_lower:
        categories.append("fire")
    if "earth" in sys_word_lower or any(earth in sys_word_lower for earth in ["ground", "soil", "rock", "mountain"]):
        categories.append("earth")
    if "air" in sys_word_lower or "wind" in sys_word_lower:
        categories.append("air")
    if "weapon" in sys_word_lower or any(weapon in sys_word_lower for weapon in ["gun", "sword", "bomb", "missile", "tank"]):
        categories.append("weapon")
    if "storm" in sys_word_lower or "hurricane" in sys_word_lower or "tornado" in sys_word_lower:
        categories.append("natural_force")
    if "disease" in sys_word_lower or "virus" in sys_word_lower or "plague" in sys_word_lower or "pandemic" in sys_word_lower:
        categories.append("disease")
    
    # If no categories found, assign based on word length
    if not categories:
        if len(sys_word) < 5:
            categories.append("small")
        elif len(sys_word) < 8:
            categories.append("medium")
        else:
            categories.append("large")
    
    # Adaugă această categorizare specifică pentru animale
    # Detectează mai explicit toate animalele posibile
    animal_keywords = ["lion", "tiger", "bear", "wolf", "snake", "shark", "dragon", 
                      "elephant", "butterfly", "eagle", "bird", "insect", "fish", 
                      "animal", "mammal", "reptile", "amphibian"]
    
    if any(animal in sys_word_lower for animal in animal_keywords):
        categories.append("animal")
    
    # Cazuri speciale pentru categorizare
    if sys_word_lower == "pandemic":
        categories = ["disease", "epidemic_disease", "global", "health_threat"]  # Înlocuiește categoriile existente
    elif sys_word_lower in ["elephant", "butterfly", "eagle", "shark"]:
        categories.append("animal")  # Asigură-te că sunt categorizate ca animale
    # Adaugă cazul special pentru "broom"
    elif sys_word_lower == "broom":
        categories.append("wood_object")  # Adaugă categorie specială pentru obiecte din lemn
        materials.append("wood")  # Marchează explicit ca fiind din lemn
    # Adaugă cazul special pentru "cup"
    elif sys_word_lower == "cup":
        categories.append("small_breakable")  # Adaugă categorie pentru obiecte mici care pot fi sparte
        size = "small"  # Asigură-te că este marcat ca mic
    
    return {
        "categories": categories,
        "size": size,
        "materials": materials,
        "wordnet_categories": wordnet_categories
    }

def calculate_wordnet_score(player_word, sys_word_data, sys_word):
    """Calculate a score based on WordNet semantic relationships"""
    score = 0
    
    # Extrage categoriile din analiza cuvântului sistem
    sys_categories = sys_word_data["categories"]
    sys_wordnet_categories = sys_word_data.get("wordnet_categories", [])
    
    # Penalizare pentru Shadow
    if player_word == "Shadow":
        # Reducem scorul Shadow cu 40%
        score *= 0.6
        
        # Verificăm categoriile sistemului pentru penalizări suplimentare
        if any(cat in ["light", "fire", "cosmic", "lightning"] for cat in sys_categories):
            score *= 0.4  # Penalizare mai mare contra cuvintelor luminoase
    
    # Penalizare pentru Light
    if player_word == "Light":
        # Reducem scorul Light cu 60%
        score *= 0.4
        
        # Penalizare pentru utilizare frecventă
        usage_count = WORD_USAGE_COUNT.get("Light", 0)
        penalty = max(0.2, 1.0 - (usage_count * 0.2))  # Penalizare agresivă
        score *= penalty
    
    # Pentru cazuri speciale ca "Pandemic"
    if sys_word.lower() == "pandemic":
        if player_word == "Vaccine":
            score *= 5.0  # Prioritate mare pentru Vaccine
        elif player_word == "Cure":
            score *= 3.0  # Cure rămâne a doua opțiune
    
    return score

def what_beats(sys_word):
    """Determine the best word to beat the given system word"""
    # Ensure words have been categorized
    if not PLAYER_WORDS[1].get("categories"):
        categorize_player_words()
    
    # Cazuri speciale pentru cuvinte specifice
    if sys_word.lower() == "broom":
        # Pentru mătură, preferăm "Flame" pentru că e din lemn
        for word_id, info in PLAYER_WORDS.items():
            if info["text"] == "Flame":
                print(f"Special case: 'Broom' detected - using Flame")
                return word_id
    
    elif sys_word.lower() == "cup":
        # Pentru ceașcă, preferăm "Rock" sau "Stone" pentru că e un obiect mic și fragil
        for word_id, info in PLAYER_WORDS.items():
            if info["text"] in ["Rock", "Stone"]:
                print(f"Special case: 'Cup' detected - using {info['text']}")
                return word_id
    
    # Analyze system word
    sys_word_analysis = analyze_system_word(sys_word)
    sys_categories = sys_word_analysis["categories"]
    sys_size = sys_word_analysis["size"]
    sys_materials = sys_word_analysis["materials"]
    sys_wordnet_categories = sys_word_analysis["wordnet_categories"]
    
    # Calculate scores for each player word
    word_scores = {}
    for word_id, info in PLAYER_WORDS.items():
        player_word = info["text"]
        cost = info["cost"]
        player_categories = info["categories"]
        player_wordnet_categories = info.get("wordnet_categories", [])
        player_size = info["size"]
        player_power = info["power"]
        
        # Base score starts with the power level
        base_score = player_power * 10
        
        # Size relationship adjustment - penalize small words against large threats
        size_adjustment = 0
        
        # Apply size adjustments
        if player_size == "tiny" and sys_size in ["enormous", "cosmic"]:
            size_adjustment = SIZE_ADJUSTMENTS["tiny_vs_enormous"]
        elif player_size == "tiny" and sys_size in ["large", "huge"]:
            size_adjustment = SIZE_ADJUSTMENTS["tiny_vs_large"]
        elif player_size == "small" and sys_size in ["enormous", "cosmic"]:
            size_adjustment = SIZE_ADJUSTMENTS["small_vs_enormous"]
        elif player_size == "small" and sys_size in ["large", "huge"]:
            size_adjustment = SIZE_ADJUSTMENTS["small_vs_large"]
        elif player_size == "medium" and sys_size in ["enormous", "cosmic"]:
            size_adjustment = SIZE_ADJUSTMENTS["medium_vs_enormous"]
        elif player_size in ["large", "huge"] and sys_size == "tiny":
            size_adjustment = SIZE_ADJUSTMENTS["large_vs_tiny"]
        elif player_size in ["enormous", "cosmic"] and sys_size == "tiny":
            size_adjustment = SIZE_ADJUSTMENTS["enormous_vs_tiny"]
        elif player_size in ["enormous", "cosmic"] and sys_size == "small":
            size_adjustment = SIZE_ADJUSTMENTS["enormous_vs_small"]
            
        # Apply material-based hard counters
        material_boost = 0
        for material in sys_materials:
            if material in MATERIAL_COUNTERS and player_word in MATERIAL_COUNTERS[material]:
                material_boost += MATERIAL_COUNTERS[material][player_word]
        
        # Calculează scorul WordNet normal
        wordnet_score = calculate_wordnet_score(player_word, sys_word_analysis, sys_word)
        word_scores[word_id] = (
            base_score + 
            (size_adjustment * 0.5) +  # Reduce size impact by half
            (material_boost * 2.0) +  # Double material counters
            wordnet_score
        )
        
        # Cazuri speciale pentru cuvinte specifice
        if sys_word.lower() == "broom":
            if player_word == "Flame":
                word_scores[word_id] *= 5.0  # Boost major pentru Flame împotriva Broom
            elif player_word == "Fire":
                word_scores[word_id] *= 4.0  # Boost mare pentru Fire împotriva Broom
        
        elif sys_word.lower() == "cup":
            if player_word in ["Rock", "Stone"]:
                word_scores[word_id] *= 5.0  # Boost major pentru Rock/Stone împotriva Cup
        
        # Apply category-specific strength modifiers
        category_strength = 0
        for sys_cat in sys_categories:
            if player_word in WORD_STRENGTH and sys_cat in WORD_STRENGTH[player_word]:
                category_strength += WORD_STRENGTH[player_word][sys_cat] * 20
        
        # Apply category-specific weakness modifiers
        category_weakness = 0
        for sys_cat in sys_categories:
            if player_word in WORD_WEAKNESS and sys_cat in WORD_WEAKNESS[player_word]:
                category_weakness += WORD_WEAKNESS[player_word][sys_cat] * 20
        
        # Cost factor - modificat pentru cuvinte medii
        if cost <= 3:  # Very cheap
            cost_factor = 40  # Crescut și mai mult
        elif cost <= 6:  # Cheap
            cost_factor = 80  # Mare
        elif cost == 7:  # Specific pentru Shadow și Light
            cost_factor = 20  # Redus dramatic
        elif cost == 8:  # Sound, Time, Fate
            cost_factor = 70  # Bun
        elif cost == 9:  # Earthquake, Storm, Vaccine
            cost_factor = 100  # Foarte bun
        elif cost <= 15:  # Celelalte cuvinte medii
            cost_factor = 60
        elif cost <= 20:  # Expensive
            cost_factor = 35
        else:  # Very expensive
            cost_factor = 15
            
        # Combine all factors
        word_scores[word_id] += (
            (size_adjustment * 0.5) +  # Reduce size impact by half
            (material_boost * 2.0) +  # Double material counters
            category_strength +
            category_weakness +
            cost_factor
        )
        for sys_cat in sys_wordnet_categories:
            if sys_cat in CATEGORY_COUNTERS and player_word in CATEGORY_COUNTERS[sys_cat]:
                word_scores[word_id] += 300
        
        # Special cases
        if player_word == "Feather" and sys_size in ["large", "huge", "enormous", "cosmic"]:
            word_scores[word_id] = 0.5  # Severely penalize using feather against big things
        
        if sys_word.lower() in ["alien", "monster", "ghost", "zombie", "vampire"]:
            if player_word in ["Gun", "Light", "Logic"]:
                word_scores[word_id] += 200  # Boost for specific counters
    
    # Get top 3 scoring words
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Verifică opțiuni pentru diversitate
    if len(sorted_words) >= 2:
        best_id, best_score = sorted_words[0]
        second_id, second_score = sorted_words[1]
        
        best_word = PLAYER_WORDS[best_id]["text"]
        second_word = PLAYER_WORDS[second_id]["text"]
        
        # Verifică dacă primul cuvânt e folosit frecvent și al doilea e suficient de bun
        if best_word in WORD_USAGE_COUNT and WORD_USAGE_COUNT[best_word] > 1:
            if second_score > best_score * 0.8:  # Dacă al doilea e la cel puțin 80% din scor
                # Verifică dacă al doilea e folosit mai puțin
                if second_word not in WORD_USAGE_COUNT or WORD_USAGE_COUNT.get(second_word, 0) < WORD_USAGE_COUNT.get(best_word, 0):
                    best_id = second_id  # Alege cuvântul mai puțin folosit
    
    # Actualizăm contorul pentru cuvântul ales
    best_word_id = sorted_words[0][0]
    best_word = PLAYER_WORDS[best_word_id]["text"]
    
    # Incrementăm contorul
    WORD_USAGE_COUNT[best_word] = WORD_USAGE_COUNT.get(best_word, 0) + 1
    
    return best_id

def test_strategy():
    """Test our strategy against a variety of custom words outside the 60-word list"""
    # Make sure categories are initialized
    if not PLAYER_WORDS[1].get("categories"):
        categorize_player_words()
    
    # Create a diverse set of test words
    test_words = [
        # Materials
        "Wood", "Steel", "Glass", "Diamond", "Plastic", "Gold", "Rubber",
        
        # Natural objects
        "Tree", "Mountain", "River", "Forest", "Desert", "Island", "Jungle",
        
        # Animals
        "Tiger", "Eagle", "Shark", "Spider", "Elephant", "Dinosaur", "Dragon",
        
        # Technology
        "Computer", "Smartphone", "Airplane", "Submarine", "Satellite", "Robot", "Spaceship",
        
        # Abstract
        "Love", "Hope", "Fear", "Death", "Knowledge", "Intelligence", "Soul",
        
        # Celestial
        "Planet", "Asteroid", "Comet", "Galaxy", "Universe", "Nebula", "Solar System",
        
        # Mixed sizes
        "Ant", "House", "City", "Continent", "Ocean", "Atom", "Mountain Range",
        
        # Specific objects
        "Chair", "Candle", "Car", "Sword", "Book", "Camera", "Helicopter",
        
        # Game examples from the original challenge
        "Candle", "Hammer", "Tank", "Flood", "Pandemic", "Sun", "Lion", "Tornado",
        
        # WordNet categories to test
        "Entity", "Object", "Weapon", "Animal Material", "Light", "Fire", "Storm",
        "Atmospheric Phenomenon", "Mountain", "Star", "Epidemic Disease", "Conflict"
    ]
    
    # Keep track of results
    results = []
    
    # Test each word
    for test_word in test_words:
        # Get our counter
        counter_id = what_beats(test_word)
        
        # Get counter details
        counter_word = PLAYER_WORDS[counter_id]["text"]
        counter_cost = PLAYER_WORDS[counter_id]["cost"]
        
        # Get analysis of test word
        word_analysis = analyze_system_word(test_word)
        
        # Store results
        results.append({
            "test_word": test_word,
            "counter": counter_word,
            "counter_id": counter_id,
            "cost": counter_cost,
            "size": word_analysis["size"],
            "categories": word_analysis["categories"],
            "materials": word_analysis["materials"],
            "wordnet_categories": word_analysis["wordnet_categories"]
        })
    
    # Display results in a formatted table
    print(f"{'Test Word':<15} | {'Counter':<20} | {'Cost':<5} | {'Size':<10} | {'Materials':<15} | {'WordNet Categories'}")
    print("-" * 100)
    
    for result in results:
        materials = ", ".join(result["materials"]) if result["materials"] else "none"
        wordnet_categories = ", ".join(result["wordnet_categories"][:3]) if len(result["wordnet_categories"]) > 3 else ", ".join(result["wordnet_categories"])
        
        print(f"{result['test_word']:<15} | {result['counter']:<20} | ${result['cost']:<4} | {result['size']:<10} | {materials:<15} | {wordnet_categories}")
    
    # Calculate statistics
    costs = [r["cost"] for r in results]
    avg_cost = sum(costs) / len(costs)
    
    # Count words in each cost tier
    cost_distribution = {
        "very_cheap": len([c for c in costs if c <= 3]),
        "cheap": len([c for c in costs if 4 <= c <= 6]),
        "moderate": len([c for c in costs if 7 <= c <= 15]),
        "expensive": len([c for c in costs if 16 <= c <= 20]),
        "very_expensive": len([c for c in costs if c > 20])
    }
    
    print("\nSummary Statistics:")
    print(f"Average cost: ${avg_cost:.2f}")
    print("Cost distribution:")
    print(f"  Very cheap (1-3): {cost_distribution['very_cheap']} words ({cost_distribution['very_cheap']/len(costs)*100:.1f}%)")
    print(f"  Cheap (4-6): {cost_distribution['cheap']} words ({cost_distribution['cheap']/len(costs)*100:.1f}%)")
    print(f"  Moderate (7-15): {cost_distribution['moderate']} words ({cost_distribution['moderate']/len(costs)*100:.1f}%)")
    print(f"  Expensive (16-20): {cost_distribution['expensive']} words ({cost_distribution['expensive']/len(costs)*100:.1f}%)")
    print(f"  Very expensive (>20): {cost_distribution['very_expensive']} words ({cost_distribution['very_expensive']/len(costs)*100:.1f}%)")
    
    # Add sample game simulation
    print("\n----- SAMPLE GAME SIMULATION -----")
    simulate_game()

def simulate_game():
    """Simulate a game with 20 random words"""
    import random
    
    # Sample system words (expanded to 20 diverse examples)
    system_words = [
        # Originale
        "Candle", "Hammer", "Lion", "Flood", "Pandemic",
        
        # Elemente naturale
        "Fire", "River", "Mountain", "Forest", "Wind",
        
        # Animale
        "Eagle", "Shark", "Elephant", "Butterfly", 
        
        # Tehnologie și obiecte
        "Computer", "Smartphone", "Car", "Book", "Airplane",
        
        # Concepte
        "Love", "War", "Death", "Universe", "Music",
        
        # Fenomene
        "Lightning", "Tornado", "Earthquake", "Rainbow",
        
        # Materiale
        "Gold", "Diamond", "Plastic", "Steel", "Cotton",
        
        # Alimente
        "Coffee", "Chocolate", "Apple", "Bread"
    ]
    
    # Selectează 20 de cuvinte (sau folosește toate dacă sunt 20 sau mai puține)
    selected_words = system_words[:20]
    
    total_cost = 0
    word_counts = {}  # Pentru a ține evidența cuvintelor folosite
    
    print(f"{'Round':<6} | {'System Word':<15} | {'Our Counter':<15} | {'Cost':<5} | {'Total Cost':<10} | {'Size Match':<15}")
    print("-" * 85)
    
    for round_id, sys_word in enumerate(selected_words, 1):
        # Get our counter
        counter_id = what_beats(sys_word)
        counter_word = PLAYER_WORDS[counter_id]["text"]
        counter_cost = PLAYER_WORDS[counter_id]["cost"]
        
        # Numără utilizarea
        word_counts[counter_word] = word_counts.get(counter_word, 0) + 1
        
        # Update total cost
        total_cost += counter_cost
        
        # Get analysis
        sys_analysis = analyze_system_word(sys_word)
        
        # Create size match description
        sys_size = sys_analysis["size"]
        player_size = PLAYER_WORDS[counter_id]["size"]
        
        if sys_size == player_size:
            size_match = "Perfect match"
        elif (player_size in ["large", "huge", "enormous"] and sys_size in ["tiny", "small"]):
            size_match = "Overkill"
        elif (player_size in ["tiny", "small"] and sys_size in ["large", "huge", "enormous"]):
            size_match = "Underpowered"
        else:
            size_match = "Acceptable"
            
        print(f"{round_id:<6} | {sys_word:<15} | {counter_word:<15} | ${counter_cost:<4} | ${total_cost:<9} | {size_match}")
    
    # Afișează statistici despre utilizarea cuvintelor
    most_used = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nFinal score: ${total_cost}")
    print(f"Average cost per word: ${total_cost/len(selected_words):.2f}")
    
    print("\nWord usage distribution:")
    for word, count in most_used:
        if count > 1:  # Arată doar cuvintele folosite de mai multe ori
            print(f"  {word}: {count} times ({count/len(selected_words)*100:.1f}%)")
    
    # Calculează indicele de diversitate
    diversity_index = len(word_counts) / len(selected_words)
    print(f"\nDiversity index: {diversity_index:.2f} (higher is better, max=1.0)")

def test_specific_words():
    """Test counters for specific words"""
    test_words = input("Enter words to test (separated by comma): ").split(",")
    test_words = [word.strip() for word in test_words]
    
    print(f"\n{'Word':<15} | {'Best Counter':<15} | {'Cost':<5} | {'Size':<10} | {'WordNet Categories':<30}")
    print("-" * 80)
    
    for word in test_words:
        if not word:
            continue
            
        # Get the best counter
        counter_id = what_beats(word)
        counter_word = PLAYER_WORDS[counter_id]["text"]
        counter_cost = PLAYER_WORDS[counter_id]["cost"]
        
        # Get analysis
        word_analysis = analyze_system_word(word)
        wordnet_cats = ", ".join(word_analysis["wordnet_categories"][:3]) if word_analysis["wordnet_categories"] else "none"
        
        print(f"{word:<15} | {counter_word:<15} | ${counter_cost:<4} | {word_analysis['size']:<10} | {wordnet_cats}")

def play_game(player_id=PLAYER_ID):
    """Play the word challenge game for a given player."""
    # Asigură-te că am clasificat cuvintele înainte de a începe jocul
    if not PLAYER_WORDS[1].get("categories"):
        categorize_player_words()
        
    print(f"Jucătorul {player_id} începe jocul...")
    
    for round_id in range(1, NUM_ROUNDS + 1):
        round_num = -1
        while round_num != round_id:
            try:
                response = requests.get(get_url)
                response_data = response.json()
                print(f"Response from get-word: {response_data}")
                
                # Verifică structura răspunsului - ajustează dacă este necesar
                if 'word' in response_data:
                    sys_word = response_data['word']
                else:
                    print(f"Warning: 'word' not found in response: {response_data}")
                    sleep(2)
                    continue
                    
                if 'round' in response_data:
                    round_num = response_data['round']
                else:
                    print(f"Warning: 'round' not found in response: {response_data}")
                    sleep(2)
                    continue
                
                if round_num != round_id:
                    print(f"Waiting for round {round_id}, current round is {round_num}")
                    sleep(2)
            except Exception as e:
                print(f"Error fetching word: {e}")
                sleep(2)

        # Verifică status-ul jocului
        try:
            status = requests.get(status_url)
            status_data = status.json()
            print(f"Game status: {status_data}")
        except Exception as e:
            print(f"Error fetching status: {e}")

        # Folosește funcția what_beats pentru a alege cuvântul
        chosen_word_id = what_beats(sys_word)
        chosen_word_text = PLAYER_WORDS[chosen_word_id]["text"]
        print(f"Player {player_id}, Round {round_id}: System word: {sys_word}, Chosen word: {chosen_word_text} (ID: {chosen_word_id})")

        # Pregătește datele pentru trimitere
        data = {
            "player_id": player_id,
            "word_id": chosen_word_id,
            "round_id": round_id
        }
        
        # Trimite răspunsul
        try:
            response = requests.post(post_url, json=data)
            response_data = response.json()
            print(f"Submit response: {response_data}")
        except Exception as e:
            print(f"Error submitting word: {e}")
        
        # Actualizăm contorul pentru cuvântul ales pentru a menține diversitatea
        WORD_USAGE_COUNT[chosen_word_text] = WORD_USAGE_COUNT.get(chosen_word_text, 0) + 1
        
        # Așteaptă puțin înainte de următoarea rundă
        print(f"Waiting for next round...")
        sleep(2)

if __name__ == "__main__":
    print("WordNet-Enhanced Word Power Strategy")
    print("===========================================")
    print("1. Test against a variety of common words")
    print("2. Test specific words")
    print("3. Simulate a sample game")
    print("4. Joacă în competiția live")
    
    choice = input("\nAlege opțiunea (1-4): ").strip()
    
    if choice == "1":
        test_strategy()
    elif choice == "2":
        test_specific_words()
    elif choice == "3":
        if not PLAYER_WORDS[1].get("categories"):
            categorize_player_words()
        simulate_game()
    elif choice == "4":
        # Folosește direct player ID-ul specificat
        print(f"Starting game with player ID: {PLAYER_ID}")
        play_game(PLAYER_ID)
    else:
        print("Opțiune invalidă. Ieșire.")