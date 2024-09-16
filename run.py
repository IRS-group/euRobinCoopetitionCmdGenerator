import argparse
import tkinter as tk
from cmd_gen import CommandGenerator
from utils.utils import *
from gui import CommandGeneratorGUI

def main(test=False, league="wp2", cmds_number=0):
    ######################################################################
    # LOAD TASK PARAMETERS
    # (objects, rooms, person names)
    ######################################################################
    league_names = ["wp0", "wp1", "wp2", "wp3"]

    if league == league_names[2]:
        task_params_file_path = './params/wp2/params.yaml'
    elif league == league_names[3]:
        task_params_file_path = './params/wp3/params.yaml'
    else:
        print("Could not load params.yaml for league " + league)
        exit(1)

    task_params = read_yaml_file(file_path=task_params_file_path)  
    
    rooms_data = save_parameters(task_params, "room_names")
    room_names, location_names, placement_location_names = parse_room_data(rooms_data)
    
    object_data = save_parameters(task_params, "objects")
    object_categories_plural, object_categories_singular, object_names = parse_objects(object_data)
    
    ######################################################################
    # CREATE COMMAND GENERATOR
    # ()
    ######################################################################
    generator = CommandGenerator(league_names, league, location_names, placement_location_names, room_names, object_names,
                                 object_categories_plural, object_categories_singular)
    
    if test:
        for _ in range(cmds_number):  
            command = generator.generate_command_start(cmd_category="")
            command = command[0].upper() + command[1:]
            print(command)
    else:
        root = tk.Tk()
        app = CommandGeneratorGUI(root, generator)
        root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Generator")
    parser.add_argument('--league', type=str, default=0, 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    parser.add_argument('--test', type=int, default=0, 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    
    args = parser.parse_args()
    
    main(test=args.test > 0, league=args.league, cmds_number=args.test)
