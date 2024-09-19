
class OSPFflow:


    def create_and_add_port_to_vlan(self, DUT, port, vlan):

        # Opening the port

        DUT.int.no_shut_interfaces(port)

        # Creating the VLAN on a DUT

        DUT.vl.create_vlan(vlan=vlan)

        # Adding the ports to the VLAN

        DUT.vl.add_ports_to_vlan(ports=port, vlan=vlan)

    def create_interfaces_vlan(self, DUT, vlan, ip, mask):

        # Create IP interfaces on DUT for the specific VLANs

        DUT.ip.add_ip_interfaces(vlan, int_vlan=[ip, mask])
        DUT.ip.no_shut_int_vlans(vlan)

    def create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(self,  DUT, port, vlan, ip, mask):

        # Create IP interfaces on DUT for the specific VLANs

        DUT.ip.add_ip_interface(int_vlan=vlan, ip=ip, mask=mask)
        DUT.ip.no_shut_int_vlan(int_vlan=vlan)

        # Opening the port

        DUT.int.no_shut_interface(interface=port)

        # Adding the ports to the VLAN

        DUT.vl.add_ports_to_vlan(ports=port, vlan=vlan)

    def create_routed_port_and_add_ip(self, DUT, interface, ip, mask):

        # Creating routed port

        DUT.int.add_routed_port(interface=interface)

        # Opening the port

        DUT.int.no_shut_interface(interface=interface)

        # Create IP Routed Port

        DUT.ip.add_ip_routed_port(interface=interface, ip=ip, mask=mask)

    def remove_routed_port(self, DUT, *args):

        # Removing routed port

        for int in args:

            DUT.int.remove_routed_port(interface=int)


    def enable_and_advertise_networks(self, DUT, **kargs):

        # Enable OSPF on all DUTs and advertise the Network IPs

        DUT.ospf.enable_ospf()

        for item in kargs.values():

            DUT.ospf.advertise_network(ip_network=item[0],area=item[1])

    def confirm_network_details_in_the_routing_table(self, DUT, network, protocol=None, AD=None, metric=None, metric_type=None, mask=None):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network in dict_of_networks.keys()
        print(f"The network {network} is in the routing table of DUT {DUT.hostname}")

        if protocol is not None:

            if metric_type is not None:

                assert dict_of_networks[network]['Protocol'] == protocol + metric_type
                print(f"The network {network} has the protocol {dict_of_networks[network]['Protocol']}")

            else:

                assert dict_of_networks[network]['Protocol'] == protocol
                print(f"The network {network} has the Protocol {dict_of_networks[network]['Protocol']}")

        if AD is not None:

            assert dict_of_networks[network]['AD'] == AD
            print(f"The network {network} has the AD {dict_of_networks[network]['AD']}")

        if metric is not None:

            assert dict_of_networks[network]['Metric'] == metric
            print(f"The network {network} has the Metric {dict_of_networks[network]['Metric']}")

        if mask is not None:

            assert dict_of_networks[network]['Mask'] == mask
            print(f"The network {network} has the Mask {dict_of_networks[network]['Mask']}")


    def confirm_network_in_the_routing_table(self, DUT, network):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network in dict_of_networks.keys()
        print(f"The network {network} is in the routing table of DUT {DUT.hostname}")

    def confirm_network_not_in_the_routing_table(self, DUT, network):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network not in dict_of_networks.keys()
        print(f"The network {network} is not in the routing table of DUT {DUT.hostname}")

    def confirm_ospf_neighbors(self, DUT, neighbor_id, state):

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert neighbor_id in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[neighbor_id]['Neighbor-ID'] == neighbor_id
        assert state in dict_of_ospf_neighbors[neighbor_id]['State']

        print(f"The adjacency state of neighbor {dict_of_ospf_neighbors[neighbor_id]['Neighbor-ID']} "
              f"is {dict_of_ospf_neighbors[neighbor_id]['State']} on DUT {DUT.hostname}")

    def confirm_neighbor_not_present(self, DUT, neighbor_id):

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert neighbor_id not in dict_of_ospf_neighbors.keys()

        print(f"The adjacency state of neighbor {neighbor_id} is not present on DUT {DUT.hostname}")

    def disable_OSPF(self, DUT):

        DUT.ospf.disable_ospf()

    def remove_networks(self, DUT, **kwargs):

        # Remove the Network IPs from OSPF

        for item in kwargs.values():

            DUT.ospf.remove_network(ip_network=item[0], area=item[1])


    def remove_vlans_and_interfaces_vlan(self, DUT, *args):

        for vlan in args:

            DUT.ip.remove_vlan_interfaces(vlan)

            DUT.vl.remove_vlans(vlan)

    def shut_interfaces(self, DUT, *args):

        for interface in args:

            DUT.int.shut_interfaces(interface)

    def no_shut_interfaces(self, DUT, *args):

        for interface in args:

            DUT.int.no_shut_interfaces(interface)

    def check_authentication_key_in_running_config(self, DUT, authentication, authentication_key, message_digest_key):

        dict_key, dict_of_keys = DUT.ospf.show_run_ospf_key()
        print(dict_of_keys)

        assert dict_of_keys[f'key {message_digest_key}']['Authentication'] == authentication
        assert authentication_key not in dict_of_keys[f'key {message_digest_key}']['key_Text']

        print(f"The message_digest_key {message_digest_key} with authentication key {authentication_key}"
              f" is not present in the running-config of DUT {DUT.hostname}")