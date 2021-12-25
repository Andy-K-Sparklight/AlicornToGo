#-*- coding:utf-8 -*-
import os, stat
from tkinter.messagebox import showinfo
from tkinter import StringVar, Tk, Label, HORIZONTAL
from tkinter.ttk import Progressbar
from webbrowser import open_new_tab
from requests import get
from subprocess import Popen
from sys import exit
from time import localtime, strftime
from zipfile import ZipFile
import _thread as thread
from traceback import format_exc
from shutil import rmtree


def main():
    home = os.path.expanduser("~")
    alicorn_beacon = os.path.join(home, "alicorn-launcher")
    if os.path.exists(alicorn_beacon):
        Popen(alicorn_beacon)
        exit(0)
        return
    else:
        fetch()


def catch_file_down(ui, progress, sv):
    try:
        file_down(ui, progress)
    except:
        print(format_exc())
        open_new_tab("https://alc.pages.dev/from-togo")
        ui.destroy()


def file_down(ui, progress):
    home = os.path.expanduser("~")
    today = localtime()
    y = int(strftime("%Y", today))
    m = int(strftime("%m", today))
    headers = {'Proxy-Connection': 'keep-alive'}
    while y >= 2021:
        cur = str(y) + "." + str(m)
        u = "https://cdn.jsdelivr.net/gh/Andy-K-Sparklight/AlicornVersions@" + cur + "/url"
        print("Requesting " + u)
        r2 = get(u, headers=headers)
        if r2.status_code == 200:
            urls = r2.content.decode("utf-8").split(" ")
            r = None
            for u in urls:
                print("Trying " + u)
                r = get(u, stream=True, headers=headers)
                if r.status_code == 200:
                    print("Will download from " + u)
                    break
                else:
                    print("URL " + u + " failed! Trying next one.")
            if r.status_code != 200:
                print("All urls have failed!")
                open_new_tab("https://alc.pages.dev/from-togo")
                ui.destroy()
                exit(0)
                return False
            progress["mode"] = "determinate"
            progress.stop()
            size = 0
            chk = 1024
            total = int(r.headers['content-length'])
            print("File size is: " + str(total))
            f = os.path.join(home, "alicorn-to-go.zip")
            with open(f, "wb") as file:
                for data in r.iter_content(chunk_size=chk):
                    file.write(data)
                    size += len(data)
                    prog = int((size / total) * 100)
                    progress["value"] = prog
                file.close()
            z = ZipFile(f)
            d = os.path.join(home, "alicorn-to-go")
            rmtree(d)
            os.makedirs(d)
            z.extractall(d)
            z.close()
            os.remove(f)
            al = os.path.join(d, "Alicorn-win32-x64", "Alicorn.exe")
            os.chmod(al, stat.S_IRWXO)
            os.chmod(al, stat.S_IRWXG)
            os.chmod(al, stat.S_IRWXU)
            Popen(al)
            root.destroy()
            return True
        else:
            m -= 1
            if m <= 0:
                m = 12
                y -= 1
    return False


def fetch():
    closed = False
    root = Tk()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = sw / 4
    wh = sh / 4
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    root.title("Alicorn ToGo")
    sv = StringVar()
    sv.set("这是你第一次使用 Alicorn ToGo，我们需要进行一些准备工作。\n这不会需要很久的。")
    label = Label(root, textvariable=sv, justify="center")
    label.pack(pady=wh / 5)
    progress = Progressbar(root,
                           orient=HORIZONTAL,
                           length=ww * 0.8,
                           mode="indeterminate")
    progress.pack()
    os.environ["NO_PROXY"] = "*"
    thread.start_new_thread(catch_file_down, (root, progress, sv))
    progress.start()
    root.mainloop()


if __name__ == '__main__':
    main()
