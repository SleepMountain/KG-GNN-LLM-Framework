import pandas as pd
from py2neo import Graph, Node

# 读取 CSV 文件
df = pd.read_csv("./课程-知识点-相关课程.csv")

# 提取所有课程、知识点和相关课程
courses = set()
topics = set()
related_courses = set()

for index, row in df.iterrows():
    courses.add(row['课程'])
    # 检查知识点是否为字符串再进行处理
    if isinstance(row['知识点'], str):
        topics.update(row['知识点'].split(','))
    # 检查相关课程是否为字符串再进行处理
    if isinstance(row['相关课程'], str):
        related_courses.update(row['相关课程'].split(','))

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

# 创建课程、知识点和相关课程节点
try:
    for course in courses:
        node_course = Node('Course', name=course)
        g.create(node_course)
        print(f"创建课程节点: {course}")

    for topic in topics:
        node_topic = Node('Topic', name=topic)
        g.create(node_topic)
        print(f"创建知识点节点: {topic}")

    for related_course in related_courses:
        node_related_course = Node('Course', name=related_course)
        g.create(node_related_course)
        print(f"创建相关课程节点: {related_course}")
except Exception as e:
    print(f"创建节点失败: {e}")
    exit()

# 创建课程和知识点之间的关系
try:
    for index, row in df.iterrows():
        course_name = row['课程']
        if isinstance(row['知识点'], str):
            topics_list = row['知识点'].split(',')

            for topic in topics_list:
                query = f"MATCH (c:Course {{name:'{course_name}'}}), (t:Topic {{name:'{topic}'}}) CREATE (c)-[:HAS_TOPIC]->(t)"
                g.run(query)
                print(f"创建关系: {course_name}-[:HAS_TOPIC]->{topic}")

except Exception as e:
    print(f"创建关系失败: {e}")
    exit()

# 创建课程和相关课程之间的关系
try:
    for index, row in df.iterrows():
        course_name = row['课程']
        if isinstance(row['相关课程'], str):
            related_courses_list = row['相关课程'].split(',')

            for related_course in related_courses_list:
                query = f"MATCH (c1:Course {{name:'{course_name}'}}), (c2:Course {{name:'{related_course}'}}) CREATE (c1)-[:RELATED_TO]->(c2)"
                g.run(query)
                print(f"创建关系: {course_name}-[:RELATED_TO]->{related_course}")

except Exception as e:
    print(f"创建关系失败: {e}")
    exit()

print("数据导入完成")
