import ssh_script
from netmiko import ConnectHandler
device_ip = ssh_script.devices


def main():
    for ip in device_ip:
        connect = {"device_type":"cisco_ios",
           "ip":ip,
           "username":ssh_script.user,
           "password":ssh_script.password,
           "secret":ssh_script.enable_pass
           }
        net_connect = ConnectHandler(**connect)
        print(f"Connected to {ip}")
        net_connect.enable()
        net_connect.send_config_set(["router ospf 1", "net 0.0.0.0 255.255.255.255 area 0","exit","shell processing full", "end", "wr"])
        output = net_connect.send_command("sh ip protocols | grep ospf")
        print(output)
if __name__=="__main__":
    main()