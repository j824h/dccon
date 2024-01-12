import urllib.request
import json
import os
import time


def con_open(no):
    """
    Open the con image file with path number string no.
    """
    con_url = urllib.request.Request('https://dcimg1.dcinside.com/dccon.php?no='+no)
    con_url.add_header('Referer', 'https://dccon.dcinside.com/')
    con_file = urllib.request.urlopen(con_url)
    return con_file


def save_b(path, b):
    """
    Save bytes at file path.
    """
    with open(path, 'wb') as f:
        f.write(b)
        f.close()


def save_s(path, string):
    """
    Save string as a text file at file path.
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(string)
        f.close()

      f.close()


def save_con(path, no):
    """
    Save the con image with path number string no.
    """
    con_file = con_open(no)
    name = con_file.info().get('Content-Disposition').split('=')[1]
    save_b(os.path.join(path, name), con_file.read())       


def load_package(idx):
    """
    Load package information from index idx.
    """
    url = 'https://dccon.dcinside.com/index/package_detail'
    headers = { 'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'ci_c='
        }
    data = ('ci_t=&package_idx='+str(idx)).encode()
    package_request = urllib.request.Request(url, data, headers)
    package_f = urllib.request.urlopen(package_request)
    package = json.load(package_f)
    return package


def save_package(package):
    """
    Save package information, log, con images from loaded package.
    """
    path = package['info']['title']
    save_info = 'Version: 1.1\n' + 'Save time: ' + time.strftime("%c")
    os.mkdir(path)
    save_s(os.path.join(path, 'package_details.json'),
         json.dumps(package, ensure_ascii=False))
    save_s(os.path.join(path, 'save_info.txt'), save_info)       
    for con in package['detail']:
        save_con(path, con['path'])


def quick(idx):
    """
    The one quick command to use.
    """
    save_package(load_package(idx))
