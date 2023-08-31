import paramiko
import time
from config import vlan, interfaces, ip, ping


def connection(ip="10.2.109.238", username="admin", password="Admin1234!"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("show ip int \r\n")
    shell.send("ping 8.8.8.8\r\n")
    time.sleep(1)
    output = shell.recv(65535)
    print(output)


def show_vlan_pagination_enable_disable(ip="10.2.109.198",username="admin", password = "Admin1234!"):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("conf t\r\n")
    shell.send("set cli pagination off\r\n")
    shell.send("do show vlan\r\n")
    time.sleep(2)
    output = shell.recv(65535)
    print(output)


# connection()
# show_vlan_pagination_enable_disable()

# ip_session = "10.2.109.238"
# vl = vlan.VLAN(ip_session=ip_session)
# int1 = interfaces.Interface(ip_session=ip_session)
#
#
# def exercitiu():
#
#
#     vl.create_vlan(vlan="150")
#     int1.no_shut_interface(interface="Gi 0/4")
#
#
# exercitiu()

d = { "Tete" : 2, "Sete" : 3}

for i in d:
    print(i)

