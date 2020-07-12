import argparse
import subprocess
import os
import sys
import json
from multiprocessing.pool import Pool
import multiprocessing

def get_iplist(iplist):
    if '-' in iplist:
        iplist = iplist.split('-')
        new_iplist = [f'{iplist[0][:-1]}{i}' for i in range(int(iplist[0][-1]), int(iplist[1][-1])+1)]
        # print(new_iplist)
        return new_iplist
    else:
        new_ip = iplist
        return new_ip


def func_ping(ip):
    print(f"ping -c 3 {ip}")
    commond = f"ping -c 3 {ip}"
    subt = subprocess.Popen(commond, shell=True,
                            stdout=subprocess.PIPE, encoding='utf-8')
    flag = 1
    for line in iter(subt.stdout.readline, ''):
        print(line)
        if 'timeout' in line:
            print(f'{ip} 不可用')
            flag = 0
            break
    if flag == 0:
        pass
    else:
        print(f'{ip} 可用')
        ip_used = ip
        return ip_used

    subt.stdout.close()
    subt.wait()

def func_tcp(ip, port):
    
    port_list = []
    # for port in range(min_port, max_port+1):
    print(f'开始扫描端口：{port}')
    print(f"nc -vz -w 2 {ip} {port}")
    commond = f"nc -vz -w 2 {ip} {port}"
    subt = subprocess.Popen(commond, shell=True,
                            stdout=subprocess.PIPE, encoding='utf-8')
    line = subt.stdout.readlines()
    print(line)
    if 'successed' in line:
        print(f'端口：{port} 可用')
        port_list.append(port)
        # break
    subt.stdout.close()
    subt.wait()
    return port_list
    




if __name__ == "__main__":
    # pass
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', dest='Num', type=int, help='target Num')
    parser.add_argument('-f', '--func', dest='Func', type=str, choices=['ping', 'tcp'], help='target Func')
    parser.add_argument('-ip', '--iplist', dest='Ip', type=str, help='target Ip')
    parser.add_argument('-w', '--write', dest='Write', type=str, help='target FileName')

    cmd_info = parser.parse_args()
    iplist = get_iplist(cmd_info.Ip)
    print(iplist)
    p = Pool(cmd_info.Num)
    if cmd_info.Func == 'ping':
        # iplist_used = []
        # for ip in iplist:
        #     ip_used = func_ping(ip)
        #     iplist_used.append(ip_used)

        # with open('./iplist.txt','a+') as f:
        
        for ip in iplist:
            p.apply_async(func_ping, args=(ip,))
        #             ip_used = func_ping(ip)
        #             if ip_used:
        #                 iplist_used.append(ip_used)
        #                 f.write(ip_used + '\n')
        p.close()
        p.join()
        # print("父进程结束。")
        p.terminate()
    else:
        min_port = 1
        max_port = 1024
        
        print(f'扫描端口的范围为{min_port}--{max_port}')
        for port in range(min_port, max_port+1):
            # port_list = func_tcp(iplist)
            p.apply_async(func_tcp, args=(iplist, port))
        p.close()
        p.join()
        # print("父进程结束。")
        p.terminate()
            # print(f"{iplist} 可用的端口列表为 {port_list}")
            # port_dict = {"{iplist}":port_list}
            # 暂时先不做保存到json
            # if cmd_info.Write:
            #     with open("../config/record.json","w") as f:
            #     json.dump(new_dict,f)
            #     print("加载入文件完成...")