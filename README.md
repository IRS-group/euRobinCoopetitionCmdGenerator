# euRobin Command Generator

This repository provides a command generator tailored for the euRobin Coopetition, supporting both Service Robots League and Outdoors Robots League. It includes Docker support and can be easily launched for either league. Below are the steps to install dependencies, run the application locally, or use Docker.



## Requirements
To run the project locally, make sure you have the following installed:

1. System dependencies:

    - Tkinter: Required for the GUI.
    ```
    sudo apt-get install python3-tk
    ```

2. Python dependencies: 
    - Pillow: Used for image processing.
    ```
    pip install Pillow==9.5.0
    ```

    - PyYAML: To handle YAML configuration files.
    ```
    pip install pyyaml
    ```

    QRCode: Generates QR codes based on the command.
    ```
    pip install qrcode[pil]
    ```

    Alternatively, install all Python dependencies from the ```requirements.txt``` file:
    ```
    pip install -r requirements.txt
    ```

## Virtual Environment
To create and activate a virtual environment for this project:
 ```
virtualenv command_generator && source commmand_generator/bin/activate
```

Next, install the required dependencies:

```
pip install -r requirements.txt
```

For instructions on running the command generator, refer to the **Running Locally** section below.

When you're finished, deactivate the virtual environment with:
```
deactivate
```

## Docker
If you prefer to run this repository in a Docker container, follow the steps below:

1. Navigate to the Docker folder (assuming the project was clone to your home directory):
    ```
    cd ~/euRobinCommandGenerator/docker/
    ```

2. Build the Docker image using the ```Makefile```:
    ```
    sudo make build
    ```

3. Set execution permissions for the launch scripts:
    ```
    sudo chmod +x launch_cmd_gen_wp2.sh && sudo chmod +x launch_cmd_gen_wp3.sh
    ```

4. Launch the Docker container for the desired league:
    #### Service Robots League
    ```
    ./launch_cmd_gen_wp2.sh
    ```

    To run with the **unknown objects**:
    ```
    ./launch_cmd_gen_wp2_unknown_objs
    ```

    #### Outdoors Robots League
    ```
    ./launch_cmd_gen_wp3.sh
    ```

    To run it for the **drones**:
    ```
    ./launch_cmd_gen_wp3_drones.sh
    ```

5. If you no longer need the Docker images, you can clean them up by running:
    ```
    make clean
    ```

### GUI in Docker
Since this application uses a graphical interface, running it in Docker requires special attention to GUI rendering. This can be done by mounting the X11 socket (/tmp/.X11-unix) or by using VNC or X11 forwarding. The provided launch scripts handle X11 mounting, allowing the GUI to display on your host machine.






## Running Locally

To run the command generator locally, you can use the following commands:

#### Service Robots League
```
python3 run.py --league wp2
```

To run with the **unknown objects**:
```
python3 run.py --league wp2 --unknown_objs true
```


#### Outdoors Robots League
```
python3 run.py --league wp3
```

To run it for the **drones**:
```
python run.py --league wp3 --drones true
```

### Test Mode

You can also run the command generator in test mode for the Service Robots or Outdoors Robots League, specifying the number of tests:

```
python3 run.py --league wp2 --test 500
python3 run.py --league wp3 --test 500
```





# Acknowledgements

This repository is an optimized, cleaned-up, and customized version of the command generator from https://github.com/johaq/, specifically designed for **RoboCup** and the **euRobin Coopetition**.

