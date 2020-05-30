#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import json


class FilterModule(object):
    def filters(self):
        return {
            'replace_special_characters': self.replace_special_characters,
            'map_ports_to_uris': self.map_ports_to_uris,
            'map_vlans_to_uris': self.map_vlans_to_uris,
            'json_to_dict': self.json_to_dict,
            'add_lacp_key_interface': self.add_lacp_key_interface,
            'add_mtu_interface': self.add_mtu_interface,
            'add_admin_state_interface': self.add_admin_state_interface,
            'replace_value_in_key': self.replace_value_in_key,
            'add_key_and_value': self.add_key_and_value
        }

    def replace_special_characters(self, str_special_chars):
        """
        Replaces special characters in a string with their percent-encoded counterparts
            ':' -> '%3A'
            '/' -> '%2F'
            ',' -> '%2C'
        (e.g. "1/1/9" -> "1%2F1%2F9")
        :param str_special_chars: string in which to substitute characters
        :return: new string with characters replaced by their percent-encoded counterparts
        """
        str_percents = str_special_chars.replace(":", "%3A").replace("/", "%2F").replace(
            ",", "%2C")
        return str_percents
        
    def map_ports_to_uris(self, port_info_list):
        """
        Maps a list of port dictionaries to a list of Port table entry URIs
        (e.g. [{"name": "1/1/1", "description": "one"}, {"name": "1/1/2"}] ->
            ["/rest/v1/system/interfaces/1", "/rest/v1/system/interfaces/2"])
        :param port_info_list: List of port dictionaries
        return: List of Port table entry URIs
        """
        
        return ["/rest/v1/system/interfaces/%s" % self.replace_special_characters(port) for port in port_info_list]

    def map_vlans_to_uris(self, vlans_list):
        """
        Maps a list of VLAN IDs to a list of VLAN table entry URIs
        (e.g. [1, 2] -> ["/rest/v1/system/vlans/1", "/rest/v1/system/vlans/2"])
        :param vlans_list: List of VLAN IDs
        return: List of VLAN table entry URIs
        """
        
        return ["/rest/v1/system/vlans/%d" % int(vlan) for vlan in vlans_list]
    
    def json_to_dict(self, json_string):
        """
        This function converts the JSON string to a dict
        :param json_string: JSON string
        :return: interface_json
        """
        return json.loads(json_string)

    def add_lacp_key_interface(self, interface_json, lag_id):
        """
        This function sets the LACP aggregation key field in an Interface entry JSON
        :param interface_json: JSON from REST API GET /rest/v1/system
        :param lag_id: Numeric ID of the LAG to which the port is to be added
        :return: interface_json
        """
        if 'other_config' in interface_json.keys():
            interface_json['other_config']['lacp-aggregation-key'] = int(lag_id)
        else:
            interface_json['other_config'] = {'lacp-aggregation-key': int(lag_id)}

        return interface_json

    def add_mtu_interface(self, interface_json, mtu):
        """
        This function sets the MTU value in an Interface entry JSON
        :param interface_json: JSON from REST API GET /rest/v1/system
        :param mtu: Numeric MTU value
        :return: interface_json
        """
        if 'user_config' in interface_json.keys():
            interface_json['user_config']['mtu'] = int(mtu)
        else:
            interface_json['user_config'] = {'mtu': int(mtu)}

        return interface_json

    def add_admin_state_interface(self, interface_json, enabled):
        """
        This function sets the admin state in an Interface entry JSON
        :param interface_json: JSON from REST API GET /rest/v1/system
        :param enabled: True to enable; False otherwise
        :return: interface_json
        """
        if enabled:
            state = "up"
        else:
            state = "down"

        if 'user_config' in interface_json.keys():
            interface_json['user_config']['admin'] = state
        else:
            interface_json['user_config'] = {'admin': state}

        return interface_json

    def replace_value_in_key(self, get_json_data, json_key, json_value):
        """
        This function replaces the given key's value in the provided JSON
        with the given value. There is no error checking or validation.
        :param get_json_data: JSON from REST API GET
        :param json_key: Key string expected to be in get_json_data
        :param json_value: Value to be stored in get_json_data
        :return: get_json_data
        """
        
        if json_key in get_json_data.keys():
            if type(json_value) == type(get_json_data[json_key]):
                get_json_data[json_key] = json_value
        
        return get_json_data

    def add_key_and_value(self, get_json_data, json_key, json_value):
        """
        This function adds the given key to the provided JSON
        with the given value. There is no error checking or validation.
        :param get_json_data: JSON from REST API GET
        :param json_key: Key string to be added to get_json_data
        :param json_value: Value to be stored in get_json_data
        :return: get_json_data
        """
        
        get_json_data[json_key] = json_value
        
        return get_json_data
