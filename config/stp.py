import re

from Management import ssh,telnet
from config import ip,vlan


class STP:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa STP")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.vlan_obj = vlan.VLAN(ip_session)
        self.ip_obj = ip.IP(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def add_rstp_bridge_priority(self, bridge_priority=None):

        if bridge_priority is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"spanning-tree priority {bridge_priority}\r\n")
            print(f"The bridge priority of the switch {self.ip_session} was changed to {bridge_priority}")

        else:

            print(f"The bridge priority of the swtich {self.ip_session} remains the same ")

    def remove_rstp_bridge_priority(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no spanning-tree priority \r\n")
        print(f"The bridge priority of the switch {self.ip_session} was changed to default")

    def add_rstp_port_cost(self, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree cost {cost}\r\n")
        self.session.send_cmd("!")

    def remove_rstp_port_cost(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree cost\r\n")
        self.session.send_cmd("!")

    def add_rstp_port_priority(self, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree port-priority {port_priority}\r\n")
        self.session.send_cmd("!")

    def remove_rstp_port_priority(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree port-priority\r\n")
        self.session.send_cmd("!")

    def show_spanning_tree_rstp(self):

        d_root_id = {}
        d_bridge_id = {}
        d1 = {
            "Name":"",
            "Role":"",
            "State":"",
            "Cost":"",
            "Prio":"",
            "Type":""
        }
        ports = list()

        self.session.connect()
        self.session.send_cmd("show span\r\n")
        output = self.session.read()
        print(output)

        match = re.findall(r"\s+Priority\s+(\d+)\S+\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output) # Regex pentru Root ID si Bridge ID
        match1 = re.findall(r"([GExi\d/]+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+([\w\d]+)", output) # Regex pentru porturi

        print(match)
        print(match1)

        print("###################")

        d_root_id["Root Priority"] = match[0][0]
        d_root_id["Root MAC-Address"] = match[0][1]

        d_bridge_id["Bridge Priority"] = match[1][0]
        d_bridge_id["Bridge MAC-Address"] = match[1][1]

        print(d_root_id)
        print(d_bridge_id)

        print("###################")

        for attributes in match1:
            # print(attributes)
            d2 = {}
            for key, attribute in zip(d1.keys(), attributes):
                # print(key,attribute)
                d2[key] = attribute
            ports.append(d2)
        print(ports)

        return d_root_id, d_bridge_id, ports


obj = STP("10.2.109.178")
# obj.add_rstp_bridge_priority(bridge_priority=0)
# obj.remove_rstp_bridge_priority()
obj.add_rstp_port_cost(port="Gi 0/3", cost="4")
obj.remove_rstp_port_cost(port="Gi 0/3")
obj.add_rstp_port_priority(port="Ex 0/1", port_priority= "64")
obj.show_spanning_tree_rstp()
obj.remove_rstp_port_priority(port="Ex 0/1")
