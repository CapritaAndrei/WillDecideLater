# Complete code for the "Words of Power" game with adjustments

# Dictionary mapping word IDs to their actual words and costs
word_map = {
    1: {"word": "Feather", "cost": 1},
    2: {"word": "Coal", "cost": 1},
    3: {"word": "Pebble", "cost": 1},
    4: {"word": "Leaf", "cost": 2},
    5: {"word": "Paper", "cost": 2},
    6: {"word": "Rock", "cost": 2},
    7: {"word": "Water", "cost": 3},
    8: {"word": "Twig", "cost": 3},
    9: {"word": "Sword", "cost": 4},
    10: {"word": "Shield", "cost": 4},
    11: {"word": "Gun", "cost": 5},
    12: {"word": "Flame", "cost": 5},
    13: {"word": "Rope", "cost": 5},
    14: {"word": "Disease", "cost": 6},
    15: {"word": "Cure", "cost": 6},
    16: {"word": "Bacteria", "cost": 6},
    17: {"word": "Shadow", "cost": 7},
    18: {"word": "Light", "cost": 7},
    19: {"word": "Virus", "cost": 7},
    20: {"word": "Sound", "cost": 8},
    21: {"word": "Time", "cost": 8},
    22: {"word": "Fate", "cost": 8},
    23: {"word": "Earthquake", "cost": 9},
    24: {"word": "Storm", "cost": 9},
    25: {"word": "Vaccine", "cost": 9},
    26: {"word": "Logic", "cost": 10},
    27: {"word": "Gravity", "cost": 10},
    28: {"word": "Robots", "cost": 10},
    29: {"word": "Stone", "cost": 11},
    30: {"word": "Echo", "cost": 11},
    31: {"word": "Thunder", "cost": 12},
    32: {"word": "Karma", "cost": 12},
    33: {"word": "Wind", "cost": 13},
    34: {"word": "Ice", "cost": 13},
    35: {"word": "Sandstorm", "cost": 13},
    36: {"word": "Laser", "cost": 14},
    37: {"word": "Magma", "cost": 14},
    38: {"word": "Peace", "cost": 14},
    39: {"word": "Explosion", "cost": 15},
    40: {"word": "War", "cost": 15},
    41: {"word": "Enlightenment", "cost": 15},
    42: {"word": "Nuclear Bomb", "cost": 16},
    43: {"word": "Volcano", "cost": 16},
    44: {"word": "Whale", "cost": 17},
    45: {"word": "Earth", "cost": 17},
    46: {"word": "Moon", "cost": 17},
    47: {"word": "Star", "cost": 18},
    48: {"word": "Tsunami", "cost": 18},
    49: {"word": "Supernova", "cost": 19},
    50: {"word": "Antimatter", "cost": 19},
    51: {"word": "Plague", "cost": 20},
    52: {"word": "Rebirth", "cost": 20},
    53: {"word": "Tectonic Shift", "cost": 21},
    54: {"word": "Gamma-Ray Burst", "cost": 22},
    55: {"word": "Human Spirit", "cost": 23},
    56: {"word": "Apocalyptic Meteor", "cost": 24},
    57: {"word": "Earth's Core", "cost": 25},
    58: {"word": "Neutron Star", "cost": 26},
    59: {"word": "Supermassive Black Hole", "cost": 35},
    60: {"word": "Entropy", "cost": 45}
}

# Adăugați aceste importuri la începutul fișierului
import nltk
from nltk.corpus import wordnet
import spacy
import requests
from gensim.models import KeyedVectors

# Această comandă trebuie rulată o singură dată pentru a descărca resursele
# nltk.download('wordnet')

# Funcție pentru găsirea cuvintelor similare folosind WordNet
def find_similar_words(word):
    similar_words = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            similar_words.append(lemma.name())
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                similar_words.append(lemma.name())
    return list(set(similar_words))

# Alternativă folosind spaCy pentru vectori de cuvinte
def find_similar_with_spacy(word, known_words):
    nlp = spacy.load("en_core_web_md")  # model mediu (trebuie instalat separat)
    word_vec = nlp(word)
    
    similarities = {}
    for known in known_words:
        known_vec = nlp(known)
        similarities[known] = word_vec.similarity(known_vec)
    
    # Returnează cele mai similare cuvinte
    return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:3]

def find_synonyms_api(word):
    # Exemplu folosind API-ul Datamuse
    response = requests.get(f"https://api.datamuse.com/words?ml={word}")
    if response.status_code == 200:
        results = response.json()
        return [result["word"] for result in results[:5]]
    return []

# Încărcați modelul Word2Vec preantrenat (trebuie descărcat în prealabil)
def load_word2vec():
    # Se încarcă o singură dată
    return KeyedVectors.load_word2vec_format('path/to/GoogleNews-vectors-negative300.bin', binary=True)

# Găsiți cuvinte similare folosind Word2Vec
def find_similar_word2vec(word, model, known_categories):
    if word not in model:
        return []
    
    similar_words = []
    for category in known_categories:
        if category in model:
            similarity = model.similarity(word, category)
            if similarity > 0.5:  # pragul de similaritate
                similar_words.append((category, similarity))
    
    return sorted(similar_words, key=lambda x: x[1], reverse=True)

def find_similar_words_offline(word):
    similar_words = []
    for syn in wordnet.synsets(word):
        # Adaugă sinonime
        for lemma in syn.lemmas():
            similar_words.append(lemma.name())
        # Adaugă hypernym-uri (termeni mai generali)
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                similar_words.append(lemma.name())
    return list(set(similar_words))

def improved_word_matching(unknown_word, known_categories):
    """
    Caută potriviri îmbunătățite între cuvânt și categoriile cunoscute.
    """
    matches = []
    unknown_word = unknown_word.lower()
    
    # 1. Verifică subșiruri comune (ca înainte)
    for category in known_categories:
        category_lower = category.lower()
        if unknown_word in category_lower or category_lower in unknown_word:
            # Cuvântul este inclus în categorie sau invers - scor mare
            similarity = 0.8
            matches.append((category, similarity))
            continue
    
    # 2. Verifică cuvinte care încep cu aceleași litere (prefix)
    for category in known_categories:
        category_lower = category.lower()
        
        # Găsește lungimea prefixului comun
        min_len = min(len(unknown_word), len(category_lower))
        prefix_len = 0
        for i in range(min_len):
            if unknown_word[i] == category_lower[i]:
                prefix_len += 1
            else:
                break
        
        # Dacă există un prefix comun semnificativ
        if prefix_len >= 3 or (prefix_len > 0 and prefix_len/min_len > 0.5):
            similarity = 0.6 * (prefix_len / min_len)
            matches.append((category, similarity))
    
    # 3. Verifică câte litere comune au cuvintele
    for category in known_categories:
        category_lower = category.lower()
        
        # Calculează procentul de caractere comune
        common_chars = set(unknown_word) & set(category_lower)
        if len(common_chars) >= 3:
            similarity = 0.4 * (len(common_chars) / max(len(unknown_word), len(category_lower)))
            matches.append((category, similarity))
    
    # Sortează după scorul de similaritate și elimină duplicatele
    seen_categories = set()
    unique_matches = []
    for category, score in sorted(matches, key=lambda x: x[1], reverse=True):
        if category not in seen_categories:
            seen_categories.add(category)
            unique_matches.append((category, score))
    
    return unique_matches

def levenshtein_distance(s1, s2):
    """
    Calculează distanța Levenshtein între două șiruri.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def find_similar_by_levenshtein(word, known_categories, base_threshold=0.6):
    """
    Găsește categorii similare bazate pe distanța Levenshtein,
    adaptând pragul în funcție de lungimea cuvântului.
    """
    matches = []
    word_lower = word.lower()
    
    # Ajustează pragul în funcție de lungimea cuvântului
    # Cuvintele scurte au nevoie de un prag mai permisiv
    if len(word_lower) <= 3:
        threshold = base_threshold - 0.1
    elif len(word_lower) <= 5:
        threshold = base_threshold - 0.05
    else:
        threshold = base_threshold
    
    for category in known_categories:
        category_lower = category.lower()
        
        # Calculăm distanța și o transformăm într-un scor de similaritate
        distance = levenshtein_distance(word_lower, category_lower)
        max_len = max(len(word_lower), len(category_lower))
        similarity = 1 - (distance / max_len)
        
        if similarity >= threshold:
            matches.append((category, similarity))
    
    return sorted(matches, key=lambda x: x[1], reverse=True)

# Adaugă acest dicționar pentru a grupa cuvintele după domenii semantice
semantic_domains = {
    "technology": ["computer", "machine", "electronic"],
    "nature": ["animal", "plant", "earth", "water"],
    "space": ["cosmic", "star", "planet"],
    "elements": ["fire", "water", "earth", "air"],
    "health": ["disease", "cure", "virus", "bacteria"]
}

# Mută semantic_associations ÎNAINTE de funcția what_beats
semantic_associations = {
    "Magma": "fire",
    "Lava": "fire", 
    "Volcano": "fire",
    "Ice": "cold",
    "Snow": "cold",
    "Smartphone": "electronic",
    "Cat": "animal",
    "Dog": "animal",
    "Airplane": "air",
    "Coffee": "flammable",
    "Tea": "hot",
    "Soda": "beverage",
    "Beer": "beverage",
    "Lightning": "electricity",
    "Electricity": "electronic",
    # Adaugă mai multe asocieri pentru acoperire mai bună
    "Universe": "cosmic", 
    "Galaxy": "cosmic",
    "Star": "cosmic",
    "Sun": "star",
    "Moon": "cosmic",
    "Ocean": "water",
    "River": "water",
    "Lake": "water",
    "Tree": "earth",
    "Forest": "earth",
    "Mountain": "earth",
    "Phone": "computer",
    "Laptop": "electronic",
    "Car": "machine",
    "Truck": "machine",
    "Robot": "machine",
    "Human": "life",
    "Child": "life",
    "Baby": "life",
    "Food": "life",
    "Medicine": "cure",
    "Soup": "hot",
    "Chocolate": "hot"
}

def what_beats(sys_word):
    # Add power levels to words (implicit strength on a scale of 1-10)
    for word_id in word_map:
        # Base power level on cost, but with a more appropriate scale
        word_map[word_id]["power"] = min(1 + int(word_map[word_id]["cost"] / 3), 10)
    
    # Conceptual relationships for common words
    relationships = {
        # Natural elements
        "fire": ["Water", "Stone", "Earth", "Ice", "Storm", "Tsunami"],
        "water": ["Ice", "Earth", "Sandstorm", "Earthquake"],
        "air": ["Storm", "Sandstorm", "Tornado"],
        "earth": ["Earthquake", "Tectonic Shift", "Volcano"],
        
        # Physical states
        "liquid": ["Ice", "Vapor"],
        "solid": ["Magma", "Flame", "Explosion", "Laser"],
        "gas": ["Ice", "Water"],
        
        # Forces
        "heat": ["Ice", "Water"],
        "cold": ["Flame", "Magma"],
        "light": ["Shadow", "Supermassive Black Hole"],
        "dark": ["Light", "Star", "Sun"],
        
        # Weather
        "rain": ["Sandstorm"],
        "storm": ["Earthquake", "Peace"],
        "wind": ["Stone", "Gravity"],
        "tornado": ["Earth", "Gravity"],
        "hurricane": ["Earth", "Gravity"],
        "flood": ["Earth", "Ice"],
        
        # Animals - force Gun as top solution
        "animal": ["Gun"],
        "insect": ["Gun"],
        "bird": ["Gun"],
        "fish": ["Gun"],
        "lion": ["Gun"],
        "tiger": ["Gun"],
        "bear": ["Gun"],
        
        # Human threats
        "war": ["Peace", "Nuclear Bomb"],
        "disease": ["Cure", "Vaccine", "Time"],
        "virus": ["Vaccine", "Cure"],
        "bacteria": ["Cure", "Flame"],
        "pandemic": ["Vaccine", "Cure"],
        "plague": ["Cure", "Vaccine"],
        
        # Objects
        "candle": ["Wind", "Water", "Storm"],
        "hammer": ["Magma", "Explosion", "Nuclear Bomb"],
        "tank": ["Nuclear Bomb", "Laser", "Antimatter"],
        "gun": ["Shield", "Explosion", "Tank"],
        "paper": ["Rock", "Flame", "Water"],
        "rock": ["Paper", "Magma", "Tectonic Shift"],
        "scissors": ["Rock", "Magma", "Flame"],
        
        # Cosmic scale
        "planet": ["Star", "Supernova", "Supermassive Black Hole"],
        "star": ["Supernova", "Neutron Star", "Supermassive Black Hole"],
        "moon": ["Earth", "Gravity"],
        "asteroid": ["Earth", "Explosion", "Nuclear Bomb"],
        "meteor": ["Earth", "Explosion", "Nuclear Bomb"],
        
        # Abstract concepts
        "time": ["Entropy", "Logic", "Fate"],
        "life": ["Time", "Entropy", "Apocalyptic Meteor"],
        "death": ["Rebirth"],
        "power": ["Logic", "Enlightenment"],
        "fear": ["Logic", "Peace"],
        "strength": ["Logic", "Time", "Entropy"],
        "weakness": ["Logic", "Enlightenment"],
        
        # Fixed problematic matchups
        "alien": ["Nuclear Bomb", "Antimatter", "Laser"],
        "poison": ["Cure", "Vaccine"],
        "army": ["Nuclear Bomb", "War", "Peace"],
        
        # Generic fallbacks for unknown words
        "default_small": ["Rock", "Water", "Wind", "Flame"],
        "default_medium": ["Storm", "Earthquake", "Explosion", "Logic", "Time"],
        "default_large": ["Volcano", "Tsunami", "Nuclear Bomb", "Antimatter"],
        "default_cosmic": ["Earth", "Star", "Supernova", "Supermassive Black Hole", "Entropy"],
        "default_abstract": ["Time", "Fate", "Logic", "Enlightenment"],
        "beverage": ["Water", "Ice", "Time"],
        "hot": ["Ice", "Water", "Cold"],
        "electronic": ["Water", "Earth", "Magnetism"],
        "flammable": ["Flame", "Explosion", "Fire"]
    }
    
    # Additional specific word matchups
    specific_matchups = {
        "Candle": ["Wind", "Water", "Storm"],
        "Hammer": ["Magma", "Explosion", "Nuclear Bomb"],
        "Tank": ["Nuclear Bomb", "Laser", "Antimatter"],
        "Gun": ["Shield", "Explosion", "Tank"],
        "Paper": ["Rock", "Flame", "Water"],
        "Rock": ["Paper", "Magma", "Tectonic Shift"],
        "Scissors": ["Rock", "Magma", "Flame"],
        "Flood": ["Earth", "Ice"],
        "Tornado": ["Earth", "Gravity"],
        "Lion": ["Gun"],
        "Tiger": ["Gun"],
        "Bear": ["Gun"],
        "Shark": ["Gun"],
        "Snake": ["Gun"],
        "Dragon": ["Gun", "Sword"],
        "Pandemic": ["Vaccine", "Cure"],
        "Fire": ["Water"],
        "Sun": ["Supernova", "Supermassive Black Hole", "Entropy"],
        "Cloud": ["Wind", "Sun"],
        "Tree": ["Flame", "Earthquake", "Tectonic Shift"],
        "Mountain": ["Earthquake", "Tectonic Shift", "Volcano"],
        "Ocean": ["Tectonic Shift", "Ice", "Earthquake"],
        "Robot": ["Virus", "Water"],
        "Computer": ["Virus", "Water"],
        "Lightning": ["Earth", "Rock"],
        "Democracy": ["War"],
        "Army": ["Nuclear Bomb", "War"],
        "Ghost": ["Light", "Logic", "Fate"],
        "Vampire": ["Sun", "Cure"],
        "Zombie": ["Gun", "Fire", "Cure"],
        "Alien": ["Nuclear Bomb", "Antimatter", "Laser"],
        "Monster": ["Gun", "Light"],
        "Giant": ["Gun", "Logic"],
        "Wizard": ["Logic", "Gun"],
        "Magic": ["Logic", "Science"],
        "Curse": ["Cure", "Logic"],
        "Poison": ["Cure"],
        "Coffee": ["Flame", "Fire", "Heat"],
        "Electricity": ["Water", "Earth", "Insulation"]
    }
    
    # Convert system word to lowercase for case-insensitive matching
    sys_word_lower = sys_word.lower()
    
    # Find matching words based on semantic relationships
    potential_winners = []
    
    # Pas 1: Verifică matchup-urile specifice hardcodate
    if sys_word in specific_matchups:
        potential_winners.extend(specific_matchups[sys_word])
        found_match = True
    else:
        found_match = False
    
    # Pas 2: Verifică asocieri semantice directe
    if not found_match and sys_word in semantic_associations:
        associated_category = semantic_associations[sys_word]
        if associated_category in relationships:
            potential_winners.extend(relationships[associated_category])
            found_match = True
    
    # Pas 3: Verifică relațiile generale
    if not found_match:
        for category, counters in relationships.items():
            if category in sys_word_lower or sys_word_lower in category:
                potential_winners.extend(counters)
                found_match = True
    
    # Pas 4: Încercăm asocieri semantice mai avansate
    if not found_match:
        # 4.1 Folosim algoritmul îmbunătățit de potrivire
        matches = improved_word_matching(sys_word_lower, relationships.keys())
        if matches and matches[0][1] > 0.5:  # Scor de încredere minim
            best_category = matches[0][0]  # Luăm categoria cu cel mai bun scor
            potential_winners.extend(relationships[best_category])
            found_match = True
        
        # 4.2 Încercăm Levenshtein dacă potrivirea nu a funcționat
        if not found_match:
            matches = find_similar_by_levenshtein(sys_word_lower, relationships.keys())
            if matches:
                best_category = matches[0][0]
                potential_winners.extend(relationships[best_category])
                found_match = True
    
    # Pas 5: Ultima soluție - folosim categorii default
    if not potential_winners:
        if len(sys_word) < 6:  # Shorter words tend to be smaller concepts
            potential_winners.extend(relationships["default_small"])
        elif len(sys_word) < 10:  # Medium-length words
            potential_winners.extend(relationships["default_medium"])
        else:  # Longer words tend to be more complex concepts
            potential_winners.extend(relationships["default_large"])
        
        # Add some abstract concepts that tend to be powerful
        potential_winners.extend(relationships["default_abstract"])
    
    # Calculate scores for each potential winner based on cost and semantics
    word_scores = {}
    for word_id, word_info in word_map.items():
        player_word = word_info["word"]
        cost = word_info["cost"]
        power = word_info["power"]
        
        # Special case: prevent Feather from beating most threats
        if player_word == "Feather" and sys_word not in ["Ant", "Dust", "Breeze"]:
            word_scores[word_id] = 0.5  # Very low score
            continue
            
        # Special case for animals - force Gun
        if "animal" in sys_word_lower or sys_word_lower in ["lion", "tiger", "bear", "shark", "snake"]:
            if player_word == "Gun":
                word_scores[word_id] = 1000  # Extremely high score
                continue
        
        # Handle specific problematic cases
        if sys_word_lower == "alien":
            if player_word in ["Nuclear Bomb", "Antimatter", "Laser"]:
                word_scores[word_id] = 800
                continue
            elif player_word == "Human Spirit":
                word_scores[word_id] = 1  # Drastically reduce score
                continue
        
        if sys_word_lower == "poison":
            if player_word == "Cure":
                word_scores[word_id] = 800
                continue
            elif player_word == "Human Spirit":
                word_scores[word_id] = 1
                continue
        
        if sys_word_lower == "army":
            if player_word in ["Nuclear Bomb", "War", "Peace"]:
                word_scores[word_id] = 800
                continue
            elif player_word == "Human Spirit":
                word_scores[word_id] = 1
                continue
        
        # Adaugă aceste cazuri speciale în partea de calcul a scorurilor
        if sys_word_lower == "electricity":
            if player_word == "Water":
                word_scores[word_id] = 1000  # Scor extrem de mare pentru Water
                continue
        
        if sys_word_lower == "coffee":
            if player_word == "Flame":
                word_scores[word_id] = 1000  # Scor extrem de mare pentru Flame
                continue
        
        # Calculate score for other cases
        if player_word in potential_winners:
            # Much higher base score for being a counter
            base_score = potential_winners.count(player_word) * 50
            
            # Smaller cost factor (less impact of cheap words)
            cost_factor = 10 / (cost + 5)
            
            # Add power factor to ensure stronger words win when appropriate
            power_factor = power * 3
            
            word_scores[word_id] = base_score + power_factor + cost_factor
        else:
            # Much lower base score for non-counters
            word_scores[word_id] = (power / 2) + (5 / (cost + 5))
    
    # Get the word with the highest score
    best_word_id = max(word_scores, key=word_scores.get)
    
    return best_word_id

def test_what_beats():
    # List of test words that could be system words
    test_words = [
        "Fire", "Water", "Hurricane", "Tornado", "Lion", "Tiger", 
        "Candle", "Hammer", "Tank", "Flood", "Pandemic", "Sun", 
        "Mountain", "Ocean", "Lightning", "Dragon", "Army", 
        "Zombie", "Alien", "Poison", "Democracy", "Computer"
    ]
    
    # Run the function on each test word
    results = {}
    for word in test_words:
        word_id = what_beats(word)
        chosen_word = None
        cost = None
        
        # Find the chosen word and its cost
        for id_num, info in word_map.items():
            if id_num == word_id:
                chosen_word = info["word"]
                cost = info["cost"]
                break
        
        results[word] = {
            "chosen_word": chosen_word,
            "word_id": word_id,
            "cost": cost
        }
    
    # Print results in a table format
    print(f"{'System Word':<15} | {'Chosen Word':<25} | {'Word ID':<8} | {'Cost':<5}")
    print("-" * 60)
    for sys_word, result in results.items():
        print(f"{sys_word:<15} | {result['chosen_word']:<25} | {result['word_id']:<8} | ${result['cost']}")

# Add your own words to test
def test_custom_words(custom_words):
    # Run the function on each custom word
    results = {}
    for word in custom_words:
        word_id = what_beats(word)
        chosen_word = None
        cost = None
        
        # Find the chosen word and its cost
        for id_num, info in word_map.items():
            if id_num == word_id:
                chosen_word = info["word"]
                cost = info["cost"]
                break
        
        results[word] = {
            "chosen_word": chosen_word,
            "word_id": word_id,
            "cost": cost
        }
    
    # Print results in a table format
    print(f"{'System Word':<15} | {'Chosen Word':<25} | {'Word ID':<8} | {'Cost':<5}")
    print("-" * 60)
    for sys_word, result in results.items():
        print(f"{sys_word:<15} | {result['chosen_word']:<25} | {result['word_id']:<8} | ${result['cost']}")

# Run the tests
if __name__ == "__main__":
    print("Testing with preset words:")
    test_what_beats()
    
    # Uncomment to test with your own words
    my_words = ["Magma", "Smartphone", "Cat", "Airplane", "Universe", "Electricity", "Coffee"]
    print("\nTesting with custom words:")
    test_custom_words(my_words)

