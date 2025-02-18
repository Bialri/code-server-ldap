import psutil
import time
import requests
import yaml

UPDATE_DELAY = 1 # in seconds
print("started Network Controller")
def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
counter = 0
zero_counter = 0
while True:
    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the stats again
    io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    # print the total download/upload along with current speeds
    counter+=1
    if not us and not ds:
        zero_counter+=1
    else:
        counter=0
    if counter == 120:
        if (zero_counter / counter) > 0.97:
            hash_file = open('/home/coder/.config/code-server/config.yaml')
            hash_yaml = yaml.safe_load(hash_file)
            try:
                requests.post("http://auth:8000/shutContainer",json={"code_server_hash":hash_yaml['hashed-password']})
            except requests.exceptions.ConnectionError:
                pass
        counter = 0
        zero_counter = 0
    print(f"Upload: {get_size(io_2.bytes_sent)}   "
          f", Download: {get_size(io_2.bytes_recv)}   "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ")
    # update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv