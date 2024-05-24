import subprocess

# 使用ip addr show命令获取所有IP地址
p = subprocess.Popen(['ip', 'addr', 'show'],stdout=subprocess.PIPE)
output,_ = p.communicate()
ip_output = output.decode('utf-8')

# 提取IP地址
ip_addresses = []
for line in ip_output.split('\n'):
    if 'inet ' in line:
        parts = line.split()
        ip_address = parts[1].split('/')[0]
        if ip_address != '127.0.0.1':  # 排除本地回环地址
            ip_addresses.append(ip_address)

print("所有IP地址：", ip_addresses)

# 读取路由路径文件
route_path = []
with open('/home/ustc/shortest_path.txt', 'r') as f:
    for line in f:
        node = line.strip()
        route_path.append(node)

# 读取节点名与IP地址耦合文件
node_ip_mapping = {}
with open('/home/ustc/node_ip_mapping.txt', 'r') as f:
    for line in f:
        node, ip = line.strip().split(': ')
        node_ip_mapping[node] = ip

last_node = route_path[-1]
last_node_ip=node_ip_mapping[last_node]

# 遍历每个IP地址，找到下一跳节点
for ip_address in ip_addresses:
    for i in range(len(route_path)):
        node = route_path[i]
        if node in node_ip_mapping:
            node_ip = node_ip_mapping[node]
            if node_ip == ip_address:
                if i+1 < len(route_path):
                    next_hop_node = route_path[i+1]
                    next_hop_ip = node_ip_mapping.get(next_hop_node)
                    if next_hop_ip:
                        print(f"IP地址 {ip_address} 的下一跳节点是 {next_hop_node}，IP地址为 {next_hop_ip}，配置静态路由...")
                        
                        # 配置静态路由
                        if last_node_ip == next_hop_ip:
                            print(f'no need to do')
                        else:
                            command = f"sudo ip route add {last_node_ip} via {next_hop_ip}"
                            subprocess.run(command, shell=True)
                        
                            print(f"静态路由配置完成，将IP地址 {ip_address} 的路由指向下一跳节点 {next_hop_node} 的IP地址 {next_hop_ip}。")
                    else:
                        print(f"找不到下一跳节点 {next_hop_node} 的IP地址，请检查节点名与IP地址的映射文件。")
                else:
                    print(f"IP地址 {ip_address} 已经是路由路径的最后一个节点，无需配置静态路由。")
