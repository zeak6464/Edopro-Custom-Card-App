import tkinter as tk
from tkinter import ttk

class ScriptBuilder(ttk.Frame):
    def __init__(self, parent, script_text_widget):
        super().__init__(parent)
        self.script_text = script_text_widget
        self.effect_counter = 1  # Track number of effects
        
        # Common effect types with detailed options
        self.effect_types = {
            "Quick Effect": {
                "type": "EFFECT_TYPE_QUICK_O",
                "code": "EVENT_FREE_CHAIN",
                "timing": {
                    "Any Phase": "0",
                    "Standby Phase": "TIMING_STANDBY_PHASE",
                    "Main Phase": "TIMING_MAIN_END",
                    "Battle Phase": "TIMING_BATTLE_PHASE",
                    "End Phase": "TIMING_END_PHASE"
                },
                "costs": {
                    "Discard this card": {"type": "discard", "value": "self"},
                    "Discard 1 card": {"type": "discard", "value": "1"},
                    "Pay LP": {"type": "pay_lp", "value": "amount"},
                    "Banish this card": {"type": "banish", "value": "self"},
                    "Banish 1 card": {"type": "banish", "value": "1"},
                    "Tribute this card": {"type": "tribute", "value": "self"},
                    "Tribute 1 monster": {"type": "tribute", "value": "1"}
                },
                "locations": {
                    "Hand": "LOCATION_HAND",
                    "Monster Zone": "LOCATION_MZONE",
                    "Spell/Trap Zone": "LOCATION_SZONE",
                    "Field Zone": "LOCATION_FZONE",
                    "Graveyard": "LOCATION_GRAVE",
                    "Banished": "LOCATION_REMOVED"
                },
                "effects": {
                    "Destroy card(s)": {
                        "code": "CATEGORY_DESTROY",
                        "target": True,
                        "options": {
                            "target_type": ["monster", "spell/trap", "any"],
                            "count": ["1", "all"],
                            "target_player": ["opponent", "either", "both"]
                        }
                    },
                    "Special Summon": {
                        "code": "CATEGORY_SPECIAL_SUMMON",
                        "target": False,
                        "options": {
                            "location": ["hand", "deck", "extra_deck", "grave", "banished"],
                            "position": ["attack", "defense", "face_down"],
                            "count": ["1", "2", "3", "all"],
                            "type": ["monster", "specific_card"],
                            "card_id": "number"
                        }
                    },
                    "Search Deck": {
                        "code": "CATEGORY_SEARCH+CATEGORY_TOHAND",
                        "target": False,
                        "options": {
                            "type": ["Monster", "Spell", "Trap", "any"],
                            "attribute": ["LIGHT", "DARK", "WATER", "FIRE", "EARTH", "WIND", "any"],
                            "race": ["Warrior", "Spellcaster", "Fairy", "Fiend", "Dragon", "Zombie", "Machine", "any"],
                            "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "any"],
                            "card_name": "text",
                            "archetype": "text"
                        }
                    },
                    "Draw Cards": {
                        "code": "CATEGORY_DRAW",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "player": ["self", "opponent", "both"],
                            "timing": ["immediate", "end_phase"]
                        }
                    },
                    "Banish Card(s)": {
                        "code": "CATEGORY_REMOVE",
                        "target": True,
                        "options": {
                            "face_position": ["up", "down"],
                            "location": ["field", "grave", "hand", "deck"],
                            "count": ["1", "2", "3", "all"],
                            "duration": ["permanent", "until_end"]
                        }
                    },
                    "Change ATK/DEF": {
                        "code": "CATEGORY_ATKCHANGE",
                        "target": True,
                        "options": {
                            "stat": ["atk", "def", "both"],
                            "amount": "number",
                            "duration": ["turn", "permanent"],
                            "target_type": ["monster", "all_monsters"]
                        }
                    },
                    "Negate Effect": {
                        "code": "CATEGORY_NEGATE",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell", "trap", "any"],
                            "duration": ["temporary", "permanent"],
                            "scope": ["single", "field"]
                        }
                    },
                    "Add Counter": {
                        "code": "CATEGORY_COUNTER",
                        "target": True,
                        "options": {
                            "counter_type": ["spell", "predator", "bushido", "psychic", "crystal"],
                            "amount": "number",
                            "target_type": ["card", "player"]
                        }
                    },
                    "Pay LP": {
                        "code": "CATEGORY_DAMAGE",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "timing": ["cost", "effect"]
                        }
                    },
                    "Gain LP": {
                        "code": "CATEGORY_RECOVER",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "target": ["self", "opponent", "both"]
                        }
                    },
                    "Change Position": {
                        "code": "CATEGORY_POSITION",
                        "target": True,
                        "options": {
                            "position": ["attack", "defense", "face_down"],
                            "target_type": ["monster", "all_monsters"]
                        }
                    },
                    "Return to Deck": {
                        "code": "CATEGORY_TODECK",
                        "target": True,
                        "options": {
                            "position": ["top", "bottom", "shuffle"],
                            "location": ["field", "hand", "grave", "banished"],
                            "count": ["1", "2", "3", "all"]
                        }
                    },
                    "Equip Card": {
                        "code": "CATEGORY_EQUIP",
                        "target": True,
                        "options": {
                            "equip_from": ["hand", "deck", "grave", "banished"],
                            "target_type": ["monster", "specific_card"]
                        }
                    },
                    "Change Control": {
                        "code": "CATEGORY_CONTROL",
                        "target": True,
                        "options": {
                            "duration": ["temporary", "permanent"],
                            "target_type": ["monster", "spell/trap"]
                        }
                    },
                    "Disable Effect": {
                        "code": "CATEGORY_DISABLE",
                        "target": True,
                        "options": {
                            "duration": ["turn", "permanent"],
                            "target_type": ["monster", "spell/trap", "any"]
                        }
                    },
                    "Tribute": {
                        "code": "CATEGORY_RELEASE",
                        "target": True,
                        "options": {
                            "count": ["1", "2", "3", "all"],
                            "type": ["monster", "any"]
                        }
                    },
                    "Copy Effect": {
                        "code": "CATEGORY_DISABLE_EFFECT",
                        "target": True,
                        "options": {
                            "duration": ["turn", "permanent"],
                            "target_type": ["monster", "spell/trap"]
                        }
                    },
                    "Send to GY": {
                        "code": "CATEGORY_TOGRAVE",
                        "target": True,
                        "options": {
                            "location": ["deck", "hand", "field"],
                            "count": ["1", "2", "3", "all"],
                            "type": ["monster", "spell/trap", "any"]
                        }
                    },
                    "Attach Material": {
                        "code": "CATEGORY_OVERLAY",
                        "target": True,
                        "options": {
                            "location": ["hand", "field", "grave", "deck"],
                            "type": ["monster", "specific_card"]
                        }
                    },
                    "Detach Material": {
                        "code": "CATEGORY_DETACH",
                        "target": True,
                        "options": {
                            "amount": "number",
                            "send_to": ["grave", "banished", "deck"]
                        }
                    },
                    "Change Name": {
                        "code": "CATEGORY_CHANGE_NAME",
                        "target": True,
                        "options": {
                            "duration": ["turn", "permanent"],
                            "new_name": "text"
                        }
                    },
                    "Change Type/Attribute": {
                        "code": "CATEGORY_CHANGE_ATTRIBUTE",
                        "target": True,
                        "options": {
                            "change": ["type", "attribute", "level"],
                            "duration": ["turn", "permanent"],
                            "new_value": "text"
                        }
                    },
                    "Inflict Damage": {
                        "code": "CATEGORY_DAMAGE",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "type": ["effect", "battle"],
                            "target": ["opponent", "both"]
                        }
                    },
                    "Negate Summon": {
                        "code": "CATEGORY_DISABLE_SUMMON",
                        "target": True,
                        "options": {
                            "summon_type": ["normal", "special", "any"],
                            "duration": ["single", "turn"]
                        }
                    },
                    "Mill Deck": {
                        "code": "CATEGORY_DECKDES",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "player": ["opponent", "self", "both"]
                        }
                    },
                    "Recover from GY": {
                        "code": "CATEGORY_GRAVE_ACTION",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell/trap", "any"],
                            "count": ["1", "2", "3", "all"],
                            "action": ["add", "special_summon", "set"]
                        }
                    },
                    "Set Card(s)": {
                        "code": "CATEGORY_SET",
                        "target": True,
                        "options": {
                            "location": ["hand", "deck", "grave"],
                            "type": ["monster", "spell/trap", "any"],
                            "count": ["1", "2", "3", "all"]
                        }
                    },
                    "Activate from Hand": {
                        "code": "CATEGORY_ACTIVATE",
                        "target": False,
                        "options": {
                            "type": ["spell", "trap"],
                            "timing": ["opponent_turn", "any_time"]
                        }
                    },
                    "Chain Block": {
                        "code": "CATEGORY_DISABLE_CHAIN",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell", "trap", "any"],
                            "duration": ["chain", "turn"]
                        }
                    }
                }
            },
            "Trigger Effect": {
                "type": "EFFECT_TYPE_SINGLE+EFFECT_TYPE_TRIGGER_O",
                "triggers": {
                    "When sent to GY": "EVENT_TO_GRAVE",
                    "When Normal Summoned": "EVENT_SUMMON_SUCCESS",
                    "When Special Summoned": "EVENT_SPSUMMON_SUCCESS",
                    "When destroyed": "EVENT_DESTROYED",
                    "When targeted": "EVENT_TARGETED",
                    "When removed from field": "EVENT_REMOVE",
                    "When banished": "EVENT_REMOVE",
                    "When drawn": "EVENT_DRAW",
                    "When battle damage": "EVENT_BATTLE_DAMAGE",
                    "When card activated": "EVENT_ACTIVATE",
                    "When attacked": "EVENT_BE_BATTLE_TARGET",
                    "When leaves field": "EVENT_LEAVE_FIELD",
                    "When tributed": "EVENT_RELEASE",
                    "When flipped": "EVENT_FLIP",
                    "When equipped": "EVENT_EQUIP",
                    "When chain resolved": "EVENT_CHAIN_SOLVED",
                    "During Standby Phase": "EVENT_PHASE+PHASE_STANDBY",
                    "During End Phase": "EVENT_PHASE+PHASE_END",
                    "When card effect activated": "EVENT_CHAINING",
                    "When Card is Set": "EVENT_SSET",
                    "When Card is Activated": "EVENT_ACTIVATE",
                    "When LP Changes": "EVENT_LP_CHANGE",
                    "When Counter is Added": "EVENT_ADD_COUNTER",
                    "When Counter is Removed": "EVENT_REMOVE_COUNTER",
                    "When Card is Discarded": "EVENT_DISCARD",
                    "When Phase Changes": "EVENT_PHASE_START"
                },
                "timing": {
                    "Immediate": "0",
                    "On next chain": "EFFECT_FLAG_DELAY"
                },
                "conditions": {
                    "None": "0",
                    "Once per turn": "1",
                    "Once while face-up": "2",
                    "Once per duel": "3",
                    "Hard once per turn": "4"
                },
                "effects": {
                    "Draw Cards": {
                        "code": "CATEGORY_DRAW",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "player": ["self", "opponent", "both"],
                            "timing": ["immediate", "end_phase"]
                        }
                    },
                    "Special Summon": {
                        "code": "CATEGORY_SPECIAL_SUMMON",
                        "target": False,
                        "options": {
                            "location": ["hand", "deck", "extra_deck", "grave", "banished"],
                            "position": ["attack", "defense", "face_down"],
                            "count": ["1", "2", "3", "all"],
                            "type": ["monster", "specific_card"],
                            "card_id": "number"
                        }
                    },
                    "Search Deck": {
                        "code": "CATEGORY_SEARCH+CATEGORY_TOHAND",
                        "target": False,
                        "options": {
                            "type": ["Monster", "Spell", "Trap", "any"],
                            "attribute": ["LIGHT", "DARK", "WATER", "FIRE", "EARTH", "WIND", "any"],
                            "race": ["Warrior", "Spellcaster", "Fairy", "Fiend", "Dragon", "Zombie", "Machine", "any"],
                            "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "any"],
                            "card_name": "text",
                            "archetype": "text"
                        }
                    },
                    "Destroy Card(s)": {
                        "code": "CATEGORY_DESTROY",
                        "target": True,
                        "options": {
                            "target_type": ["monster", "spell/trap", "any"],
                            "count": ["1", "all"],
                            "target_player": ["opponent", "either", "both"]
                        }
                    },
                    "Send to GY": {
                        "code": "CATEGORY_TOGRAVE",
                        "target": True,
                        "options": {
                            "location": ["deck", "hand", "field"],
                            "count": ["1", "2", "3", "all"],
                            "type": ["monster", "spell/trap", "any"]
                        }
                    },
                    "Banish Card(s)": {
                        "code": "CATEGORY_REMOVE",
                        "target": True,
                        "options": {
                            "face_position": ["up", "down"],
                            "location": ["field", "grave", "hand", "deck"],
                            "count": ["1", "2", "3", "all"],
                            "duration": ["permanent", "until_end"]
                        }
                    },
                    "Add Counter": {
                        "code": "CATEGORY_COUNTER",
                        "target": True,
                        "options": {
                            "counter_type": ["spell", "predator", "bushido", "psychic", "crystal"],
                            "amount": "number",
                            "target_type": ["card", "player"]
                        }
                    },
                    "Gain LP": {
                        "code": "CATEGORY_RECOVER",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "target": ["self", "opponent", "both"]
                        }
                    },
                    "Inflict Damage": {
                        "code": "CATEGORY_DAMAGE",
                        "target": False,
                        "options": {
                            "amount": "number",
                            "type": ["effect", "battle"],
                            "target": ["opponent", "both"]
                        }
                    },
                    "Change ATK/DEF": {
                        "code": "CATEGORY_ATKCHANGE",
                        "target": True,
                        "options": {
                            "stat": ["atk", "def", "both"],
                            "amount": "number",
                            "duration": ["turn", "permanent"],
                            "target_type": ["monster", "all_monsters"]
                        }
                    },
                    "Add from Deck": {
                        "code": "CATEGORY_SEARCH",
                        "target": False,
                        "options": {
                            "type": ["Monster", "Spell", "Trap", "any"],
                            "attribute": ["LIGHT", "DARK", "WATER", "FIRE", "EARTH", "WIND", "any"],
                            "race": ["Warrior", "Spellcaster", "Fairy", "Fiend", "Dragon", "Zombie", "Machine", "any"],
                            "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "any"]
                        }
                    },
                    "Return from GY": {
                        "code": "CATEGORY_GRAVE_ACTION",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell/trap", "any"],
                            "count": ["1", "2", "3", "all"],
                            "action": ["add", "special_summon", "set"]
                        }
                    },
                    "Attach as Material": {
                        "code": "CATEGORY_OVERLAY",
                        "target": True,
                        "options": {
                            "location": ["hand", "field", "grave", "deck"],
                            "type": ["monster", "specific_card"]
                        }
                    },
                    "Copy Effect": {
                        "code": "CATEGORY_DISABLE_EFFECT",
                        "target": True,
                        "options": {
                            "duration": ["turn", "permanent"],
                            "target_type": ["monster", "spell/trap"]
                        }
                    },
                    "Change Position": {
                        "code": "CATEGORY_POSITION",
                        "target": True,
                        "options": {
                            "position": ["attack", "defense", "face_down"],
                            "target_type": ["monster", "all_monsters"]
                        }
                    }
                }
            },
            "Field Effect": {
                "type": "EFFECT_TYPE_FIELD",
                "targets": {
                    "Your monsters": "1",
                    "Opponent's monsters": "2",
                    "All monsters": "3",
                    "Your Spells/Traps": "4",
                    "Opponent's Spells/Traps": "5",
                    "All Spells/Traps": "6"
                },
                "scope": {
                    "All cards": "LOCATION_ALL",
                    "Monsters only": "LOCATION_MZONE",
                    "Spells only": "LOCATION_SZONE",
                    "Traps only": "LOCATION_SZONE",
                    "Hand only": "LOCATION_HAND",
                    "Deck only": "LOCATION_DECK"
                },
                "conditions": {
                    "While face-up on field": "LOCATION_MZONE",
                    "While in GY": "LOCATION_GRAVE",
                    "While banished": "LOCATION_REMOVED",
                    "While in hand": "LOCATION_HAND",
                    "During your turn": "LOCATION_MZONE+EFFECT_FLAG_PLAYER_TARGET",
                    "During either turn": "LOCATION_MZONE+EFFECT_FLAG_BOTH_SIDE"
                },
                "effects": {
                    "Negate Effects": {
                        "code": "EFFECT_DISABLE",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell", "trap", "any"],
                            "duration": ["temporary", "permanent"],
                            "scope": ["single", "field"]
                        }
                    },
                    "Prevent Activation": {
                        "code": "EFFECT_CANNOT_ACTIVATE",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell", "trap", "any"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Summoning": {
                        "code": "EFFECT_CANNOT_SUMMON",
                        "target": True,
                        "options": {
                            "summon_type": ["normal", "special", "any"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Change ATK/DEF": {
                        "code": "EFFECT_UPDATE_ATTACK",
                        "target": True,
                        "options": {
                            "stat": ["atk", "def", "both"],
                            "amount": "number",
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Skip Phase": {
                        "code": "EFFECT_SKIP_PHASE",
                        "target": True,
                        "options": {
                            "phase": ["standby", "main1", "battle", "main2", "end"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Drawing": {
                        "code": "EFFECT_CANNOT_DRAW",
                        "target": True,
                        "options": {
                            "player": ["opponent", "both"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Adding": {
                        "code": "EFFECT_CANNOT_TO_HAND",
                        "target": True,
                        "options": {
                            "type": ["monster", "spell", "trap", "any"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent LP Payment": {
                        "code": "EFFECT_CANNOT_PAY_COST",
                        "target": True,
                        "options": {
                            "player": ["opponent", "both"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Lock Battle Position": {
                        "code": "EFFECT_CANNOT_CHANGE_POSITION",
                        "target": True,
                        "options": {
                            "target_type": ["monster", "all_monsters"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Control Change": {
                        "code": "EFFECT_CANNOT_CHANGE_CONTROL",
                        "target": True,
                        "options": {
                            "target_type": ["monster", "all_cards"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Restrict Attacks": {
                        "code": "EFFECT_CANNOT_SELECT_BATTLE_TARGET",
                        "target": True,
                        "options": {
                            "target_type": ["monster", "all_monsters"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Change Attribute": {
                        "code": "EFFECT_CHANGE_ATTRIBUTE",
                        "target": True,
                        "options": {
                            "attribute": ["LIGHT", "DARK", "WATER", "FIRE", "EARTH", "WIND"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Change Type": {
                        "code": "EFFECT_CHANGE_RACE",
                        "target": True,
                        "options": {
                            "race": ["Warrior", "Spellcaster", "Fairy", "Fiend", "Dragon", "Zombie", "Machine"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Special Summon": {
                        "code": "EFFECT_CANNOT_SPECIAL_SUMMON",
                        "target": True,
                        "options": {
                            "summon_type": ["fusion", "synchro", "xyz", "link", "any"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Halve LP": {
                        "code": "EFFECT_SET_LP_COST",
                        "target": True,
                        "options": {
                            "player": ["opponent", "both"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Double Damage": {
                        "code": "EFFECT_DOUBLE_DAMAGE",
                        "target": True,
                        "options": {
                            "damage_type": ["battle", "effect", "both"],
                            "duration": ["turn", "permanent"]
                        }
                    },
                    "Prevent Battle Damage": {
                        "code": "EFFECT_AVOID_BATTLE_DAMAGE",
                        "target": True,
                        "options": {
                            "player": ["self", "opponent", "both"],
                            "duration": ["turn", "permanent"]
                        }
                    }
                }
            },
            "Continuous Effect": {
                "type": "EFFECT_TYPE_SINGLE",
                "conditions": {
                    "While face-up on field": "LOCATION_MZONE",
                    "While in GY": "LOCATION_GRAVE",
                    "While banished": "LOCATION_REMOVED",
                    "While in hand": "LOCATION_HAND",
                    "While in deck": "LOCATION_DECK",
                    "While in Extra Deck": "LOCATION_EXTRA",
                    "During your turn": "LOCATION_MZONE+EFFECT_FLAG_PLAYER_TARGET",
                    "During either turn": "LOCATION_MZONE+EFFECT_FLAG_BOTH_SIDE",
                    "While attacking": "LOCATION_MZONE+EFFECT_FLAG_SINGLE_RANGE"
                },
                "effects": {
                    "Gain ATK": {
                        "code": "EFFECT_UPDATE_ATTACK",
                        "options": {
                            "amount": "number",
                            "target": "self"
                        }
                    },
                    "Gain DEF": {
                        "code": "EFFECT_UPDATE_DEFENSE",
                        "options": {
                            "amount": "number",
                            "target": "self"
                        }
                    },
                    "Cannot be targeted": {
                        "code": "EFFECT_CANNOT_BE_EFFECT_TARGET",
                        "target": True
                    },
                    "Cannot be destroyed": {
                        "code": "EFFECT_INDESTRUCTABLE_EFFECT",
                        "target": True
                    },
                    "Negate effects": {
                        "code": "EFFECT_DISABLE",
                        "target": True
                    },
                    "Cannot attack": {
                        "code": "EFFECT_CANNOT_ATTACK",
                        "target": True
                    },
                    "Must attack": {
                        "code": "EFFECT_MUST_ATTACK",
                        "target": True
                    },
                    "Direct attack": {
                        "code": "EFFECT_DIRECT_ATTACK",
                        "target": True
                    },
                    "Pierce": {
                        "code": "EFFECT_PIERCE",
                        "target": True
                    },
                    "Cannot be tributed": {
                        "code": "EFFECT_UNRELEASABLE",
                        "target": True
                    },
                    "Cannot be used as material": {
                        "code": "EFFECT_CANNOT_BE_MATERIAL",
                        "target": True
                    },
                    "Cannot change position": {
                        "code": "EFFECT_CANNOT_CHANGE_POSITION",
                        "target": True
                    },
                    "Cannot activate effects": {
                        "code": "EFFECT_CANNOT_TRIGGER",
                        "target": True
                    },
                    "Cannot be banished": {
                        "code": "EFFECT_CANNOT_REMOVE",
                        "target": True
                    },
                    "Cannot be returned": {
                        "code": "EFFECT_CANNOT_TO_DECK",
                        "target": True
                    },
                    "Cannot special summon": {
                        "code": "EFFECT_CANNOT_SPECIAL_SUMMON",
                        "target": True
                    },
                    "Immune to effects": {
                        "code": "EFFECT_IMMUNE_EFFECT",
                        "target": True
                    },
                    "Double damage": {
                        "code": "EFFECT_DOUBLE_DAMAGE",
                        "target": True
                    },
                    "Half damage": {
                        "code": "EFFECT_HALF_DAMAGE",
                        "target": True
                    },
                    "Cannot chain": {
                        "code": "EFFECT_CANNOT_ACTIVATE",
                        "target": True
                    },
                    "Negate summons": {
                        "code": "EFFECT_CANNOT_SUMMON",
                        "target": True
                    },
                    "Cannot be negated": {
                        "code": "EFFECT_CANNOT_NEGATE",
                        "target": True
                    },
                    "Cannot leave field": {
                        "code": "EFFECT_CANNOT_LEAVE_FIELD",
                        "target": True
                    },
                    "Gain effects": {
                        "code": "EFFECT_ADD_CODE",
                        "target": True
                    },
                    "Change attribute": {
                        "code": "EFFECT_CHANGE_ATTRIBUTE",
                        "target": True
                    },
                    "Change type": {
                        "code": "EFFECT_CHANGE_RACE",
                        "target": True
                    },
                    "Change level": {
                        "code": "EFFECT_CHANGE_LEVEL",
                        "target": True
                    },
                    "Treat as tuner": {
                        "code": "EFFECT_ADD_TYPE",
                        "target": True
                    },
                    "Treat name as": {
                        "code": "EFFECT_CHANGE_CODE",
                        "target": True
                    },
                    "Cannot be Set": {"code": "EFFECT_CANNOT_SET", "target": True},
                    "Cannot be Flipped": {"code": "EFFECT_CANNOT_FLIP", "target": True},
                    "Cannot be Discarded": {"code": "EFFECT_CANNOT_DISCARD", "target": True},
                    "Cannot be Equipped": {"code": "EFFECT_CANNOT_EQUIP", "target": True},
                    "Cannot be Selected": {"code": "EFFECT_CANNOT_SELECT", "target": True},
                    "Cannot be Affected": {"code": "EFFECT_IMMUNE_EFFECT", "target": True},
                    "Cannot Declare Attacks": {"code": "EFFECT_CANNOT_ATTACK_ANNOUNCE", "target": True},
                    "Must Attack if Able": {"code": "EFFECT_MUST_ATTACK_ANNOUNCE", "target": True},
                    "Cannot be Link Material": {"code": "EFFECT_CANNOT_BE_LINK_MATERIAL", "target": True},
                    "Cannot be Synchro Material": {"code": "EFFECT_CANNOT_BE_SYNCHRO_MATERIAL", "target": True},
                    "Cannot be Xyz Material": {"code": "EFFECT_CANNOT_BE_XYZ_MATERIAL", "target": True},
                    "Cannot be Fusion Material": {"code": "EFFECT_CANNOT_BE_FUSION_MATERIAL", "target": True}
                }
            }
        }
        
        # Common categories with descriptions
        self.categories = {
            "Destroy": {"code": "CATEGORY_DESTROY", "desc": "Destroy card(s)"},
            "Special Summon": {"code": "CATEGORY_SPECIAL_SUMMON", "desc": "Special Summon monster(s)"},
            "Search": {"code": "CATEGORY_SEARCH", "desc": "Add card(s) from Deck"},
            "Draw": {"code": "CATEGORY_DRAW", "desc": "Draw card(s)"},
            "Banish": {"code": "CATEGORY_REMOVE", "desc": "Banish card(s)"},
            "To Hand": {"code": "CATEGORY_TOHAND", "desc": "Add to hand"},
            "To Grave": {"code": "CATEGORY_TOGRAVE", "desc": "Send to Graveyard"},
            "To Deck": {"code": "CATEGORY_TODECK", "desc": "Return to Deck"},
            "Negate": {"code": "CATEGORY_NEGATE", "desc": "Negate activation/effect"},
            "Position": {"code": "CATEGORY_POSITION", "desc": "Change battle position"},
            "Counter": {"code": "CATEGORY_COUNTER", "desc": "Place/Remove counter(s)"},
            "Disable": {"code": "CATEGORY_DISABLE", "desc": "Negate effects"},
            "Recover": {"code": "CATEGORY_RECOVER", "desc": "Gain LP"},
            "Damage": {"code": "CATEGORY_DAMAGE", "desc": "Inflict damage"},
            "Atkchange": {"code": "CATEGORY_ATKCHANGE", "desc": "Change ATK/DEF"}
        }
        
        # Common properties with descriptions
        self.properties = {
            "Card Target": {"code": "EFFECT_FLAG_CARD_TARGET", "desc": "Target specific card(s)"},
            "Cannot Disable": {"code": "EFFECT_FLAG_CANNOT_DISABLE", "desc": "Effect cannot be disabled"},
            "Cannot Negate": {"code": "EFFECT_FLAG_CANNOT_NEGATE", "desc": "Activation cannot be negated"},
            "Delay": {"code": "EFFECT_FLAG_DELAY", "desc": "Trigger in new chain"},
            "Damage Step": {"code": "EFFECT_FLAG_DAMAGE_STEP", "desc": "Can activate in Damage Step"},
            "Both Players": {"code": "EFFECT_FLAG_PLAYER_TARGET", "desc": "Affects both players"},
            "Initial": {"code": "EFFECT_FLAG_INITIAL", "desc": "Initial effect"}
        }
        
        # Common effect patterns
        self.effect_patterns = {
            "Search Pattern": """
    if chk==0 then return Duel.IsExistingMatchingCard(s.filter,tp,LOCATION_DECK,0,1,nil) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_ATOHAND)
    local g=Duel.SelectMatchingCard(tp,s.filter,tp,LOCATION_DECK,0,1,1,nil)
    if #g>0 then
        Duel.SendtoHand(g,nil,REASON_EFFECT)
        Duel.ConfirmCards(1-tp,g)
    end""",
            "Special Summon Pattern": """
    if chk==0 then return Duel.GetLocationCount(tp,LOCATION_MZONE)>0
        and Duel.IsExistingMatchingCard(s.spfilter,tp,LOCATION_HAND+LOCATION_DECK,0,1,nil,e,tp) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_SPSUMMON)
    local g=Duel.SelectMatchingCard(tp,s.spfilter,tp,LOCATION_HAND+LOCATION_DECK,0,1,1,nil,e,tp)
    if #g>0 then
        Duel.SpecialSummon(g,0,tp,tp,false,false,POS_FACEUP)
    end""",
            "Destroy Pattern": """
    if chk==0 then return Duel.IsExistingMatchingCard(Card.IsDestructable,tp,LOCATION_ONFIELD,LOCATION_ONFIELD,1,nil) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_DESTROY)
    local g=Duel.SelectMatchingCard(tp,Card.IsDestructable,tp,LOCATION_ONFIELD,LOCATION_ONFIELD,1,1,nil)
    if #g>0 then
        Duel.Destroy(g,REASON_EFFECT)
    end""",
            "Negate Pattern": """
    if chk==0 then return Duel.IsExistingMatchingCard(Card.IsNegatable,tp,0,LOCATION_ONFIELD,1,nil) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_NEGATE)
    local g=Duel.SelectMatchingCard(tp,Card.IsNegatable,tp,0,LOCATION_ONFIELD,1,1,nil)
    if #g>0 then
        local tc=g:GetFirst()
        Duel.NegateRelatedChain(tc,RESET_TURN_SET)
        local e1=Effect.CreateEffect(e:GetHandler())
        e1:SetType(EFFECT_TYPE_SINGLE)
        e1:SetCode(EFFECT_DISABLE)
        e1:SetReset(RESET_EVENT+RESETS_STANDARD+RESET_PHASE+PHASE_END)
        tc:RegisterEffect(e1)
    end""",
            "Banish Pattern": """
    if chk==0 then return Duel.IsExistingMatchingCard(Card.IsAbleToRemove,tp,LOCATION_GRAVE,LOCATION_GRAVE,1,nil) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_REMOVE)
    local g=Duel.SelectMatchingCard(tp,Card.IsAbleToRemove,tp,LOCATION_GRAVE,LOCATION_GRAVE,1,1,nil)
    if #g>0 then
        Duel.Remove(g,POS_FACEUP,REASON_EFFECT)
    end""",
            "Draw Pattern": """
    if chk==0 then return Duel.IsPlayerCanDraw(tp,2) end
    Duel.Draw(tp,2,REASON_EFFECT)""",
            "Change Position Pattern": """
    if chk==0 then return Duel.IsExistingMatchingCard(Card.IsCanChangePosition,tp,LOCATION_MZONE,LOCATION_MZONE,1,nil) end
    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_POSCHANGE)
    local g=Duel.SelectMatchingCard(tp,Card.IsCanChangePosition,tp,LOCATION_MZONE,LOCATION_MZONE,1,1,nil)
    if #g>0 then
        Duel.ChangePosition(g,POS_FACEUP_DEFENSE,POS_FACEDOWN_DEFENSE,POS_FACEUP_ATTACK,POS_FACEUP_ATTACK)
    end"""
        }
        
        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)
        
        # Create Effect Type Selection
        type_frame = ttk.LabelFrame(main_frame, text="Effect Type")
        type_frame.pack(fill="x", padx=5, pady=5)
        
        self.effect_type_var = tk.StringVar()
        type_desc = {
            "Quick Effect": "Can be activated during either player's turn",
            "Trigger Effect": "Activates when a specific condition is met",
            "Continuous Effect": "Applies its effect continuously while active",
            "Field Effect": "Affects multiple cards on the field"
        }
        
        for effect_type, desc in type_desc.items():
            rb = ttk.Radiobutton(type_frame, text=effect_type, value=effect_type,
                               variable=self.effect_type_var,
                               command=self.update_effect_options)
            rb.pack(anchor="w", padx=5, pady=2)
            CreateToolTip(rb, desc)
        
        # Effect Selection Frame
        self.effect_frame = ttk.LabelFrame(main_frame, text="Effect")
        self.effect_frame.pack(fill="x", padx=5, pady=5)
        
        # Options frame for effect-specific options
        self.options_frame = ttk.Frame(main_frame)
        self.options_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add Effect Button at bottom
        add_button_frame = ttk.Frame(main_frame)
        add_button_frame.pack(fill="x", padx=5, pady=10)
        ttk.Button(add_button_frame, text="Add Effect to Script",
                  command=self.generate_effect).pack(pady=5)

    def update_effect_options(self, *args):
        # Clear previous options
        for widget in self.effect_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        effect_type = self.effect_type_var.get()
        if not effect_type or effect_type not in self.effect_types:
            return
            
        options = self.effect_types[effect_type]
        
        # Effect Selection
        self.effect_var = tk.StringVar()
        effect_cb = ttk.Combobox(self.effect_frame, textvariable=self.effect_var,
                               values=list(options["effects"].keys()))
        effect_cb.pack(fill="x", padx=5, pady=2)
        effect_cb.set(list(options["effects"].keys())[0])
        effect_cb.bind("<<ComboboxSelected>>", self.update_effect_specific_options)
        
        # Add effect-specific options
        self.update_effect_specific_options()
        
        # Add categories and properties
        self.add_categories_and_properties()

    def create_tooltip_checkbutton(self, parent, text, tooltip_text, variable):
        """Create a checkbutton with a tooltip."""
        cb = ttk.Checkbutton(parent, text=text, variable=variable)
        CreateToolTip(cb, tooltip_text)
        return cb

    def add_categories_and_properties(self):
        # Add Categories frame with tooltips
        cat_frame = ttk.LabelFrame(self.options_frame, text="Categories")
        cat_frame.pack(fill="x", padx=5, pady=5)
        
        self.category_vars = {}
        for cat, info in self.categories.items():
            var = tk.BooleanVar()
            self.category_vars[cat] = var
            cb = self.create_tooltip_checkbutton(cat_frame, cat, info["desc"], var)
            cb.pack(anchor="w", padx=5)
        
        # Add Properties frame with tooltips
        prop_frame = ttk.LabelFrame(self.options_frame, text="Properties")
        prop_frame.pack(fill="x", padx=5, pady=5)
        
        self.property_vars = {}
        for prop, info in self.properties.items():
            var = tk.BooleanVar()
            self.property_vars[prop] = var
            cb = self.create_tooltip_checkbutton(prop_frame, prop, info["desc"], var)
            cb.pack(anchor="w", padx=5)

    def update_effect_specific_options(self, event=None):
        effect_type = self.effect_type_var.get()
        effect = self.effect_var.get()
        
        # Clear previous specific options
        if hasattr(self, 'specific_frame'):
            self.specific_frame.destroy()
        
        self.specific_frame = ttk.Frame(self.options_frame)
        self.specific_frame.pack(fill="x", padx=5, pady=5)
        
        if not effect_type or not effect:
            return
            
        options = self.effect_types[effect_type]["effects"].get(effect, {}).get("options", {})
        if not options:
            return
            
        # Create a frame for each option
        for option_name, option_values in options.items():
            option_frame = ttk.Frame(self.specific_frame)
            option_frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(option_frame, text=f"{option_name.replace('_', ' ').title()}:").pack(side="left", padx=2)
            
            if isinstance(option_values, list):
                # Create combobox for list options
                var = tk.StringVar()
                setattr(self, f"{option_name}_var", var)
                cb = ttk.Combobox(option_frame, textvariable=var, values=option_values)
                cb.pack(side="left", padx=2, fill="x", expand=True)
                cb.set(option_values[0])
            elif option_values == "number":
                # Create entry for numeric values
                entry = ttk.Entry(option_frame, width=10)
                setattr(self, f"{option_name}_entry", entry)
                entry.pack(side="left", padx=2)
                entry.insert(0, "0")
            elif option_values == "text":
                # Create entry for text values
                entry = ttk.Entry(option_frame)
                setattr(self, f"{option_name}_entry", entry)
                entry.pack(side="left", padx=2, fill="x", expand=True)
                
        # Add target selection if effect requires targeting
        if self.effect_types[effect_type]["effects"].get(effect, {}).get("target", False):
            target_frame = ttk.LabelFrame(self.specific_frame, text="Target Selection")
            target_frame.pack(fill="x", padx=5, pady=5)
            
            # Target count
            count_frame = ttk.Frame(target_frame)
            count_frame.pack(fill="x", padx=5, pady=2)
            ttk.Label(count_frame, text="Target Count:").pack(side="left", padx=2)
            self.target_count_var = tk.StringVar()
            count_cb = ttk.Combobox(count_frame, textvariable=self.target_count_var,
                                  values=["1", "2", "3", "all"])
            count_cb.pack(side="left", padx=2)
            count_cb.set("1")
            
            # Target player
            player_frame = ttk.Frame(target_frame)
            player_frame.pack(fill="x", padx=5, pady=2)
            ttk.Label(player_frame, text="Target Player:").pack(side="left", padx=2)
            self.target_player_var = tk.StringVar()
            player_cb = ttk.Combobox(player_frame, textvariable=self.target_player_var,
                                   values=["your", "opponent", "both"])
            player_cb.pack(side="left", padx=2)
            player_cb.set("opponent")
            
            # Target location
            location_frame = ttk.Frame(target_frame)
            location_frame.pack(fill="x", padx=5, pady=2)
            ttk.Label(location_frame, text="Target Location:").pack(side="left", padx=2)
            self.target_location_var = tk.StringVar()
            location_cb = ttk.Combobox(location_frame, textvariable=self.target_location_var,
                                     values=["field", "hand", "deck", "grave", "banished"])
            location_cb.pack(side="left", padx=2)
            location_cb.set("field")

    def generate_effect(self):
        effect_type = self.effect_type_var.get()
        effect = self.effect_var.get()
        if not effect_type or not effect:
            return
            
        effect_num = self.effect_counter
        self.effect_counter += 1
        
        script = []
        options = self.effect_types[effect_type]["effects"][effect]
        
        # Get effect-specific options
        effect_options = {}
        if "options" in options:
            for option_name, option_values in options["options"].items():
                if isinstance(option_values, list):
                    var = getattr(self, f"{option_name}_var", None)
                    if var:
                        effect_options[option_name] = var.get()
                elif option_values in ["number", "text"]:
                    entry = getattr(self, f"{option_name}_entry", None)
                    if entry:
                        effect_options[option_name] = entry.get()
        
        # Get targeting options if applicable
        if options.get("target", False):
            effect_options["target_count"] = getattr(self, "target_count_var", tk.StringVar()).get()
            effect_options["target_player"] = getattr(self, "target_player_var", tk.StringVar()).get()
            effect_options["target_location"] = getattr(self, "target_location_var", tk.StringVar()).get()
        
        # Generate basic effect structure
        script.extend([
            f"    -- {effect}",
            f"    local e{effect_num}=Effect.CreateEffect(c)",
            f"    e{effect_num}:SetType({self.effect_types[effect_type]['type']})"
        ])
        
        # Add categories
        categories = []
        for cat, var in self.category_vars.items():
            if var.get():
                categories.append(self.categories[cat]["code"])
        if categories:
            script.append(f"    e{effect_num}:SetCategory(" + "+".join(categories) + ")")
        
        # Add properties
        properties = []
        for prop, var in self.property_vars.items():
            if var.get():
                properties.append(self.properties[prop]["code"])
        if properties:
            script.append(f"    e{effect_num}:SetProperty(" + "+".join(properties) + ")")
        
        # Add effect-type specific code
        if effect_type == "Quick Effect":
            script.extend([
                f"    e{effect_num}:SetCode({options['code']})",
                f"    e{effect_num}:SetRange({self.effect_types[effect_type]['locations'][self.location_var.get()]})",
                f"    e{effect_num}:SetCountLimit(1)"
            ])
            
            # Add cost if specified
            cost = self.effect_types[effect_type]["costs"][self.cost_var.get()]
            if cost["type"] == "pay_lp" and "amount" in effect_options:
                script.append(f"    e{effect_num}:SetCost(function(e,tp,eg,ep,ev,re,r,rp,chk)")
                script.append(f"        if chk==0 then return Duel.CheckLPCost(tp,{effect_options['amount']}) end")
                script.append(f"        Duel.PayLPCost(tp,{effect_options['amount']})")
                script.append("    end)")
            
        elif effect_type == "Trigger Effect":
            script.extend([
                f"    e{effect_num}:SetCode({self.effect_types[effect_type]['triggers'][self.trigger_var.get()]})",
                f"    e{effect_num}:SetRange(LOCATION_MZONE)",
                f"    e{effect_num}:SetCountLimit(1)"
            ])
            
        elif effect_type == "Field Effect":
            script.extend([
                f"    e{effect_num}:SetRange(LOCATION_MZONE)",
                f"    e{effect_num}:SetTargetRange({self.effect_types[effect_type]['targets'][self.target_var.get()]},0)"
            ])
        
        # Add effect-specific operations
        if effect == "Search Deck":
            script.extend(self.generate_search_effect(effect_num, effect_options))
        elif effect == "Special Summon":
            script.extend(self.generate_special_summon_effect(effect_num, effect_options))
        elif effect == "Destroy card(s)":
            script.extend(self.generate_destroy_effect(effect_num, effect_options))
        elif effect == "Draw Cards":
            script.extend(self.generate_draw_effect(effect_num, effect_options))
        elif effect == "Change ATK/DEF":
            script.extend(self.generate_stat_change_effect(effect_num, effect_options))
        
        # Register the effect
        script.append(f"    c:RegisterEffect(e{effect_num})")
        script.append("")
        
        # Add to existing script
        current_script = self.script_text.get("1.0", tk.END).strip()
        if not current_script or current_script == "--Card Script\nlocal s,id=GetID()\nfunction s.initial_effect(c)\n\nend":
            # Create new script
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert("1.0", f"""--Card Script
local s,id=GetID()
function s.initial_effect(c)
{chr(10).join(script)}
end""")
        else:
            # Add to existing script
            last_end = current_script.rindex("end")
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert("1.0", current_script[:last_end] + "\n" + "\n".join(script) + "\n" + current_script[last_end:])

    def generate_search_effect(self, effect_num, options):
        filter_conditions = []
        
        if options.get("type") != "any":
            filter_conditions.append(f"c:IsType(TYPE_{options['type'].upper()})")
        
        if options.get("attribute") != "any":
            filter_conditions.append(f"c:IsAttribute(ATTRIBUTE_{options['attribute']})")
        
        if options.get("race") != "any":
            filter_conditions.append(f"c:IsRace(RACE_{options['race'].upper()})")
        
        if options.get("level") != "any":
            filter_conditions.append(f"c:IsLevel({options['level']})")
        
        if options.get("card_name"):
            filter_conditions.append(f"c:IsCode({options['card_name']})")
            
        filter_str = " and ".join(filter_conditions) if filter_conditions else "true"
        
        return [
            f"function s.filter{effect_num}(c)",
            f"    return {filter_str} and c:IsAbleToHand()",
            "end",
            "",
            f"function s.thtg{effect_num}(e,tp,eg,ep,ev,re,r,rp,chk)",
            f"    if chk==0 then return Duel.IsExistingMatchingCard(s.filter{effect_num},tp,LOCATION_DECK,0,1,nil) end",
            "    Duel.SetOperationInfo(0,CATEGORY_TOHAND,nil,1,tp,LOCATION_DECK)",
            "end",
            "",
            f"function s.thop{effect_num}(e,tp,eg,ep,ev,re,r,rp)",
            "    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_ATOHAND)",
            f"    local g=Duel.SelectMatchingCard(tp,s.filter{effect_num},tp,LOCATION_DECK,0,1,1,nil)",
            "    if #g>0 then",
            "        Duel.SendtoHand(g,nil,REASON_EFFECT)",
            "        Duel.ConfirmCards(1-tp,g)",
            "    end",
            "end"
        ]

    def generate_special_summon_effect(self, effect_num, options):
        location = f"LOCATION_{options.get('location', 'HAND').upper()}"
        position = f"POS_{options.get('position', 'ATTACK').upper()}"
        count = options.get('count', '1')
        
        return [
            f"function s.sptg{effect_num}(e,tp,eg,ep,ev,re,r,rp,chk)",
            f"    if chk==0 then return Duel.GetLocationCount(tp,LOCATION_MZONE)>0",
            f"        and Duel.IsExistingMatchingCard(Card.IsCanBeSpecialSummoned,tp,{location},0,1,nil,e,tp) end",
            f"    Duel.SetOperationInfo(0,CATEGORY_SPECIAL_SUMMON,nil,{count},tp,{location})",
            "end",
            "",
            f"function s.spop{effect_num}(e,tp,eg,ep,ev,re,r,rp)",
            "    if Duel.GetLocationCount(tp,LOCATION_MZONE)<=0 then return end",
            "    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_SPSUMMON)",
            f"    local g=Duel.SelectMatchingCard(tp,Card.IsCanBeSpecialSummoned,tp,{location},0,1,{count},nil,e,tp)",
            "    if #g>0 then",
            f"        Duel.SpecialSummon(g,0,tp,tp,false,false,{position})",
            "    end",
            "end"
        ]

    def generate_destroy_effect(self, effect_num, options):
        target_type = options.get('target_type', 'any')
        count = options.get('count', '1')
        
        filter_condition = ""
        if target_type != "any":
            filter_condition = f"Card.IsType,TYPE_{target_type.upper()}"
        else:
            filter_condition = "Card.IsDestructable"
            
        return [
            f"function s.destg{effect_num}(e,tp,eg,ep,ev,re,r,rp,chk,chkc)",
            "    if chk==0 then return Duel.IsExistingTarget(Card.IsDestructable,tp,LOCATION_ONFIELD,LOCATION_ONFIELD,1,nil) end",
            f"    Duel.SetOperationInfo(0,CATEGORY_DESTROY,nil,{count},0,0)",
            "end",
            "",
            f"function s.desop{effect_num}(e,tp,eg,ep,ev,re,r,rp)",
            "    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_DESTROY)",
            f"    local g=Duel.SelectTarget(tp,Card.IsDestructable,tp,LOCATION_ONFIELD,LOCATION_ONFIELD,1,{count},nil)",
            "    if #g>0 then",
            "        Duel.Destroy(g,REASON_EFFECT)",
            "    end",
            "end"
        ]

    def generate_draw_effect(self, effect_num, options):
        amount = options.get('amount', '1')
        player = options.get('player', 'self')
        
        player_code = "tp" if player == "self" else "1-tp" if player == "opponent" else "p"
        
        return [
            f"function s.drawtg{effect_num}(e,tp,eg,ep,ev,re,r,rp,chk)",
            f"    if chk==0 then return Duel.IsPlayerCanDraw({player_code},{amount}) end",
            f"    Duel.SetOperationInfo(0,CATEGORY_DRAW,nil,0,{player_code},{amount})",
            "end",
            "",
            f"function s.drawop{effect_num}(e,tp,eg,ep,ev,re,r,rp)",
            f"    Duel.Draw({player_code},{amount},REASON_EFFECT)",
            "end"
        ]

    def generate_stat_change_effect(self, effect_num, options):
        stat = options.get('stat', 'atk')
        amount = options.get('amount', '500')
        duration = options.get('duration', 'turn')
        
        reset = "RESET_EVENT+RESETS_STANDARD+RESET_PHASE+PHASE_END" if duration == "turn" else "RESET_EVENT+RESETS_STANDARD"
        
        return [
            f"function s.atktg{effect_num}(e,tp,eg,ep,ev,re,r,rp,chk,chkc)",
            "    if chk==0 then return Duel.IsExistingTarget(Card.IsFaceup,tp,LOCATION_MZONE,LOCATION_MZONE,1,nil) end",
            "    Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_TARGET)",
            "    Duel.SelectTarget(tp,Card.IsFaceup,tp,LOCATION_MZONE,LOCATION_MZONE,1,1,nil)",
            "end",
            "",
            f"function s.atkop{effect_num}(e,tp,eg,ep,ev,re,r,rp)",
            "    local tc=Duel.GetFirstTarget()",
            "    if tc and tc:IsRelateToEffect(e) and tc:IsFaceup() then",
            f"        local e1=Effect.CreateEffect(e:GetHandler())",
            f"        e1:SetType(EFFECT_TYPE_SINGLE)",
            f"        e1:SetCode(EFFECT_UPDATE_ATTACK)",
            f"        e1:SetValue({amount})",
            f"        e1:SetReset({reset})",
            "        tc:RegisterEffect(e1)",
            "    end",
            "end"
        ]

    def load_script(self):
        current_text = self.script_text.get("1.0", tk.END).strip()
        if current_text and not tk.messagebox.askyesno("Load Script", 
            "Loading a script will replace the current script. Continue?"):
            return
            
        file_path = tk.filedialog.askopenfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("All files", "*.*")],
            title="Load Script"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    script = file.read()
                    self.script_text.delete("1.0", tk.END)
                    self.script_text.insert("1.0", script)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load script: {str(e)}")

    def save_script(self):
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("All files", "*.*")],
            title="Save Script"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    script = self.script_text.get("1.0", tk.END)
                    file.write(script)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to save script: {str(e)}")

    def clear_script(self):
        if tk.messagebox.askyesno("Clear Script", "Are you sure you want to clear the script?"):
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert("1.0", """--Card Script
local s,id=GetID()
function s.initial_effect(c)

end""")

class CreateToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
    
    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
    
    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None 