# aiopsutil-python

**aiopsutil: Asynchronous Utilities for Gathering System and Process Information**

`aiopsutil` is an asynchronous version of the popular `psutil` library, designed to provide an efficient and non-blocking way to retrieve information on running processes and system utilization. This Python package is tailored for developers who need to monitor and manage system resources in an asynchronous programming environment.

## Table of Contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Initialization](#initialization)
- [API Methods](#api-methods)
- [AsyncProcess Class](#asyncprocess-class)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Key Features
- **Asynchronous Operations**: Leverage Python's `asyncio` library to perform system and process monitoring without blocking the event loop.
- **Comprehensive Functionality**: Offers a rich set of functions to retrieve information about system CPU, memory, disks, network, sensors, and running processes.
- **Ease of Integration**: Designed with a familiar interface for users of `psutil`, making it easy to adopt in existing projects.
- **Cross-Platform Support**: Works on multiple operating systems, including Linux, Windows, and macOS.

## Installation
To use `aiopsutil`, you must have `psutil` installed. You can install it using pip:
```bash
pip install psutil
```

## Initialization
Create an instance of `AsyncPSUtil` within an asynchronous context:
```python
async def main():
    aps = AsyncPSUtil()
    # Use aps to call methods...
```

## API Methods
`aiopsutil` provides a variety of methods to asynchronously gather system and process information. Here's a brief overview:

### CPU Related
- `cpu_percent(interval: float = 0.1, percpu: bool = False) -> float`: Get CPU usage percentage.
- `cpu_stats() -> Dict`: Return CPU statistics.
- `cpu_freq(percpu: bool = False) -> Dict`: Get CPU frequency information.

### Memory Related
- `virtual_memory() -> Dict`: Return virtual memory information.
- `swap_memory() -> Dict`: Return swap memory information.

### Disk Related
- `disk_usage(path: str = "/") -> Dict`: Get disk usage information for the given path.
- `disk_io_counters(perdisk: bool = False) -> Dict`: Return disk I/O statistics.

### Network Related
- `net_io_counters(pernic: bool = False) -> Dict`: Return network I/O statistics.
- `net_connections(kind: str = 'inet') -> List[Dict]`: Return a list of network connections.

### Sensors Related
- `sensors_temperatures() -> Dict`: Return temperature data grouped by sensor.
- `sensors_battery() -> Dict`: Return battery status information.

### System Information
- `boot_time() -> float`: Return system boot timestamp.
- `users() -> List[Dict]`: Return a list of logged-in users.

### Process Management
- `process_iter(attrs: List[str] = None)`: An asynchronous iterator for iterating over processes.
- `process_by_pid(pid: int) -> AsyncProcess`: Get a process object by PID.

## AsyncProcess Class
The `AsyncProcess` class provides methods to interact with individual processes:
- `memory_info() -> Dict`: Return memory information.
- `terminate()` / `kill()`: Terminate the process.
- `children(recursive: bool = False) -> List[AsyncProcess]`: Get a list of child processes.

## Usage Examples
Here's an example of how to use `aiopsutil` to monitor system resources:
```python
import asyncio

async def monitor_system():
    aps = AsyncPSUtil()
    
    # Get CPU usage
    cpu_usage = await aps.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")
    
    # Get memory information
    mem_info = await aps.virtual_memory()
    print(f"Memory Used: {mem_info['used'] / 1024**3:.2f} GB")
    
    # Iterate over processes
    async for proc in aps.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python':
            p = await aps.process_by_pid(proc.info['pid'])
            mem = await p.memory_info()
            print(f"Python process using {mem['rss']} bytes")

# Run the monitor system function
asyncio.run(monitor_system())
```

## Contributing
Contributions to `aiopsutil` are welcome! Please ensure that your code follows the existing coding standards and passes all tests before submitting a pull request.

## License
`aiopsutil` is licensed under the BSD 3-Clause License. See the LICENSE file for more details.

---