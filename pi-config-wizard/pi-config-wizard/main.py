import socketserver
import os
import subprocess
import json
import http.server
import ha_api

URL_PREFIX = '/api/v1'
ha_api.init()

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return (0, output.strip())
    except subprocess.CalledProcessError as e:
        return (e.returncode, e.output.strip())

def is_boot_mounted():
    is_mounted = os.path.ismount('/tmp/boot')
    return is_mounted

def mount_boot():
    if is_boot_mounted():
        return True, None
    try:
        boot_partition = get_boot_partition()
    except Exception as e:
        return False, str(e)

    cmd = f'mount -t vfat {boot_partition} /tmp/boot'
    status, result = run_command(cmd)
    if status != 0:
        error = f"Error: Command '{cmd}' failed with status {status} and output '{result}'"
        return False, error
    else:
        return True, None

def edit_config_txt(search_key, newline):
    found = False
    with open('/tmp/boot/config.txt', 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if search_key in line:
                lines[i] = newline
                break
        else:
            lines.append(newline)
    with open('/tmp/boot/config.txt', 'w') as file:
        file.writelines(lines)

def enable_i2c():
    # Check if /tmp/boot/CONFIG/modules exists
    if not os.path.exists('/tmp/boot/CONFIG/modules'):
        os.makedirs('/tmp/boot/CONFIG/modules')
    # Check if /tmp/boot/CONFIG/modules/rpi-i2c.conf exists
    if not os.path.exists('/tmp/boot/CONFIG/modules/rpi-i2c.conf'):
        with open('/tmp/boot/CONFIG/modules/rpi-i2c.conf', 'w') as file:
            file.write('i2c-dev\n')
    else:
        with open('/tmp/boot/CONFIG/modules/rpi-i2c.conf', 'r') as file:
            lines = file.readlines()
            if 'i2c-dev' not in lines:
                with open('/tmp/boot/CONFIG/modules/rpi-i2c.conf', 'a') as file:
                    file.write('i2c-dev\n')
    # 
    edit_config_txt('dtparam=i2c_arm', 'dtparam=i2c_arm=on\n')

def disable_i2c():
    run_command('rm -rf /tmp/boot/CONFIG/modules/rpi-i2c.conf')
    edit_config_txt('dtparam=i2c_arm', '#dtparam=i2c_arm=on\n')

def enable_spi():
    edit_config_txt('dtparam=spi', 'dtparam=spi=on\n')

def disable_spi():
    edit_config_txt('dtparam=spi', '#dtparam=spi=on\n')

def get_data_partition():
    '''
    Get which disk is mounted on /data
    '''
    command = "df /data | awk 'NR==2{print $1}'"
    status, result = run_command(command)
    if status != 0:
        raise Exception(f'Failed to get disk: {result}')
    return result

def get_parent_disk(partition):
    '''
    Get which disk is partition is on
    '''
    command = f"lsblk -no pkname {partition}"
    status, result = run_command(command)
    if status != 0:
        raise Exception(f'Failed to get parent disk: {result}')
    return f'/dev/{result}'

def get_data_disk():
    '''
    Get which disk is partition /data is on
    '''
    partition = get_data_partition()
    # Get which disk is partition /data is on
    return get_parent_disk(partition)

def get_boot_partition():
    '''
    Get which disk is mounted on /boot
    '''
    disk = get_data_disk()
    # Get all partitions on the disk
    command = f"lsblk -no kname {disk}"
    status, result = run_command(command)
    if status != 0:
        raise Exception(f'Failed to get boot partition: {result}')
    partitions = result.split()
    partitions = [f'/dev/{partition}' for partition in partitions]
    partitions.remove(disk)
    partitions.sort()
    return partitions[0]


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def respond(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == f'{URL_PREFIX}/configTxt':
            with open('/tmp/boot/config.txt', 'r') as file:
                configTxt = file.read()
            self.respond(200, {'configTxt': configTxt})
        elif self.path == f'{URL_PREFIX}/mounted':
            is_mounted = is_boot_mounted()
            self.respond(200, {'is_mounted': is_mounted})
        elif self.path == f'{URL_PREFIX}/i2c':
            _, result = run_command('ls /dev/i2c*')
            result = result.strip().split('\n')
            self.respond(200, {'enable': '/dev/i2c-1' in result})
        elif self.path == f'{URL_PREFIX}/spi':
            _, result = run_command('ls /dev/spidev*')
            result = result.strip().split('\n')
            self.respond(200, {'enable': '/dev/spidev0.0' in result})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == f'{URL_PREFIX}/configTxt':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length).decode()
            data = json.loads(data)
            configTxt = data['configTxt']
            with open('/tmp/boot/config.txt', 'w') as file:
                file.write(configTxt)
            self.respond(200, {})
        elif self.path == f'{URL_PREFIX}/mount':
            state, error = mount_boot()
            if state:
                self.respond(200, {})
            else:
                self.respond(500, {'error': error})
        elif self.path == f'{URL_PREFIX}/i2c':
            enable = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode())['enable']
            print(f"i2c: {enable}")
            if enable:
                enable_i2c()
            else:
                disable_i2c()
            self.respond(200, {})
        elif self.path == f'{URL_PREFIX}/spi':
            enable = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode())['enable']
            print(f"spi: {enable}")
            if enable:
                enable_spi()
            else:
                disable_spi()
            self.respond(200, {})
        elif self.path == f'{URL_PREFIX}/reboot':
            ha_api.reboot()
            self.respond(200, {})
        else:
            super().do_POST()

# 设置服务器的IP地址和端口号
host = '0.0.0.0'
port = 8000

# 切换到当前文件下的www目录
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/www')

# 创建HTTP服务器并指定请求处理程序
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer((host, port), MyRequestHandler) as httpd:
    print(f'Server started at http://{host}:{port}')
    httpd.serve_forever()