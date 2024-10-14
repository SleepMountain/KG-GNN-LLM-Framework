"""neo4j链接"""
from neo4j import GraphDatabase
import sys
sys.path.append('..')
from env_loader import GetEnv

uri = GetEnv("neo4j_uri")
username = GetEnv("neo4j_user")
password = GetEnv("neo4j_password")

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