# euRobin Command Generator

This repository provides a command generator tailored for the euRobin Coopetition, supporting both Service Robots League and Outdoors Robots League. It includes Docker support and can be easily launched for either league. Below are the steps to install dependencies, run the application locally, or use Docker.



## Requirements
To run the project locally, make sure you have the following installed:

- Tkinter: Required for the GUI.
```
sudo apt-get install python3-tk
```
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



## Docker
If you prefer to run this repository in a Docker container, follow the steps below:

1. Navigate to the Docker folder (assuming the project was clone to your home directory):
```
cd ~/euRobin-Command-Generator/docker/
```

2. Build the Docker image using the ```Makefile```:
```
make build
```

3. Set execution permissions for the launch scripts:
```
chmod +x launch_cmd_gen_wp2.sh && chmod +x launch_cmd_gen_wp3.sh
```

4. Launch the Docker container for the desired league:
#### Service Robots League
```
./launch_cmd_gen_wp2
```

#### Outdoors Robots League
```
./launch_cmd_gen_wp3
```

### GUI in Docker
Since this application uses a graphical interface, running it in Docker requires special attention to GUI rendering. This can be done by mounting the X11 socket (/tmp/.X11-unix) or by using VNC or X11 forwarding. The provided launch scripts handle X11 mounting, allowing the GUI to display on your host machine.






## Running Locally

To run the command generator locally, you can use the following commands:

#### Service Robots League
```
python3 run.py --league wp2
```

#### Outdoors Robots League
```
python3 run.py --league wp3
```

### Test Mode

You can also run the command generator in test mode for the Service Robots or Outdoors Robots League, specifying the number of tests:

```
python3 run.py --league wp2 --test 500
python3 run.py --league wp3 --test 500
```





# Acknowledgements

This repository is an optimized, cleaned-up, and customized version of the command generator from https://github.com/johaq/, specifically designed for **RoboCup** and the **euRobin Coopetition**.

