# -*- coding:utf-8 -*-
# @author: xrx
# @time: 2024/3/9 18:30
# @project: spiderslab
# @file: main.py
# @software: PyCharm
# desc: python3.6.10
import geopandas as gpd
import networkx  as nx
from shapely.wkt import loads as wkt_loads
from shapely.geometry import Point
import matplotlib.pyplot as plt
from fractions import gcd
# 加载道路网络数据
g = nx.read_shp("./edges.shp")

print(g[(116.453808, 39.9012627)][(116.4532719, 39.9012698)])
# 定义起点和终点坐标
start_point = Point(116.3000, 39.8600)
end_point = Point(116.4500, 39.9000)

# 找到最近的起点节点
start_nearest_node = None
start_nearest_distance = float('inf')
for edge in g.edges(data=True):
    line = wkt_loads(edge[2]['Wkt'])  # 使用 Shapely 的 wkt_loads 函数解析 WKT 字符串
    nearest_point = line.interpolate(line.project(start_point))
    distance = nearest_point.distance(start_point)
    if distance < start_nearest_distance:
        start_nearest_distance = distance
        start_nearest_node = list(line.coords)[0]

# 找到最近的终点节点
end_nearest_node = None
end_nearest_distance = float('inf')
for edge in g.edges(data=True):
    line = wkt_loads(edge[2]['Wkt'])  # 使用 Shapely 的 wkt_loads 函数解析 WKT 字符串
    nearest_point = line.interpolate(line.project(end_point))
    distance = nearest_point.distance(end_point)
    if distance < end_nearest_distance:
        end_nearest_distance = distance
        end_nearest_node = list(line.coords)[-1]

# 使用
shortest_path = nx.shortest_path(g, source=start_nearest_node, target=end_nearest_node, weight='length')
# 计算最短路径长度
shortest_path_length = nx.shortest_path_length(g, source=start_nearest_node, target=end_nearest_node, weight='length')
print("最短路径长度:", shortest_path_length)

# 可视化路径
fig, ax = plt.subplots()
edges = gpd.read_file("./edges.shp")
edges.plot(ax=ax, color='gray', linewidth=0.5)

# 获取数据的整体边界
min_x, min_y, max_x, max_y = edges.total_bounds

# 标记起点和终点
plt.scatter(start_point.x, start_point.y, color='green', label='Start')
plt.scatter(end_point.x, end_point.y, color='blue', label='End')

# 绘制路径
path_geom = []
for u, v in zip(shortest_path[:-1], shortest_path[1:]):
    print(u, v)
    print(g[u][v])
    line = wkt_loads(g[u][v]['Wkt'])
    print(line.length)
    path_geom.append(line)
    ax.plot(*line.xy, color='red', linewidth=2)

plt.legend()
plt.show()
