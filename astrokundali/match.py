"""
astrokundali/match.py

Secular Ashtakoota (Guna Milan) marriage matching module.
Features:
- Secular approach without religious remedies
- Angshik & Purna Manglik dosha classification
- Chandra Manglik Dosha with severity levels
- Complete 14-animal Yoni compatibility matrix
- Enhanced Graha Maitri scoring (0, 0.5, 1, 3, 4, 5)
- Advanced dosha cancellation rules
- Weighted compatibility & risk assessment
- Behavioral and practical remedies only
- Constructive interpretations based on psychology
"""

import json
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from .astro_data import AstroData
from .dispositions import get_dispositions

# Load secular constructive remedies from JSON
def load_constructive_remedies():
    """Load secular constructive remedies from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'cons_rem_marriage.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: cons_rem_marriage.json not found. Using default remedies.")
        return {}

CONSTRUCTIVE_REMEDIES = load_constructive_remedies()

# Enhanced mappings with complete data
VARNA_MAP = {1:3, 2:2, 3:1, 4:3, 5:4, 6:2, 7:1, 8:3, 9:4, 10:2, 11:1, 12:4}
VARNA_NAME = {1:'Brahmin', 2:'Kshatriya', 3:'Vaishya', 4:'Shudra'}

VASHA_MAP = {
    1:'Chatushpada', 2:'Manav', 3:'Jalachara', 4:'Jalachara',
    5:'Chatushpada', 6:'Manav', 7:'Manav', 8:'Vanachara',
    9:'Manav', 10:'Chatushpada', 11:'Chatushpada', 12:'Jalachara'
}

# Complete Gana groups mapping
GANA_GROUPS = {
    1:'Deva', 5:'Deva', 7:'Deva', 8:'Deva', 13:'Deva', 15:'Deva', 
    17:'Deva', 22:'Deva', 27:'Deva',
    2:'Manushya', 4:'Manushya', 6:'Manushya', 12:'Manushya', 20:'Manushya', 
    21:'Manushya', 25:'Manushya', 26:'Manushya',
    3:'Rakshasa', 9:'Rakshasa', 10:'Rakshasa', 11:'Rakshasa', 14:'Rakshasa', 
    16:'Rakshasa', 18:'Rakshasa', 19:'Rakshasa', 23:'Rakshasa', 24:'Rakshasa'
}

# Complete 14-animal Yoni mapping
YONI_MAP = {
    1:'Horse', 2:'Elephant', 3:'Sheep', 4:'Snake', 5:'Snake', 6:'Dog',
    7:'Cat', 8:'Sheep', 9:'Cat', 10:'Rat', 11:'Rat', 12:'Cow', 
    13:'Buffalo', 14:'Tiger', 15:'Buffalo', 16:'Tiger', 17:'Deer', 18:'Deer',
    19:'Dog', 20:'Monkey', 21:'Mongoose', 22:'Monkey', 23:'Lion', 24:'Horse',
    25:'Lion', 26:'Cow', 27:'Elephant'
}

# Enhanced Nadi mapping
NADI_MAP = {
    1:'Adi', 6:'Adi', 7:'Adi', 12:'Adi', 13:'Adi', 18:'Adi', 19:'Adi', 24:'Adi', 25:'Adi',
    2:'Madhya', 5:'Madhya', 8:'Madhya', 11:'Madhya', 14:'Madhya', 17:'Madhya', 20:'Madhya', 23:'Madhya', 26:'Madhya',
    3:'Antya', 4:'Antya', 9:'Antya', 10:'Antya', 15:'Antya', 16:'Antya', 21:'Antya', 22:'Antya', 27:'Antya'
}

# Enhanced Koota information
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

# Secular remedies (no religious content)
REMEDIES = {
    'Varna': [
        'Practice mutual respect for different social backgrounds',
        'Engage in educational activities together',
        'Focus on personal character development'
    ],
    'Vashya': [
        'Develop balanced decision-making skills',
        'Practice healthy communication techniques',
        'Learn conflict resolution strategies'
    ],
    'Tara': [
        'Maintain healthy lifestyle habits together',
        'Practice stress management techniques',
        'Focus on preventive healthcare'
    ],
    'Yoni': [
        'Improve emotional and physical communication',
        'Practice patience and understanding',
        'Focus on emotional bonding activities'
    ],
    'Gana': [
        'Learn anger management techniques',
        'Practice empathy and understanding',
        'Develop conflict de-escalation skills'
    ],
    'Bhakoot': [
        'Practice transparent financial communication',
        'Develop emotional regulation skills',
        'Focus on partnership building'
    ],
    'Graha Maitri': [
        'Practice active listening skills',
        'Develop emotional intelligence',
        'Create shared interests and activities'
    ],
    'Nadi': [
        'Focus on healthy lifestyle practices',
        'Maintain open health communication',
        'Seek proper medical guidance when needed'
    ],
    'Manglik': [
        'Practice anger management techniques',
        'Learn constructive conflict resolution',
        'Focus on patience and understanding'
    ]
}

# Planetary friendship matrix
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

@dataclass
class MatchResult:
    """Data class for match result"""
    koota_name: str
    boy_type: str
    girl_type: str
    obtained: float
    maximum: float
    significance: str

def varna_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Varna Koota (Max: 1)"""
    boy_varna = VARNA_MAP[m1['sign_number']]
    girl_varna = VARNA_MAP[m2['sign_number']]
    
    # Boy's varna should be equal or higher than girl's
    return 1 if boy_varna >= girl_varna else 0

def vashya_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Vashya Koota (Max: 2) with enhanced scoring"""
    vashya_scores = {
        # Same group = 2 points
        ("Chatushpada", "Chatushpada"): 2,
        ("Manav", "Manav"): 2,
        ("Jalachara", "Jalachara"): 2,
        ("Vanachara", "Vanachara"): 2,
        
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

def tara_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Tara Koota (Max: 3) - CORRECTED VERSION"""
    n1, n2 = m1['nakshatra'], m2['nakshatra']
    
    # Calculate remainders
    r1 = (n2 - n1) % 9
    r2 = (n1 - n2) % 9
    
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

def yoni_koota(m1: Dict, m2: Dict) -> float:
    """Complete 14-animal Yoni compatibility matrix"""
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
        
        # Neutral yonis = 2 points
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
    
    return yoni_scores.get((boy_yoni, girl_yoni), 2)

def graha_maitri_koota(m1: Dict, m2: Dict) -> float:
    """Enhanced Graha Maitri with complete scoring (0, 0.5, 1, 3, 4, 5)"""
    boy_lord = m1['sign_lord']
    girl_lord = m2['sign_lord']
    
    if boy_lord == girl_lord:
        return 5
    
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

def gana_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Gana Koota (Max: 6)"""
    boy_gana = GANA_GROUPS[m1['nakshatra']]
    girl_gana = GANA_GROUPS[m2['nakshatra']]
    
    if boy_gana == girl_gana:
        return 6
    elif (boy_gana == "Deva" and girl_gana == "Manushya") or \
         (boy_gana == "Manushya" and girl_gana == "Deva"):
        return 5
    elif (boy_gana == "Manushya" and girl_gana == "Rakshasa") or \
         (boy_gana == "Rakshasa" and girl_gana == "Manushya"):
        return 1
    else:  # Deva-Rakshasa
        return 0

def bhakoot_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Bhakoot Koota (Max: 7)"""
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
        return 0
    else:
        return 7

def nadi_koota(m1: Dict, m2: Dict) -> float:
    """Calculate Nadi Koota (Max: 8)"""
    boy_nadi = NADI_MAP[m1['nakshatra']]
    girl_nadi = NADI_MAP[m2['nakshatra']]
    
    if boy_nadi != girl_nadi:
        return 8
    else:
        return 0

def manglik_dosha(data: AstroData) -> str:
    """
    Enhanced Manglik classification
    Returns: 'None', 'Anshik' (partial), or 'Purna' (complete)
    """
    raw = data.get_rashi_data()
    asc = raw['ascendant']['lon'] % 360
    mars = raw['mars']['lon'] % 360
    house = int(((mars - asc) % 360) // 30) + 1
    
    if house in {7, 8}:
        return 'Purna'   # Complete Manglik
    elif house in {1, 2, 4, 12}:
        return 'Anshik'  # Partial Manglik
    else:
        return 'None'    # Non-Manglik

def chandra_manglik_dosha_detailed(data: AstroData) -> Dict[str, Any]:
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

def check_dosha_cancellations(m1: Dict, m2: Dict, faults: List[str], d1: Dict, d2: Dict) -> Dict:
    """Enhanced dosha cancellation with comprehensive rules"""
    canceled_doshas = []
    cancellation_reasons = {}
    
    # Nadi Dosha Cancellation Rules
    if 'Nadi' in faults:
        if m1.get('sign_number') == m2.get('sign_number'):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Same Rashi (Moon Sign) cancels Nadi Dosha'
        elif m1.get('nakshatra') == m2.get('nakshatra'):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Same Nakshatra cancels Nadi Dosha'
        elif _are_planets_friends(m1.get('sign_lord', ''), m2.get('sign_lord', '')):
            canceled_doshas.append('Nadi')
            cancellation_reasons['Nadi'] = 'Friendly Moon sign lords cancel Nadi Dosha'
    
    # Bhakoot Dosha Cancellation Rules
    if 'Bhakoot' in faults:
        if m1.get('sign_lord') == m2.get('sign_lord'):
            canceled_doshas.append('Bhakoot')
            cancellation_reasons['Bhakoot'] = 'Same sign lord cancels Bhakoot Dosha'
        elif _are_planets_friends(m1.get('sign_lord', ''), m2.get('sign_lord', '')):
            canceled_doshas.append('Bhakoot')
            cancellation_reasons['Bhakoot'] = 'Friendly sign lords cancel Bhakoot Dosha'
    
    # Gana Dosha Cancellation Rules
    if 'Gana' in faults:
        if m1.get('sign_lord') == m2.get('sign_lord'):
            canceled_doshas.append('Gana')
            cancellation_reasons['Gana'] = 'Same sign lord cancels Gana Dosha'
    
    return {
        'canceled_doshas': canceled_doshas,
        'cancellation_reasons': cancellation_reasons,
        'active_doshas': [d for d in faults if d not in canceled_doshas]
    }

def calculate_compatibility_percentage(scores: Dict) -> Dict:
    """Enhanced weighted compatibility calculation"""
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
    
    weighted_score = 0
    total_weight = 0
    
    for koota, score in scores.items():
        if koota in koota_weights and koota in KOOTA_INFO:
            max_score = KOOTA_INFO[koota]['max']
            normalized_score = score / max_score
            weight = koota_weights[koota]
            weighted_score += normalized_score * weight
            total_weight += weight
    
    compatibility_percentage = (weighted_score / total_weight) * 100 if total_weight > 0 else 0
    
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
    
    koota_breakdown.sort(key=lambda x: x['contribution'], reverse=True)
    
    return {
        'weighted_percentage': round(compatibility_percentage, 2),
        'traditional_percentage': round((sum(scores.values()) / sum(info['max'] for info in KOOTA_INFO.values())) * 100, 2),
        'koota_breakdown': koota_breakdown,
        'primary_strengths': [k for k in koota_breakdown if k['status'] == 'Strong'],
        'areas_for_improvement': [k for k in koota_breakdown if k['status'] == 'Weak']
    }

def assess_relationship_risks(scores: Dict, boy_manglik: Dict, girl_manglik: Dict, canceled_doshas: List) -> Dict:
    """Enhanced risk assessment with cancellation consideration"""
    risks = []
    risk_mitigation = []
    
    # Adjust risks based on cancellations
    effective_nadi_score = 8 if 'Nadi' in canceled_doshas else scores.get('Nadi', 0)
    effective_bhakoot_score = 7 if 'Bhakoot' in canceled_doshas else scores.get('Bhakoot', 0)
    effective_manglik_risk = False if 'Manglik' in canceled_doshas else \
                           (boy_manglik.get('is_manglik', False) != girl_manglik.get('is_manglik', False))
    
    # High-priority risks
    if effective_nadi_score == 0:
        risks.append({
            'level': 'HIGH',
            'area': 'Health & Progeny',
            'description': 'Same Nadi indicates potential health compatibility issues',
            'impact': 'May affect health harmony and genetic compatibility'
        })
        risk_mitigation.append('Focus on healthy lifestyle practices and open health communication')
    
    if effective_bhakoot_score == 0:
        risks.append({
            'level': 'HIGH',
            'area': 'Emotional & Financial Stability',
            'description': 'Bhakoot Dosha indicates emotional and financial challenges',
            'impact': 'May cause disagreements and financial stress'
        })
        risk_mitigation.append('Practice financial planning and emotional regulation techniques')
    
    # Medium-priority risks
    if scores.get('Gana', 0) <= 1:
        risks.append({
            'level': 'MEDIUM',
            'area': 'Temperamental Compatibility',
            'description': 'Different temperaments may cause conflicts',
            'impact': 'May lead to misunderstandings and personality clashes'
        })
        risk_mitigation.append('Develop patience and understanding of different perspectives')
    
    if scores.get('Yoni', 0) <= 1:
        risks.append({
            'level': 'MEDIUM',
            'area': 'Physical & Intimate Compatibility',
            'description': 'Low physical compatibility indicators',
            'impact': 'May affect physical intimacy and attraction'
        })
        risk_mitigation.append('Focus on emotional bonding and open communication')
    
    # Manglik-related risks
    if effective_manglik_risk:
        risks.append({
            'level': 'HIGH',
            'area': 'Manglik Dosha',
            'description': 'Different Manglik status may cause relationship challenges',
            'impact': 'May lead to conflicts and misunderstandings'
        })
        risk_mitigation.append('Practice anger management and conflict resolution techniques')
    
    # Calculate overall risk level
    high_risks = [r for r in risks if r['level'] == 'HIGH']
    medium_risks = [r for r in risks if r['level'] == 'MEDIUM']
    
    overall_risk_level = 'HIGH' if len(high_risks) >= 2 else 'MEDIUM' if len(high_risks) >= 1 or len(medium_risks) >= 3 else 'LOW'
    
    return {
        'overall_risk_level': overall_risk_level,
        'total_risks': len(risks),
        'risk_breakdown': {
            'high': len(high_risks),
            'medium': len(medium_risks),
            'low': 0
        },
        'detailed_risks': risks,
        'mitigation_strategies': risk_mitigation,
        'risk_summary': f"Identified {len(risks)} risk areas with {overall_risk_level} overall risk level"
    }

def generate_detailed_interpretation(scores: Dict, total_score: float, max_total: float,
                                   boy_manglik: Dict, girl_manglik: Dict, 
                                   canceled_doshas: List) -> Dict:
    """Enhanced interpretation with cancellation awareness"""
    effective_total = total_score
    for dosha in canceled_doshas:
        if dosha in KOOTA_INFO:
            effective_total += KOOTA_INFO[dosha]['max']
    
    effective_percentage = (effective_total / max_total) * 100
    compatibility_percentage = (total_score / max_total) * 100
    
    # Enhanced compatibility assessment
    if effective_percentage >= 85:
        overall_status = "Excellent"
        overall_description = "This is an exceptional match with outstanding compatibility. The canceled doshas further enhance the prospects."
    elif effective_percentage >= 70:
        overall_status = "Very Good"
        overall_description = "This is a very good match with strong compatibility potential and favorable prospects."
    elif effective_percentage >= 55:
        overall_status = "Good"
        overall_description = "This is a good match with acceptable compatibility showing promise for stability."
    elif effective_percentage >= 40:
        overall_status = "Fair"
        overall_description = "This is a fair match with moderate compatibility requiring understanding."
    else:
        overall_status = "Poor"
        overall_description = "This match shows significant compatibility challenges requiring consideration."
    
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
    
    return {
        'overall_compatibility': {
            'percentage': round(compatibility_percentage, 2),
            'effective_percentage': round(effective_percentage, 2),
            'status': overall_status,
            'description': overall_description
        },
        'strength_areas': strength_areas,
        'concern_areas': concern_areas,
        'recommendations': [],
        'cancellation_impact': len(canceled_doshas),
        'detailed_summary': f"With {int(total_score)} out of {max_total} points (effective: {int(effective_total)}), this match shows {overall_status.lower()} compatibility. {overall_description}"
    }

def generate_constructive_interpretation(scores: Dict, faults: List, canceled_doshas: List,
                                       compatibility_percentage: float) -> str:
    """Generate secular interpretation focusing on behavioral and practical guidance"""
    
    interpretation = f"**Compatibility Analysis: {compatibility_percentage:.1f}%**\n\n"
    
    interpretation += "**Author's Secular Approach:** This analysis is based on traditional astrological principles but focuses entirely on practical behavioral insights. The author believes that successful relationships are built through conscious effort, understanding, and personal development rather than religious rituals. These recommendations are grounded in psychology and relationship science.\n\n"
    
    interpretation += "**Evidence-Based Compatibility Assessment:**\n"
    interpretation += "While astrological patterns may indicate certain tendencies, your conscious choices, behaviors, and commitment to growth are what truly determine your relationship's success. This analysis provides insights into potential areas of harmony and challenge, offering practical tools for building a strong partnership.\n\n"
    
    # Address canceled doshas positively
    if canceled_doshas:
        interpretation += "**Positive Aspects:**\n"
        for dosha in canceled_doshas:
            interpretation += f"• {dosha} challenges have been naturally neutralized, reducing potential difficulties\n"
        interpretation += "\n"
    
    # Address active concerns constructively
    if faults:
        active_faults = [f for f in faults if f not in canceled_doshas]
        if active_faults:
            interpretation += "**Areas for Personal Growth:**\n"
            interpretation += "These areas require conscious effort and practical behavioral changes:\n\n"
            
            for fault in active_faults:
                interpretation += f"**{fault} Compatibility:**\n"
                interpretation += f"Focus on developing these practical skills:\n"
                
                # Add practical remedies from JSON
                practical_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {}).get('practical', [])
                behavioral_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {}).get('behavioral', [])
                
                for remedy in practical_remedies[:3]:
                    interpretation += f"• {remedy}\n"
                
                interpretation += f"\n**Behavioral Development:**\n"
                for remedy in behavioral_remedies[:2]:
                    interpretation += f"• {remedy}\n"
                interpretation += "\n"
    
    # Universal relationship principles
    interpretation += "**Evidence-Based Relationship Principles:**\n"
    interpretation += "Research in psychology shows these principles strengthen relationships:\n\n"
    
    interpretation += "• **Communication Skills**: Practice active listening and clear expression\n"
    interpretation += "• **Emotional Intelligence**: Develop self-awareness and empathy\n"
    interpretation += "• **Conflict Resolution**: Learn to disagree constructively\n"
    interpretation += "• **Personal Growth**: Focus on self-improvement rather than changing partner\n"
    interpretation += "• **Shared Activities**: Engage in meaningful activities together\n"
    interpretation += "• **Patience & Understanding**: Accept that growth takes time\n"
    interpretation += "• **Appreciation**: Regularly express gratitude for positive qualities\n\n"
    
    interpretation += "**Remember**: Your relationship success depends on your daily choices, communication skills, and commitment to mutual growth. Use these insights as a guide for personal development and building a strong, respectful partnership based on understanding and shared values."
    
    return interpretation

def generate_enhanced_remedies(faults: List, canceled_doshas: List) -> Dict:
    """Generate enhanced secular remedies"""
    remedies = {}
    
    for fault in faults:
        if fault in canceled_doshas:
            continue
            
        fault_remedies = CONSTRUCTIVE_REMEDIES.get(fault, {})
        
        remedies[fault] = {
            'practical_approaches': fault_remedies.get('practical', []),
            'behavioral_changes': fault_remedies.get('behavioral', []),
            'physical_activities': fault_remedies.get('physical_activities', []),
            'guidance': f"Focus on practical behavioral changes and personal development. The most effective approach combines self-awareness with consistent effort to improve communication and understanding."
        }
    
    return remedies

# Helper functions
def _are_planets_friends(planet1: str, planet2: str) -> bool:
    """Check if two planets are friends"""
    if planet1 in FRIENDSHIP and planet2 in FRIENDSHIP[planet1].get('friends', []):
        return True
    return False

def format_remedy_text(remedy_list: List[str]) -> List[str]:
    """Ensure all remedies are properly formatted sentences"""
    formatted = []
    for remedy in remedy_list:
        # Ensure it ends with a period
        if not remedy.endswith('.'):
            remedy += '.'
        # Ensure it starts with capital letter
        remedy = remedy[0].upper() + remedy[1:] if remedy else ''
        formatted.append(remedy)
    return formatted

def format_table_value(value: str) -> str:
    """Standardize table display values"""
    if not value:
        return 'N/A'
    return value.title() if value.lower() != value else value

def build_enhanced_table(scores, m1, m2, dosha_cancellations):
    """Build table with consistent formatting"""
    
    # Define display value mappings
    rashi_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                   'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    table = []
    for k, pts in scores.items():
        info = KOOTA_INFO[k]
        
        # Get properly formatted boy/girl types
        if k == 'Varna':
            boy_type = VARNA_NAME[VARNA_MAP[m1['sign_number']]]
            girl_type = VARNA_NAME[VARNA_MAP[m2['sign_number']]]
        elif k == 'Vashya':
            boy_type = VASHA_MAP[m1['sign_number']]
            girl_type = VASHA_MAP[m2['sign_number']]
        elif k == 'Tara':
            from .dispositions import NAKSHATRA_LORDS
            boy_type = NAKSHATRA_LORDS[m1['nakshatra']-1].title()
            girl_type = NAKSHATRA_LORDS[m2['nakshatra']-1].title()
        elif k == 'Yoni':
            boy_type = YONI_MAP[m1['nakshatra']]
            girl_type = YONI_MAP[m2['nakshatra']]
        elif k == 'Graha Maitri':
            boy_type = m1.get('sign_lord', 'Unknown').title()
            girl_type = m2.get('sign_lord', 'Unknown').title()
        elif k == 'Gana':
            boy_type = GANA_GROUPS[m1['nakshatra']]
            girl_type = GANA_GROUPS[m2['nakshatra']]
        elif k == 'Bhakoot':
            boy_type = rashi_names[m1['sign_number']-1]
            girl_type = rashi_names[m2['sign_number']-1]
        elif k == 'Nadi':
            boy_type = NADI_MAP[m1['nakshatra']]
            girl_type = NADI_MAP[m2['nakshatra']]
        else:
            boy_type = 'N/A'
            girl_type = 'N/A'
        
        # Add cancellation indicator with proper formatting
        significance = info['desc']
        if k in dosha_cancellations['canceled_doshas']:
            significance += f" (✓ CANCELED: {dosha_cancellations['cancellation_reasons'][k]})"
        
        table.append({
            'Particular': f"{k} Koota",
            'Boy': boy_type,
            'Girl': girl_type,
            'Max': info['max'],
            'Obtained': pts,
            'Significance': significance
        })
    
    return table


def match_kundli(a: AstroData, b: AstroData) -> Dict[str, Any]:
    """
    Main secular matching function with all enhancements
    """
    # Get dispositions and Moon info
    d1 = get_dispositions(a)
    d2 = get_dispositions(b)
    m1, m2 = d1['moon'], d2['moon']
    
    # Compute koota scores
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
    
    # Identify faults
    faults = [k for k, v in scores.items() if v == 0]
    
    # Enhanced Manglik checks
    mg_a = manglik_dosha(a)
    mg_b = manglik_dosha(b)
    boy_manglik = {'is_manglik': mg_a != 'None', 'type': mg_a}
    girl_manglik = {'is_manglik': mg_b != 'None', 'type': mg_b}
    
    if mg_a != mg_b:
        faults.append('Manglik')
    
    # Chandra Manglik details
    ch_mang_a = chandra_manglik_dosha_detailed(a)
    ch_mang_b = chandra_manglik_dosha_detailed(b)
    
    # Advanced analysis
    dosha_cancellations = check_dosha_cancellations(m1, m2, faults, d1, d2)
    compatibility_analysis = calculate_compatibility_percentage(scores)
    risk_assessment = assess_relationship_risks(scores, boy_manglik, girl_manglik, 
                                              dosha_cancellations['canceled_doshas'])
    detailed_interpretation = generate_detailed_interpretation(scores, total, max_total, 
                                                             boy_manglik, girl_manglik, 
                                                             dosha_cancellations['canceled_doshas'])
    constructive_interpretation = generate_constructive_interpretation(scores, faults,
                                                                     dosha_cancellations['canceled_doshas'],
                                                                     compatibility_analysis['weighted_percentage'])
    enhanced_remedies = generate_enhanced_remedies(faults, dosha_cancellations['canceled_doshas'])
    
    # Build enhanced table
    table = []
    for k, pts in scores.items():
        info = KOOTA_INFO[k]
        
        # Determine boy/girl types
        if k == 'Varna':
            boy_type = VARNA_NAME[VARNA_MAP[m1['sign_number']]].title()
            girl_type = VARNA_NAME[VARNA_MAP[m2['sign_number']]].title()
        elif k == 'Vashya':
            boy_type = VASHA_MAP[m1['sign_number']].title()
            girl_type = VASHA_MAP[m2['sign_number']].title()
        elif k == 'Tara':
            from .dispositions import NAKSHATRA_LORDS
            boy_type = NAKSHATRA_LORDS[m1['nakshatra']-1].title()
            girl_type = NAKSHATRA_LORDS[m2['nakshatra']-1].title()
        elif k == 'Yoni':
            boy_type = YONI_MAP[m1['nakshatra']].title()
            girl_type = YONI_MAP[m2['nakshatra']].title()
        elif k == 'Gana':
            boy_type = GANA_GROUPS[m1['nakshatra']].title()
            girl_type = GANA_GROUPS[m2['nakshatra']].title()
        elif k == 'Nadi':
            boy_type = NADI_MAP[m1['nakshatra']].title()
            girl_type = NADI_MAP[m2['nakshatra']].title()
        else:
            boy_type = girl_type = ''
        
        # Add cancellation indicator
        significance = info['desc']
        if k in dosha_cancellations['canceled_doshas']:
            significance += f" (✓ CANCELED: {dosha_cancellations['cancellation_reasons'][k]})"
        
        table.append({
            'Particular': f"{k} Koota",
            'Boy': boy_type,
            'Girl': girl_type,
            'Max': info['max'],
            'Obtained': pts,
            'Significance': significance
        })
    
    # Add total row
    table.append({
        'Particular': 'Total',
        'Boy': '-', 'Girl': '-',
        'Max': max_total,
        'Obtained': total,
        'Significance': f"Overall Compatibility: {compatibility_analysis['weighted_percentage']:.1f}% (Traditional: {compatibility_analysis['traditional_percentage']:.1f}%)"
    })
    
    return {
        'table': table,
        'enhanced_table': build_enhanced_table(scores, m1, m2, dosha_cancellations),
        'faults': faults,
        'remedies': {f: REMEDIES.get(f, []) for f in faults},
        'enhanced_remedies': enhanced_remedies,
        'manglik_status': {
            'boy': {'type': mg_a, 'is_manglik': mg_a != 'None'},
            'girl': {'type': mg_b, 'is_manglik': mg_b != 'None'}
        },
        'chandra_manglik': {
            'boy': ch_mang_a, 
            'girl': ch_mang_b
        },
        'dosha_cancellations': dosha_cancellations,
        'compatibility_analysis': compatibility_analysis,
        'risk_assessment': risk_assessment,
        'detailed_interpretation': detailed_interpretation,
        'constructive_interpretation': constructive_interpretation,
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
