import tkinter as tk
import socket as sk
import sqlite3 as db
import threading
import time
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import concurrent.futures
import multiprocessing
import queue

class PortScannerDAL:
    def __init__(self):
        self.is_conn_open = False
        self.__connect_()
    def __connect_(self):
        if not self.is_conn_open:
            self.conn = db.connect('PortScanner.sqlite3')
            self.conn.row_factory = db.Row
            self.cur = self.conn.cursor()
            self.is_conn_open = True

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    def read_host(self, host_ip, host_name = None):
        try:
            self.cur.execute("SELECT HostId, HostName, HostIp FROM Host WHERE HostIp = ?", (host_ip,))
            r = self.cur.fetchall()
            return r
        except Exception as e:
            print(e)

    def save_host(self, host_ip, host_name):
        result = self.read_host(host_ip)
        if len(result) == 0:
            self.create_host(host_ip=host_ip, host_name=host_name)
            result = self.read_host(host_ip)

        else:
            pass
        return result[0]['HostId']

    def create_host(self, host_ip, host_name):
        self.cur.execute('INSERT INTO Host(HostName, HostIp) VALUES(?, ?)', (host_name, host_ip))
        self.conn.commit()

    def count_Table(self):
        self.cur.execute('select count(*) from Host')
        self.conn.commit()
        return self.cur.fetchone()[0]

    def trunc_table(self):
        self.cur.execute('delete from Host')
        self.cur.execute('delete from Scan')
        self.cur.execute('delete from PortStatus')
        self.conn.commit()

    def create_scan(self, host_id):
        self.ScanStartTime=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        self.cur.execute('INSERT INTO Scan(HostId, ScanStartTime) VALUES(?, ?)', (host_id, self.ScanStartTime))
        self.conn.commit()
        return self.cur.lastrowid

    def update_scan_end_time(self, scan_id):
        endtime = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        self.cur.execute('UPDATE Scan SET ScanEndTime=? WHERE ScanId=?', (endtime,scan_id))
        self.conn.commit()

    def read_scan(self):
        try:
            self.cur.execute("SELECT * from Scan")
            r = self.cur.fetchall()
            return r
        except Exception as e:
            print(e)

    def read_status(self):
        try:
            self.cur.execute("SELECT * from PortStatus")
            r = self.cur.fetchall()
            return r
        except Exception as e:
            print(e)

    def read_port_status(self, host_ip, host_name):
        self.cur.execute('''
        SELECT ps.*, s.ScanStartTime
        FROM PortStatus ps
        JOIN Scan s on ps.ScanId = s.ScanId
        JOIN Host h on h.HostId = s.HostId
        WHERE h.HostIP = ? AND h.HostName = ?
        ''',(host_ip, host_name))
        return self.cur.fetchall()

    def create_port_status(self, scan_id, port, is_open):
        self.cur.execute('INSERT INTO PortStatus(ScanId, PortNumber,IsPortOpen) VALUES(?, ?, ?)', (scan_id, port, is_open))
        self.conn.commit()

    def __close_connection_(self):
        if self.is_conn_open:
            self.conn.commit()
            self.conn.close()
            self.is_conn_open = False

    def __del__(self):
        self.__close_connection_()


class ResultsDialog(tk.Toplevel):
    def __init__(self, master, host_ip, host_name):
        dal = PortScannerDAL()
        reports = dal.read_port_status(host_ip, host_name)
        treeScroll = ttk.Scrollbar(master, orient="vertical")

        self.result_dialog = tk.Toplevel(master)
        self.result_dialog.title('Show Results')
        # self.om1_var = tk.StringVar()
        self.grd = tk.Frame(self.result_dialog)
        self.grd.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.treeview = ttk.Treeview(self.grd)
        self.treeview['columns'] = ('ScanID', 'PortNumber', 'IsOpen', 'ScanTime')
        self.treeview.heading('ScanID', text='ScanID')
        self.treeview.heading('PortNumber', text='Port Number')
        self.treeview.heading('IsOpen', text='Is Open')
        self.treeview.heading('ScanTime', text='Scan Time')
        cpt = 0
        for row in reports:
            #self.treeview.insert('', 'end', text=str(cpt), values=(row[0], row[1], row[2], row[3]))
            self.treeview.insert('', 0, values=(row[0], row[1], row[2], row[3]))
            cpt += 1
        self.treeview.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.result_dialog.mainloop()

def scan_port(ip, port, delay):
        if ip==None or ip=='':
            print('error')
        else:

            s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
            s.settimeout(delay)
            try:
                result = s.connect_ex((ip, port))
                if result == 0:
                    print('%s : %s is open.' % (ip, port))
                else:
                    print('%s:%s is close.' % (ip, port))
            except Exception as e:
                print('%r generated an exception: %s %s' % (ip, port, e))
                #msg.showerror('Error',str(e))
        return port

class PortScanner:
    def __init__(self):
        self.keep_alive=False
        self.min_port=0
        self.max_port=1024
        self.ip_address="127.0.0.1"
        self.dal = PortScannerDAL()
        self.que = queue.Queue()
        self.Host_Id = None
        self.host_name = ""
        self.__init_gui()

    def __init_gui(self):
        self.root = tk.Tk()
        self.root.geometry("250x150")
        self.root.title('Port Scanner')
        lbl_ip = tk.Label(self.root, text='Host IP:').grid(row=0,column=0)
        lbl_host_name = tk.Label(self.root, text='Host Name:').grid(row=1,column=0)
        self.the_host_name = tk.StringVar()
        self.lbl_host_name_show = tk.Label(self.root, textvariable=self.the_host_name).grid(row=1,column=1)
        #self.the_host_name=self.text=str(self.__update_host_name)
        # self.lbl_host_name_show.config(self.the_host_name)
        self.ip_val=tk.StringVar()
        self.tb_ip=tk.Entry(self.root,textvariable=self.ip_val).grid(row=0,column=1)
        self.btn_scan=tk.Button(self.root,text="Scan",state=tk.NORMAL,command=self.__start_scanner)
        self.btn_view_result=tk.Button(self.root,text="View Results",command=self.__view_results)
        self.btn_scan.place(x = 70, y = 50, width=125, height=25)
        self.btn_view_result.place(x = 70, y = 80, width=125, height=25)
        self.scanStatus = tk.StringVar()
        self.scanStatus.set("Scanner is idle")
        self.lbl_status=tk.Label(self.root,textvariable=self.scanStatus)
        self.lbl_status.place(x = 0, y = 120, width=300, height=25)
        # self.btn_scan.grid(row=2,columnspan=2)
        # self.btn_view_result.grid(row=3,columnspan=2)
        self.worker = None
        WORKING, CANCELED, TERMINATING, IDLE = ("WORKING", "CANCELED",
"TERMINATING", "IDLE")
        self.state = multiprocessing.Manager().Value("i", IDLE)
        self.root.mainloop()

    def __start_scanner(self):
        #set the host name here
        self.btn_scan.config(state=tk.DISABLED)
        s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        ip=self.ip_val.get()
        self.ip_address = ip
        try:
            self.h_name = sk.gethostbyaddr(ip)[0]
        except Exception as e:
            self.btn_scan.config(state=tk.ACTIVE)
            return
        self.the_host_name.set(self.h_name)
        self.host_name = self.h_name
        self.Host_Id = self.dal.save_host(self.ip_address, self.h_name)
        self.worker = threading.Thread(target=self.start_scanner, args=(ip,))
        self.worker.daemon = True
        self.worker.start()
        self.update_me()



    def process(self, future):
        result = future.result()
        self.scanStatus.set("Scanning port number %s" % result)

    def update_me(self):
        try:
            while 1:
                msg = self.que.get_nowait()
                self.scanStatus.set("Scanning port number %s" % msg)
        except queue.Empty:
            pass
        self.root.after(100, self.update_me)
    #self.start_scanner1()
    def start_scanner(self, ip):
        futures = set()
        dal = PortScannerDAL()
        scanid = dal.create_scan(self.Host_Id)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for port in range(self.min_port, self.max_port):
                    future = executor.submit(self.scan_port, ip, port, 10, self.que, scanid)
                    futures.add(future)
                    #future.add_done_callback(self.process)
                concurrent.futures.wait(futures)
                self.btn_scan.config(state=tk.ACTIVE)
                self.scanStatus.set("Finished scanning.")
                dal.update_scan_end_time(scanid)
        except Exception as e:
            pass


    def scan_port(self, ip, port, delay, queue, scanid):
        dal = PortScannerDAL()
        if ip==None or ip=='':
            print('error')
        else:
            s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
            s.settimeout(delay)
            try:
                queue.put(port)
                result = s.connect_ex((ip, port))
                if result == 0:
                    #print('%s : %s is open.' % (ip, port))
                    pass
                else:
                    #print('%s:%s is close.' % (ip, port))
                    result = 1
                dal.create_port_status(scanid, port, result)
            except Exception as e:
                print(e)
                #msg.showerror('Error',str(e))
        return port



    def __view_results(self):
        ip=self.ip_val.get()
        self.ip_address = ip
        try:
            self.h_name = sk.gethostbyaddr(ip)[0]
        except Exception as e:
            return
        self.the_host_name.set(self.h_name)
        self.host_name = self.h_name
        ResultsDialog(self.root, self.ip_address, self.host_name)


    def __update_host_name(self):
        # self.lbl_host_name_show(text=self.h_name)
        self.h_name="123"

if __name__ == '__main__':
    ps = PortScanner()
