from netmiko import ConnectHandler
import sys
import time

##getting system date
day=time.strftime('%d')
month=time.strftime('%m')
year=time.strftime('%Y')
today=day+"-"+month+"-"+year
dtype = 'aruba_os'

class ArubaSSH:
    def __init__(self, uname, passwd, ipaddr):
        super(ArubaSSH, self).__init__()
        self.uname = uname
        self.passwd = passwd
        self.ipaddr = ipaddr
        # self.ipFile = "iplist.txt"
        # self.cmdFile = "aruba_cmd.txt"

        # selectIpfile = open(self.ipFile,'r')
        # selectIpfile.seek(0)
        # ipList = selectIpfile.readlines()
        # selectIpfile.close()        #
        # selectCmdfile = open(self.cmdFile,'r')
        # selectCmdfile.seek(0)
        # cmdList = selectCmdfile.readlines()
        # selectCmdfile.close()

    def connectSsh(self):
        ipaddr = self.ipaddr.rstrip()

        try:
            net_connect = ConnectHandler(device_type=dtype, ip=ipaddr, username=self.uname, password=self.passwd)
            time.sleep(1)
            #Configure switch using cmd file

            #net_connect.send_config_from_file(cmdList)
            hostname = net_connect.find_prompt()
            hostname = hostname.rstrip('#')
            if hostname:
                return "success"
            else:
                return "failed"
            #
            # for cmd in cmdList:
            #     cmd = cmd.rstrip()
            #     cmdOutput = net_connect.send_command(cmd, expect_string=r"#")
            #     print("Sending command '" + cmd + "' to " + ipaddr)
            #     print(cmdOutput)
            #
            # filename = hostname + '-' +ipaddr + '-' + today + ".txt"
            #Get running config
            # sRoutput = net_connect.send_command('show run')
            # saveconfig=open(filename,'w+')
            # print(ipaddr + " Saving running configuration to file")
            # saveconfig.write(sRoutput + "\n")
            # saveconfig.close()
        except:
            return "offline"
            pass
