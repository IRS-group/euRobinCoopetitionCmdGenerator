import yaml

def read_yaml_file(file_path):
    try:
        # Open and read the YAML file
        with open(file_path, 'r') as file:
            # Load the YAML content
            yaml_content = yaml.safe_load(file)
    except:
        print("Could not open yaml file: " + file_path)
        exit(1)
    
    return yaml_content


def parse_room_data(data):
    # Initialize empty lists to store the extracted information
    room_names = []
    location_names = []
    valid_placement_locations = []
    valid_pick_locations = []

    # Loop through each room in the provided data
    for room in data:
        # Extract the room name (key) and its information (value)
        room_name, room_info = list(room.items())[0]
        room_names.append(room_name)

        # Extract locations for the current room
        locations = room_info[0]['locations']
        for location in locations:
            # Extract the location name (key) and its properties (value)
            location_name, location_info = list(location.items())[0]
            location_names.append(location_name)

            # Check for valid placement locations
            if location_info[0]['placement_location']:
                valid_placement_locations.append(location_name)
            # Check for valid pick locations
            if location_info[1]['pick_location']:
                valid_pick_locations.append(location_name)

    return room_names, location_names, valid_placement_locations, valid_pick_locations



def parse_objects(data):
    # Initialize empty lists to hold the results
    category_plural = []
    category_values = []
    all_items = []

    # Loop through each dictionary in the provided list
    for entry in data:
        # Extract the plural category name (key)
        plural_name = list(entry.keys())[0]
        category_plural.append(plural_name)

        # Extract the category value and items from the entry
        category_info = entry[plural_name][0]['category']
        items = entry[plural_name][1]['items']

        # Append the category value and items to their respective lists
        category_values.append(category_info)
        all_items.extend(items)  # Use extend to add multiple items to the list

    return category_plural, category_values, all_items



def save_parameters(params, var):
    try:
        arr = params[var]
    except:
        print("Could not save " + var + "! Please make it exists in the Parameter File!")
        exit(1)
    
    return arr