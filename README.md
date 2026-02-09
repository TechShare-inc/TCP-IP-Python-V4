# Dobot TCP-IP Python API V4

**Modern Python API for Dobot CR-series robots with comprehensive i18n support**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-4.1.0-green.svg)](https://github.com/TechShare-inc/TCP-IP-Python-V4)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Note**: This repository is a clone from [Dobot-Arm/TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4) and is modified and maintained by TechShare Corp.

## Features

- 🌐 **Multi-language Support**: 10 languages for alarm messages (English, Chinese, Japanese, German, Korean, Vietnamese, Spanish, Russian, French)
- 🔌 **Modern Architecture**: Clean, modular package design with full type hints
- 🤖 **Complete Robot Control**: Motion, I/O, error handling, and real-time feedback
- 📦 **Easy Installation**: Standard pip package with minimal dependencies
- 🔍 **Advanced Error Monitoring**: HTTP-based alarm retrieval with local i18n translations
- 📝 **Comprehensive Logging**: Structured logging with loguru

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/TechShare-inc/TCP-IP-Python-V4.git
cd TCP-IP-Python-V4

# Install in development mode
pip install -e .
```

### Basic Example

```python
from dobot_api import DobotApiDashboard, DobotApiFeedBack

# Connect to robot
dashboard = DobotApiDashboard("192.168.1.6", 29999)
feed = DobotApiFeedBack("192.168.1.6", 30004)

# Enable and configure robot
dashboard.EnableRobot()
dashboard.ClearError()
dashboard.VelL(50)  # Set linear velocity to 50%

# Move to position (Cartesian coordinates)
dashboard.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)

# Read feedback
data = feed.feedBackData()
if data:
    print(f"Joint positions: {data['QActual']}")
    print(f"Robot mode: {data['RobotMode']}")

# Cleanup
dashboard.DisableRobot()
dashboard.close()
feed.close()
```

---

## Core Components

### 1. DobotApiDashboard
Main control interface for robot operations.

**Connection & Control**
```python
dashboard = DobotApiDashboard("192.168.1.6", 29999)
dashboard.EnableRobot()        # Enable robot
dashboard.DisableRobot()       # Disable robot
dashboard.ClearError()         # Clear error messages
dashboard.ResetRobot()         # Reset robot state
```

**Motion Commands**
```python
# Linear/Joint movements
dashboard.MovJ(x, y, z, rx, ry, rz, coordinateMode=0)  # Joint space
dashboard.MovL(x, y, z, rx, ry, rz, coordinateMode=0)  # Linear space
dashboard.Arc(x1, y1, z1, rx1, ry1, rz1, x2, y2, z2, rx2, ry2, rz2)

# Relative movements
dashboard.RelMovJUser(offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz)
dashboard.RelMovLUser(offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz)

# Servo control
dashboard.ServoJ(j1, j2, j3, j4, j5, j6)
dashboard.ServoP(x, y, z, rx, ry, rz)
```

**Speed & Acceleration**
```python
dashboard.VelL(velocity)       # Linear velocity (0-100%)
dashboard.VelJ(velocity)       # Joint velocity (0-100%)
dashboard.AccL(acceleration)   # Linear acceleration (0-100%)
dashboard.AccJ(acceleration)   # Joint acceleration (0-100%)
```

**I/O Operations**
```python
dashboard.DO(index, status)    # Digital output
dashboard.GetDO(index)         # Read digital output
dashboard.AO(index, value)     # Analog output
dashboard.GetAO(index)         # Read analog output
```

**Coordinate Systems**
```python
dashboard.User(index)          # Switch user coordinate system
dashboard.Tool(index)          # Switch tool coordinate system
dashboard.SetUser(x, y, z, rx, ry, rz)  # Define user coordinate
dashboard.SetTool(x, y, z, rx, ry, rz)  # Define tool coordinate
```

### 2. DobotApiFeedBack
Real-time robot status feedback. The robot provides **three feedback ports**:

- **Port 30004**: Real-time feedback every **8ms** (highest frequency, recommended for real-time control)
- **Port 30005**: Feedback every **200ms** (lower frequency, suitable for monitoring)
- **Port 30006**: Configurable feedback port, default **50ms** (adjustable rate)

```python
# Use port 30004 for real-time control (8ms updates)
feed = DobotApiFeedBack("192.168.1.6", 30004)

# Or use port 30005 for monitoring (200ms updates)
# feed = DobotApiFeedBack("192.168.1.6", 30005)

# Or use port 30006 for configurable rate (default 50ms)
# feed = DobotApiFeedBack("192.168.1.6", 30006)

data = feed.feedBackData()
if data:
    # Joint positions (radians)
    joint_positions = data['QActual']
    
    # Cartesian position
    tool_position = data['ToolVectorActual']
    
    # Robot state
    robot_mode = data['RobotMode']
    
    # I/O states
    digital_inputs = data['DigitalInputs']
    digital_outputs = data['DigitalOutputs']
    
    # Safety information
    safety_status = data['SafetyStatusBits']
```

**Data Packet Format**: Each feedback returns a 1440-byte data packet containing comprehensive robot state information.

### 3. RobotErrorMonitor
HTTP-based error monitoring with multi-language support.

```python
from dobot_api import RobotErrorMonitor

monitor = RobotErrorMonitor("192.168.1.6", dashboard_port=29999)

# Check for errors in specific language
has_errors = monitor.check_errors(language="en")

# Get raw error data
error_info = monitor.get_error_info(language="zh_CN")
if error_info and error_info.get("errMsg"):
    for error in error_info["errMsg"]:
        print(f"ID: {error['id']}")
        print(f"Description: {error['description']}")
        print(f"Solution: {error['solution']}")

# Save error log to file
monitor.save_error_log(filename="robot_errors.log")

# Continuous monitoring
monitor.monitor_errors(interval=10, language="en")  # Check every 10 seconds
```

**GetError Interface** (Dashboard method)
```python
# Get error information directly from dashboard
error_info = dashboard.GetError(language="en")

# Supported languages: zh_cn, zh_hant, en, ja, de, vi, es, fr, ko, ru
```

**Error Response Format**
```json
{
    "errMsg": [
        {
            "id": 1537,
            "level": 1,
            "description": "E-Stop button pressed",
            "solution": "Release the E-Stop button and clear the error",
            "mode": "Safety controller error",
            "date": "2025-01-09",
            "time": "10:30:15"
        }
    ]
}
```

### 4. AlarmI18n
Local internationalization for alarm messages (NEW in v4.1.0).

```python
from dobot_api import AlarmI18n

# Initialize with preferred language
i18n = AlarmI18n(default_language="en")

# Get controller alarm
alarm = i18n.get_controller_alarm(16)
print(f"Description: {alarm['description']}")
print(f"Solution: {alarm['solution']}")

# Get servo alarm
alarm = i18n.get_servo_alarm(8752)
print(f"Description: {alarm['description']}")

# Auto-detect alarm type by ID
alarm = i18n.get_alarm(16)  # Automatically determines if controller/servo

# Switch language dynamically
i18n.set_language("zh_CN")
alarm = i18n.get_controller_alarm(16)
print(f"描述: {alarm['description']}")

# Format alarm for display
formatted = i18n.format_alarm(16)
print(formatted)

# Enrich error data with translations
error_data = {"id": 16, "type": "controller"}
enriched = i18n.enrich_alarm(error_data)
print(enriched['description'])
```

**Supported Languages**
- `en` - English
- `zh_CN` - Simplified Chinese (简体中文)
- `zh_Hant` - Traditional Chinese (繁體中文)
- `ja` - Japanese (日本語)
- `de` - German (Deutsch)
- `ko` - Korean (한국어)
- `vi` - Vietnamese (Tiếng Việt)
- `es` - Spanish (Español)
- `ru` - Russian (Русский)
- `fr` - French (Français)

---

## Configuration

### Logging

The API uses [loguru](https://github.com/Delgan/loguru) for structured logging.

**Configure Log Level**
```python
import os

# Method 1: Environment variable (before import)
os.environ["DOBOT_LOG_LEVEL"] = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
from dobot_api import DobotApiDashboard

# Method 2: Configure logger directly
from dobot_api import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stderr, level="WARNING")
logger.add("robot.log", rotation="10 MB")  # Log to file with rotation
```

**Log Levels**
- `ERROR`: Connection failures, critical errors
- `WARNING`: Connection issues, retries
- `INFO`: Successful operations (default)
- `DEBUG`: Detailed operation data

### Error Handling

The API raises `ValueError` for invalid parameters:

```python
try:
    dashboard.MovJ(100, 0, 200, 0, 90, 0, coordinateMode=2)  # Invalid
except ValueError as e:
    print(f"Error: {e}")
    # ValueError: Invalid coordinateMode parameter: 2. Expected 0 (pose) or 1 (joint)
```

---

## Project Structure

```
TCP-IP-Python-V4/
├── dobot_api/                  # Core API package
│   ├── __init__.py            # Package exports
│   ├── base.py                # Base communication class
│   ├── dashboard.py           # Robot control commands
│   ├── feedback.py            # Real-time feedback
│   ├── error_monitor.py       # HTTP error monitoring
│   ├── i18n_manager.py        # Multi-language support (NEW)
│   ├── utils.py               # Utility functions
│   └── locales/               # Translation files (NEW)
│       ├── alarms.en.yml
│       ├── alarms.zh_CN.yml
│       ├── alarms.ja.yml
│       └── ...
├── examples/                   # Example programs
│   ├── basic_demo.py          # Basic usage
│   ├── error_handling.py      # Error monitoring demo
│   ├── i18n_demo.py           # I18n features demo (NEW)
│   └── main.py                # Main entry point
├── pyproject.toml             # Package configuration
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## Examples

### Complete Robot Control Flow

```python
from dobot_api import DobotApiDashboard, DobotApiFeedBack, AlarmI18n
import threading

# Initialize
dashboard = DobotApiDashboard("192.168.1.6", 29999)
feed = DobotApiFeedBack("192.168.1.6", 30004)
i18n = AlarmI18n("en")

# Enable robot
if "0" not in dashboard.EnableRobot():
    print("Failed to enable robot")
    exit(1)

dashboard.ClearError()

# Configure motion parameters
dashboard.VelL(50)
dashboard.AccL(50)

# Define positions
home = [300, 0, 200, 0, 90, 0]
pick = [400, 100, 150, 0, 90, 0]
place = [400, -100, 150, 0, 90, 0]

# Execute motion sequence
try:
    dashboard.MovJ(*home, coordinateMode=0)
    dashboard.MovL(*pick, coordinateMode=0)
    dashboard.DO(1, 1)  # Activate gripper
    dashboard.MovL(*place, coordinateMode=0)
    dashboard.DO(1, 0)  # Release gripper
    dashboard.MovJ(*home, coordinateMode=0)
    
except Exception as e:
    print(f"Motion error: {e}")
    
    # Check for alarms
    error_info = dashboard.GetError("en")
    if error_info and error_info.get("errMsg"):
        for error in error_info["errMsg"]:
            # Get detailed translation
            alarm = i18n.get_alarm(error["id"])
            print(f"Alarm: {alarm['description']}")
            print(f"Solution: {alarm['solution']}")

finally:
    dashboard.DisableRobot()
    dashboard.close()
    feed.close()
```

### Real-time Feedback Monitoring

```python
from dobot_api import DobotApiFeedBack
import threading

feed = DobotApiFeedBack("192.168.1.6", 30004)

def monitor_feedback():
    while True:
        data = feed.feedBackData()
        if data:
            # Validate data integrity
            if hex(data["TestValue"][0]) == "0x123456789abcdef":
                mode = data["RobotMode"][0]
                joints = data["QActual"]
                di = data["DigitalInputs"][0]
                
                print(f"Mode: {mode}, Joints: {joints[:3]}, DI: {bin(di)}")

# Run in background thread
thread = threading.Thread(target=monitor_feedback, daemon=True)
thread.start()
```

### Multi-language Error Display

```python
from dobot_api import AlarmI18n

i18n = AlarmI18n("en")

# Display same alarm in multiple languages
languages = ["en", "zh_CN", "ja", "de", "ko"]

print("Emergency Stop Alarm in Multiple Languages:\\n")
for lang in languages:
    i18n.set_language(lang)
    alarm = i18n.get_controller_alarm(16)
    print(f"[{lang}] {alarm['description']}")
```

---

## Requirements

| Requirement | Details |
|---|---|
| **Python** | 3.9 or higher |
| **Network** | Robot IP in 192.168.x.x range |
| **Ports** | 29999 (Dashboard), 30004 (Real-time 8ms), 30005 (200ms), 30006 (Configurable 50ms), 22000 (HTTP monitoring) |
| **Communication** | TCP/IP protocol |
| **Operating System** | Windows, Linux, macOS |
| **Dashboard Port** | 29999 |
| **Feedback Port (Real-time)** | 30004 (8ms updates) |
| **Feedback Port (Standard)** | 30005 (200ms updates) |
| **Feedback Port (Configurable)** | 30006 (default 50ms) |
| **HTTP Monitoring Port** | 22000 |
| **Robot Mode** | TCP/IP control mode enabled |

### Dependencies

```toml
numpy>=1.20.0
loguru>=0.7.0
python-i18n>=0.3.9
pyyaml>=6.0
```

---

## Troubleshooting

### Common Issues

**1. Connection Refused**
- Check if port 29999 is already in use
- Verify robot IP address is correct
- Ensure robot is in TCP/IP mode

**2. Import Error: No module named 'numpy'**
```bash
pip install numpy
```

**3. Robot Not Responding**
- Check network connectivity: `ping 192.168.x.x`
- Verify firewall settings
- Confirm robot is powered on and initialized

**4. Command Execution Failed**
- Clear robot errors: `dashboard.ClearError()`
- Check robot mode: Should be in normal operating mode
- Release emergency stop if pressed

**5. GetError Returns None**
- Verify port 22000 is accessible
- Check HTTP interface is enabled on robot
- Try different language code

### Error States

| Message | State | Solution |
|---------|-------|----------|
| "Control Mode Is Not Tcp" | Wrong control mode | Switch to TCP/IP mode in DobotStudio |
| "The robot is in an error state" | Robot error | Call `ClearError()` |
| "The robot is in emergency stop state" | E-stop active | Release emergency stop button |
| "The robot is in power down state" | Not powered | Power on the robot |

---

## API Reference

### coordinateMode Parameter

All movement commands require explicit `coordinateMode`:
- `0` = Cartesian pose coordinates (x, y, z, rx, ry, rz)
- `1` = Joint angle coordinates (j1, j2, j3, j4, j5, j6)

### Response Parsing

Dashboard commands return string responses:
```python
response = dashboard.EnableRobot()
# "0,{},EnableRobot();"  -> Success (code 0)
# "-1,{},EnableRobot();" -> Failure (code -1)

# Parse response
import re
match = re.search(r"(-?\d+)", response)
if match and int(match.group(1)) == 0:
    print("Success")
```

---

## Version History

### v4.1.0 (Current)
- ✨ Added `AlarmI18n` class for local multi-language alarm translation
- ✨ YAML-based translation files (10 languages)
- ✨ Enhanced `RobotErrorMonitor` with local i18n
- 🗑️ Removed deprecated `alarmAlarmJsonFile()` function
- 📦 Updated dependencies (python-i18n, pyyaml)
- 🐛 Improved error handling and logging

### v4.0.0
- 🏗️ Modular package architecture
- 📦 Pip installable package
- 🔧 Type hints and improved error handling
- 📝 Comprehensive logging with loguru
- 🌐 HTTP-based error monitoring

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

- **GitHub**: [TechShare-inc/TCP-IP-Python-V4](https://github.com/TechShare-inc/TCP-IP-Python-V4)
- **Issues**: [Report bugs](https://github.com/TechShare-inc/TCP-IP-Python-V4/issues)
- **Original Repository**: [Dobot-Arm/TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- **Documentation**: [Official Dobot Documentation](https://www.dobot.cc/)

---

**Modified and maintained by TechShare Corp.** | Version 4.1.0 | Last Updated: February 2026
