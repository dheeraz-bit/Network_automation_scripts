import telnetlib3
from getpass4 import getpass
import asyncio
import datetime

ip_list = ["192.168.20.33", "192.168.20.34","192.168.20.35"]

async def copy_config(ip, user, password, enable_pass):
    try:
        reader, writer = await telnetlib3.open_connection(ip,port=23)
        #logging in with the credentials 
        await reader.readuntil(b'Username:')
        print(f'Connection sucessfull to {ip}')
        await asyncio.sleep(0.5)
        writer.write(user+'\r\n')
        await reader.readuntil(b"Password:")
        writer.write(password+'\r\n')
        await asyncio.sleep(0.5)

        writer.write('en\r\n')
        await reader.readuntil(b'Password:')
        await asyncio.sleep(0.5)
        writer.write(enable_pass+'\r\n')

        #copy config 
        writer.write('terminal length 0\r\n')
        await asyncio.sleep(0.5)
        writer.write('sh run\r\n')
        await asyncio.sleep(1)

        output =""
        while True:
            try:
                chunk = await asyncio.wait_for(reader.read(512), timeout=1.5)
                if not chunk:
                    break
                output += chunk
            except asyncio.TimeoutError:
                break
        actual_ouptput = output
        file_name = f'cml_config{ip.replace('.','_')}.txt'
        with open(file_name, "w") as f:
            f.write(actual_ouptput+'\n'+ datetime.datetime.now().strftime('%d/%m%Y, %H:%M:%S'))
        print(f'Saved config from {ip} to {file_name}')
        writer.write('exit\r\n')
        writer.close()

    except TimeoutError:
        print('Connection timed out')
    except ConnectionError:
        print('Check internet connection.')
    except ConnectionRefusedError:
        print('Connection refused by remote nodes.')    
    except Exception as e:
        print(f'Unexpected error: {e}')  


if __name__ == "__main__":
    user = input('Enter your username: ')
    password = getpass('Enter your telnet password: ')
    enable_pass = getpass("Enter your enable password: ")
    async def run_all():
        async with asyncio.TaskGroup() as tg:
            for ip in ip_list:
                task=tg.create_task(copy_config (ip, user, password, enable_pass))
    asyncio.run(run_all())        