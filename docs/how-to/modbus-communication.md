---
type: how-to
---

# How to Use Modbus Communication

The Dobot V4 controller can act as a Modbus TCP or RTU master to communicate with external devices such as PLCs, sensors, and actuators.

## Create a Modbus TCP Connection

```python
dashboard = robot.dashboard

# Create Modbus TCP connection
# Parameters: ip, port, slave_id, is_copy (optional)
dashboard.modbus_create("192.168.1.100", 502, 1)
```

## Create a Modbus RTU Connection

```python
# Parameters: slave_id, baud_rate, data_bit, stop_bit, parity
dashboard.modbus_rtu_create(1, 9600, 8, 1, "N")
```

## Close a Modbus Connection

```python
dashboard.modbus_close(0)  # Close connection index 0
```

## Read Coils

```python
# Read 8 coils starting at address 0
result = dashboard.get_coils(0, 0, 8)
print(f"Coils: {result}")
```

## Write Coils

```python
# Write a single coil at address 0
dashboard.set_coils(0, 0, 1, 1)  # index, addr, count, value
```

## Read Holding Registers

```python
# Read 4 holding registers starting at address 0
result = dashboard.get_hold_regs(0, 0, 4)
print(f"Registers: {result}")
```

## Write Holding Registers

```python
# Write value to holding register at address 0
dashboard.set_hold_regs(0, 0, 1, 100)  # index, addr, count, value
```

## Read Input Registers

```python
result = dashboard.get_in_regs(0, 0, 4)
print(f"Input registers: {result}")
```

## Read Input Bits (Discrete Inputs)

```python
result = dashboard.get_in_bits(0, 0, 8)
print(f"Input bits: {result}")
```

## Internal Variables

The controller also exposes internal Modbus-mapped variables for use in programs:

### Read Internal Variables

```python
# Boolean
val = dashboard.get_input_bool(0)

# Integer (16-bit)
val = dashboard.get_input_int(0)

# Float (32-bit)
val = dashboard.get_input_float(0)
```

### Write Internal Variables

```python
dashboard.set_output_bool(0, True)
dashboard.set_output_int(0, 42)
dashboard.set_output_float(0, 3.14)
```

### Read Internal Outputs

```python
val = dashboard.get_output_bool(0)
val = dashboard.get_output_int(0)
val = dashboard.get_output_float(0)
```

## Practical Example: Reading a Sensor via Modbus TCP

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    dashboard = robot.dashboard

    # Connect to a Modbus TCP sensor
    dashboard.modbus_create("192.168.1.100", 502, 1)

    # Read sensor value from holding register 0
    value = dashboard.get_hold_regs(0, 0, 1)
    print(f"Sensor value: {value}")

    # Clean up
    dashboard.modbus_close(0)
```

::: tip
Modbus connection indices are assigned sequentially starting from 0. Keep track of the index returned by `modbus_create` / `modbus_rtu_create`.
:::
