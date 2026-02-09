# TCP-IP-Python-V4 Project Documentation

## ⚠️ V4.0.0 BREAKING CHANGES

**Version 4.0.0 introduces architectural refactoring with breaking changes!**

### Major Changes:

1. **Modular Package Structure**: Code refactored into `dobot_api` Python package with V3 architecture pattern
2. **Separated Movement API**: Restored `DobotApiMove` class (V3-style) for movement commands
3. **Import Path Changes**:
   ```python
   # New import method
   from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack
   
   # Create instances (V3 pattern: separated dashboard and move instances)
   dashboard = DobotApiDashboard(ip, 29999)
   move = DobotApiMove(ip, 29999)  # Same port, independent API
   feed = DobotApiFeedBack(ip, 30004)
   
   # Control commands through dashboard
   dashboard.EnableRobot()
   dashboard.VelL(50)
   
   # Movement commands through move instance
   move.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)  # coordinateMode: 0=pose, 1=joint
   ```

4. **Package Installation**: Now supports `pip install -e .` development mode
5. **Detailed Migration Guide**: See [MIGRATION_V3_TO_V4.md](MIGRATION_V3_TO_V4.md) for V3 vs V4 API differences

### Quick Migration:
- All V4 method signatures and features remain unchanged
- Movement commands now go through `move` instance instead of `dashboard`
- Examples updated to new architecture, see `examples/` directory

---

## Project Overview

This project is the Dobot Robot TCP-IP-CR-Python-V4 secondary development API program, used to control Dobot robots through TCP/IP protocol. The project provides complete robot control interfaces, including motion control, status monitoring, alarm handling, and other functions.

**V4.0.0 adopts modular architecture**, organizing code into a professional Python package for improved maintainability and code clarity.

## Environment Requirements

### Python Version

- Python 3.9 or higher

### Installation Method

#### Development Mode (Recommended)

```bash
# Clone the project
git clone https://github.com/Dobot-Arm/TCP-IP-Python-V4.git
cd TCP-IP-Python-V4

# Install as editable package (development mode)
pip install -e .
```

#### Manual Dependency Installation

```bash
# Install only numpy dependency
pip install numpy
```

### Required Libraries

- `numpy>=1.20.0` - Numerical computation and data structures
- Python built-in libraries: `socket`, `threading`, `time`, `json`, `re`
- Optional: `tkinter` (usually comes with Python, for GUI examples)

### Network Configuration Requirements

- Local machine IP address needs to be set to 192.168.X.X network segment
- Robot needs to be switched to TCP/IP mode
- Ensure ports 29999 and 30004 are not occupied

## Main Program Files and Functions

### 1. dobot_api/ Package (Core API)

**V4.0.0 Modular Architecture**: Code refactored into professional Python package

#### dobot_api/base.py
- **DobotApi**: Base TCP communication class
- **MyType**: V4 feedback data structure definitions (PascalCase fields)
- Type hints and improved error handling

#### dobot_api/dashboard.py  
- **DobotApiDashboard**: Robot control and configuration commands
  - Enable/Disable: `EnableRobot()`, `DisableRobot()`
  - Speed control: `VelJ()`, `VelL()`, `AccJ()`, `AccL()`
  - Coordinate systems: `User()`, `Tool()`, `SetUser()`, `SetTool()`
  - IO operations: `DO()`, `GetDO()`, `AO()`, `GetAO()`
  - Alarm handling: `ClearError()`, `GetError(language)`
  - V4 new features: Kinematics, force control settings, collision detection, SafeSkin
  
#### dobot_api/move.py
- **DobotApiMove**: Movement commands (V3-style separated class, V4 signatures)
  - Basic movements: `MovJ()`, `MovL()`, `Arc()`, `Circle()`
  - Servo control: `ServoJ()`, `ServoP()`
  - Relative movements: `RelMovJUser()`, `RelMovLUser()`, `RelJointMovJ()`
  - V4 new features: `RunTo()`, `MovS()`, conveyor tracking, welding, force control movements
  - **Note**: All movement commands require `coordinateMode` parameter (0=pose, 1=joint)

#### dobot_api/feedback.py
- **DobotApiFeedBack**: Real-time status feedback
  - Get robot status (1440-byte data packet)
  - V4 fields use PascalCase: `QActual`, `DigitalInputs`, `RobotMode`, etc.

#### dobot_api/utils.py
- Alarm file reading: `alarmAlarmJsonFile()`

### 2. examples/ Directory

#### examples/basic_demo.py
- Basic robot control example (updated to V4.0.0)
- Demonstrates separated dashboard and move instances
- Includes motion loops and feedback monitoring

#### examples/error_handling.py  
- GetError interface usage example
- Multi-language alarm information retrieval
- Alarm monitoring class implementation

#### examples/main.py
- Project main entry example

#### examples/ui_demo/
- **main_UI.py**: GUI main program
- **ui.py**: Graphical user interface (updated to V4.0.0)
  - Visual robot control
  - Real-time status display
  - Supports drag teaching and jogging

### 3. Documentation Files

#### MIGRATION_V3_TO_V4.md (New)
- **Detailed V3 vs V4 API comparison**
- Method signature changes
- Migration checklist
- Code example comparisons

#### GetError_README.md / GetError_README_EN.md
- Detailed GetError interface documentation (Chinese/English)

## Project Directory Structure

```
TCP-IP-Python-V4/
├── dobot_api/                 # Core API package (V4.0.0 new architecture)
│   ├── __init__.py           # Package exports
│   ├── base.py               # Base communication class
│   ├── dashboard.py          # Control commands
│   ├── move.py               # Movement commands (V3-style separation)
│   ├── feedback.py           # Status feedback
│   ├── utils.py              # Utility functions
│   └── files/                # Alarm configuration files
│       ├── alarmController.json
│       ├── alarmController.py
│       ├── alarmServo.json
│       └── alarmServo.py
├── examples/                  # Example programs (V4.0.0 updated)
│   ├── basic_demo.py         # Basic example
│   ├── error_handling.py     # Alarm handling example
│   ├── main.py               # Main program entry
│   └── ui_demo/              # GUI examples
│       ├── main_UI.py
│       └── ui.py
├── pyproject.toml            # Package configuration file (new)
├── MIGRATION_V3_TO_V4.md     # API migration guide (new)
├── README.md                 # Chinese documentation
├── README-EN.md              # English documentation
├── GetError_README.md        # GetError Chinese documentation
├── GetError_README_EN.md     # GetError English documentation
├── LICENSE
└── picture/                  # Image resources
```

## Quick Start

### 1. Environment Setup

```bash
# Clone the project
git clone https://github.com/Dobot-Arm/TCP-IP-CR-Python-V4.git
cd TCP-IP-Python-V4

# Install package (development mode)
pip install -e .
```

### 2. Network Configuration

- Set local machine IP to 192.168.X.X network segment
- Ensure robot is in TCP/IP mode
- Ensure ports 29999 and 30004/30005 are not occupied

### 3. Basic Usage Example

```python
from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

# Connect to robot (V4.0.0 architecture: separated dashboard and move)
ip = "192.168.1.6"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 29999)        # Same port, independent movement API
feed = DobotApiFeedBack(ip, 30004)

# Enable robot
dashboard.EnableRobot()
dashboard.ClearError()

# Set speed
dashboard.VelL(50)  # V4 uses VelL (V3 was SpeedL)

# Movement commands (through move instance)
# coordinateMode: 0=Cartesian pose, 1=joint angles
move.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)

# Read feedback (V4 uses PascalCase fields)
data = feed.feedBackData()
if data is not None:
    joint_pos = data['QActual'][0]  # Joint position
    robot_mode = data['RobotMode'][0]  # Robot mode
    
# Cleanup
dashboard.DisableRobot()
dashboard.close()
move.close()
feed.close()
```

### 4. Run Example Programs

```bash
# Run basic example
python examples/main.py

# Run GUI interface
python examples/ui_demo/main_UI.py

# Run alarm handling example
python examples/error_handling.py
```


## Common Problem Solutions

### 1. ModuleNotFoundError: No module named 'numpy'

**Solution**: Install numpy library

```bash
pip install numpy
```

### 2. Connection refused, IP:Port has been occupied

**Solution**: Check if port 29999 is occupied, close the program occupying that port

### 3. Control Mode Is Not Tcp

**Solution**: Switch robot mode to TCP/IP mode in DobotStudio Pro

### 4. Robot Status Abnormal

| Output Message                        | Robot Status        | Solution                           |
| ------------------------------------- | ------------------- | ---------------------------------- |
| Command execution failed              | Command failed      | Check command parameters and robot status |
| The robot is in an error state       | Robot error state   | Clear alarms and retry             |
| The robot is in emergency stop state | Emergency stop state| Release emergency stop button      |
| The robot is in power down state     | Power down state    | Power on the robot                 |

## Precautions

1. **Safety First**: Ensure the robot is in a safe position before running examples to prevent collisions
2. **Network Configuration**: Ensure correct network configuration with IP addresses in the same network segment
3. **Port Occupation**: Ensure ports 29999 and 30004/30005 are not occupied by other programs
4. **Robot Mode**: Ensure the robot is in TCP/IP control mode
5. **V4.0.0 Changes**: Note the new architecture's import and usage patterns, movement commands go through `move` instance
6. **coordinateMode Parameter**: All movement commands require explicit coordinateMode specification (0=pose, 1=joint)

## V4.0.0 Architecture Advantages

- ✅ **Modular Design**: Clear code organization, easy to maintain
- ✅ **Separation of Concerns**: Control and movement commands separated (V3-style)
- ✅ **Type Hints**: Complete type annotations, better IDE support
- ✅ **Improved Error Handling**: Clear exceptions and error messages
- ✅ **Complete V4 Features**: Retains all V4 advanced features (force control, kinematics, welding, etc.)
- ✅ **Package Management**: Supports standard pip installation

## Technical Support

If you encounter problems, please refer to:

- **API Migration Guide**: [MIGRATION_V3_TO_V4.md](MIGRATION_V3_TO_V4.md)
- **Example Code**: `examples/` directory
- **GetError Documentation**: GetError_README_EN.md
- **Dobot Official Support**: https://www.dobot.cc/

---

**Version**: V4.0.0  
**Update Date**: 2026-02-09  
**Maintainer**: Dobot  
**Major Changes**: Modular architecture refactoring, V3-style separated movement API
