import asyncio
import psutil
from functools import partial
from typing import Dict, Any, List, Optional, Tuple

class AsyncPSUtil:
    """异步系统监控工具类"""
    
    def __init__(self):
        self._loop = asyncio.get_running_loop()
    
    async def _run_in_executor(self, func, *args, **kwargs):
        """在executor中运行同步函数"""
        return await self._loop.run_in_executor(
            None,
            partial(func, *args, **kwargs)
        )
    
    # ====================
    # CPU相关方法
    # ====================
    async def cpu_percent(self, interval: float = 0.1, percpu: bool = False) -> float:
        """异步获取CPU使用率"""
        return await self._run_in_executor(
            psutil.cpu_percent,
            interval,
            percpu
        )
    
    async def cpu_stats(self) -> Dict[str, Any]:
        """异步获取CPU统计信息"""
        return await self._run_in_executor(psutil.cpu_stats)
    
    async def cpu_freq(self, percpu: bool = False) -> Dict[str, Any]:
        """异步获取CPU频率"""
        return await self._run_in_executor(psutil.cpu_freq, percpu)
    
    # ====================
    # 内存相关方法
    # ====================
    async def virtual_memory(self) -> Dict[str, Any]:
        """异步获取虚拟内存信息"""
        mem = await self._run_in_executor(psutil.virtual_memory)
        return self._convert_namedtuple(mem)
    
    async def swap_memory(self) -> Dict[str, Any]:
        """异步获取交换内存信息"""
        swap = await self._run_in_executor(psutil.swap_memory)
        return self._convert_namedtuple(swap)
    
    # ====================
    # 磁盘相关方法
    # ====================
    async def disk_usage(self, path: str = "/") -> Dict[str, Any]:
        """异步获取磁盘使用情况"""
        usage = await self._run_in_executor(psutil.disk_usage, path)
        return self._convert_namedtuple(usage)
    
    async def disk_io_counters(self, perdisk: bool = False) -> Dict[str, Any]:
        """异步获取磁盘IO统计"""
        counters = await self._run_in_executor(
            psutil.disk_io_counters,
            perdisk=perdisk
        )
        if perdisk:
            return {k: self._convert_namedtuple(v) for k, v in counters.items()}
        return self._convert_namedtuple(counters)
    
    async def disk_partitions(self, all: bool = False) -> List[Dict[str, Any]]:
        """异步获取磁盘分区信息"""
        partitions = await self._run_in_executor(psutil.disk_partitions, all=all)
        return [self._convert_namedtuple(p) for p in partitions]
    
    # ====================
    # 网络相关方法
    # ====================
    async def net_io_counters(self, pernic: bool = False) -> Dict[str, Any]:
        """异步获取网络IO统计"""
        counters = await self._run_in_executor(
            psutil.net_io_counters,
            pernic=pernic
        )
        if pernic:
            return {k: self._convert_namedtuple(v) for k, v in counters.items()}
        return self._convert_namedtuple(counters)
    
    async def net_connections(self, kind: str = 'inet') -> List[Dict[str, Any]]:
        """异步获取网络连接信息"""
        conns = await self._run_in_executor(
            psutil.net_connections,
            kind=kind
        )
        return [self._convert_namedtuple(c) for c in conns]
    
    async def net_if_addrs(self) -> Dict[str, Any]:
        """异步获取网络接口地址"""
        addrs = await self._run_in_executor(psutil.net_if_addrs)
        return {k: [self._convert_namedtuple(a) for a in v] for k, v in addrs.items()}
    
    async def net_if_stats(self) -> Dict[str, Any]:
        """异步获取网络接口状态"""
        stats = await self._run_in_executor(psutil.net_if_stats)
        return {k: self._convert_namedtuple(v) for k, v in stats.items()}
    
    # ====================
    # 传感器相关方法
    # ====================
    async def sensors_temperatures(self) -> Dict[str, Any]:
        """异步获取温度传感器信息"""
        temps = await self._run_in_executor(psutil.sensors_temperatures)
        return {k: [self._convert_namedtuple(t) for t in v] for k, v in temps.items()}
    
    async def sensors_battery(self) -> Dict[str, Any]:
        """异步获取电池状态"""
        battery = await self._run_in_executor(psutil.sensors_battery)
        if battery is not None:
            return self._convert_namedtuple(battery)
        return {}
    
    async def sensors_fans(self) -> Dict[str, Any]:
        """异步获取风扇传感器信息"""
        fans = await self._run_in_executor(psutil.sensors_fans)
        return {k: [self._convert_namedtuple(t) for t in v] for k, v in fans.items()}
    
    # ====================
    # 系统信息
    # ====================
    async def users(self) -> List[Dict[str, Any]]:
        """异步获取当前登录用户信息"""
        users = await self._run_in_executor(psutil.users)
        return [self._convert_namedtuple(u) for u in users]
    
    async def boot_time(self) -> float:
        """异步获取系统启动时间"""
        return await self._run_in_executor(psutil.boot_time)
    
    async def getloadavg(self) -> Tuple[float, float, float]:
        """异步获取系统负载平均值"""
        return await self._run_in_executor(psutil.getloadavg)
    
    # ====================
    # 进程相关方法
    # ====================
    async def process_iter(self, attrs: Optional[List[str]] = None, ad_value: Optional[Any] = None):
        """异步进程迭代器"""
        procs = await self._run_in_executor(
            psutil.process_iter,
            attrs=attrs,
            ad_value=ad_value
        )
        for p in procs:
            yield AsyncProcess(p)
    
    async def pid_exists(self, pid: int) -> bool:
        """异步检查进程是否存在"""
        return await self._run_in_executor(psutil.pid_exists, pid)
    
    async def process_by_pid(self, pid: int):
        """异步获取进程对象"""
        return AsyncProcess(await self._run_in_executor(psutil.Process, pid))
    
    # ====================
    # 工具方法
    # ====================
    @staticmethod
    def _convert_namedtuple(obj) -> Dict[str, Any]:
        """将namedtuple转换为字典"""
        if isinstance(obj, list):
            return [AsyncPSUtil._convert_namedtuple(x) for x in obj]
        if hasattr(obj, "_asdict"):
            return {k: AsyncPSUtil._convert_namedtuple(v) for k, v in obj._asdict().items()}
        return obj


class AsyncProcess:
    """异步进程处理类"""
    
    def __init__(self, proc: psutil.Process):
        self._proc = proc
        self._loop = asyncio.get_running_loop()
    
    async def _run_in_executor(self, func, *args, **kwargs):
        return await self._loop.run_in_executor(
            None,
            partial(func, *args, **kwargs)
        )
    
    async def name(self) -> str:
        """获取进程名称"""
        return await self._run_in_executor(self._proc.name)
    
    async def cmdline(self) -> List[str]:
        """获取进程命令行"""
        return await self._run_in_executor(self._proc.cmdline)
    
    async def status(self) -> str:
        """获取进程状态"""
        return await self._run_in_executor(self._proc.status)
    
    async def cpu_percent(self, interval: float = 0.1) -> float:
        """获取进程CPU使用率"""
        return await self._run_in_executor(self._proc.cpu_percent, interval)
    
    async def memory_info(self) -> Dict[str, Any]:
        """获取进程内存使用情况"""
        mem = await self._run_in_executor(self._proc.memory_info)
        return AsyncPSUtil._convert_namedtuple(mem)
    
    async def memory_percent(self) -> float:
        """获取进程内存使用率"""
        return await self._run_in_executor(self._proc.memory_percent)
    
    async def create_time(self) -> float:
        """获取进程创建时间"""
        return await self._run_in_executor(self._proc.create_time)
    
    async def uid(self) -> int:
        """获取进程的用户ID"""
        return await self._run_in_executor(self._proc.uid)
    
    async def gid(self) -> int:
        """获取进程的组ID"""
        return await self._run_in_executor(self._proc.gid)
    
    async def username(self) -> str:
        """获取进程的用户名"""
        return await self._run_in_executor(self._proc.username)
    
    async def exe(self) -> str:
        """获取进程的可执行文件路径"""
        return await self._run_in_executor(self._proc.exe)
    
    async def cwd(self) -> str:
        """获取进程的工作目录"""
        return await self._run_in_executor(self._proc.cwd)
    
    async def ppid(self) -> int:
        """获取父进程ID"""
        return await self._run_in_executor(self._proc.ppid)
    
    async def children(self, recursive: bool = False):
        """获取子进程"""
        children = await self._run_in_executor(
            self._proc.children,
            recursive=recursive
        )
        return [AsyncProcess(c) for c in children]
    
    async def terminate(self):
        """终止进程"""
        return await self._run_in_executor(self._proc.terminate)
    
    async def kill(self):
        """杀死进程"""
        return await self._run_in_executor(self._proc.kill)
    
    async def send_signal(self, sig: int):
        """发送信号"""
        return await self._run_in_executor(self._proc.send_signal, sig)
    
    async def wait(self, timeout: float = None):
        """等待进程结束"""
        return await self._run_in_executor(self._proc.wait, timeout)
    
    async def is_running(self) -> bool:
        """检查进程是否正在运行"""
        return await self._run_in_executor(self._proc.is_running)
    
    async def is_alive(self) -> bool:
        """检查进程是否存活"""
        return await self._run_in_executor(self._proc.is_alive)
    
    async def suspend(self):
        """挂起进程"""
        return await self._run_in_executor(self._proc.suspend)
    
    async def resume(self):
        """恢复进程"""
        return await self._run_in_executor(self._proc.resume)
    
    async def nice(self, value: int = None) -> int:
        """获取或设置进程优先级"""
        if value is not None:
            return await self._run_in_executor(self._proc.nice, value)
        return await self._run_in_executor(self._proc.nice)
    
    async def ionice(self, ioclass: int = None, value: int = None):
        """获取或设置进程I/O优先级"""
        if ioclass is not None and value is not None:
            return await self._run_in_executor(
                self._proc.ionice,
                ioclass=ioclass,
                value=value
            )
        return await self._run_in_executor(self._proc.ionice)
    
    async def io_counters(self):
        """获取进程I/O统计"""
        return await self._run_in_executor(self._proc.io_counters)
    
    async def num_ctx_switches(self):
        """获取进程上下文切换次数"""
        return await self._run_in_executor(self._proc.num_ctx_switches)
    
    async def num_fds(self) -> int:
        """获取进程打开的文件描述符数量"""
        return await self._run_in_executor(self._proc.num_fds)
    
    async def num_threads(self) -> int:
        """获取进程线程数量"""
        return await self._run_in_executor(self._proc.num_threads)
    
    async def threads(self):
        """获取进程线程信息"""
        return await self._run_in_executor(self._proc.threads)
    
    async def environ(self) -> Dict[str, str]:
        """获取进程的环境变量"""
        return await self._run_in_executor(self._proc.environ)
    
    async def memory_maps(self):
        """获取进程的内存映射"""
        maps = await self._run_in_executor(self._proc.memory_maps)
        return [AsyncPSUtil._convert_namedtuple(m) for m in maps]
    
    async def open_files(self):
        """获取进程打开的文件"""
        files = await self._run_in_executor(self._proc.open_files)
        return [AsyncPSUtil._convert_namedtuple(f) for f in files]