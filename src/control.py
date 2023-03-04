import subprocess
import linecache
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
        choice_lines = input("サーバーの番号を入力してください: ")
        if not choice_lines or not choice_lines.isdigit():
            continue
        if int(choice_lines) <= 0 or int(minecraft_server_dir_list_txt_lines_count) < int(choice_lines) - 1 or int(minecraft_server_list_txt_lines_count) < int(choice_lines):
            continue
        break
    return choice_lines

def run():
    print("サーバー起動モード")
    # txtファイルカウント
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])

    if not minecraft_server_dir_list_txt_lines_count == minecraft_server_list_txt_lines_count:
        print("txtファイルの行数が合わないため、続行できません。")
        sys.exit(1)

    print("起動するサーバーを選んでください\n")
    # サーバー情報を読み込む
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    while True:
        choice_xms = input("Xms(サーバー最小割当メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(サーバー最大割当メモリ)を入力してください(G) ※数字のみ: ")
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
    print("サーバーポート変更モード")
    print("ポートを変更する、サーバーを選択してください。")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        input_port = input("変更するポートを入力してください: ")
        if not input_port or not str.isnumeric(input_port):
                continue
        else:
            break
    make.file_identification_rewriting(path+"/server.properties", "server-port=", "server-port="+input_port+"\n")
    print("サーバーのポートを変更しました。")

def make_sh():
    print("Please select the server where you want to create the sh-bat file.")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        choice_xms = input("Xms(サーバー最小割当メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(サーバー最大割当メモリ)を入力してください(G) ※数字のみ: ")
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
    print("sh-batファイルを作成しました。")

def network_info():
    network_info_select = make.input_yes_no("\n注意: IPを公開するのは、危険度が高いです。\nIPアドレスは重要な情報です。(電話番号のようなものです。) \nもし、あなたが配信やIPアドレスを見せたくない状況の場合には表示しないことをおすすめします。\n`yes` か `no`を選択してください。\n[Y/N]: ")
    if not network_info_select:
        return
    active, global_ip, private_ip = check.network("https://ifconfig.me")
    if not active:
        global_ip = "取得できません。"
    print("プライベートIP (同じネットワークで参加するために必要です。)"+private_ip)
    print("グローバルIP (外のネットワークから参加するために必要です。)"+global_ip)
    input()

def main():
    while True:
        choice = input("\nモードを選択してください。\nサーバー起動モード[run]\nサーバーポート変更モード[port]\nshとbatファイル作成[sh],[bat]\nネットワークの情報確認モード[IP]\n戻る | Exit (exit)\n[R,P,S,B,N,E]：").lower()
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