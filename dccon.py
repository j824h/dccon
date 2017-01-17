import urllib.request
import json
import os
import time

def con_open(no):
    '''
    Open the con image file with path number string no.
    '''
    con_url = urllib.request.Request('http://dcimg1.dcinside.com/dccon.php?no='+no)
    con_url.add_header('Referer', 'http://dccon.dcinside.com/')
    con_file = urllib.request.urlopen(con_url)
    return con_file

def save(path, bytes):
    '''
    Save bytes at file path.
    '''
    with open(path, "wb") as f:
        f.write(bytes)
        f.close()

def save_con(path, no):
    '''
    Save the con image with path number string no.
    '''
    con_file = con_open(no)
    name = con_file.info().get('Content-Disposition').split('=')[1]
    save(path + '\\' + name, con_file.read())

def load_package(idx):
    '''
    Load package information from index idx.
    '''
    url = 'http://dccon.dcinside.com/index/package_detail'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'ci_c='
        }
    data = ('ci_t=&package_idx='+str(idx)).encode()
    package_request = urllib.request.Request(url, data, headers)
    package_f = urllib.request.urlopen(package_request)
    package = json.load(package_f)
    return package

def save_package(package):
    '''
    Save package information, log, con images from loaded package.
    '''
    path = package['info']['title']
    save_info = 'Version: 1.0 \n' + 'Save time: ' + time.strftime("%c")
    os.mkdir(path)
    save(path + '\\' + 'package_details.json', json.dumps(package).encode())
    save(path + '\\' + 'save_info.txt', save_info.encode())
    for con in package['detail']:
        save_con(path, con['path'])

def quick(idx):
    '''
    The one quick command to use.
    '''
    save_package(load_package(idx))
