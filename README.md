# aoscx-ansible-dcn-workflows
Welcome to the Aruba Switching Github repository for Data Center Networking (DCN) automation using Ansible workflows.
This repository provides several ready-to-run Ansible playbooks that automate provisioning for AOS-CX switches
in DCN architectures. 

## Contents
* [DCN Architectures](https://github.com/aruba/aoscx-ansible-dcn-workflows#dcn-architectures)
* [Project Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
* [Workflows](https://github.com/aruba/aoscx-ansible-dcn-workflows#workflows)  
    * [Architecture I - Campus Attached DC ToR](https://github.com/aruba/aoscx-ansible-dcn-workflows#architecture-i---campus-attached-dc-tor)  
    * [Architecture II - Dedicated Data Center Two-Tier](https://github.com/aruba/aoscx-ansible-dcn-workflows#architecture-ii---dedicated-data-center-two-tier)  
    * [Architecture III - Dedicated Data Center Layer 3 Spine/Leaf Topology - EBGP EVPN (multi-AS) VXLAN with VSX](https://github.com/aruba/aoscx-ansible-dcn-workflows#architecture-iii---dedicated-data-center-layer-3-spineleaf-topology---ebgp-evpn-multi-as-vxlan-with-vsx)  
    * [Architecture III - Dedicated Data Center Layer 3 Spine/Leaf Topology - IBGP EVPN VXLAN with VSX](https://github.com/aruba/aoscx-ansible-dcn-workflows#architecture-iii---layer-3-spineleaf-topology---ibgp-evpn-vxlan-with-vsx)  
    * [Configure VSX Standalone Playbook](https://github.com/aruba/aoscx-ansible-dcn-workflows#configure-vsx-standalone-playbook) 
    * [Configure Muti-Chassis LAG Standalone Playbook](https://github.com/aruba/aoscx-ansible-dcn-workflows#configure-multi-chassis-lag-standalone-playbook) 
* [Project Structure](https://github.com/aruba/aoscx-ansible-dcn-workflows#project-structure)
* [How To Contribute](https://github.com/aruba/aoscx-ansible-dcn-workflows#how-to-contribute)

## DCN Architectures
The workflows in this repository provision the switches according to the architectures outlined in the Validated Reference Designs (VRDs). The VRDs have been posted on the Aruba Airheads Community:
* [Architecture I - Campus Attached DC ToR (green box)](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-a-DC-Collapsed-Core-with-NetEdit/ta-p/555487)  
![Architecture I - Campus Attached DC ToR](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/files/images/campus_attached.png?raw=true)
* [Architecture II - Dedicated Data Center Two-Tier](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-a-2-Tier-DC-Network-with-NetEdit/ta-p/556403)  
![Architecture II - Dedicated Data Center Two-Tier](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/files/images/2tier.PNG?raw=true)
* Architecture III - Layer 3 Spine/Leaf Topology Dedicated Data Center
  * [IBGP EVPN VXLAN VSX Centralized L3 Gateway](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-IBGP-EVPN-VXLAN-VSX-Centralized-L3-Gateway-with/ta-p/626010)  
  * [EBGP EVPN (multi-AS) VXLAN with VSX Centralized L3 Gateway](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-EBGP-EVPN-multi-AS-VXLAN-with-VSX-Centralized-L3/ta-p/627317)
  
![Architecture III - Layer 3 Spine/Leaf Topology](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/files/images/spine_leaf.PNG?raw=true)


## Prerequisites
These workflows can be run on any Unix-based system. 

### Installations
* The Ansible control machine must have **Python2.7** or **Python3.5+** and at least **Ansible 2.8.1** installed. See [Ansible Documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) for more information on Ansible installation.

* This project requires the AOS-CX Ansible Role to be installed. The easiest way to install the role is by executing the `ansible-galaxy` command on the `requirements.yml` file:  
`$ ansible-galaxy install -r requirements.yml`  
For more information on how to use the `aoscx_role` visit our [Github](https://github.com/aruba/aoscx-ansible-role#aoscx).

* This project requires the Python libraries listed below to be installed. The easiest way to install the required libraries is using the `pip` command on the `requirements.txt` file:  
`$ pip install -r requirements.txt`

### Inventory Setup
This project contains multiple inventories, each corresponding to a specific workflow. Which inventory files correspond to which workflows is described in the [Workflows](https://github.com/aruba/aoscx-ansible-dcn-workflows#workflows) section of this document.
  
#### Making The Inventory Your Own
Each inventory provided is made to be an example. You are encouraged to change IP addressing and interface values to match your environment. 
Note that these inventories use a logical grouping method of to group VSX Pairs and assumes that each VSX pair of access/leaf switches is in a group. 
The names of these groups can be any alphanumeric name; this is just one approach to coupling VSX pairs. 
You can change the "rack#" nomenclature in the example inventory files to your liking as long as you keep the names consistent throughout the inventory.  
  
All the variables in the inventory files are necessary for the workflows to run. There are three broad categories of variables:
1. Some variables are static, such as the AOS-CX Ansible connection variables. These variables maintain constant values that should not be changed.
1. Some variables' values necessarily must be changed to match device information for your specific environment.
1. Some variables have default values that can be changed. Changing these is optional. 

Before executing a workflow, look through the inventory file used by that workflow, and change any variable values that must be changed, and also any variables you would like to change. 

* Examples of static inventory variables that **should not** be changed:
```YAML
ansible_connection: httpapi   # DO NOT CHANGE
ansible_network_os: aoscx   # DO NOT CHANGE
ansible_httpapi_use_ssl: True   # DO NOT CHANGE
config_template: leaf.j2
```

* Examples of inventory variables that **need** to be changed:
```YAML
ansible_host: 10.10.10.56 # IP address of the switch, change to match devices in your environment
server_vlans: [11]    # VLANs to be created on leafs for server traffic
core_mclag_uplink_ports: ['1/1/49', '1/1/50'] # Interfaces that will be a part of the MCLAG connecting access device to core
vsx_keepalive_int: 1/1/31
vsx_isl_ports: ['1/1/32']
```

* Examples of inventory variables that **can** be changed, but have default values that work:
```YAML
spine_L3fabric_ips:
  - 192.168.2.1
  - 192.168.2.3
  - 192.168.2.5
  - 192.168.2.7
loopback0_ip: 192.168.1.1
loopback1_ip: 192.168.100.1  
```


## Workflows
This project currently holds the following workflows to provision devices according to each architecture listed in 
[DCN Architectures](https://github.com/aruba/aoscx-ansible-dcn-workflows#dcn-architectures):


### Architecture I - Campus Attached DC ToR
This workflow provisions a campus attached data center set of top of rack AOS-CX switches in a VSX pair based on the [validated reference design](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-a-DC-Collapsed-Core-with-NetEdit/ta-p/555487).  

#### Workflow Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- Ensure the provided Ansible inventory file [inventory_2tier_dedicated_dc.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml)
 has been modified to suit your environment, according to the instructions in [Inventory Setup](https://github.com/aruba/aoscx-ansible-dcn-workflows#inventory-setup) above.
- L3 Campus Core
- DC Core switches = 2 AOS-CX switches (8xxx series, use latest firmware available)
  - DC Core switches should be in a VSX pair
- Out-of-Band management (OOBM) connection to management port on AOS-CX switches
  - Ansible control machine should be reachable via from each device's OOBM


 
#### Files Used
* Playbook : [deploy_campus_attached_dc_tor.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/deploy_campus_attached_dc_tor.yml)  
* Inventory : [inventory_2tier_dedicated_dc.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml)  
  * ***Note:** This inventory file is also used for the Architecture II workflow, so it contains additional information for access switches (Zone1-Rack<1/3>-Access<1/2/3/4>). 
  Valid values for variables relating to those devices are not necessary for this workflow.*
* Jinja2 Templates : [templates/2Tier/core.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/core.j2)  


#### Workflow Walkthrough
* **Prior to executing the Ansible playbook, the environment must be in this initial state:**
  * Zone1-Core<1a/1b> - These devices each have a default configuration with an IP address (DHCP/Static) assigned to the management interface. This IP address should match the value of [`ansible_host`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L49) for each device in the inventory.
* The playbook will perform the following actions on every `core` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L77), using REST API unless otherwise noted:
  1. Generate a configuration based on the template file [templates/2Tier/core.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/core.j2) and values defined in the inventory
  1. Push the generated configuration to the device using the AOS-CX Ansible **SSH** module `aoscx_config`
  1. Enable 10g speed interface groups (if defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L76)) 
 using the AOS-CX Ansible **SSH** module `aoscx_config`
  1. Create [VSX Keepalive](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31) L3 Interface
  1. Create [VSX Inter-switch link](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L32-L33)
  1. Configure [VSX attributes](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L44-L46) on the switch and specify device role as outlined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L49)
  1. Create all VLANs defined as `server_vlans` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L25)
  1. Create SVIs for all VLANs defined as `core_vlan_interfaces` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L105-L109)
  1. Configure the multi-chassis LAGs that connect to each access switch and trunk the VLANs in [`trunk_vlans`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L90).
     * **Note:** `vsx_pair_mclags` is a list of VSX Pair (rack# grouping) information for the core devices to use for configuring downlink interfaces. You should modify these values appropriately to match your environment.
  
  1. Configure BGP neighbor for iBGP peering between the core switches    

* For example final configurations for this workflow, see [configs/sample_configs/arch1](https://github.com/aruba/aoscx-ansible-dcn-workflows/configs/sample_configs/arch1)
  
**Because of path requirements, you must run this workflow from the root level of the cloned repository:**  
`ansible-playbook deploy_campus_attached_dc_tor.yml -i inventory_2tier_dedicated_dc.yml`
  
    
### Architecture II - Dedicated Data Center Two-Tier
This workflow provisions a VSX pair of switches acting as a centralized collapsed Data Center core 
 and campus attached access AOS-CX switches in VSX pairs based on the [validated reference design](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-a-2-Tier-DC-Network-with-NetEdit/ta-p/556403). 

#### Workflow Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- Ensure the provided Ansible inventory file [inventory_2tier_dedicated_dc.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml)
 has been modified to suit your environment, according to the instructions in [Inventory Setup](https://github.com/aruba/aoscx-ansible-dcn-workflows#inventory-setup) above.
- DC Core switches = 2 AOS-CX switches (8xxx series, use latest firmware available)
  - DC Core switches should be in a VSX pair
- Access switches = 4 or more AOS-CX switches (8xxx series, use latest firmware available)
  - Access switches should be in VSX pairs
- Out-of-Band management (OOBM) connection to management port on AOS-CX switches
  - Ansible control machine should be reachable via from each device's OOBM

 
#### Files Used
* Playbook : [deploy_2tier_dedicated_datacenter.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/deploy_2tier_dedicated_datacenter.yml)  
* Inventory : [inventory_2tier_dedicated_dc.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml)  
* Jinja2 Templates :
  * [templates/2Tier/access.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/access.j2)  
  * [templates/2Tier/core.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/core.j2)


#### Workflow Walkthrough
* **Before the Ansible playbook will be executed, the environment is in this initial state:**
  * Zone1-Core<1a/1b> + Zone1-Rack<1/3>-Access<1/2/3/4> - These devices each have a default configuration with an IP address (DHCP/Static) assigned to the management interface. This IP address should match the value of [`ansible_host`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L49) for each device in the inventory.  
  * Zone1-Rack1-Access<1/2> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31-L33)
  * Zone1-Rack3-Access<3/4> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31-L33) 
  * Zone1-Core<1a/1b> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31-L33)
* The playbook will perform the following actions on **every** device in the inventory file [inventory_2tier_dedicated_dc.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml) 
using **SSH**:
  1. Generate a configuration based on the template file [templates/2Tier/core.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/core.j2) or [templates/2Tier/access.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/2Tier/access.j2) and values defined in the inventory
  1. Push the generated configuration to the device using the AOS-CX Ansible SSH module `aoscx_config`
  1. Enable 10g speed interface groups (if defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L76)) 
 using the AOS-CX Ansible SSH module `aoscx_config`
* The playbook will perform the following actions on every `core` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml) 
using **REST API**:
  1. Create [VSX Keepalive](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31) L3 Interface
  1. Create [VSX Inter-switch link](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L32-L33)
  1. Configure [VSX attributes](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L44-L46) on the switch and specify device role as outlined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L51)
  1. Create all VLANs defined as `server_vlans` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L25)
  1. Create SVIs for all VLANs defined as `core_vlan_interfaces` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L105-L109)
  1. Configure the multi-chassis LAGs that connect to each access switch and trunk the VLANs in [`trunk_vlans`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L90).
     * **Note:** `vsx_pair_mclags` is a list of VSX Pair (rack# grouping) information for the core devices to use for configuring downlink interfaces. You should modify these values appropriately to match your environment.
    
  1. Configure BGP neighbor for iBGP peering between the core switches  
  
* The playbook will perform the following actions on every `access` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml) 
using **REST API**:
  1. Create [VSX Keepalive](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L31) L3 Interface
  1. Create [VSX Inter-switch link](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L32-L33)
  1. Configure [VSX attributes](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L44-L46) on the switch and specify device role as outlined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L49)
  1. Create all VLANs defined as `server_vlans` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_2tier_dedicated_dc.yml#L25)
  1. Configure the multi-chassis LAG that connects to each core switch and trunk the `server_vlans` 
* For example final configurations for this workflow, see [configs/sample_configs/arch2](https://github.com/aruba/aoscx-ansible-dcn-workflows/configs/sample_configs/arch2)
  
**Because of path requirements, you must run this workflow from the root level of the cloned repository:** 
`ansible-playbook deploy_2tier_dedicated_datacenter.yml -i inventory_2tier_dedicated_dc.yml`
  

### Architecture III - Dedicated Data Center Layer 3 Spine/Leaf Topology - EBGP EVPN (multi-AS) VXLAN with VSX
This workflow provisions switches in a Spine/Leaf topology using eBGP EVPN for the Layer3 fabric and L2 VXLAN with VSX  
based on the [validated reference design](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-EBGP-EVPN-multi-AS-VXLAN-with-VSX-Centralized-L3/ta-p/627317). 
This workflow **does not** configure the centralized L3 gateway.  
  
  
#### Workflow Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- Ensure the provided Ansible inventory file [inventory_spine_leaf.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml)
 matches your environment, see [How to Setup Your Inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows#how-to-setup-your-inventory) above.
- Spine switches = 2 AOS-CX switches  
  - spine switches should be in a VSX pair and **must support EVPN** (8325/8400 required)
- Leaf switches = 4 or more AOS-CX switches
  - leaf switches should be in a VSX pair and **must support EVPN/VXLAN** (8325 required)
- Out-of-Band management connection to management port on AOS-CX switches
  - Ansible control machine should be reachable from device OOBM


#### Files Used
* Playbook : [deploy_ebgp_evpn_vxlan.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/deploy_ebgp_evpn_vxlan.yml)  
* Inventory : [inventory_spine_leaf.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml)  
* Jinja2 Templates :
  * [templates/eBGP/spine.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/eBGP/spine.j2)  
  * [templates/eBGP/leaf.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/eBGP/leaf.j2)

#### Workflow Walkthrough
* **Before the Ansible playbook will be executed, the environment is in this initial state:**
  * Zone1-Spine<1/2> + Zone1-Rack1-Leaf<1a/1b> + Zone1-Rack3-Leaf<3a/3b> - These devices have a default configuration with an IP address (DHCP/Static) assigned to 
the management interface, this IP address should be the value of [`ansible_host`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L57) for each device in the inventory.  
  * Zone1-Rack1-Leaf<1a/1b> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L30-L32)
  * Zone1-Rack3-Leaf<3a/3b> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L30-L32) 
* The playbook will perform the following actions on **every** device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml) 
using **SSH**:
  1. Generate a configuration based on the template file [templates/eBGP/spine.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/eBGP/spine.j2) or [templates/eBGP/leaf.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/eBGP/leaf.j2)  
 and values defined in the inventory
  1. Push the generated configuration to the device using the AOS-CX SSH Ansible module `aoscx_config`
  1. Enable 10g speed interface groups (if defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L114) 
 using the AOS-CX SSH Ansible module `aoscx_config`
* The playbook will perform the following actions on every `spine` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L115) 
using **REST API**:
  1. Configure BGP neighbors and EVPN address families for [every leaf's loopback IP address](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L120-L124) on every leaf's BGP ASN  
* The playbook will perform the following actions on every `leaf` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L34) 
using **REST API**:
  1. 
  s and EVPN address families for [every spine's loopback IP address](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L25-L27)
  1. Create all VLANs defined as `server_vlans` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L28) 
  1. Create all EVPN instance and map VLANs defined in `server_vlans`
* For example final configurations for this workflow see [configs/sample_configs/arch3_eBGP](https://github.com/aruba/aoscx-ansible-dcn-workflows/configs/sample_configs/arch3_eBGP)
  
**To run this workflow, you must be at the root level of the cloned repository:**  
`ansible-playbook deploy_ebgp_evpn_vxlan.yml -i inventory_spine_leaf.yml`
  
  
### Architecture III - Dedicated Data Center Layer 3 Spine/Leaf Topology - IBGP EVPN VXLAN with VSX
This workflow provisions switches in a Spine/Leaf topology using OSPF EVPN for the Layer3 fabric and L2 VXLAN with VSX  
based on the [validated reference design](https://community.arubanetworks.com/t5/Data-Center-Networking-Solutions/Deploying-IBGP-EVPN-VXLAN-VSX-Centralized-L3-Gateway-with/ta-p/626010).  
  This workflow **does not** configure the centralized L3 gateway.
  
#### Workflow Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- Ensure the provided Ansible inventory file [inventory_spine_leaf.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml)
 matches your environment, see [How to Setup Your Inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows#how-to-setup-your-inventory) above.
- Spine switches = 2 AOS-CX switches 
  - spine switches should be in a VSX pair and **must support EVPN** (8325/8400 required)
- Leaf switches = 4 or more AOS-CX switches
  - leaf switches should be in VSX pairs and **must support EVPN/VXLAN** (8325 required)
- Out-of-Band management connection to management port on AOS-CX switches
  - Ansible control machine should be reachable from device OOBM  

#### Files Used
* Playbook : [deploy_ibgp_evpn_vxlan.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/deploy_ibgp_evpn_vxlan.yml)  
* Inventory : [inventory_spine_leaf.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml)  
* Jinja2 Templates :
  * [templates/iBGP/spine.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/iBGP/spine.j2)  
  * [templates/iBGP/leaf.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/iBGP/leaf.j2)

#### Workflow Walkthrough
* **Before the Ansible playbook will be executed, the environment is in this initial state:**
  * Zone1-Spine<1/2> + Zone1-Rack1-Leaf<1a/1b> + Zone1-Rack3-Leaf<3a/3b> - These devices have a default configuration with an IP address (DHCP/Static) assigned to 
the management interface, this IP address should be the value of [`ansible_host`](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L57) for each device in the inventory.  
  * Zone1-Rack1-Leaf<1a/1b> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L30-L32)
  * Zone1-Rack3-Leaf<3a/3b> - These devices are in a VSX pair with their physical links matching the values defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L30-L32) 
* The playbook will perform the following actions on **every** device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml) 
using **SSH**:
  1. Generate a configuration based on the template file [templates/iBGP/spine.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/iBGP/spine.j2) or [templates/iBGP/leaf.j2](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/templates/iBGP/leaf.j2)  
 and values defined in the inventory
  1. Push the generated configuration to the device using the AOS-CX SSH Ansible module `aoscx_config`
  1. Enable 10g speed interface groups (if defined in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L114) 
 using the AOS-CX SSH Ansible module `aoscx_config`
* The playbook will perform the following actions on every `spine` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L115) 
using **REST API**:
  1. Configure BGP neighbors and EVPN address families for [every leaf's loopback IP address](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L120-L124)  
* The playbook will perform the following actions on every `leaf` device in the [inventory file](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L34) 
using **REST API**:
  1. Configure BGP neighbors and EVPN address families for [every spine's loopback IP address](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L25-L27)
  1. Create all VLANs defined as `server_vlans` in the [inventory](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/inventory_spine_leaf.yml#L28) 
  1. Create all EVPN instance and map VLANs defined in `server_vlans`
* For example final configurations for this workflow see [configs/sample_configs/arch3_iBGP](https://github.com/aruba/aoscx-ansible-dcn-workflows/configs/sample_configs/arch3_iBGP)
  
**To run this workflow, you must be at the root level of the cloned repository:**  
`ansible-playbook deploy_ibgp_evpn_vxlan.yml -i inventory_spine_leaf.yml`

### Configure VSX Standalone Playbook
This playbook is a standalone workflow that configures VSX and its attributes on a AOS-CX switch.

#### Playbook Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- This playbook uses playbook variables therefore it's only necessary for the inventory file to include all the [necessary REST API connection variables](https://github.com/aruba/aoscx-ansible-role#inventory-variables) for the aoscx_role.
- Out-of-Band management connection to management port on AOS-CX switches
  - Ansible control machine should be reachable from device OOBM

 
#### Files Used
* Playbook : [configure_vsx.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_vsx.yml)  


#### Playbook Walkthrough
  1. Create [VSX Keepalive](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_vsx.yml#L7) L3 Interface
  1. Create [VSX Inter-switch link](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_vsx.yml#L11-L14) for VSX
  1. Configure [VSX attributes](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_vsx.yml#L8-L10) on the switch and specify device role as outlined in the [playbook variable](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_vsx.yml#L6)

### Configure Multi-Chassis LAG Standalone Playbook
This playbook is a standalone workflow that configures a multi-chassis LAG and its interfaces on a AOS-CX switch.

#### Playbook Prerequisites
- All prerequisites defined above in [Prerequisites](https://github.com/aruba/aoscx-ansible-dcn-workflows#prerequisites)
- This playbook uses playbook variables therefore it's only necessary for the inventory file to include all the [necessary REST API connection variables](https://github.com/aruba/aoscx-ansible-role#inventory-variables) for the aoscx_role.
- Out-of-Band management connection to management port on AOS-CX switches
  - Ansible control machine should be reachable from device OOBM

 
#### Files Used
* Playbook : [configure_mclag.yml](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_mclag.yml)  


#### Playbook Walkthrough
  1. Create all VLANs defined as `mclag_vlans` in the [playbook](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_mclag.yml#L7-L9)
  1. Configure the multi-chassis LAG and it's [interfaces](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/configure_mclag.yml#L10-L12) and trunk the `mclag_vlans` 
  
## Project Structure
```bash
├───configs                                 # Directory for generated configurations
│   ├───sample_configs                          # Sample Final Configurations for all workflows
├───files                                   # Place for any additional files that are used in tasks
│   ├───images                              # Images for README.md
├───filter_plugins                          # Ansible default directory for custom filter plugins
├───tasks                                   # Ansible tasks
│   ├───aoscx                                   # URI Tasks for AOS-CX
├───templates                               # Place to hold Jinja templates for config generation
├───CONTRIBUTING.md                         # Document outlining contributing requirements
├───LICENSE                                 # Project license
├───README.md                               # Document outlining project requirements
├───ansible.cfg                             # Ansible configuration file
├───configure_mclag.yml                     # Standalone playbook for MCLAG configuration
├───configure_vsx.yml                       # Standalone playbook for VSX configuration        
├───deploy_2tier_dedicated_datacenter.yml   # Playbook for Architecture II   
├───deploy_campus_attached_dc_tor.yml       # Playbook for Architecture I 
├───deploy_ebgp_evpn_vxlan.yml              # Playbook for Architecture III - eBGP and EVPN with VXLAN
├───deploy_ibgp_evpn_vxlan.yml              # Playbook for Architecture III - OSPF and EVPN with VXLAN
├───inventory_2tier_dedicated_dc.yml        # Inventory file for Architecture I and Architecture II
├───inventory_2tier_dedicated_dc.yml        # Inventory file for Architecture III workflows
├───requirements.txt                        # Python library requirements for project
├───requirements.yml                        # Galaxy role requirements for project
```  
  
## How To Contribute
Please follow our guidelines outlined in our [CONTRIBUTING.md](https://github.com/aruba/aoscx-ansible-dcn-workflows/blob/master/CONTRIBUTING.md)
