# 从文件中读取节点之间的连接关系和权重
def read_graph_from_file(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        for line in file:
            node1, node2, weight = line.strip().split(',')
            if node1 not in graph:
                graph[node1] = {}
            if node2 not in graph:
                graph[node2] = {}
            graph[node1][node2] = float(weight)
            graph[node2][node1] = float(weight)
    return graph

# 使用 Dijkstra 算法计算最短路径
def dijkstra(graph, source, target):
    shortest_paths = {node: (float('inf'), None) for node in graph}
    shortest_paths[source] = (0, None)
    visited = set()

    while visited != set(graph):
        current_node = min((node for node in graph if node not in visited), key=lambda node: shortest_paths[node][0])
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            path_length = shortest_paths[current_node][0] + weight
            if path_length < shortest_paths[neighbor][0]:
                shortest_paths[neighbor] = (path_length, current_node)

    path = []
    current_node = target
    while current_node is not None:
        path.insert(0, current_node)
        current_node = shortest_paths[current_node][1]

    return path

# 读取图形数据
graph_file = r'C:\Users\弘鬼\satellite_edges.txt'  # 使用原始字符串表示文件路径
graph = read_graph_from_file(graph_file)

# 输入要计算最短路径的两个节点名称
source_index = int(input("请输入起始节点数字: "))
target_index = int(input("请输入目标节点数字: "))

source_node = [node for node in graph if str(source_index) in node][0]
target_node = [node for node in graph if str(target_index) in node][0]

if source_node in graph and target_node in graph:
    # 计算最短路径
    shortest_path = dijkstra(graph, source_node, target_node)

    # 将最短路径写入文件
    output_file = r'shortest_path.txt'  # 使用原始字符串表示文件路径
    with open(output_file, 'w') as file:
        for node in shortest_path:
            file.write(node + '\n')

    print(f"最短路径已经计算并保存到 {output_file} 文件中。")
else:
    print("输入的节点名称无效，请重新输入。")
