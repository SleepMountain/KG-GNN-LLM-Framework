import pandas as pd
from py2neo import Graph, Node

# 读取 CSV 文件
df = pd.read_csv("./学生-选课（测试集）.csv")

# 提取所有课程、知识点和相关课程
student = set()
selected = set()

for index, row in df.iterrows():
    student.add(row['学生id'])
    # 检查知识点是否为字符串再进行处理
    if isinstance(row['大一至大二课程'], str):
        selected.update(row['大一至大二课程'].split(','))

# 连接 Neo4j 数据库
try:
    g = Graph("url", auth=("neo4j", "czxczx3224039710"))
    print("成功连接到 Neo4j 数据库")
except Exception as e:
    print(f"连接到 Neo4j 数据库失败: {e}")
    exit()

# 清空数据库中已有的节点和关系（可选）
# try:
#     g.delete_all()
#     print("已清空数据库中所有节点和关系")
# except Exception as e:
#     print(f"清空数据库失败: {e}")
#     exit()

# 创建课程、知识点和相关课程节点
try:
    for s in student:
        node_course = Node('Student', name=s)
        g.create(node_course)
        print(f"创建学生id节点: {s}")

    for topic in selected:
        node_topic = Node('Class', name=topic)
        g.create(node_topic)
        print(f"创建课程节点: {topic}")

except Exception as e:
    print(f"创建节点失败: {e}")
    exit()

try:
    for index, row in df.iterrows():
        student_id = row['学生id']
        if isinstance(row['大一至大二课程'], str):
            topics_list = row['大一至大二课程'].split(',')

            for topic in topics_list:
                query = f"MATCH (c:Student {{name:'{student_id}'}}), (t:Class {{name:'{topic}'}}) CREATE (c)-[:HAS_SELECTED]->(t)"
                g.run(query)
                print(f"创建关系: {student_id}-[:HAS_SELECTED]->{topic}")

except Exception as e:
    print(f"创建关系失败: {e}")
    exit()

print("数据导入完成")
