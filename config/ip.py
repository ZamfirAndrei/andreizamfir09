import re

from config import vlan
from Management import ssh,telnet


class IP:

    def __init__(self, ip):

        print("Clasa IP")

        self.ip = ip
        self.session = ssh.SSH(ip)
        self.vlan_obj = vlan.VLAN(ip) # Creez obiectul prin care ma voi folosii de metodele/functiile specifice vlan
                                      # vlan --> folderul unde am creat functiile de vlan,
                                      # .VLAN --> apelez clasa din interiorul folderului vlan

    def create_int_vlan(self, int_vlan=None):

        output = ""

        if int_vlan is None:

            print("Baga drq o interfata")

        else:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"int vlan {int_vlan}\r\n")
            self.session.send_cmd("no shut\r\n")
            output = self.session.read()
            print(output)
            print("The interface VLAN was created succesfully")
            self.session.close()

        return output

    def remove_int_vlan(self, int_vlan=None):

        output = ""

        if int_vlan is None:
            print("Selecteaza drq o interfata")
        else:
            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"no int vlan {int_vlan}\r\n")
            output = self.session.read()

            if "%The VLAN interface must be administratively down before deleting" in output:

                print("We have to shut the interface first")
                self.session.send_cmd(f"int vlan {int_vlan}\r\n")
                self.session.send_cmd("shut\r\n")
                self.session.send_cmd("!\r\n")
                self.session.send_cmd(f"no int vlan {int_vlan}\r\n")
                output = self.session.read()
                print(output)
                print(f"The inteface vlan {int_vlan} has been removed succesfully")


            elif "% Invalid Interface Index" in output:

                print("The interface does not exist")
                print(output)

            else:

                print(output)
                print(f"The inteface vlan {int_vlan} has been removed succesfully")

        self.session.close()

        return output

    def show_ip_int(self, int_vlan=None):

        output = ""

        d = {
            "Int Vlan":"",
            "The Interface is":"",
            "Line Protocol is":"",
            "Ip Address":"",
            "Mask":""
        }

        if int_vlan is not None:

            self.session.connect()
            self.session.send_cmd(f"show ip int vlan {int_vlan}\r\n")
            output = self.session.read()
            print(output)

            if "% Invalid Vlan Interface" in output:

                print("The interface does not exist")

            else:

                match = re.findall(r"(vlan\d+) is (\w+).\s+line protocol is (\w+).+Internet Address is (\d+.\d+.\d+.\d+)/(\d+)", output)
                print(match)

                for key, attribute in zip(d.keys(),match[0]):
                    d[key] = attribute
                print(d)

        else:

            self.session.send_cmd("show ip int\r\n")
            output = self.session.read()
            print(output)

        self.session.close()

        return output

    def add_ip_interface(self, int_vlan=None, ip=None, mask=None, dhcp="No"):

        output = ""

        if int_vlan is not None and ip is not None and mask is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"int vlan {int_vlan}\r\n")

            if dhcp == "No":

                self.session.send_cmd(f"ip add {ip} {mask}\r\n")

            else:

                self.session.send_cmd("ip add dhcp\r\n")

            output = self.session.read()
            print(output)

        else:

            print("Mai baga o fisa")

        self.session.close()

        return output

    def remove_ip_interface(self,int_vlan=None):

        output = ""

        if int_vlan is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"int vlan {int_vlan}\r\n")
            self.session.send_cmd("no ip add\r\n")
            output = self.session.read()
            print(output)

        self.session.close()

        return output

    def add_static_route(self, network_dest=None, mask_dest=None, next_hop=None):

        output = ""

        if network_dest is not None and mask_dest is not None and next_hop is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"ip route {network_dest} {mask_dest} {next_hop}\r\n")
            output = self.session.read()
            print(output)

        else:

            print("Tete")

        self.session.close()

        return output

    def remove_static_route(self, network_dest=None, mask_dest=None, next_hop=None):

        output = ""

        if network_dest is not None and mask_dest is not None and next_hop is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"no ip route {network_dest} {mask_dest} {next_hop}\r\n")
            output = self.session.read()
            print(output)

            if "% Route entry not Present" in output:

                print("The route does not exist!")

            else:

                print("The route was removed succesfully!")

        self.session.close()

        return output

    def show_ip_route(self,network = None):

        output = ""

        # Dictionar pentru Rutele Direct Conectate

        # d1 = {
        #     "Protocol":"",
        #     "Network":"",
        #     "Mask":"",
        #     "Vlan/Port":""
        # }
        # Dictionar pentru Rutele invatate printr-un protocol de rutare/Rute statice

        d2 = {
            "Protocol":"",
            "Network":"",
            "Mask":"",
            "AD":"",
            "Metric":"",
            "Next Hop":""
        }

        self.session.connect()

        networks = list()
        ip_route = {}

        if network is None:

            self.session.send_cmd("show ip route\r\n")
            output = self.session.read()
            # print(output)
            match = re.findall(r"([SRO\sIANE12]+)\s+(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)/(\d+)\S via (\d+.\d+.\d+.\d+)", output)
            # print(match)
            # print(len(match[0]))
            # print(len(d2))
            for i in range(len(match)):
                # print("##################")
                # print(match[i])
                d3 = {} # Creez un nou dictionar care va folosii key ile de la dictionarul d2 si va lua valorile din lista de tupluri de la match
                        # Daca foloseam doar dictionarul d2 atunci mereu se updata dictionarul cu ultimul tuplu iterat.

                for key, attribute in zip(d2.keys(), match[i]):

                    d3[key] = attribute

                # print(d3)
                networks.append(d3)

                # print("##################")


            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            match2 = re.findall(r"(C)\s(\d+.\d+.\d+.\d+)/(\d+)\s+is (directly connected), ([\w/\d]+)", output)
            # print(match2)

            networks_connected = list()

            # Varianta de populare a unui dictionar nu pre-made ca mai sus.

            for i in range(len(match2)):
                d1 = {}
                #print(match2)

                for attribute in range(len(match2[i])):
                    #print(attribute)

                    d1["Protocol"] = match2[i][0]
                    d1["Network"] = match2[i][1]
                    d1["Mask"] = match2[i][2]
                    d1["Vlan/Port"] = match2[i][4]

                # print(d1)
                networks_connected.append(d1)
                networks.append(d1)

                # print(networks_connected) # Lista pentru networkurile direct connectate

            print(networks)  # Am format o Lista de dictionare
            # print(networks[1])
            # print(networks[1]['Network']) # Aflam pt elem 1 din lista ip-ul de la cheia Network
        else:

            self.session.send_cmd(f"show ip route {network}\r\n")
            output = self.session.read()
            # print(output)

            if "is directly connected" not in output:
                match = re.findall(r"([SRO\sIANE12]+)\s+(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)/(\d+)\S via (\d+.\d+.\d+.\d+)",output)
                # print(match)

                ip_route["Protocol"] = match[1][0]
                ip_route["Network"] = match[1][1]
                ip_route["Mask"] = match[1][2]
                ip_route["AD"] = match[1][3]
                ip_route["Metric"] = match[1][4]
                ip_route["Next Hop"] = match[1][5]

                print(ip_route)

            else:
                match = re.findall(r"(C)\s(\d+.\d+.\d+.\d+)/(\d+)\s+is (directly connected), ([\w/\d]+)", output)
                # print(match)

                ip_route["Protocol"] = match[0][0]
                ip_route["Network"] = match[0][1]
                ip_route["Mask"] = match[0][2]
                ip_route["Vlan/Port"] = match[0][4]

                print(ip_route)

        self.session.close()

        return output



obj = IP("10.2.109.178")
# obj.create_int_vlan()
# obj.create_int_vlan(int_vlan="200")
# obj.remove_int_vlan(int_vlan="1000")
# obj.remove_int_vlan(int_vlan="100")
# obj.remove_int_vlan()
# obj.remove_int_vlan(int_vlan="201")
# obj.show_ip_int("50")
# obj.show_ip_int("30")
# obj.show_ip_int()
# obj.show_ip_int(int_vlan="200")
# obj.add_ip_interface(int_vlan="200",ip="200.0.0.1",mask="255.255.0.0")
# obj.add_ip_interface(ip="200.0.0.1",mask="255.255.0.0",dhcp="Yes")
# obj.remove_ip_interface(int_vlan="200")
# obj.show_ip_int(int_vlan="500")
#obj.add_static_route(network_dest="220.0.0.0", mask_dest="255.0.0.0", next_hop="14.0.0.1")
# obj.remove_static_route(network_dest="220.0.0.0", mask_dest="255.0.0.0", next_hop="14.0.0.1")
# obj.remove_static_route(network_dest="100.0.0.0", mask_dest="255.0.0.0", next_hop="14.0.0.1")
obj.show_ip_route()
print("#######################")
obj.show_ip_route("15.0.0.0")
print("#######################")
obj.show_ip_route("14.0.0.0")
print("#######################")
obj.show_ip_route("111.0.0.0")
print("#######################")
obj.show_ip_route("66.0.0.0")