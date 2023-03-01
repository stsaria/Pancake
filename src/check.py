import requests
import shutil
import socket
import sys
import os

def except_print(except_text, text, stop):
    print("An error (exception) occurred.\n",text)
    while True:
        except_choice = input("\nShow Exceptions? \nYes[YES]\nNo[No]\n[Y/n]:").lower()
        if except_choice in ["yes", "ye", "y"]:
            print("Error Details------\n",except_text)
            break
        if except_choice in ["no", "n"]:
            break
    if stop:
        sys.exit(1)

def network(url):
    try:
        temporalSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temporalSocket.connect(("8.8.8.8", 80))
        private_ip, port = temporalSocket.getsockname()
        temporalSocket.close()
        
        global_ip = requests.get(str(url))
    except Exception as e:
        return False, e, None
    return True, global_ip.text, private_ip

def run():
    print("File", end="...")
    paths = ["data", "data/minecraft-list.txt", "data/minecraft-dir-list.txt", "minecraft"]
    attributes = ["dir", "file", "file", "dir"]
    for i in range(len(paths)):
        if not os.path.exists(paths[i]):
            if attributes[i] == "dir":
                os.mkdir(paths[i])
            if attributes[i] == "file":
                f = open(str(paths[i]), 'w')
                f.write('')
                f.close()
    print("OK")
    
    print("NetWork", end="...")
    network_result = network("https://ifconfig.me")
    if not network_result[0]:
        print("Error")
        except_print(network_result[1], "There is a problem with the network.", True)
    print("OK")
    
    print("Java Path", end="...")
    if shutil.which('java') == None:
        print("Error")
        print("Javaのパス（環境変数）が通っていません。")
        sys.exit(1)
    print("OK")