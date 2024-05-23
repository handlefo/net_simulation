def generate_node_ip_mapping():
    node_ip_mapping = {}
    for i in range(1, 10):
        ip_address = input(f"请输入 satellite{i} 的 IP 地址: ")
        node_ip_mapping[f"satellite{i}"] = ip_address
    return node_ip_mapping

def save_node_ip_mapping_to_file(node_ip_mapping, output_file):
    with open(output_file, 'w') as file:
        for node, ip in node_ip_mapping.items():
            file.write(f"{node}:{ip}\n")

# 生成节点名称与对应的 IP 地址映射
node_ip_mapping = generate_node_ip_mapping()

# 将节点名称与对应的 IP 地址保存到新文件
output_file = "node_ip_mapping.txt"
save_node_ip_mapping_to_file(node_ip_mapping, output_file)

print(f"节点名称与对应的 IP 地址已保存到 {output_file} 文件中。")