"""neo4j链接"""
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"   # Neo4j数据库的URI
username = "neo4j"              # 数据库用户名
password = "czxczx3224039710"   # 数据库密码

# 创建连接
driver = GraphDatabase.driver(uri, auth=(username, password))

"""neo4j删除"""
def delete_person_and_relationships(tx, name):
    # 删除具有给定名字的所有节点及其关系
    tx.run("MATCH (n:Person {name: $name}) DETACH DELETE n", name=name)

# 使用事务删除节点及其关系
with driver.session() as session:
    session.execute_write(delete_person_and_relationships, "Alice")
    session.execute_write(delete_person_and_relationships, "Bob")
    print("remove successfully")