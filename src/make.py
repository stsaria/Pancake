from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import linecache
import requests
import datetime
import control
import urllib
import shutil
import check
import os

def get_minecraft_new_version(version):
    minecraft_server_donwload_page_url = "https://mcversions.net/download/"+str(version)
    try:
        res = requests.get(minecraft_server_donwload_page_url)
        res.raise_for_status()
    except Exception as e:
        return False, str(res).replace('<Response [', '').replace(']>', '')
    html = requests.get(minecraft_server_donwload_page_url)
    soup = BeautifulSoup(html.content, "html.parser")
    div = soup.find('div', 'downloads block lg:flex lg:mt-0 p-8 md:p-12 md:pr-0 lg:col-start-1')
    if div:
        minecraft_server_donwload_page_a = soup.find('a', 'text-xs whitespace-nowrap py-3 px-8 bg-green-700 hover:bg-green-900 rounded text-white no-underline font-bold transition-colors duration-200')
        if minecraft_server_donwload_page_a:
            return True, minecraft_server_donwload_page_a.get('href')
        else:
            return False, "not"

def get_minecraft_new_version(version):
    minecraft_server_donwload_page_url = "https://mcversions.net/download/"+str(version)
    try:
        res = requests.get(minecraft_server_donwload_page_url)
        res.raise_for_status()
    except Exception as e:
        return False, str(res).replace('<Response [', '').replace(']>', '')
    html = requests.get(minecraft_server_donwload_page_url)
    soup = BeautifulSoup(html.content, "html.parser")
    div = soup.find('div', 'downloads block lg:flex lg:mt-0 p-8 md:p-12 md:pr-0 lg:col-start-1')
    if div:
        minecraft_server_donwload_page_a = soup.find('a', 'text-xs whitespace-nowrap py-3 px-8 bg-green-700 hover:bg-green-900 rounded text-white no-underline font-bold transition-colors duration-200')
        if minecraft_server_donwload_page_a:
            return True, minecraft_server_donwload_page_a.get('href')
        else:
            return False, "not"

def input_yes_no(text):
    while True:
        choice = input(text)
        if choice in ["yes", "ye", "y"]:
            return True
        if choice in ["no", "n"]:
            return False

def download(url, save_name):
    urllib.request.urlretrieve(url, save_name)

def setting_week_day_or_month(dt_now):
    # 月をmatch.caseで設定する(3文字)
    match dt_now.strftime('%m'):
        case "01": month="Jan"
        case "02": month="Feb"
        case "03": month="Mar"
        case "04": month="Apr"
        case "05": month="May"
        case "06": month="Jun"
        case "07": month="Jul"
        case "08": month="Aug"
        case "09": month="Sep"
        case "10": month="Oct"
        case "11": month="Nov"
        case "12": month="Dec"
    # 曜日をmatch.caseで設定する(3文字)
    match dt_now.weekday():
        case 0: day_of_week="Sun"
        case 1: day_of_week="Mon"
        case 2: day_of_week="Tue"
        case 3: day_of_week="Wed"
        case 4: day_of_week="Thu"
        case 5: day_of_week="Fri"
        case 6: day_of_week="Sat"
    return month,day_of_week

def download_text(url, file_name):
    # そのままだとurllib.error.HTTPError: HTTP Error 403: Forbiddenでコケるからユーザーエージェントを偽装
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    html = html.decode('utf-8')
    # ファイル書き込み(server.properties)
    file = open(file_name, mode='w')
    file.write(str(html))
    file.close()

# 特定の文字列の行を書き換える関数
def replace_func(fname, replace_set):
    target, replace = replace_set
    
    with open(fname, 'r') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

# ↑を呼び出す関数
def file_identification_rewriting(file_name, before, after):
    replace_setA = (before, after) # (検索する文字列, 置換後の文字列)
    # call func
    replace_func(file_name, replace_setA)

# サーバー情報入力関数 
def input_server_info():
    while True:
        server_name = input("Please enter a server name: ")
        if server_name == "":
            continue
        break
    while True:
        server_port = input("Please enter the port you wish to configure: ")
        if not server_port.isdigit():
            print("Not a number.")
            continue
        if int(server_port) < 1 or int(server_port) > 49151:
            print("These are unexpected numbers.")
            continue
        break
    while True:
        choice = input("If you want to use the minecraft server for mods and plugins \n(mod: forge | plugin: spigot,papermc), choose `yes`(jar file), \nif not (download the official server), choose `no`.\n[Y,N]: ")
        if choice in ["yes", "ye", "y"]:
            version = None
            while True:
                choice = input("If you want to put Forge on your server, please enter `yes`, \nif you want to put Jar files such as Spigot, Papermc, etc., please enter `no`.\n[Y,N]: ")
                if choice in ["yes", "ye", "y"]:
                    local_jar_mode = 2
                    while True:
                        jar_start_file = None
                        jar_installer_file = input("Enter the Jar file for the Forge installation. (e.g. C:/Users/user/Download/forge-installer.jar): ")
                        try:
                            if not os.path.isfile(jar_installer_file):
                                print("We don't have that file.")
                                continue
                            if not jar_installer_file.endswith(".jar"):
                                print("The file is not a Jar file.")
                                continue
                        except Exception as e:
                            check.except_print(e, "", False)
                            continue
                        break
                
                elif choice in ["no", "n"]:
                    local_jar_mode = 1
                    while True:
                        jar_installer_file = None
                        jar_start_file = input("Enter the Jar file you want to include. (e.g. C:/Users/user/Download/spigotmc.jar): ")
                        try:
                            if not os.path.isfile(jar_start_file):
                                print("We don't have that file.")
                                continue
                            if not jar_start_file.endswith(".jar"):
                                print("The file is not a Jar file.")
                                continue
                        except Exception as e:
                            check.except_print(e, "", False)
                            continue
                        break
                break
            break
        
        elif choice in ["no", "n"]:
            jar_installer_file = None
            jar_start_file = None
            local_jar_mode = 0
            while True:
                version = input("Enter the server version: ")
                if not get_minecraft_new_version(version)[0]:
                    continue
                break
            break
    while True:
        choice = input("If you want to create more than one, enter `plural`, if you want to create immediately, enter `add`. \n[P,A]: ")
        if choice in ["add", "ad", "a"]:
            return True, server_name, version, server_port, local_jar_mode, jar_installer_file, jar_start_file
        elif choice in ["plural", "plura", "plur", "plu", "pl", "p"]:
            return False, server_name, version, server_port, local_jar_mode, jar_installer_file, jar_start_file

def run():
    print("Make Mode")
    server_count = 1
    while True:
        print(str(server_count)+"st")
        server_add, server_name, server_version, server_port, local_jar_mode, jar_installer_file, jar_start_file = input_server_info()
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        with open("tmp/"+str(server_count)+".tmp", 'w', encoding="utf-8") as f:
            print(server_name+"\n"+str(server_version)+"\n"+server_port+"\n"+str(local_jar_mode)+"\n"+str(jar_start_file)+"\n"+str(jar_installer_file), file=f)
        if server_add:
            break
        server_count = server_count + 1
    eula = input_yes_no("\nDo you agree to the EULA/Software License Agreement? \nPlease click here for more information about the EULA for ，Minecraft.\nhttps://www.minecraft.net/ja-jp/eula\nYes Please select with No. [Y/n]: ")
    
    for i in range(server_count):
        i = i + 1
        print("Server being created ("+str(i)+"st)")
        
        dt_now = datetime.datetime.now()
        minecraft_dir = "minecraft/minecraft-"+dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')
        os.mkdir(minecraft_dir)
        
        server_name = linecache.getline("tmp/"+str(i)+".tmp", 1).replace('\n', '')
        server_version = linecache.getline("tmp/"+str(i)+".tmp", 2).replace('\n', '')
        server_port = linecache.getline("tmp/"+str(i)+".tmp", 3).replace('\n', '')
        local_jar_mode = int(linecache.getline("tmp/"+str(i)+".tmp", 4))
        jar_local_file = linecache.getline("tmp/"+str(i)+".tmp", 5).replace('\n', '')
        jar_installer_file = linecache.getline("tmp/"+str(i)+".tmp", 6).replace('\n', '')
        
        month, day_of_week = setting_week_day_or_month(dt_now)
        
        if not local_jar_mode == 0:
            
            if local_jar_mode == 1:
                server_version = os.path.splitext(os.path.basename(jar_local_file))[0]
                shutil.copy(jar_local_file, minecraft_dir)
                jar_start_file = "server.jar"
            
            if local_jar_mode == 2:
                shutil.copy(jar_installer_file, minecraft_dir)
                jar_start_file = jar_installer_file.replace('-installer', '')
                server_version = os.path.splitext(os.path.basename(jar_start_file))[0]
                control.exec_java(minecraft_dir, jar_installer_file, "1", "1", "--installServer")
        else:
            try:
                print("Version "+server_version+" Download.")
                # マイクラjarファイルダウンロード
                download(get_minecraft_new_version(server_version)[1], minecraft_dir+"/server.jar")
                jar_start_file = "server.jar"
            # ダウンロード時の例外処理
            except Exception as e:
                check.except_print(e, "", True)
        
        
        # eula.txt create&write
        f = open(minecraft_dir+"/eula.txt", 'w')
        f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+day_of_week+" "+month+" "+dt_now.strftime('%d')+" "+dt_now.strftime('%H:%M:%S')+" "+str(dt_now.tzinfo)+" "+dt_now.strftime('%Y')+"\neula="+str(eula))
        f.close()
        
        # server properties donwload
        download_text("https://server.properties/", minecraft_dir+"/server.properties")
        # server properties edit port
        file_identification_rewriting(minecraft_dir+"/server.properties", "server-port=", "server-port="+server_port+"\n")
        # server properties edit motd(server name)
        file_identification_rewriting(minecraft_dir+"/server.properties", "motd=", "motd="+server_name+"\n")
        
        server_list_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
        with open('data/minecraft-list.txt', 'a', encoding="utf-8") as f:
            print("["+str(server_list_lines_count + 1)+"] Server name: "+server_name+" | Creation time: "+dt_now.strftime('%Y/%m/%d %H:%M:%S')[:-3]+" | Server Version: "+server_version+" | Minecraft Server Directory: "+minecraft_dir+"/", file=f)
        with open('data/minecraft-dir-list.txt', 'a', encoding="utf-8") as f:
            print(minecraft_dir, file=f)
        
        # サーバーディレクトリに管理用txtファイルを作成
        with open("data/"+minecraft_dir.replace('/', '-')+".txt", 'w', encoding="UTF-8") as f:
            print(server_version+"\n"+jar_start_file, file=f)

    # Remove directory temp
    shutil.rmtree("tmp")
    print("\nServer make complete!\n")