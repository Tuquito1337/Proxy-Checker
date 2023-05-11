import httpx
import threading
import os

global hits
global bad
hits = 0
bad = 0


hits_list = []


def title():
    global total
    os.system(
        "title " + f'''MAL ^| Total: {total} ^| Checked = {hits + bad} ^| Hits = {hits} ^| Bad = {bad} ^| Created By: cracked.io/PepeArgento''')


def save(name, data):
    cleaned = [*set(data)]
    with open(name + '.txt', 'w', encoding="utf-8") as fp:
        for line in cleaned:
            fp.write("%s\n" % line)


def load_proxies(proxy, port):
    proxies = open('proxies.txt', "r+", encoding="UTF-8").read().splitlines()
    for proxyy in proxies:
        proxy.append(proxyy.split(':')[0])
        port.append(proxyy.split(':')[1])


def check_account(proxy, port):
    global hits
    global bad
    
    try:
        url = 'https://www.google.com/'
        with httpx.Client(proxies=f'http://{proxy}:{port}') as client:
            response = client.get(url, timeout=3)
            if response.status_code == 200:
                hits_list.append(f"{proxy}:{port}")
                save('aliveproxies', hits_list)
                hits += 1
            else:
                bad += 1
    except:
        bad += 1
        pass


def start_threads(thread):
    global hits
    global bad
    global total
    
    total = 0
    
    
    proxy = []
    port = []
    
    load_proxies(proxy, port)
    total += len(proxy)
    
    num = 0
    while 1:
        title()
        if threading.active_count() < int(thread):
            if len(proxy) > num:
                try:
                    threading.Thread(
                    target=check_account,
                    args=(proxy[num], port[num]),
                    ).start()
                    num += 1
                except:
                    pass
    
    
if __name__ == '__main__':
    start_threads(input('Introduce el total de threads que deseas utilizar: '))