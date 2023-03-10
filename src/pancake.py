import control
import check
import make
import time
import sys

version = 0.8
edition = "beta".lower()

def pancake():
    print("\nPancake\nVersion: ",str(version)+"-"+edition,"\n")
    if not edition == "release":
        print("このプログラムは不安定版です。")
    print("\nモードを選択してください。")
    
    while True:
        mode = input("作成モード[Make]\n管理モード[Control]\nソフトウェアを終了[Exit]\n[M,C,E]: ").lower()
        if mode in ["make", "mak", "ma", "m"]:
            make.run()
        if mode in ["control", "contro", "contr", "cont", "con", "co", "c"]:
            control.main()
        if mode in ["exit", "exi", "ex", "e"]:
            sys.exit(0)

if __name__ == "__main__":
    title = "Autoer!"
    for i in title:
        time.sleep(0.1)
        print(i, end="", flush=True)
        time.sleep(0.1)
    print()
    
    check.run()
    pancake()