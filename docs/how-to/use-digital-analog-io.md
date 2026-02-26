---
type: how-to
---

# How to Use Digital and Analog I/O

Ensure the robot is connected and enabled before controlling I/O.

## Digital Output

Set a digital output pin:

```python
dashboard = robot.dashboard

# Set DO index 1 to HIGH
dashboard.do_output(1, 1)

# Set DO index 1 to LOW
dashboard.do_output(1, 0)
```

For immediate output (bypasses the command queue):

```python
dashboard.do_instant(1, 1)  # Immediate HIGH on DO1
```

## Read Digital Output State

```python
state = dashboard.get_do(1)
print(f"DO1 state: {state}")
```

## Digital Output Groups

Set or read multiple digital outputs at once:

```python
# Set DO1=1, DO2=0, DO3=1 as a group
dashboard.do_group(1, 1, 0, 1)

# Read a group of DOs
result = dashboard.get_do_group(1, 3)  # Read DO1 through DO3

# Set/get as decimal bitmask
dashboard.do_group_dec(1, 3, 5)  # Binary 101 → DO1=1, DO2=0, DO3=1
result = dashboard.get_do_group_dec(1, 3)
```

## Digital Input

Read a digital input pin:

```python
state = dashboard.di(1)
print(f"DI1: {state}")
```

Read multiple inputs:

```python
result = dashboard.di_group(1, 4)      # DI1 through DI4
result = dashboard.di_group_dec(1, 4)   # As decimal bitmask
```

## Tool Digital I/O

Control tool-side digital outputs:

```python
dashboard.tool_do(1, 1)             # Tool DO1 = HIGH
dashboard.tool_do_instant(1, 0)     # Tool DO1 = LOW (immediate)
state = dashboard.get_tool_do(1)    # Read tool DO1
state = dashboard.tool_di(1)        # Read tool DI1
```

## Analog Output

Set an analog output voltage:

```python
dashboard.ao(1, 5.0)              # AO1 = 5.0V
dashboard.ao_instant(1, 3.3)      # AO1 = 3.3V (immediate)
```

## Read Analog Input

```python
value = dashboard.ai(1)           # Read AI1
tool_value = dashboard.tool_ai(1) # Read tool AI1
print(f"AI1: {value}")
```

## Read Analog Output

```python
value = dashboard.get_ao(1)
print(f"AO1: {value}")
```

## Configure Tool Interface

```python
# Set tool RS-485 baud rate
dashboard.set_tool_485(115200)

# Set tool power supply voltage
dashboard.set_tool_power(24)  # 0, 12, or 24V

# Set tool mode
dashboard.set_tool_mode(1)  # Mode depends on end-effector
```

## Practical Example: Gripper Control

```python
GRIPPER_DO = 1

def open_gripper(robot):
    robot.dashboard.do_output(GRIPPER_DO, 0)
    import time; time.sleep(0.5)

def close_gripper(robot):
    robot.dashboard.do_output(GRIPPER_DO, 1)
    import time; time.sleep(0.5)
```

::: tip
Use `do_instant` / `ao_instant` when you need the I/O to change immediately without waiting for the motion command queue.
:::
