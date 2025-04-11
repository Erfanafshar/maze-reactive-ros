# Maze Reactive Controller (ROS + Gazebo)

This project implements a reactive robot controller for autonomous navigation in a maze-like environment using ROS and Gazebo. The system is built around two ROS nodes: `obstacle-detector` and `velocity-controller`. These nodes enable a TurtleBot to navigate the maze safely and continuously based on real-time sensor input.

## System Overview

The robot operates in a closed-loop configuration with no prior knowledge of the maze layout. Navigation decisions are based solely on live sensor data, specifically from the laser scanner and bumper sensors. The goal is continuous motion through the maze while avoiding collisions.

### Node Descriptions

- **`obstacle-detector`**  
  Subscribes to `/scan` and `/mobile_base/events/bumper` topics. Processes sensor data to detect obstacles within the robot’s field of view. Publishes a Boolean flag or directional signal to the `obstacle_detected` topic, indicating whether the path ahead is blocked.

- **`velocity-controller`**  
  Subscribes to `obstacle_detected` and issues velocity commands to the `/cmd_vel` topic. When no obstacle is detected, the robot moves forward. If an obstacle is present, the node adjusts angular velocity to steer the robot away and prevent collision.

### Features Implemented

- Reactive control based on real-time sensory feedback
- Continuous maze traversal without prior mapping or planning
- Basic obstacle avoidance using laser scan and bumper data
- Modular ROS node separation for sensing and control
- Support for long-duration simulation (15+ minutes) to validate system stability

### Evaluation Metrics

The system was tested in the provided `funky-maze.world` environment. From a fixed starting pose near the maze origin:

- The robot successfully completed multiple loops around the maze
- No critical collisions occurred during the 15-minute run
- Bumper triggers were minimal or zero depending on angular adjustment strategy
- Average velocity remained within the safe operational bounds of TurtleBot’s dynamics

Optional measures such as path smoothness and loop counts were tracked manually or through basic script logging.
