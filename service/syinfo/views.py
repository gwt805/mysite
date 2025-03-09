import json
import time
import socket
import psutil
import platform
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

def get_disk_info():
    partitions = psutil.disk_partitions()
    mountpoints = []
    totals = []
    useds = []
    frees = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total = round(usage.total / (1024 ** 3), 2)  # 转换为 GB
            used = round(usage.used / (1024 ** 3), 2)
            free = round(usage.free / (1024 ** 3), 2)
            mountpoints.append(partition.mountpoint)
            totals.append(total)
            useds.append(used)
            frees.append(free)
        except PermissionError:
            continue

    return [mountpoints, totals, useds, frees]

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
    return cpu_usage

def get_memory_info():
    memory = psutil.virtual_memory()
    total = round(memory.total / (1024 ** 3), 2)  # 转换为 GB
    used = round(memory.used / (1024 ** 3), 2)
    free = round(memory.free / (1024 ** 3), 2)
    return [{'name': 'Total', 'value': total}, {'name': 'Used', 'value': used}, {'name': 'Free', 'value': free}]

def get_system_info():
    system_info = [
        {'name': 'System', 'value': platform.system()},
        {'name': 'Node Name', 'value': platform.node()},
        {'name': 'Release', 'value': platform.release()},
        {'name': 'Version', 'value': platform.version()},
        {'name': 'Machine', 'value': platform.machine()},
        {'name': 'Processor', 'value': platform.processor()},
        {'name': 'Username', 'value': psutil.Process().username()},
        {'name': 'IP Address', 'value': socket.gethostbyname(socket.gethostname())}
    ]
    return system_info

def main():
    data = [
        get_disk_info(), # [[disk_name],[total][used],[free]]
        [{'name': '利用率', 'value': get_cpu_usage()}],
        get_memory_info(), # [memory_total, memory_used, memory_free]
        get_system_info() # [{'name': 'System', 'value': 'Linux'}, ...]
    ]
    return data

@csrf_exempt
def sse(request):
    def event_stream():
        while True:
            message = {"data": main()}
            yield f"data: {json.dumps(message)}\n\n"
            time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response