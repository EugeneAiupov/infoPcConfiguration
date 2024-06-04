import psutil
import os
import platform
import subprocess
import _wmi

def get_processor_name():
    name = subprocess.check_output(['wmic', 'cpu', 'get', 'name']).decode()
    return name.strip().split("\n")[1]

def get_os_info():
    info= {
        "Platform": platform.system(),
        "Platform Release": platform.release(),
        "Platform version": platform.version(),
        "Architicture": platform.machine(),
        "Hostname": platform.node(),
        "Processor": platform.processor(),
        "Boot Time": psutil.boot_time(),
    }
    return info

def get_cpu_info():
    info = {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": psutil.cpu_freq().max,
        "Min Frequency": psutil.cpu_freq().min,
        "Current Frequency": psutil.cpu_freq().current,
        "CPU Usage Per Core": psutil.cpu_percent(interval=1, percpu=True),
        "Total CPU Usage": psutil.cpu_percent(interval=1),
    }
    return info

def get_mamore_info():
    svmem = psutil.virtual_memory()
    info = {
        "Total memory": svmem.total,
        "Available Memory": svmem.available,
        "Used memory": svmem.used,
        "Memory Percentage": svmem.percent
    }
    return info

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disk_info[partition.device] = {
            "Total Size": partition_usage.total,
            "Used": partition_usage.used,
            "Free": partition_usage.free,
            "Percentage": partition_usage.percent,
        }
    return disk_info

def get_gpu_info():
    try:
        gpu_info = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
        gpu_name = gpu_info.decode()
        
    except:
        gpu_name = "Could not fetch GPU details"
    return {"GPU": gpu_name}


def write_file(file_path, info):
    with open(file_path, "w") as file:
        for key, value in info.items():
            file.write(f"{key}:\n")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    file.write(f"\t{sub_key}: {sub_value}\n")
            else:
                file.write(f"\t{value}\n")
            file.write("\n")
            
all_info = {
    "OS Information": get_os_info(),
    "CPU Name": get_processor_name(),
    "CPU Information": get_cpu_info(),
    "Memory Information": get_mamore_info(),
    "Disk Information": get_disk_info(),
    "GPU Information": get_gpu_info(),
}

write_file("system_info.txt", all_info)
print("System information has been saved to system_info.txt")
    
