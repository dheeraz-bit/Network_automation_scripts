import getpass
import netmiko
import socket
import threading
import time
devices = ["192.168.20.36", "192.168.20.37","192.168.20.38", "192.168.20.39"]
loopback_ips =["10.10.10.10" , "20.20.20.20", "30.30.30.30", "40.40.40.40"]

user = input("Enter your username: " )
password = getpass.getpass("Enter your password: " )
enable_pass = getpass.getpass("Enter your enable seceret: ")

        
def main(devices, loopback_ips, user,password, enable_pass):
      connect = {"device_type":"cisco_ios",
                "ip":ip,
                "username":user,
                "password":password,
                "secret":enable_pass}
      try :
            net_connect = netmiko.ConnectHandler(**connect)
            print(f"Sucessfully connnected to {ip}")
            net_connect.enable()
            output=net_connect.send_command("sh ip int br")
            print(output)
            print()
            config = ["int loop 0", f"ip add {loopback_ip} 255.255.255.0", "no shut","exit"]
            net_connect.send_config_set(config)

            output=net_connect.send_command("sh ip int br")
            print(output)
            print()
      except netmiko.NetMikoAuthenticationException:
            print(f"Invalid login credentials for {ip}")
      except netmiko.NetMikoTimeoutException:
            print(f"{ip} Connection left idle and has timedout")

      except Exception as e:
            print("Unexpected error occured.")
            print(e)
            exit() 

    
if __name__=="__main__":
      threds = []
      start = time.time()
      for ip, loopback_ip in zip(devices,loopback_ips):
            try:
                  socket.create_connection((ip, 22,),5)
                  th = threading.Thread(target=main, args=(devices, loopback_ips, user,password, enable_pass))
                  threds.append(th)
                  th.start()
                  print(len(threds))
            except OSError:
                  print("Couldn't reach "+ip)
                  continue
      for th in threds:
            th.join()
      end = time.time()
      print(round((end-start),2))
