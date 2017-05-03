import PortScanner

def main():
    dal = PortScanner.PortScannerDAL()

    sql_create_hosts_table = """
        CREATE TABLE IF NOT EXISTS Host(
             HostId INTEGER PRIMARY KEY   AUTOINCREMENT,
             HostName char(50) NOT NULL,
             HostIp   char(50) NOT NULL
        );
    """

    sql_create_Scan_table = """
        CREATE TABLE IF NOT EXISTS Scan(
             ScanId INTEGER PRIMARY KEY   AUTOINCREMENT,
             HostId INTEGER NOT NULL,
             ScanStartTime TEXT NULL,
             ScanEndTime TEXT NULL
        );
    """

    sql_create_PortStatus_table = """
        CREATE TABLE IF NOT EXISTS PortStatus(
             ScanId INTEGER not null,
             PortNumber Integer not null,
             IsPortOpen   Integer not null
        );
    """

    #dal.create_table(sql_create_hosts_table)
    #dal.create_table(sql_create_Scan_table)
    #dal.create_table(sql_create_PortStatus_table)


    #HostId = dal.save_host( '127.0.0.1', 'gdgd')
    #dal.trunc_table()
    cnt = dal.read_scan()
    print(cnt[0][0])
    print(cnt[0][1])
    print(cnt[0][2])
    print(cnt[0][3])

    cnt = dal.read_host('127.0.0.1')
    print(cnt[0][0])
    print(cnt[0][1])
    print(cnt[0][2])

    print('====================================')

    reports = dal.read_port_status('127.0.0.1', 'T1XPS8100-01.office.tournament1.com')
    print(reports[0][0])
if __name__ == '__main__':
    main()