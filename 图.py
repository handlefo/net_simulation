import os
import json5

# 读取 JSON5 文件
def read_json5_file(file_path):
    with open(file_path, 'r') as file:
        data = json5.load(file)
    return data

# 提取卫星节点名称和权重信息
def extract_data_from_json(data):
    satellite_nodes = []
    for key, value in data.items():
        if key.startswith('satellite'):
            satellite_nodes.append(value)
    delay_value = data.get('delayValue', 0)
    weight = 1000 if delay_value == 0 else delay_value
    return satellite_nodes, weight

# 构建图结构数据
def build_graph(json5_files):
    edges = []
    for file_path in json5_files:
        data = read_json5_file(file_path)
        satellite_nodes, weight = extract_data_from_json(data)
        for i in range(len(satellite_nodes) - 1):
            edge = f"{satellite_nodes[i]},{satellite_nodes[i+1]},{weight}"
            edges.append(edge)
    return edges

# 获取文件夹中的 JSON5 文件路径
def get_json5_files(folder_path):
    json5_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.json5'):
            json5_files.append(os.path.join(folder_path, file))
    return json5_files

# 读取包含多个 JSON5 文件路径的文件夹并构建图结构
folder_path = r'D:\test\info'  # 使用原始字符串表示文件夹路径
json5_files = get_json5_files(folder_path)
edges = build_graph(json5_files)

# 将图结构保存为文本文件
output_file = "satellite_edges.txt"
with open(output_file, 'w') as file:
    for edge in edges:
        file.write(edge + '\n')

print("节点之间的连接关系和权重已经保存到 satellite_edges.txt 文件中。")