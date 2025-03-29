import requests
from time import sleep
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

# Server endpoints
host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5
PLAYER_ID = "Llwr60Mns2"  # Fixed player ID

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

def analyze_system_word(sys_word):
    """Analyze a system word and return its categories and properties"""
    # Preprocess the word
    sys_word_lower = sys_word.lower()
    lemmatized = lemmatizer.lemmatize(sys_word_lower)
    
    categories = []
    materials = []
    size = None
    
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
    
    # Check for direct matches in our counter database
    if sys_word in DIRECT_COUNTERS:
        categories.append("known")
        
    # Check WordNet for categories
    synsets = wn.synsets(lemmatized)
    if synsets:
        # Get the most common definitions
        for synset in synsets[:2]:
            # Extract hypernyms (categories)
            for hypernym in synset.hypernyms():
                categories.append(hypernym.name().split('.')[0])
            
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
    
    return {
        "categories": categories,
        "size": size,
        "materials": materials
    }

def what_beats(sys_word):
    """Determine the best word to beat the given system word"""
    # Ensure words have been categorized
    if not PLAYER_WORDS[1].get("categories"):
        categorize_player_words()
    
    # Analyze system word
    sys_word_analysis = analyze_system_word(sys_word)
    sys_categories = sys_word_analysis["categories"]
    sys_size = sys_word_analysis["size"]
    sys_materials = sys_word_analysis["materials"]
    
    # Calculate scores for each player word
    word_scores = {}
    for word_id, info in PLAYER_WORDS.items():
        player_word = info["text"]
        cost = info["cost"]
        player_categories = info["categories"]
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
        
        # Special case for animals - force Gun (but keep it reasonably priced)
        if "animal" in sys_categories and player_word == "Gun":
            word_scores[word_id] = 1000
            continue
        
        # Cost factor - prioritize mid-range words (peak at middle

def test_random_words():
    """Testează cuvinte aleatorii pentru a verifica răspunsul sistemului"""
    # Cuvinte aleatorii pentru test - o varietate de concepte și categorii
    test_words = [
        # Elemente naturale
        "Rain", "Snow", "Fog", "Clouds", "Glacier", "Desert", "Waterfall", "Rainbow",
        
        # Tehnologie
        "Smartphone", "Laptop", "Television", "Radio", "Internet", "Camera", "Speaker", 
        "Microphone", "Computer", "Tablet", "Printer", "Keyboard", "Battery",
        
        # Animale
        "Dog", "Cat", "Elephant", "Giraffe", "Dolphin", "Sparrow", "Eagle", "Penguin", 
        "Scorpion", "Spider", "Butterfly", "Bee", "Ant", "Crocodile", "Wolf",
        
        # Materiale
        "Steel", "Glass", "Plastic", "Gold", "Silver", "Diamond", "Rubber", "Cement",
        "Marble", "Concrete", "Titanium", "Bronze", "Cotton", "Silk", "Wool", 
        
        # Alimente și băuturi
        "Coffee", "Tea", "Soda", "Juice", "Wine", "Beer", "Pizza", "Hamburger", 
        "Chocolate", "Cake", "Ice Cream", "Bread", "Cheese", "Sugar", "Salt",
        
        # Fenomene
        "Lightning", "Thunder", "Eclipse", "Aurora", "Avalanche", "Landslide", 
        "Whirlpool", "Heatwave", "Blizzard", "Drought", "Flood", "Tornado",
        
        # Vehicule
        "Car", "Bicycle", "Motorcycle", "Ship", "Boat", "Airplane", "Helicopter", 
        "Train", "Bus", "Rocket", "Submarine", "Truck", "Spaceship",
        
        # Concepte abstracte
        "Love", "Hate", "Joy", "Sorrow", "Freedom", "Justice", "Truth", "Beauty", 
        "Friendship", "Hope", "Faith", "Dream", "Memory", "Thought", "Wisdom",
        
        # Obiecte uzuale
        "Chair", "Table", "Bed", "Mirror", "Clock", "Lamp", "Sofa", "Book", 
        "Pencil", "Scissors", "Key", "Phone", "Wallet", "Umbrella", "Backpack"
    ]
    
    print("Testarea cuvintelor aleatorii...")
    print(f"{'Cuvânt sistem':<20} | {'Cel mai bun răspuns':<25} | {'ID':<4} | {'Cost':<5}")
    print("-" * 65)
    
    for word in test_words:
        best_word_id = what_beats(word)
        best_word_info = None
        
        # Găsește informații despre cel mai bun cuvânt
        for word_id, info in PLAYER_WORDS.items():
            if word_id == best_word_id:
                best_word_info = info
                break
                
        if best_word_info:
            print(f"{word:<20} | {best_word_info['text']:<25} | {best_word_id:<4} | ${best_word_info['cost']}")
        else:
            print(f"{word:<20} | {'Nu s-a găsit':<25} | - | -")
    
    print("\nTestare completă!")

# Adaugă acest cod pentru a apela funcția de testare când rulezi scriptul direct
if __name__ == "__main__":
    categorize_player_words()  # Asigură-te că toate cuvintele sunt categorizate
    
    # Poți decomenta una dintre aceste linii pentru a testa
    # test_random_words()  # Testează cuvinte aleatorii
    
    # Sau poți testa cuvinte specifice
    custom_words = [
        "Smartphone", "Elephant", "Lightning", "Coffee", "Automobile", 
        "Diamond", "Concrete", "Thunder", "Camera", "Dragon", "Fantasy",
        "Tornado", "Chocolate", "Constitution", "Internet", "Algorithm"
    ]
    
    print("\nTestare cuvinte personalizate:")
    print(f"{'Cuvânt sistem':<20} | {'Cel mai bun răspuns':<25} | {'ID':<4} | {'Cost':<5}")
    print("-" * 65)
    
    for word in custom_words:
        best_word_id = what_beats(word)
        best_word_info = PLAYER_WORDS.get(best_word_id)
        
        if best_word_info:
            print(f"{word:<20} | {best_word_info['text']:<25} | {best_word_id:<4} | ${best_word_info['cost']}")
        else:
            print(f"{word:<20} | {'Nu s-a găsit':<25} | - | -")
    
    print("\nTestare completă!")