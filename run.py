import argparse
import tkinter as tk
from cmd_gen import CommandGenerator
from utils.utils import *
from gui import CommandGeneratorGUI

def str_to_bool(s):
    return s.strip().lower() == "true"

def main(test=False, league="wp2", cmds_number=0, unknown_objs=False, drones=False):
    ######################################################################
    # LOAD TASK PARAMETERS
    # (objects, rooms, person names)
    ######################################################################
    league_names = ["wp0", "wp1", "wp2", "wp3"]

    if league == league_names[2]:
        task_params_file_path = './params/wp2/params.yaml'
        if unknown_objs:
            task_params_file_path = './params/wp2/unknown_params.yaml'
    elif league == league_names[3]:
        task_params_file_path = './params/wp3/params.yaml'
        if drones:
            task_params_file_path = './params/wp3/drones_params.yaml'
    else:
        print("Could not load params.yaml for league " + league)
        exit(1)

    task_params = read_yaml_file(file_path=task_params_file_path)  
    
    rooms_data = save_parameters(task_params, "room_names")
    room_names, location_names, placement_location_names, pick_location_names = parse_room_data(rooms_data)
    
    object_data = save_parameters(task_params, "objects")
    object_categories_plural, object_categories_singular, object_names = parse_objects(object_data)
    
    ######################################################################
    # CREATE COMMAND GENERATOR
    # ()
    ######################################################################
    generator = CommandGenerator(league_names, league, location_names, placement_location_names, pick_location_names, room_names, object_names,
                                 object_categories_plural, object_categories_singular, unknown_objs)
    
    if test:
        for _ in range(cmds_number):  
            command = generator.generate_command_start(cmd_category="")
            command = command[0].upper() + command[1:]
            print(command)
    else:
        root = tk.Tk()
        app = CommandGeneratorGUI(root, generator, league)
        root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Generator")
    parser.add_argument('--league', type=str, default=0, 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    
    parser.add_argument('--unknown_objs', type=str, default="false", 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    
    parser.add_argument('--drones', type=str, default="false", 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    
    parser.add_argument('--test', type=int, default=0, 
                        help="Number of commands to generate for testing. If 0, GUI is used.")
    
    args = parser.parse_args()

    args.unknown_objs = str_to_bool(args.unknown_objs)
    args.drones = str_to_bool(args.drones)
    
    main(test=args.test > 0, league=args.league, cmds_number=args.test, unknown_objs=args.unknown_objs, drones=args.drones)
