import random
import re
import warnings
from utils.utils import *

class CommandGenerator:

    def __init__(self, league_names, league, location_names, placement_location_names, room_names, object_names,
                 object_categories_plural, object_categories_singular, unknown_objs):
        
        self.league_names = league_names
        self.league = league
        self.location_names = location_names
        self.placement_location_names = placement_location_names
        self.room_names = room_names
        self.object_names = object_names
        self.object_categories_plural = object_categories_plural
        self.object_categories_singular = object_categories_singular
        self.using_unknown_objs = unknown_objs

        # Load grammar data
        if self.league == self.league_names[2]:
            grammar_data_file_path = './params/wp2/grammar.yaml'
        elif self.league == self.league_names[3]:
            grammar_data_file_path = './params/wp3/grammar.yaml'
        else:
            print("Not possible to load grammar.yaml for league " + self.league)
            exit(1)

        grammar_data = read_yaml_file(file_path=grammar_data_file_path)

        self.verb_dict = grammar_data['verb_dict']
        self.prep_dict = grammar_data['prep_dict']
        self.connector_list = grammar_data['connector_list']


    def generate_command_start(self, cmd_category="", difficulty=0):
        # Load commands
        if self.league == self.league_names[2]:
            cmd_data_file_path = './params/wp2/commands.yaml'
        elif self.league == self.league_names[3]:
            cmd_data_file_path = './params/wp3/commands.yaml'
        else:
            print("Not possible to load commands.yaml for league " + self.league)
            exit(1)

        cmd_data = read_yaml_file(file_path=cmd_data_file_path)

        # Object manipulation and perception commands
        object_cmd_list = save_parameters(cmd_data, "object_cmd_list")

         # Select command list
        cmd_list = object_cmd_list

        command = random.choice(cmd_list)
        command_string = self.get_command_string(command, cmd_category, difficulty)

        if command_string == "WARNING":
            return command_string

        # Replace placeholders with values
        for ph in re.findall(r'(\{\w+\})', command_string, re.DOTALL):
            command_string = command_string.replace(ph, self.insert_placeholders(ph))

        # Adjust for articles (a/an)
        command_string = self.adjust_articles(command_string)

        # Eliminate double mentions of location
        command_string = self.eliminate_double_mentions(command_string)

        # Check dishwasher 
        if self.league == self.league_names[2]:
            command_string = self.verify_dishwasher_constraint(command_string)

        return command_string.replace('{', '').replace('}', '')

    def get_command_string(self, command, cmd_category, difficulty):
        # Define command patterns
        command_patterns = {
            "takeObjFromPlcmt": "{takeVerb} the {obj} {fromLocPrep} the {plcmtLoc} and " + self.generate_command_followup("hasObj", cmd_category, difficulty),
        }
        return command_patterns.get(command, "WARNING")

    def generate_command_followup(self, type, cmd_category="", difficulty=0):
        """Generates follow-up commands based on the type."""
        followup_commands = {
            "hasObj": ["placeObjOnPlcmt", "deliverObjToNameAtBeac"],
        }

        # Determine command list based on type and category
        if type in followup_commands:
            if type == "atLoc":
                cmd_list = followup_commands[type].get(cmd_category, followup_commands[type]["default"])
            else:
                cmd_list = followup_commands[type]
        else:
            return "WARNING"

        command = random.choice(cmd_list)

        # Define follow-up command patterns
        if self.league == self.league_names[2]:
            followup_patterns = {
                "placeObjOnPlcmt": "{placeVerb} it {onLocPrep} the {plcmtLoc2}",
                "deliverObjToNameAtBeac": "{deliverVerb} it {deliverPrep} person {inLocPrep} the {room}",
            }
        elif self.league == self.league_names[3]:
            followup_patterns = {
                "placeObjOnPlcmt": "{placeVerb} it {onLocPrep} the {plcmtLoc2}",
                "deliverObjToNameAtBeac": "{deliverVerb} it {deliverPrep} the person {inLocPrep} the {plcmtLoc2}",
            }
        else:
            print("It is not possible to generate follow up command, due to league in question " + self.league)
            exit(1)

        # Get the follow-up pattern for the command
        followup_command = followup_patterns.get(command, "WARNING")

        # Replace placeholders
        if "{followup}" in followup_command:
            # Mapping command to follow-up types
            followup_type_map = {
                "findObj": "foundObj",
                "takeObj": "hasObj"
            }

            # Determine the follow-up type based on the command
            followup_type = next(
                (ftype for cmd_key, ftype in followup_type_map.items() if cmd_key in command), 
                "foundPers"  # Default to "foundPers" if no match
            )

            # Generate follow-up command
            followup = self.generate_command_followup(followup_type)

            # Replace placeholder with the generated follow-up
            followup_command = followup_command.replace("{followup}", followup)


        return followup_command


    def insert_placeholders(self, ph):
        """Inserts the appropriate value for a given placeholder."""
        ph = ph.strip('{}')

        """Cases such as obj_singCat, loc2_room2, ..., it choose randomly loc2 or room2, in loc2_room2 example."""
        if len(ph.split('_')) > 1:
            ph = random.choice(ph.split('_'))

        placeholder_map = {
            # Verb mappings
            "goVerb": lambda: random.choice(self.verb_dict["go"]),
            "takeVerb": lambda: random.choice(self.verb_dict["take"]),
            "findVerb": lambda: random.choice(self.verb_dict["find"]),
            "meetVerb": lambda: random.choice(self.verb_dict["meet"]),
            "countVerb": lambda: random.choice(self.verb_dict["count"]),
            "tellVerb": lambda: random.choice(self.verb_dict["tell"]),
            "deliverVerb": lambda: random.choice(self.verb_dict["deliver"]),
            "talkVerb": lambda: random.choice(self.verb_dict["talk"]),
            "answerVerb": lambda: random.choice(self.verb_dict["answer"]),
            "followVerb": lambda: random.choice(self.verb_dict["follow"]),
            "placeVerb": lambda: random.choice(self.verb_dict["place"]),
            "guideVerb": lambda: random.choice(self.verb_dict["guide"]),
            "greetVerb": lambda: random.choice(self.verb_dict["greet"]),
            "bringVerb": lambda: random.choice(self.verb_dict["bring"]),
            # Preposition mappings
            "toLocPrep": lambda: random.choice(self.prep_dict["toLocPrep"]),
            "fromLocPrep": lambda: random.choice(self.prep_dict["fromLocPrep"]),
            "inLocPrep": lambda: random.choice(self.prep_dict["inLocPrep"]),
            "onLocPrep": lambda: random.choice(self.prep_dict["onLocPrep"]),
            "atLocPrep": lambda: random.choice(self.prep_dict["atLocPrep"]),
            "deliverPrep": lambda: random.choice(self.prep_dict["deliverPrep"]),
            "talkPrep": lambda: random.choice(self.prep_dict["talkPrep"]),
            "ofPrsPrep": lambda: random.choice(self.prep_dict["ofPrsPrep"]),
            # Placeholder mappings
            "connector": lambda: random.choice(self.connector_list),
            #
            "plcmtLoc": lambda: random.choice(self.placement_location_names),
            "loc": lambda: random.choice(self.location_names),
            "room": lambda: random.choice(self.room_names),
            "plcmtLoc2": lambda: "plcmtLoc2",
            "loc2": lambda: "loc2",
            "room2": lambda: "room2",
            "inRoom": lambda: random.choice(self.prep_dict["inLocPrep"]) + " the " + random.choice(self.room_names),
            "atLoc": lambda: random.choice(self.prep_dict["atLocPrep"]) + " the " + random.choice(self.location_names),
            #
            "obj": lambda: random.choice(self.object_names),
            "singCat": lambda: random.choice(self.object_categories_singular),
            "plurCat": lambda: random.choice(self.object_categories_plural),
            #
            "art": lambda: "{art}",
        }

        # Return mapped choice or warning
        return placeholder_map.get(ph, lambda: warnings.warn(f"Placeholder not covered: {ph}"))()

    def adjust_articles(self, command_string):
        """Adjust articles (a/an) in the command string."""
        art_ph = re.findall(r'\{(art)\}\s*([A-Za-z])', command_string, re.DOTALL)
        if art_ph:
            command_string = command_string.replace("art", "an" if art_ph[0][1].lower() in ["a", "e", "i", "o", "u"] else "a")
        
        return command_string

    def eliminate_double_mentions(self, command_string):
        """Eliminate double mentions of locations."""
        for placeholder, choices in [("loc2", self.location_names), ("room2", self.room_names), ("plcmtLoc2", self.placement_location_names)]:
            if placeholder in command_string:
                command_string = command_string.replace(placeholder, random.choice([x for x in choices if x not in command_string]))
        return command_string
    
    def verify_dishwasher_constraint(self, command_string):
        # Load objects data from YAML file
        if self.using_unknown_objs:
            objects_data = read_yaml_file('./params/wp2/unknown_params.yaml')
        else:
            objects_data = read_yaml_file('./params/wp2/params.yaml')
        
        # Find the object in command_string that matches any item in objects_data
        current_object = next(
            (
                obj 
                for category in objects_data['objects'] 
                for item in category.values() 
                if isinstance(item, list)  # Ensure we are accessing the list with category info
                for obj in item[1]['items']  # Access the items list
                if obj in command_string
            ), 
            None
        )

        # Debug print to check what object was matched
        # print("Extracted object:", current_object)

        # Check if "dishwasher" is mentioned in the command
        if "dishwasher" in command_string:
            # Locate items under the "dishes" category
            dish_items = next(
                (
                    item[1]['items'] 
                    for category in objects_data['objects'] 
                    for key, item in category.items() 
                    if key == "dishes"  # Access only the dishes category
                ), 
                []
            )
            # print(dish_items)
            # Check if the current object is in the dish category
            if current_object not in dish_items:
                # Replace with a random valid object from the "dishes" category
                replacement_object = random.choice(dish_items)
                print(f"Replacing '{current_object}' with valid dish item '{replacement_object}'.")

                # Replace the invalid object in the command string
                command_string = re.sub(r'\b' + re.escape(current_object) + r'\b', replacement_object, command_string)

        return command_string 
