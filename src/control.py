import subprocess
import linecache
import socket
import check
import make
import sys

def exec_java(dir_name, jar_name, xms, xmx, java_argument):
    # もし入力内容が0かnotだったら1(1GB)に
    mem = [xms, xmx]
    cmd = "java -Xmx"+mem[1]+"G -Xms"+mem[0]+"G -jar ./"+jar_name+" "+java_argument
    subprocess.call(cmd, shell=True, cwd=r""+dir_name+"/")

def select_server():
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])
    while True:
        choice_lines = input("Please input a server: ")
        if not choice_lines or not choice_lines.isdigit():
            continue
        if int(choice_lines) <= 0 or int(minecraft_server_dir_list_txt_lines_count) < int(choice_lines) - 1 or int(minecraft_server_list_txt_lines_count) < int(choice_lines):
            continue
        break
    return choice_lines

def run():
    print("Server startup mode")
    # txtファイルカウント
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])

    if not minecraft_server_dir_list_txt_lines_count == minecraft_server_list_txt_lines_count:
        print("Cannot start because the number of lines between txt files does not match.")
        sys.exit(1)

    print("Select the server you wish to activate.")
    # サーバー情報を読み込む
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    while True:
        choice_xms = input("Enter Xms (minimum memory) (G) *Number only: ")
        choice_xmx = input("Enter Xmx (maximum memory) (G) *Number only: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')

    exec_java(path, start_jar, mem_input[0], mem_input[1], "nogui")

def port():
    print("Port change mode")
    print("Select the server for which you want to change the port.")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        input_port = input("Enter the port to change to: ")
        if not input_port or not str.isnumeric(input_port):
                continue
        else:
            break
    make.file_identification_rewriting(path+"/server.properties", "server-port=", "server-port="+input_port+"\n")
    print("Port change completed.")

def make_sh():
    print("Please select the server where you want to create the sh-bat file.")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        choice_xms = input("Enter Xms (minimum memory) (G) *Number only: ")
        choice_xmx = input("Enter Xmx (maximum memory) (G) *Number only: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')
    file_name = ["start.sh", "start.bat"]
    for i in file_name:
        with open(path+"/"+i, 'w', encoding="utf-8") as f:
            print("echo Start!\njava -Xms"+mem_input[0]+"G -Xmx"+mem_input[1]+"G -jar "+start_jar+" --nogui", file=f)
    print("Created sh-bat file")

def network_info():
    network_info_select = etc_server.input_yes_no("\nAttention: please review before opening! \nThe information you are about to disclose is sensitive information, \nlike your IP address! (Like a phone number.) \nDepending on how you use this information, \nit could be used to attack your server. (like a phone number) \nThis information can be used to attack our servers, etc.,\ndepending on how it is used. \nPlease be aware of the circumstances and environment in which you disclose this information! \nDo you wish to disclose? \nPlease select with `yes` or `no`.\n[Y/N]: ")
    if not network_info_select:
        return
    active, global_ip, private_ip = check.network("https://ifconfig.me")
    if not active:
        global_ip = "Cannot be obtained."
    print("Private IP (required if joining from the same network)"+private_ip)
    print("Global IP (required when joining from an external network)"+global_ip)
    input()

def main():
    while True:
        choice = input("\nPlease select the management mode\nrunner mode[run]\nPort change mode（port）\nsh file or bat file, creation mode[sh],[bat]\nネットワークの情報確認モード(IP) | Network IP check (network)\n戻る | Exit (exit)\n[R,P,S,B,N,E]：").lower()
        if choice in ["run", "ru", "r"]:
            run()
        elif choice in["port", "por", "po", "p"]:
            port()
        elif choice in["sh", "s"]:
            make_sh()
        elif choice in["bat", "ba", "b"]:
            make_sh()
        elif choice in["network", "networ", "netwo", "netw", "net", "ne", "n"]:
            network_info()
        elif choice in["exit", "exi", "ex", "e"]:
            break
        else:
            print("There is no item for that.")