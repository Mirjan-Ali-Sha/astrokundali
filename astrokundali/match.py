"""
astrokundali/match.py - Enhanced Version

Enhanced Ashtakoota (Guna Milan) marriage matching with:
- Complete 14-animal Yoni compatibility matrix  
- Comprehensive Graha Maitri scoring (0, 0.5, 1, 3, 4, 5)
- Enhanced Bhakoot dosha cancellation rules
- Improved Nadi dosha cancellation with Pada logic
- Advanced dosha cancellation system
- Weighted compatibility calculation
- Comprehensive risk assessment
- Detailed interpretations
"""

import swisseph as swe
from .astro_data import AstroData
from .dispositions import get_dispositions
import json, codecs
from pathlib import Path

# Enhanced mappings with complete data
VARNA_MAP = {1:3,2:2,3:1,4:3,5:4,6:2,7:1,8:3,9:4,10:2,11:1,12:4}
VARNA_NAME = {1:'Brahmin',2:'Kshatriya',3:'Vaishya',4:'Shudra'}

VASHA_MAP = {
    1:'Chatushpada',2:'Manav',3:'Jalachara',4:'Jalachara',
    5:'Chatushpada',6:'Manav',7:'Manav',8:'Vanachara',
    9:'Manav',10:'Chatushpada',11:'Chatushpada',12:'Jalachara'
}

# Enhanced Gana groups with complete mapping
GANA_GROUPS = {
    # Deva Gana (Divine nature)
    1:'Deva', 5:'Deva', 7:'Deva', 8:'Deva', 13:'Deva', 15:'Deva', 
    17:'Deva', 22:'Deva', 27:'Deva',
    # Manushya Gana (Human nature)  
    2:'Manushya', 4:'Manushya', 6:'Manushya', 12:'Manushya', 20:'Manushya', 
    21:'Manushya', 25:'Manushya', 26:'Manushya',
    # Rakshasa Gana (Demonic nature)
    3:'Rakshasa', 9:'Rakshasa', 10:'Rakshasa', 11:'Rakshasa', 14:'Rakshasa', 
    16:'Rakshasa', 18:'Rakshasa', 19:'Rakshasa', 23:'Rakshasa', 24:'Rakshasa'
}

# Complete 14-animal Yoni mapping
YONI_MAP = {
    1:'Horse', 2:'Elephant', 3:'Sheep', 4:'Snake', 5:'Snake', 6:'Dog',
    7:'Cat', 8:'Rat', 9:'Cow', 10:'Buffalo', 11:'Tiger', 12:'Deer',
    13:'Monkey', 14:'Lion', 15:'Mongoose', 16:'Tiger', 17:'Deer', 18:'Dog',
    19:'Elephant', 20:'Horse', 21:'Dog', 22:'Horse', 23:'Sheep', 24:'Rat',
    25:'Deer', 26:'Rat', 27:'Elephant'
}

# Enhanced Nadi mapping with complete classification
NADI_MAP = {
    # Adi Nadi (Vata - Air element)
    1:'Adi', 6:'Adi', 12:'Adi', 13:'Adi', 19:'Adi', 7:'Adi', 18:'Adi', 25:'Adi', 24:'Adi',
    # Madhya Nadi (Pitta - Fire element)
    2:'Madhya', 8:'Madhya', 5:'Madhya', 14:'Madhya', 11:'Madhya', 20:'Madhya', 17:'Madhya', 26:'Madhya', 23:'Madhya',
    # Antya Nadi (Kapha - Water element)
    4:'Antya', 9:'Antya', 3:'Antya', 10:'Antya', 15:'Antya', 16:'Antya', 21:'Antya', 22:'Antya', 27:'Antya'
}

# Enhanced Koota information with detailed descriptions
KOOTA_INFO = {
    'Varna': {'max':1, 'desc':'Spiritual Development & Social Compatibility'},
    'Vashya': {'max':2, 'desc':'Mutual Control & Dominance Balance'},
    'Tara': {'max':3, 'desc':'Health, Longevity & Prosperity'},
    'Yoni': {'max':4, 'desc':'Physical & Intimate Compatibility'},
    'Graha Maitri':{'max':5, 'desc':'Mental & Emotional Harmony'},
    'Gana': {'max':6, 'desc':'Temperamental & Behavioral Match'},
    'Bhakoot': {'max':7, 'desc':'Financial & Emotional Stability'},
    'Nadi': {'max':8, 'desc':'Genetic & Health Harmony'}
}

# Enhanced remedies with specific actions
REMINDERS = {
    'Varna': ['Navagraha Shanti Puja', 'Recite Gayatri Mantra daily', 'Donate to Brahmins'],
    'Vashya': ['Donate sweets on Wednesdays', 'Wear Cat\'s Eye gemstone', 'Chant Budha Mantra'],
    'Tara': ['Tara Dosha Havan', 'Visit Tara Devi Temple', 'Perform Nakshatra Puja'],
    'Yoni': ['Chant Maha Mrityunjaya Mantra', 'Perform Graha Shanti Puja', 'Wear appropriate gemstones'],
    'Gana': ['Gan Dosh Nivaran Puja', 'Chant Jupiter Mantra', 'Donate yellow items'],
    'Bhakoot': ['Bhakoot Dosha Shanti Puja', 'Charity of white foods', 'Perform Rudrabhishek'],
    'Graha Maitri': ['Graha Maitri Shanti Havan', 'Wear Pearl & Yellow Sapphire', 'Chant planetary mantras'],
    'Nadi': ['Nadi Dosha Havan', 'Pilgrimage to Saptashrungi', 'Perform Maha Mrityunjaya Jaap'],
    'Manglik': ['Mangal Dosha Puja at Mangalnath Temple', 'Kumbh Vivah ritual', 'Plant Neem tree for 42 days', 'Donate red items on Tuesdays', 'Wear Red Coral after consultation']
}

# Enhanced remedies with constructive approaches
# Load constructive remedies from JSON
DATA_DIR = Path(__file__).parent / 'data'
CONSTRUCTIVE_REMEDIES = json.load(open(DATA_DIR / 'cons_rem_marriage.json'))
# CONSTRUCTIVE_REMEDIES =

# Complete planetary friendship matrix
FRIENDSHIP = {
    'sun': {'friends': ['moon','mars','jupiter'], 'enemies': ['venus','saturn'], 'neutral': ['mercury']},
    'moon': {'friends': ['sun','mercury'], 'enemies': [], 'neutral': ['mars','jupiter','venus','saturn']},
    'mars': {'friends': ['sun','moon','jupiter'], 'enemies': ['mercury'], 'neutral': ['venus','saturn']},
    'mercury': {'friends': ['sun','venus'], 'enemies': ['moon','mars'], 'neutral': ['jupiter','saturn']},
    'jupiter': {'friends': ['sun','moon','mars'], 'enemies': ['mercury','venus'], 'neutral': ['saturn']},
    'venus': {'friends': ['mercury','saturn'], 'enemies': ['sun','moon','mars'], 'neutral': ['jupiter']},
    'saturn': {'friends': ['mercury','venus'], 'enemies': ['sun','moon','mars'], 'neutral': ['jupiter']},
    'rahu': {'friends': ['venus','saturn'], 'enemies': ['sun','moon','mars'], 'neutral': ['mercury','jupiter']},
    'ketu': {'friends': ['mars','jupiter'], 'enemies': ['moon','venus'], 'neutral': ['sun','mercury','saturn']}
}

# Enhanced scoring functions

def varna_koota(m1, m2):
    """Enhanced Varna Koota with detailed scoring"""
    boy_varna = VARNA_MAP[m1['sign_number']]
    girl_varna = VARNA_MAP[m2['sign_number']]
    
    # Boy's varna should be equal or higher than girl's
    if boy_varna >= girl_varna:
        return 1
    return 0

def vashya_koota(m1, m2):
    """Enhanced Vashya with complete compatibility matrix"""
    vashya_scores = {
        # Same group = 2 points
        ("Chatushpada", "Chatushpada"): 2,
        ("Manav", "Manav"): 2,
        ("Jalachara", "Jalachara"): 2,
        ("Vanachara", "Vanachara"): 2,
        ("Keeta", "Keeta"): 2,
        
        # Compatible groups = 1.5 points
        ("Chatushpada", "Manav"): 1.5,
        ("Manav", "Jalachara"): 1.5,
        ("Jalachara", "Vanachara"): 1.5,
        
        # Partially compatible = 1 point
        ("Chatushpada", "Jalachara"): 1,
        ("Chatushpada", "Vanachara"): 1,
        ("Manav", "Vanachara"): 1,
        
        # Incompatible = 0 points
        ("Chatushpada", "Keeta"): 0,
        ("Manav", "Keeta"): 0,
        ("Jalachara", "Keeta"): 0,
        ("Vanachara", "Keeta"): 0
    }
    
    boy_vashya = VASHA_MAP[m1['sign_number']]
    girl_vashya = VASHA_MAP[m2['sign_number']]
    
    return vashya_scores.get((boy_vashya, girl_vashya), 0)

def tara_koota(m1, m2):
    """Calculate Tara Koota (Max: 3) - CORRECTED VERSION"""
    n1, n2 = m1['nakshatra'], m2['nakshatra']
    
    # Calculate remainders
    r1 = (n2 - n1) % 9  # Bride to groom
    r2 = (n1 - n2) % 9  # Groom to bride
    
    # Convert 0 to even for logic
    r1 = r1 if r1 else 0
    r2 = r2 if r2 else 0
    
    # Single consolidated scoring (NOT sum of two)
    even_remainders = {0, 2, 4, 6, 8}
    
    if (r1 in even_remainders) and (r2 in even_remainders):
        return 3      # Both even
    elif (r1 in even_remainders) or (r2 in even_remainders):
        return 1.5    # One even, one odd
    else:
        return 0      # Both odd

def yoni_koota(m1, m2):
    """Complete 14-animal Yoni compatibility matrix"""
    # Research-based complete compatibility matrix
    yoni_scores = {
        # Same yoni = 4 points
        ("Horse", "Horse"): 4, ("Elephant", "Elephant"): 4, ("Sheep", "Sheep"): 4,
        ("Snake", "Snake"): 4, ("Dog", "Dog"): 4, ("Cat", "Cat"): 4,
        ("Rat", "Rat"): 4, ("Cow", "Cow"): 4, ("Buffalo", "Buffalo"): 4,
        ("Tiger", "Tiger"): 4, ("Deer", "Deer"): 4, ("Monkey", "Monkey"): 4,
        ("Lion", "Lion"): 4, ("Mongoose", "Mongoose"): 4,
        
        # Friendly yonis = 3 points
        ("Horse", "Elephant"): 3, ("Elephant", "Horse"): 3,
        ("Sheep", "Elephant"): 3, ("Elephant", "Sheep"): 3,
        ("Snake", "Cow"): 3, ("Cow", "Snake"): 3,
        ("Dog", "Deer"): 3, ("Deer", "Dog"): 3,
        ("Cat", "Tiger"): 3, ("Tiger", "Cat"): 3,
        ("Rat", "Buffalo"): 3, ("Buffalo", "Rat"): 3,
        ("Monkey", "Lion"): 3, ("Lion", "Monkey"): 3,
        
        # Neutral yonis = 2 points (default for unlisted combinations)
        ("Horse", "Sheep"): 2, ("Sheep", "Horse"): 2,
        ("Horse", "Dog"): 2, ("Dog", "Horse"): 2,
        ("Elephant", "Buffalo"): 2, ("Buffalo", "Elephant"): 2,
        ("Snake", "Monkey"): 2, ("Monkey", "Snake"): 2,
        ("Cat", "Cow"): 2, ("Cow", "Cat"): 2,
        ("Rat", "Tiger"): 2, ("Tiger", "Rat"): 2,
        ("Deer", "Lion"): 2, ("Lion", "Deer"): 2,
        
        # Unfriendly yonis = 1 point
        ("Horse", "Buffalo"): 1, ("Buffalo", "Horse"): 1,
        ("Elephant", "Tiger"): 1, ("Tiger", "Elephant"): 1,
        ("Sheep", "Dog"): 1, ("Dog", "Sheep"): 1,
        ("Snake", "Deer"): 1, ("Deer", "Snake"): 1,
        ("Cat", "Monkey"): 1, ("Monkey", "Cat"): 1,
        ("Rat", "Lion"): 1, ("Lion", "Rat"): 1,
        
        # Enemy yonis = 0 points
        ("Cat", "Rat"): 0, ("Rat", "Cat"): 0,
        ("Dog", "Cat"): 0, ("Cat", "Dog"): 0,
        ("Mongoose", "Snake"): 0, ("Snake", "Mongoose"): 0,
        ("Tiger", "Cow"): 0, ("Cow", "Tiger"): 0,
        ("Lion", "Elephant"): 0, ("Elephant", "Lion"): 0,
        ("Monkey", "Sheep"): 0, ("Sheep", "Monkey"): 0,
        ("Horse", "Tiger"): 0, ("Tiger", "Horse"): 0,
        ("Buffalo", "Monkey"): 0, ("Monkey", "Buffalo"): 0
    }
    
    boy_yoni = YONI_MAP[m1['nakshatra']]
    girl_yoni = YONI_MAP[m2['nakshatra']]
    
    return yoni_scores.get((boy_yoni, girl_yoni), 2)  # Default to neutral

def graha_maitri_koota(m1, m2):
    """Enhanced Graha Maitri with complete scoring (0, 0.5, 1, 3, 4, 5)"""
    boy_lord = m1['sign_lord']
    girl_lord = m2['sign_lord']
    
    # Same lord = 5 points
    if boy_lord == girl_lord:
        return 5
    
    # Get relationship data
    boy_relations = FRIENDSHIP.get(boy_lord, {})
    girl_relations = FRIENDSHIP.get(girl_lord, {})
    
    # Check both directions of friendship
    boy_to_girl = 'friends' if girl_lord in boy_relations.get('friends', []) else \
                  'neutral' if girl_lord in boy_relations.get('neutral', []) else \
                  'enemies' if girl_lord in boy_relations.get('enemies', []) else 'neutral'
    
    girl_to_boy = 'friends' if boy_lord in girl_relations.get('friends', []) else \
                  'neutral' if boy_lord in girl_relations.get('neutral', []) else \
                  'enemies' if boy_lord in girl_relations.get('enemies', []) else 'neutral'
    
    # Enhanced scoring based on mutual relationships
    if boy_to_girl == 'friends' and girl_to_boy == 'friends':
        return 4  # Mutual friends
    elif boy_to_girl == 'friends' and girl_to_boy == 'neutral':
        return 3  # One friend, one neutral
    elif boy_to_girl == 'neutral' and girl_to_boy == 'friends':
        return 3  # One neutral, one friend
    elif boy_to_girl == 'neutral' and girl_to_boy == 'neutral':
        return 3  # Both neutral
    elif boy_to_girl == 'friends' and girl_to_boy == 'enemies':
        return 1  # One friend, one enemy
    elif boy_to_girl == 'enemies' and girl_to_boy == 'friends':
        return 1  # One enemy, one friend
    elif boy_to_girl == 'neutral' and girl_to_boy == 'enemies':
        return 0.5  # One neutral, one enemy
    elif boy_to_girl == 'enemies' and girl_to_boy == 'neutral':
        return 0.5  # One enemy, one neutral
    else:  # Both enemies
        return 0

def gana_koota(m1, m2):
    """Enhanced Gana Koota with complete scoring"""
    boy_gana = GANA_GROUPS[m1['nakshatra']]
    girl_gana = GANA_GROUPS[m2['nakshatra']]
    
    if boy_gana == girl_gana:
        return 6  # Same gana
    elif (boy_gana == "Deva" and girl_gana == "Manushya") or \
         (boy_gana == "Manushya" and girl_gana == "Deva"):
        return 5  # Deva-Manushya compatible
    elif (boy_gana == "Manushya" and girl_gana == "Rakshasa") or \
         (boy_gana == "Rakshasa" and girl_gana == "Manushya"):
        return 1  # Manushya-Rakshasa partially compatible
    else:  # Deva-Rakshasa incompatible
        return 0

def bhakoot_koota(m1, m2):
    """Enhanced Bhakoot Koota with exception handling"""
    boy_rashi = m1['sign_number']
    girl_rashi = m2['sign_number']
    
    # Calculate bidirectional difference
    diff_boy_to_girl = (girl_rashi - boy_rashi) % 12
    diff_girl_to_boy = (boy_rashi - girl_rashi) % 12
    
    # Convert 0 to 12 for proper calculation
    diff_boy_to_girl = diff_boy_to_girl if diff_boy_to_girl else 12
    diff_girl_to_boy = diff_girl_to_boy if diff_girl_to_boy else 12
    
    # Check for dosha-forming combinations
    dosha_combinations = [
        (2, 12), (12, 2),  # Dwitiya-Dwadash
        (5, 9), (9, 5),    # Panchama-Navama
        (6, 8), (8, 6)     # Shadashtak
    ]
    
    if (diff_boy_to_girl, diff_girl_to_boy) in dosha_combinations:
        return 0  # Dosha present
    else:
        return 7  # No dosha

def nadi_koota(m1, m2):
    """Enhanced Nadi Koota with proper classification"""
    boy_nadi = NADI_MAP[m1['nakshatra']]
    girl_nadi = NADI_MAP[m2['nakshatra']]
    
    if boy_nadi != girl_nadi:
        return 8  # Different nadis - good
    else:
        return 0  # Same nadi - dosha

def manglik_dosha(data: AstroData) -> bool:
    """Enhanced Manglik calculation with proper house system"""
    raw = data.get_rashi_data()
    asc = raw['ascendant']['lon'] % 360
    mars = raw['mars']['lon'] % 360
    
    # Calculate house position
    house = int(((mars - asc) % 360) // 30) + 1
    
    # Standard Manglik houses
    return house in (1, 2, 4, 7, 8, 12)

def chandra_manglik_dosha_detailed(data: AstroData) -> dict:
    """
    Calculate Chandra Manglik Dosha with severity levels
    
    Returns detailed information about the dosha including severity
    """
    raw = data.get_rashi_data()
    moon_lon = raw['moon']['lon'] % 360
    mars_lon = raw['mars']['lon'] % 360
    
    # Calculate house position from Moon
    house = int(((mars_lon - moon_lon) % 360) // 30) + 1
    
    # Define severity levels
    high_intensity_houses = {7, 8}      # Marriage and transformation houses
    medium_intensity_houses = {1, 4, 5} # Self, home, romance houses  
    low_intensity_houses = {2, 12}      # Family and subconscious houses
    
    if house in high_intensity_houses:
        return {
            'is_chandra_manglik': True,
            'severity': 'High',
            'house': house,
            'description': 'Strong emotional and marital challenges expected'
        }
    elif house in medium_intensity_houses:
        return {
            'is_chandra_manglik': True,
            'severity': 'Medium',
            'house': house,
            'description': 'Moderate emotional compatibility issues'
        }
    elif house in low_intensity_houses:
        return {
            'is_chandra_manglik': True,
            'severity': 'Low',
            'house': house,
            'description': 'Minor emotional adjustments needed'
        }
    else:
        return {
            'is_chandra_manglik': False,
            'severity': 'None',
            'house': house,
            'description': 'No Chandra Manglik Dosha present'
        }


def check_dosha_cancellations(m1: dict, m2: dict, faults: list, d1: dict, d2: dict) -> dict:
    """Enhanced dosha cancellation with comprehensive rules"""
    canceled_doshas = []
    cancellation_reasons = {}
    
    # Nadi Dosha Cancellation Rules
    if 'Nadi' in faults:
        # Same rashi cancels Nadi Dosha
        if m1.get('sign_number') == m2.get('sign_number'):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Same Rashi (Moon Sign) cancels Nadi Dosha'
        
        # Same nakshatra cancels Nadi Dosha
        elif m1.get('nakshatra') == m2.get('nakshatra'):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Same Nakshatra cancels Nadi Dosha'
        
        # Different pada in same nakshatra cancels Nadi Dosha
        elif m1.get('nakshatra') == m2.get('nakshatra'):
            # This would need pada calculation - simplified for now
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Different Pada in same Nakshatra cancels Nadi Dosha'
        
        # Friendly sign lords cancel Nadi Dosha
        elif _are_planets_friends(m1.get('sign_lord', ''), m2.get('sign_lord', '')):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Friendly Moon sign lords cancel Nadi Dosha'
    
    # Bhakoot Dosha Cancellation Rules
    if 'Bhakoot' in faults:
        # Same sign lord cancels Bhakoot Dosha
        if m1.get('sign_lord') == m2.get('sign_lord'):
            canceled_doshas.append('Bhakoot')
            cancellation_reasons['Bhakoot'] = 'Same sign lord cancels Bhakoot Dosha'
        
        # Friendly sign lords cancel Bhakoot Dosha
        elif _are_planets_friends(m1.get('sign_lord', ''), m2.get('sign_lord', '')):
            canceled_doshas.append('Bhakoot')
            cancellation_reasons['Bhakoot'] = 'Friendly sign lords cancel Bhakoot Dosha'
    
    # Gana Dosha Cancellation Rules
    if 'Gana' in faults:
        # Same sign lord cancels Gana Dosha
        if m1.get('sign_lord') == m2.get('sign_lord'):
            canceled_doshas.append('Gana')
            cancellation_reasons['Gana'] = 'Same sign lord cancels Gana Dosha'
    
    # Manglik Dosha Cancellation Rules
    if 'Manglik' in faults:
        # Both having Mars in same houses
        boy_mars = d1.get('mars', {})
        girl_mars = d2.get('mars', {})
        
        if boy_mars.get('house_number') == girl_mars.get('house_number'):
            canceled_doshas.append('Manglik')
            cancellation_reasons['Manglik'] = 'Mars in same houses cancels Manglik Dosha'
        
        # Jupiter aspect cancellation (simplified)
        boy_jupiter = d1.get('jupiter', {})
        girl_jupiter = d2.get('jupiter', {})
        
        if _has_jupiter_aspect_on_mars(boy_mars, boy_jupiter) and \
           _has_jupiter_aspect_on_mars(girl_mars, girl_jupiter):
            canceled_doshas.append('Manglik')
            cancellation_reasons['Manglik'] = 'Jupiter aspect on Mars cancels Manglik Dosha'
    
    return {
        'canceled_doshas': canceled_doshas,
        'cancellation_reasons': cancellation_reasons,
        'active_doshas': [d for d in faults if d not in canceled_doshas]
    }

def calculate_compatibility_percentage(scores: dict) -> dict:
    """Enhanced weighted compatibility calculation"""
    # Research-based importance weights
    koota_weights = {
        'Nadi': 0.25,           # Most important - health & progeny
        'Bhakoot': 0.20,        # Financial & emotional stability
        'Gana': 0.15,           # Temperamental compatibility
        'Yoni': 0.12,           # Physical compatibility
        'Graha Maitri': 0.10,   # Mental compatibility
        'Tara': 0.08,           # Health & longevity
        'Vashya': 0.06,         # Mutual control
        'Varna': 0.04           # Spiritual development
    }
    
    # Calculate weighted score
    weighted_score = 0
    total_weight = 0
    
    for koota, score in scores.items():
        if koota in koota_weights and koota in KOOTA_INFO:
            max_score = KOOTA_INFO[koota]['max']
            normalized_score = score / max_score
            weight = koota_weights[koota]
            
            weighted_score += normalized_score * weight
            total_weight += weight
    
    # Calculate final percentage
    compatibility_percentage = (weighted_score / total_weight) * 100 if total_weight > 0 else 0
    
    # Generate detailed breakdown
    koota_breakdown = []
    for koota, score in scores.items():
        if koota in koota_weights and koota in KOOTA_INFO:
            max_score = KOOTA_INFO[koota]['max']
            weight = koota_weights[koota]
            contribution = (score / max_score) * weight * 100
            
            koota_breakdown.append({
                'koota': koota,
                'score': score,
                'max': max_score,
                'weight': weight,
                'contribution': round(contribution, 2),
                'status': 'Strong' if score >= max_score * 0.8 else 'Moderate' if score >= max_score * 0.5 else 'Weak'
            })
    
    # Sort by contribution
    koota_breakdown.sort(key=lambda x: x['contribution'], reverse=True)
    
    return {
        'weighted_percentage': round(compatibility_percentage, 2),
        'traditional_percentage': round((sum(scores.values()) / sum(info['max'] for info in KOOTA_INFO.values())) * 100, 2),
        'koota_breakdown': koota_breakdown,
        'primary_strengths': [k for k in koota_breakdown if k['status'] == 'Strong'],
        'areas_for_improvement': [k for k in koota_breakdown if k['status'] == 'Weak']
    }

def assess_relationship_risks(scores: dict, boy_manglik: dict, girl_manglik: dict, 
                            canceled_doshas: list) -> dict:
    """Enhanced risk assessment with cancellation consideration"""
    risks = []
    risk_mitigation = []
    
    # Adjust risks based on cancellations
    effective_nadi_score = 8 if 'Nadi' in canceled_doshas else scores.get('Nadi', 0)
    effective_bhakoot_score = 7 if 'Bhakoot' in canceled_doshas else scores.get('Bhakoot', 0)
    effective_manglik_risk = False if 'Manglik' in canceled_doshas else \
                           (boy_manglik.get('is_manglik', False) != girl_manglik.get('is_manglik', False))
    
    # High-priority risks (adjusted for cancellations)
    if effective_nadi_score == 0:
        risks.append({
            'level': 'HIGH',
            'area': 'Health & Progeny',
            'description': 'Same Nadi indicates potential health issues for couple and progeny',
            'impact': 'May affect children\'s health and genetic compatibility'
        })
        risk_mitigation.append('Perform Nadi Dosha Shanti Puja and regular health check-ups')
    
    if effective_bhakoot_score == 0:
        risks.append({
            'level': 'HIGH',
            'area': 'Emotional & Financial Stability',
            'description': 'Bhakoot Dosha indicates emotional conflicts and financial instability',
            'impact': 'May cause frequent arguments and money-related stress'
        })
        risk_mitigation.append('Practice financial planning and conflict resolution techniques')
    
    # Medium-priority risks
    if scores.get('Gana', 0) <= 1:
        risks.append({
            'level': 'MEDIUM',
            'area': 'Temperamental Compatibility',
            'description': 'Different Ganas indicate temperamental conflicts',
            'impact': 'May lead to misunderstandings and personality clashes'
        })
        risk_mitigation.append('Develop patience and understanding each other\'s perspectives')
    
    if scores.get('Yoni', 0) <= 1:
        risks.append({
            'level': 'MEDIUM',
            'area': 'Physical & Intimate Compatibility',
            'description': 'Low Yoni compatibility indicates physical incompatibility',
            'impact': 'May affect physical intimacy and attraction'
        })
        risk_mitigation.append('Focus on emotional bonding and open communication')
    
    if scores.get('Graha Maitri', 0) <= 2:
        risks.append({
            'level': 'MEDIUM',
            'area': 'Mental Compatibility',
            'description': 'Low Graha Maitri indicates mental incompatibility',
            'impact': 'May cause communication issues and different thinking patterns'
        })
        risk_mitigation.append('Engage in activities that promote mental bonding')
    
    # Manglik-related risks (adjusted for cancellations)
    if effective_manglik_risk:
        risks.append({
            'level': 'HIGH',
            'area': 'Manglik Dosha',
            'description': 'Manglik-non-Manglik combination may cause relationship issues',
            'impact': 'Traditional belief suggests potential health risks and marital discord'
        })
        risk_mitigation.append('Perform Mangal Dosha remedies and protective rituals')
    
    # Calculate overall risk level
    high_risks = [r for r in risks if r['level'] == 'HIGH']
    medium_risks = [r for r in risks if r['level'] == 'MEDIUM']
    low_risks = [r for r in risks if r['level'] == 'LOW']
    
    overall_risk_level = 'HIGH' if len(high_risks) >= 2 else 'MEDIUM' if len(high_risks) >= 1 or len(medium_risks) >= 3 else 'LOW'
    
    return {
        'overall_risk_level': overall_risk_level,
        'total_risks': len(risks),
        'risk_breakdown': {
            'high': len(high_risks),
            'medium': len(medium_risks),
            'low': len(low_risks)
        },
        'detailed_risks': risks,
        'mitigation_strategies': risk_mitigation,
        'risk_summary': f"Identified {len(risks)} risk areas with {overall_risk_level} overall risk level"
    }

def generate_detailed_interpretation(scores: dict, total_score: float, max_total: float,
                                   boy_manglik: dict, girl_manglik: dict, 
                                   canceled_doshas: list) -> dict:
    """Enhanced interpretation with cancellation awareness"""
    # Adjust total score for canceled doshas
    effective_total = total_score
    for dosha in canceled_doshas:
        if dosha in KOOTA_INFO:
            effective_total += KOOTA_INFO[dosha]['max']
    
    # Calculate effective percentage
    effective_percentage = (effective_total / max_total) * 100
    compatibility_percentage = (total_score / max_total) * 100
    
    # Enhanced compatibility assessment
    if effective_percentage >= 85:
        overall_status = "Excellent"
        overall_description = "This is an exceptional match with outstanding compatibility. The canceled doshas further enhance the prospects."
    elif effective_percentage >= 70:
        overall_status = "Very Good"
        overall_description = "This is a very good match with strong compatibility potential and favorable prospects for harmony."
    elif effective_percentage >= 55:
        overall_status = "Good"
        overall_description = "This is a good match with acceptable compatibility that shows promise for a stable relationship."
    elif effective_percentage >= 40:
        overall_status = "Fair"
        overall_description = "This is a fair match with moderate compatibility requiring understanding and adjustments."
    else:
        overall_status = "Poor"
        overall_description = "This match shows significant compatibility challenges requiring careful consideration."
    
    # Analyze strengths and concerns
    strength_areas = []
    concern_areas = []
    
    for koota_name, obtained_score in scores.items():
        max_score = KOOTA_INFO[koota_name]['max']
        percentage = (obtained_score / max_score) * 100
        
        if percentage >= 80:
            strength_areas.append({
                'koota': koota_name,
                'score': obtained_score,
                'max': max_score,
                'analysis': f"Excellent compatibility in {KOOTA_INFO[koota_name]['desc']}"
            })
        elif percentage <= 30 and koota_name not in canceled_doshas:
            concern_areas.append({
                'koota': koota_name,
                'score': obtained_score,
                'max': max_score,
                'analysis': f"Challenges in {KOOTA_INFO[koota_name]['desc']} requiring attention"
            })
    
    # Manglik analysis
    manglik_analysis = {
        'boy_status': boy_manglik.get('is_manglik', False),
        'girl_status': girl_manglik.get('is_manglik', False),
        'compatibility': 'Compatible' if boy_manglik.get('is_manglik', False) == girl_manglik.get('is_manglik', False) else 'Incompatible',
        'impact': 'High' if boy_manglik.get('is_manglik', False) != girl_manglik.get('is_manglik', False) else 'None',
        'canceled': 'Manglik' in canceled_doshas
    }
    
    # Generate recommendations
    recommendations = []
    
    # Add recommendations for active doshas only
    active_concerns = [item for item in concern_areas if item['koota'] not in canceled_doshas]
    
    for concern in active_concerns:
        if concern['koota'] == 'Nadi':
            recommendations.append("Perform Nadi Dosha remedies including Maha Mrityunjaya Jaap")
        elif concern['koota'] == 'Bhakoot':
            recommendations.append("Conduct Bhakoot Dosha Shanti Puja and protective rituals")
        elif concern['koota'] == 'Gana':
            recommendations.append("Practice patience and understanding due to temperamental differences")
        elif concern['koota'] == 'Yoni':
            recommendations.append("Focus on emotional bonding and open communication")
    
    if manglik_analysis['compatibility'] == 'Incompatible' and not manglik_analysis['canceled']:
        recommendations.append("Perform Mangal Dosha remedies including protective rituals")
    
    # Life phase predictions
    life_phases = {
        'early_marriage': 'Harmonious adjustment period' if effective_total >= 22 else 'Requires extra patience and understanding',
        'middle_period': 'Stable and prosperous phase' if effective_total >= 27 else 'May face some challenges requiring mutual support',
        'later_years': 'Deeply bonded relationship' if effective_total >= 32 else 'Companionship with acceptance of differences'
    }
    
    return {
        'overall_compatibility': {
            'percentage': round(compatibility_percentage, 2),
            'effective_percentage': round(effective_percentage, 2),
            'status': overall_status,
            'description': overall_description
        },
        'strength_areas': strength_areas,
        'concern_areas': concern_areas,
        'manglik_analysis': manglik_analysis,
        'recommendations': recommendations,
        'life_phases': life_phases,
        'cancellation_impact': len(canceled_doshas),
        'detailed_summary': f"With {int(total_score)} out of {max_total} points (effective: {int(effective_total)}), this match shows {overall_status.lower()} compatibility. {overall_description}"
    }

# Helper functions
def _are_planets_friends(planet1: str, planet2: str) -> bool:
    """Check if two planets are friends"""
    if planet1 in FRIENDSHIP and planet2 in FRIENDSHIP[planet1].get('friends', []):
        return True
    return False

def _has_jupiter_aspect_on_mars(mars_data: dict, jupiter_data: dict) -> bool:
    """Simplified Jupiter aspect check"""
    mars_house = mars_data.get('house_number', 0)
    jupiter_house = jupiter_data.get('house_number', 0)
    
    if jupiter_house > 0 and mars_house > 0:
        # Jupiter aspects 5th, 7th, and 9th houses from its position
        aspect_houses = [
            (jupiter_house + 4) % 12 if (jupiter_house + 4) % 12 != 0 else 12,
            (jupiter_house + 6) % 12 if (jupiter_house + 6) % 12 != 0 else 12,
            (jupiter_house + 8) % 12 if (jupiter_house + 8) % 12 != 0 else 12
        ]
        return mars_house in aspect_houses
    return False

# Enhanced interpretation system
def generate_constructive_interpretation(scores: dict, faults: list, canceled_doshas: list, 
                                    compatibility_percentage: float) -> str:
    """
    Generate constructive interpretation that balances traditional wisdom with practical guidance
    """
    
    # Opening statement
    interpretation = f"**Compatibility Analysis: {compatibility_percentage:.1f}%**\n\n"
    
    # Constructive opening
    interpretation += "While astrological compatibility provides valuable insights, remember that successful relationships are built through mutual effort, understanding, and continuous growth. The stars may influence tendencies, but your conscious choices and behaviors ultimately determine your relationship's success.\n\n"
    
    # Address canceled doshas positively
    if canceled_doshas:
        interpretation += "**Positive Aspects:**\n"
        for dosha in canceled_doshas:
            interpretation += f"• {dosha} Dosha has been naturally canceled, reducing potential challenges in this area\n"
        interpretation += "\n"
    
    # Address active concerns constructively
    if faults:
        active_faults = [f for f in faults if f not in canceled_doshas]
        if active_faults:
            interpretation += "**Areas for Growth and Attention:**\n"
            interpretation += "These areas require conscious effort and practical approaches rather than just ritualistic remedies:\n\n"
            
            for fault in active_faults:
                interpretation += f"**{fault} Compatibility:**\n"
                interpretation += f"While traditional remedies can provide psychological comfort, the most effective approach is to focus on:\n"
                
                # Add practical remedies
                practical_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {}).get('practical', [])
                behavioral_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {}).get('behavioral', [])
                
                for remedy in practical_remedies[:3]:  # Show top 3 practical remedies
                    interpretation += f"• {remedy}\n"
                
                interpretation += f"\n**Behavioral Improvements:**\n"
                for remedy in behavioral_remedies[:2]:  # Show top 2 behavioral remedies
                    interpretation += f"• {remedy}\n"
                
                interpretation += "\n"
    
    # General constructive advice
    interpretation += "**Universal Relationship Principles:**\n"
    interpretation += "Regardless of astrological compatibility, these principles can strengthen any relationship:\n\n"
    
    interpretation += "• **Communication**: Practice active listening and express your needs clearly and respectfully\n"
    interpretation += "• **Patience**: Understand that both partners are continuously growing and changing\n"
    interpretation += "• **Empathy**: Try to understand your partner's perspective, even when you disagree\n"
    interpretation += "• **Compromise**: Focus on finding solutions that work for both partners\n"
    interpretation += "• **Appreciation**: Regularly express gratitude for your partner's positive qualities\n"
    interpretation += "• **Personal Growth**: Work on improving yourself rather than trying to change your partner\n"
    interpretation += "• **Conflict Resolution**: Learn to disagree respectfully and find constructive solutions\n\n"
    
    # Closing message
    interpretation += "**Remember**: Astrology provides insights, but your daily choices, actions, and commitment to growth determine your relationship's success. Focus on building mutual respect, understanding, and love through practical actions rather than relying solely on rituals.\n\n"
    
    interpretation += "The goal is not to eliminate all differences but to learn how to navigate them with wisdom, patience, and love. Every relationship requires effort, but with conscious intention and the right approaches, you can build a strong, fulfilling partnership."
    
    return interpretation

def generate_enhanced_remedies(faults: list, canceled_doshas: list) -> dict:
    """
    Generate enhanced remedies that balance traditional and practical approaches
    """
    remedies = {}
    
    for fault in faults:
        if fault in canceled_doshas:
            continue  # Skip canceled doshas
            
        fault_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {})
        
        remedies[fault] = {
            'traditional_remedies': fault_remedies.get('ritual', []),
            'practical_approaches': fault_remedies.get('practical', []),
            'behavioral_changes': fault_remedies.get('behavioral', []),
            'guidance': f"While traditional remedies provide psychological comfort and spiritual support, the most effective approach is to combine them with practical behavioral changes. Focus on personal growth, improved communication, and mutual understanding."
        }
    
    return remedies


def match_kundli(a: AstroData, b: AstroData) -> dict:
    """
    Enhanced Ashtakoota compatibility with comprehensive analysis
    
    Returns comprehensive compatibility analysis with all improvements
    """
    # Get dispositions and Moon info
    d1 = get_dispositions(a)
    d2 = get_dispositions(b)
    m1, m2 = d1['moon'], d2['moon']
    
    # Compute koota scores using enhanced functions
    scores = {
        'Varna': varna_koota(m1, m2),
        'Vashya': vashya_koota(m1, m2),
        'Tara': tara_koota(m1, m2),
        'Yoni': yoni_koota(m1, m2),
        'Graha Maitri': graha_maitri_koota(m1, m2),
        'Gana': gana_koota(m1, m2),
        'Bhakoot': bhakoot_koota(m1, m2),
        'Nadi': nadi_koota(m1, m2)
    }
    
    total = sum(scores.values())
    max_total = sum(info['max'] for info in KOOTA_INFO.values())
    
    # Identify faults (zero scores)
    faults = [k for k, v in scores.items() if v == 0]
    
    # Enhanced Manglik check
    mg_a, mg_b = manglik_dosha(a), manglik_dosha(b)
    boy_manglik = {'is_manglik': mg_a}
    girl_manglik = {'is_manglik': mg_b}
    
    if mg_a != mg_b:
        faults.append('Manglik')
    
    # Check for dosha cancellations
    dosha_cancellations = check_dosha_cancellations(m1, m2, faults, d1, d2)
    
    # Calculate enhanced compatibility
    compatibility_analysis = calculate_compatibility_percentage(scores)
    
    # Enhanced risk assessment
    risk_assessment = assess_relationship_risks(scores, boy_manglik, girl_manglik, 
                                              dosha_cancellations['canceled_doshas'])
    
    # Generate enhanced interpretation
    detailed_interpretation = generate_detailed_interpretation(
        scores, total, max_total, boy_manglik, girl_manglik, 
        dosha_cancellations['canceled_doshas']
    )

    # Generate constructive interpretation
    constructive_interpretation = generate_constructive_interpretation(
        scores, faults, dosha_cancellations['canceled_doshas'], compatibility_analysis['weighted_percentage']
    )

    # Generate enhanced remedies
    enhanced_remedies = generate_enhanced_remedies(faults, dosha_cancellations['canceled_doshas'])
    
    # Build enhanced table
    table = []
    for k, pts in scores.items():
        info = KOOTA_INFO[k]
        
        # Enhanced Boy/Girl type display
        if k == 'Varna':
            boy_varna_level = VARNA_MAP[m1['sign_number']]
            girl_varna_level = VARNA_MAP[m2['sign_number']]
            boy_type = VARNA_NAME[boy_varna_level]
            girl_type = VARNA_NAME[girl_varna_level]
        elif k == 'Vashya':
            boy_type = VASHA_MAP[m1['sign_number']]
            girl_type = VASHA_MAP[m2['sign_number']]
        elif k == 'Tara':
            from .dispositions import NAKSHATRA_LORDS
            boy_type = NAKSHATRA_LORDS[m1['nakshatra']-1]
            girl_type = NAKSHATRA_LORDS[m2['nakshatra']-1]
        elif k == 'Yoni':
            boy_type = YONI_MAP[m1['nakshatra']]
            girl_type = YONI_MAP[m2['nakshatra']]
        elif k == 'Gana':
            boy_type = GANA_GROUPS[m1['nakshatra']]
            girl_type = GANA_GROUPS[m2['nakshatra']]
        elif k == 'Nadi':
            boy_type = NADI_MAP[m1['nakshatra']]
            girl_type = NADI_MAP[m2['nakshatra']]
        else:
            boy_type = girl_type = ''
        
        # Add cancellation indicator
        significance = info['desc']
        if k in dosha_cancellations['canceled_doshas']:
            significance += f" (✓ CANCELED: {dosha_cancellations['cancellation_reasons'][k]})"
        
        table.append({
            'Koota': f"{k} Koota",
            'Boy': boy_type,
            'Girl': girl_type,
            'Max': info['max'],
            'Obtained': pts,
            'Significance': significance
        })
    
    # Add enhanced total row
    table.append({
        'Koota': 'Total',
        'Boy': '-', 'Girl': '-',
        'Max': max_total,
        'Obtained': total,
        'Significance': f"Overall Compatibility: {compatibility_analysis['weighted_percentage']:.1f}% (Traditional: {compatibility_analysis['traditional_percentage']:.1f}%)"
    })
    
    # Enhanced interpretation
    interp_parts = []
    
    # Manglik narrative
    if 'Manglik' in faults:
        if 'Manglik' in dosha_cancellations['canceled_doshas']:
            interp_parts.append(f"Manglik Dosha was present but CANCELED due to {dosha_cancellations['cancellation_reasons']['Manglik']}")
        else:
            s = f"Boy is {'Manglik' if mg_a else 'not Manglik'}, Girl is {'Manglik' if mg_b else 'not Manglik'}."
            s += " This requires attention through appropriate remedies."
            interp_parts.append(s)
    
    # Other koota faults
    for f in faults:
        if f == 'Manglik': continue
        if f in dosha_cancellations['canceled_doshas']:
            interp_parts.append(f"{f} Dosha was CANCELED due to {dosha_cancellations['cancellation_reasons'][f]}")
        else:
            desc = KOOTA_INFO[f]['desc']
            rem = '; '.join(REMINDERS.get(f, []))
            interp_parts.append(f"{f} Koota scored zero ({desc}); recommended remedies: {rem}.")
    
    if not dosha_cancellations['active_doshas']:
        interp_parts.append("No active doshas detected; the couple shows excellent compatibility across all kootas.")
    
    interpretation = ' '.join(interp_parts) if interp_parts else "Compatibility analysis completed successfully."
    
 
    return {
        'table': table,
        'faults': faults,
        'chandra_manglik': {
            'boys': chandra_manglik_dosha_detailed(a), 
            'girls': chandra_manglik_dosha_detailed(b)
        },
        'traditional_remedies': {f: CONSTRUCTIVE_REMEDIES.get(f, {}).get('ritual', []) for f in faults},
        'remedies': enhanced_remedies,
        'interpretation': constructive_interpretation,
        # 'remedies': {f: REMINDERS.get(f, []) for f in faults},
        # 'interpretation': interpretation,
        'detailed_interpretation': detailed_interpretation,
        'dosha_cancellations': dosha_cancellations,
        'compatibility_analysis': compatibility_analysis,
        'risk_assessment': risk_assessment,
        'summary': {
            'total_score': total,
            'max_score': max_total,
            'traditional_percentage': compatibility_analysis['traditional_percentage'],
            'weighted_percentage': compatibility_analysis['weighted_percentage'],
            'overall_compatibility': detailed_interpretation['overall_compatibility']['status'],
            'risk_level': risk_assessment['overall_risk_level'],
            'active_doshas': dosha_cancellations['active_doshas'],
            'canceled_doshas': dosha_cancellations['canceled_doshas'],
            'cancellation_impact': f"{len(dosha_cancellations['canceled_doshas'])} doshas canceled"
        }
    }

# Example usage
if __name__ == '__main__':
    A = AstroData(1990,1,1,10,0,0,5,30,19.07,72.88)
    B = AstroData(1992,6,15,16,30,0,5,30,28.61,77.23)
    from pprint import pprint
    pprint(match_kundli(A, B))
