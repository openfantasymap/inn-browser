"""
LLM Service for generating dynamic game content using OpenRouter API
"""
import json
import random
from typing import Dict, Optional
from openai import OpenAI
from django.conf import settings


class LLMService:
    """Service for interacting with LLMs via OpenRouter"""

    def __init__(self):
        """Initialize OpenRouter client"""
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_DEFAULT_MODEL
        self.enabled = settings.USE_LLM_GUEST_GENERATION and bool(self.api_key)

        if self.enabled:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )

    def generate_guest_stats(self, guest_type: str, species: str, name: str) -> Optional[Dict]:
        """
        Generate guest stats using LLM based on guest type, species, and name

        Args:
            guest_type: Type of guest (peasant, wizard, knight, etc.)
            species: Species/race (human, elf, dwarf, tiefling, etc.)
            name: Generated name for the guest

        Returns:
            Dict with guest stats or None if generation fails
        """
        if not self.enabled:
            return None

        # Define guest type characteristics for the prompt
        guest_profiles = {
            'peasant': 'a common peasant - low wealth, average patience, simple needs',
            'merchant': 'a traveling merchant - moderate wealth, busy and impatient, expects good service',
            'noble': 'a wealthy noble - high wealth, demanding and low patience, expects luxury',
            'adventurer': 'an adventurer - moderate wealth, patient, appreciates quality',
            'wizard': 'a mystical wizard - high wealth, varies in patience, scholarly and particular',
            'sorcerer': 'a powerful sorcerer - very high wealth, low patience, demands respect',
            'witch': 'a mysterious witch - moderate wealth, patient, enjoys unique items',
            'alchemist': 'an alchemist - moderate wealth, analytical and patient',
            'necromancer': 'a dark necromancer - high wealth, impatient, unsettling presence',
            'knight': 'a noble knight - moderate to high wealth, honorable, medium patience',
            'paladin': 'a holy paladin - moderate wealth, patient and virtuous',
            'ranger': 'a skilled ranger - low to moderate wealth, very patient, independent',
        }

        profile = guest_profiles.get(guest_type, 'a traveler')

        prompt = f"""Generate stats for a fantasy inn guest. Return ONLY a valid JSON object, no other text.

Guest Name: {name}
Species/Race: {species}
Guest Type: {guest_type}
Profile: {profile}

Consider species traits:
- Elves: Generally patient, graceful, may live longer and have different values
- Dwarves: Sturdy, might drink more, value craftsmanship
- Halflings: Friendly, good-natured, modest wealth
- Tieflings: Exotic, may face prejudice, varied backgrounds
- Dragonborn: Proud, honorable, commanding presence
- Tabaxi: Curious, playful, loves shiny things
- And adapt other species appropriately based on their lore

Generate realistic stats as a JSON object with these exact fields:
{{
  "patience": <integer 40-100, higher for calm types, lower for demanding types>,
  "gold_per_tick": <float 0.5-5.0, higher for wealthy types>,
  "reputation_bonus": <integer 1-10, based on guest prestige>,
  "satisfaction": <integer 50-80, starting satisfaction>,
  "stay_duration": <integer 30-120, how long they stay in seconds>
}}

Consider:
- Peasants: low gold (0.5-1.0), medium patience (60-80), low reputation (1-2)
- Merchants: medium gold (1.5-2.5), low patience (40-60), medium reputation (3-5)
- Nobles: high gold (3.0-4.5), very low patience (30-50), high reputation (6-8)
- Wizards/Sorcerers: very high gold (4.0-5.0), medium patience (50-70), high reputation (7-10)
- Knights/Paladins: medium-high gold (2.0-3.5), medium-high patience (60-80), high reputation (6-8)
- Rangers/Adventurers: low-medium gold (1.0-2.0), high patience (70-90), medium reputation (3-5)

Return ONLY the JSON object."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a game design assistant that generates balanced RPG stats. Always respond with valid JSON only, no markdown or explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Some randomness for variety
                max_tokens=200,
            )

            # Extract the response
            content = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
                content = content.strip()

            # Parse JSON
            stats = json.loads(content)

            # Validate and constrain values
            validated_stats = {
                'patience': max(30, min(100, int(stats.get('patience', 70)))),
                'gold_per_tick': max(0.5, min(5.0, float(stats.get('gold_per_tick', 1.5)))),
                'reputation_bonus': max(1, min(10, int(stats.get('reputation_bonus', 3)))),
                'satisfaction': max(50, min(100, int(stats.get('satisfaction', 70)))),
                'stay_duration': max(30, min(120, int(stats.get('stay_duration', 60)))),
            }

            return validated_stats

        except Exception as e:
            print(f"LLM guest generation failed: {str(e)}")
            return None

    def generate_guest_name(self, guest_type: str, species: str) -> Optional[str]:
        """
        Generate a contextually appropriate name for a guest type and species

        Args:
            guest_type: Type of guest
            species: Species/race of the guest

        Returns:
            Generated name or None if generation fails
        """
        if not self.enabled:
            return None

        type_hints = {
            'peasant': 'simple, common medieval names',
            'merchant': 'prosperous-sounding names',
            'noble': 'elegant, aristocratic names',
            'adventurer': 'bold, memorable names',
            'wizard': 'mystical, arcane-sounding names',
            'sorcerer': 'powerful, exotic names',
            'witch': 'nature or moon-themed names',
            'alchemist': 'scholarly, Latin or Greek influenced names',
            'necromancer': 'dark, ominous names',
            'knight': 'strong, honorable names',
            'paladin': 'holy or virtuous names',
            'ranger': 'nature or woodland themed names',
        }

        hint = type_hints.get(guest_type, 'fantasy-themed names')

        # Species-specific naming guidance
        species_guidance = {
            'elf': 'Elegant, flowing, often with apostrophes (Aer\'ethil, Silv\'ara)',
            'high_elf': 'Sophisticated, musical (Aelindra, Thalion)',
            'wood_elf': 'Nature-themed (Thornleaf, Willowbreeze)',
            'drow': 'Dark, harsh sounds (Drizzt, Malice, Zaknafein)',
            'dwarf': 'Strong consonants, often -in or -im endings (Thorin, Gimli, Balin)',
            'halfling': 'Friendly, simple (Bilbo, Pippin, Rosie)',
            'gnome': 'Clever, whimsical (Fizzbang, Tinkerwhistle)',
            'tiefling': 'Infernal or virtue names (Crimson, Sorrow, Zariel)',
            'dragonborn': 'Draconic, hard sounds (Kriv, Balasar, Medrash)',
            'tabaxi': 'Descriptive phrases (Cloud-Chaser, Soft-Paws)',
            'kenku': 'Mimicked sounds (Whistler, Caw, Echo)',
            'lizardfolk': 'Sibilant, hissing (Sessessix, Susk)',
            'orc': 'Harsh, guttural (Grom, Thrall, Durotan)',
            'goblin': 'Sharp, quick syllables (Grub, Snitch, Bogg)',
            'fairy': 'Delicate, nature-inspired (Dewdrop, Moonbeam)',
            'daemon': 'Dark, powerful (Azrazel, Malphas)',
            'katari': 'Feline, purring sounds (Mreow, Purrnash)',
            'fungril': 'Earthy, spore-like (Sporix, Mycel)',
        }

        species_hint = species_guidance.get(species.lower(), f'{species} themed')

        prompt = f"""Generate ONE fantasy name for a {species} {guest_type}.

Character Style: {hint}
Species Naming: {species_hint}

Requirements:
- Single name only (first name or moniker)
- No title or honorific
- Should fit BOTH the {species} species AND {guest_type} archetype
- Return ONLY the name, nothing else

Example responses: "Aldric", "Thal'endor", "Thornbeard", "Swift-Paw"

Generate the name:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fantasy name generator. Respond with ONLY a single name, no explanation or punctuation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1.0,  # High randomness for name variety
                max_tokens=20,
            )

            name = response.choices[0].message.content.strip()

            # Clean up the response
            name = name.replace('"', '').replace("'", "").replace('.', '').strip()

            # Validate it's a reasonable name (single word, reasonable length)
            if len(name.split()) > 1:
                name = name.split()[0]

            if 2 <= len(name) <= 20:
                return name
            else:
                return None

        except Exception as e:
            print(f"LLM name generation failed: {str(e)}")
            return None


# Global instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
