import yaml
import random
import argparse
import sys
import os

# Function to load teams from the specified league YAML file
def load_teams(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            return data['teams']
    except FileNotFoundError:
        print(f"Error: The file '{yaml_file}' was not found.")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print("Error reading YAML file:", exc)
        sys.exit(1)

# Function to shuffle and print the team execution order
def generate_execution_order(teams):
    random.shuffle(teams)
    print("Random Execution Order:")
    for i, team in enumerate(teams, start=1):
        print(f"{i}. {team}")

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random execution order for teams")
    parser.add_argument("--league", type=str, required=True, help="Specify the league (e.g., wp1, wp2, wp3)")
    args = parser.parse_args()

    league_names = ["wp0", "wp1", "wp2", "wp3"]
    league = args.league

    if league == league_names[1]:
        task_params_file_path = './params/wp1/params.yaml'
    elif league == league_names[2]:
        task_params_file_path = './params/wp2/params.yaml'
    elif league == league_names[3]:
        task_params_file_path = './params/wp3/params.yaml'
    else:
        print("Could not load params.yaml for league " + league)
        exit(1)

    # Load teams and generate random order
    teams = load_teams(task_params_file_path)
    generate_execution_order(teams)
