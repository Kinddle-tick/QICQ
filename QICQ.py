#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Kinddle
# Description: UDP局域网聊天工具

import tkinter as tk
import socket
import threading


class GUI():
    root = tk.Tk()
    My_Host = "127.0.0.1"
    To_Host = "127.0.0.1"
    QQ_Port = 8765
    def __init__(self, datalink=None, flesh_f=0.1):
        self.datadic = datalink
        root = self.root
        width = root.winfo_screenwidth() * 0.6
        height = root.winfo_screenheight() * 0.8
        self.center_window(width, height)  # 设置窗口位置
        # 可变标签初始化
        self.My_IP = tk.StringVar()
        self.My_IP.set(f"IP:{self.My_Host}")
        self.To_IP = tk.StringVar()
        self.To_IP.set(f"To:{self.To_Host}")

        # 设置框架
        self.controller_frm = tk.Frame(root, bg='#CCFFFF')
        self.Track_frm = tk.Frame(root, bg="#242424")
        self.Rate_frm = tk.Frame(root ,bg ="#CCFFFF")
        self.Fall_frm = tk.Frame(root,bg="#FFFF66")
        self.record_frm = tk.Frame(self.Track_frm,bg='#F0F0F0')
        self.send_frm = tk.Frame(self.Track_frm)
        # 框架的初始化
        self.cfg_controller()
        self.cfg_Track()
        self.cfg_Rate()
        self.cfg_Fall()
        #准备套接字
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.My_Host,self.QQ_Port))
        self.sock.setblocking(False)

        self.loop_listen()

    def listen(self):
        print("start listen")
        while True:
            try:
                data,addr = self.sock.recvfrom(65535)
            except Exception as z:
                pass
            else:
                print(addr, data)
                txt = f"from {addr[0]}:\n{data.decode()}"
                self.record.insert(tk.END,txt)

    def loop_listen(self):
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def refresh(self, T=False, R=False, F=False):
        if T:
            pass
        if R:
            self.My_IP.set('呼吸率：%d' % self.datadic['R'][2])
            self.To_IP.set('心率:%d' % self.datadic['R'][3])
        if F:
            stat = self.datadic['F']
            self.Fall_txt.insert(0.0, '\n')
            txt_insert = '平静' if stat==0 else '慢蹲或坐下' if stat == 1 else '跌倒！！' if stat == 2 else "未知数据"
            self.Fall_txt.insert(0.0,txt_insert)
# ---------------------------------------------------------------------------------#
    def center_window(self, width, height):
        root = self.root
        root.title('Contoller')
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        print(size)
        root.geometry(size)
        print(id(root) == id(self.root))
        #self.root = root
        #root.update()
        print(root.winfo_x())

    def _Mydestroy(self):
        self.sock.close()
        self.root.destroy()
    def _Mysend(self):
        txt = self.send.get(0.0,tk.END)
        print(txt)
        try:
            self.sock.sendto(txt.encode(),(self.To_Host,self.QQ_Port))
        except Exception as Z:
            print(Z)
        self.record.insert(tk.END, f"you:\n{txt}")
        self.send.delete(0.0,tk.END)
        pass
    def _MyfleshIP(self):
        txt = self.ent.get()
        self.To_Host = txt
        self.To_IP.set(f"To:{txt}")
    def _MyfleshIP_me(self):
        txt = self.ent2.get()
        self.My_Host = txt
        self.My_IP.set(f"IP:{txt}")
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.My_Host, self.QQ_Port))
        self.sock.setblocking(False)

    def cfg_controller(self):
        root = self.controller_frm
        root.place(relx=0, rely=1, relwidth=1, height=50, y=-50)
        # 退出按钮
        btnc1 = tk.Button(root, text='退出', command=self._Mydestroy)
        btnc1.place(relx=0.9, rely=0.1, relheight=0.8, relwidth=0.1*0.95)

        btnc2 = tk.Button(root, text='发送', command=self._Mysend)
        btnc2.place(relx=0.7, rely=0.1, relheight=0.8, relwidth=0.1*0.95)

    def cfg_Track(self):
        root=self.Track_frm
        root.place(relx=0, rely=0, relwidth= 0.8, relheight=1, height=-50)

        self.record_frm.place(relx=0, rely=0,relwidth=1,relheight=0.8)
        self.record=tk.Text(self.record_frm)
        self.record.place(relwidth=1, relheight=1,height=-10)
        self.send_frm.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        self.send = tk.Text(self.send_frm)
        self.send.place(relwidth=1, relheight=1)

    def cfg_Rate(self):
        root = self.Rate_frm
        root.place(relx=0.8, relheight=0.6, relwidth=0.2, height=0)
        lb_breath = tk.Label(root, textvariable=self.My_IP, font=30, bg='#83d7e6', relief = tk.GROOVE)
        lb_heart = tk.Label(root, textvariable=self.To_IP, font=30, bg='#83d7e6', relief = tk.GROOVE)
        lb_breath.place(relx=0.05, rely=0.05, relheight=0.1, relwidth=0.9)
        lb_heart.place(relx=0.05, rely=0.15, relheight=0.1, relwidth=0.9)

    def cfg_Fall(self):
        root=self.Fall_frm
        root.place(relx=0.8, rely=0.6, relheight=0.4, relwidth=0.2, height=-50)
        lb = tk.Label(root,text="设置", bg='#f2e599')
        lb.place(relheight=0.15, relwidth=1)
        lb2 = tk.Label(root, text="发至", bg='#f2e599')
        lb2.place(rely=0.2, relheight=0.15, relwidth=0.2)
        self.ent = tk.Entry(root)
        self.ent.place(relx=0.2, rely=0.2, relheight=0.15, relwidth=0.8)

        btnc1 = tk.Button(root, text='同步', command=self._MyfleshIP)
        btnc1.place(relx=0.05, rely=0.4, relheight=0.15, relwidth=0.9)

        lb2 = tk.Label(root, text="自身", bg='#f2e599')
        lb2.place(rely=0.6, relheight=0.15, relwidth=0.2)
        self.ent2 = tk.Entry(root)
        self.ent2.place(relx=0.2, rely=0.6, relheight=0.15, relwidth=0.8)

        btnc1 = tk.Button(root, text='同步', command=self._MyfleshIP_me)
        btnc1.place(relx=0.05, rely=0.8, relheight=0.15, relwidth=0.9)









if __name__=="__main__":
    # datainit = {"T": [[[0,0,0],[1,1,1],[1,2,1]],[[3,3,3],[3,3,2],[3,2,1],[3,3,3]]],
    #             'R': [0.45,0.68,60,120],
    #             'F': 0}
    x = GUI()
    # x.refresh(True, True, True)
    # datainit['F'] = 2
    # x.refresh(F=True)
    x.root.mainloop()