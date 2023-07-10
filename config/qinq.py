import re
import time

from Management import ssh, telnet


class QinQ:

    def __init__(self, ip_session = "10.2.109.178"):

        print("Clasa QinQ")
        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        # self.tn = telnet.Telnet(ip=ip_session)

    def change_bridge_mode(self, bridge_mode):

        self.session.connect()
        self.session.send_cmd(f"boot default bridge-mode {bridge_mode} --y")
        self.session.close()
        print("The bridge-mode has been changed")
        # time.sleep(100)
        # self.session.connect(username="admin",password="admin")
        # output1 = self.session.read()
        # print(output1)
        # time.sleep(2)
        # self.session.send_cmd("Admin1234!\r\n")
        # time.sleep(2)
        # self.session.send_cmd("Admin1234!\r\n")
        # output = self.session.read()
        # print(output)

    def change_bridge_port_type(self, port, bridge_port_type):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"bridge port-type {bridge_port_type}\r\n")
        self.session.send_cmd("shut\r\n")
        self.session.send_cmd("no shut\r\n")
        print(f"The bridge port-typ has been changed to {bridge_port_type}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_cvlan_to_svlan(self, port, cvlan, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} service-vlan {svlan}\r\n")
        print(f"Added customer vlan {cvlan} to svlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_cvlan_to_svlan(self, port, cvlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport customer-vlan {cvlan} service-vlan\r\n")
        print(f"Removed customer vlan {cvlan} from svlan")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_default_service_vlan(self, port, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport service-vlan {svlan}\r\n")
        print(f"Added default svlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_default_service_vlan(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport service-vlan\r\n")
        print(f"Removed default svlan")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_customer_vlan_pvid(self, port, pvid):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan pvid {pvid}\r\n")
        print(f"Added customer vlan pvid {pvid}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_customer_vlan_pvid(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan pvid disable\r\n")
        print(f"Removed customer vlan pvid")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_service_vlan_pvid(self, port, svlan, pvid):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} pvid {pvid}\r\n")
        print(f"Added for service-vlan {svlan} pvid {pvid}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_service_vlan_pvid(self, port, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} pvid disable\r\n")
        print(f"Removed for service-vlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_svlan_prio(self, port, svlan_prio):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport svlan-prio {svlan_prio}\r\n")
        print(f"Added for the default service-vlan the svlan-prio {svlan_prio}")
        output = self.session.read()
        self.session.close()

    def remove_svlan_prio(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd("switchport svlan-prio none\r\n")
        print(f"Removed for the default service-vlan the svlan-prio")
        output = self.session.read()
        self.session.close()

    def add_customer_vlan_svlan_prio(self, port, cvlan, svlan_prio):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} svlan-prio {svlan_prio}\r\n")
        print(f"Added for the customer-vlan {cvlan} the svlan-prio {svlan_prio}")
        output = self.session.read()
        self.session.close()

    def remove_customer_vlan_svlan_prio(self, port, cvlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} svlan-prio none\r\n")
        print(f"Removed for the customer-vlan {cvlan} the svlan-prio")
        output = self.session.read()
        self.session.close()


obj_qinq = QinQ("10.2.109.198")
# obj_qinq.change_bridge_mode(bridge_mode="provider-edge")
# obj_qinq.change_bridge_port_type(port="Gi 0/10",bridge_port_type="provider")
# obj_qinq.add_cvlan_to_svlan(port="Gi 0/5", cvlan="20",svlan="2000")
# obj_qinq.remove_cvlan_to_svlan(port="Gi 0/5",cvlan="20")
# obj_qinq.add_default_service_vlan(port="Gi 0/5",svlan="3000")
# obj_qinq.remove_default_service_vlan(port="Gi 0/5")
# obj_qinq.add_customer_vlan_pvid(port="Gi 0/5",pvid="99")
# obj_qinq.remove_customer_vlan_pvid(port="Gi 0/5")
# obj_qinq.remove_service_vlan_pvid(port="Gi 0/5",svlan="1000")
# obj_qinq.add_service_vlan_pvid(port="Gi 0/5",svlan="1000",pvid="77")
# obj_qinq.add_svlan_prio(port="Gi 0/5", svlan_prio="3")
# obj_qinq.remove_svlan_prio(port="Gi 0/5")
# obj_qinq.add_customer_vlan_svlan_prio(port="Gi 0/5", cvlan="10", svlan_prio="7")
# obj_qinq.remove_customer_vlan_svlan_prio(port="Gi 0/5", cvlan="10")

