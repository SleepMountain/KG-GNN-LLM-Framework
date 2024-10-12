from py2neo import Graph, Node

# 连接 Neo4j 数据库
try:
    g = Graph("url", auth=("neo4j", "czxczx3224039710"))
    print("成功连接到 Neo4j 数据库")
except Exception as e:
    print(f"连接到 Neo4j 数据库失败: {e}")
    exit()

# 清空数据库中已有的节点和关系（可选）
try:
    g.delete_all()
    print("已清空数据库中所有节点和关系")
except Exception as e:
    print(f"清空数据库失败: {e}")
    exit()