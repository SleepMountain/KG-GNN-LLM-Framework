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

"""创建节点"""
def create_person(tx, name):
    tx.run("CREATE (:Person {name: $name})", name=name)

# 使用事务创建节点
with driver.session() as session:
    session.execute_write(create_person, "Alice")
    session.execute_write(create_person, "Bob")

"""创建关系"""
def create_knows_relationship(tx, person1, person2):
    tx.run("MATCH (a:Person {name: $person1}) "
           "MATCH (b:Person {name: $person2}) "
           "CREATE (a)-[:KNOWS]->(b)", person1=person1, person2=person2)

# 使用事务创建关系
with driver.session() as session:
    session.execute_write(create_knows_relationship, "Alice", "Bob")

"""查询所有节点"""
def get_all_nodes(tx):
    result = tx.run("MATCH (n) RETURN n")
    return result.data()

# 使用事务查询所有节点
with driver.session() as session:
    nodes = session.execute_read(get_all_nodes)
    print(nodes)

"""查询特定关系"""
def get_knows_relationships(tx):
    result = tx.run("MATCH (:Person)-[r:KNOWS]->(:Person) RETURN r")
    return result.data()

# 使用事务查询所有“KNOWS”关系
with driver.session() as session:
    relationships = session.execute_read(get_knows_relationships)
    print(relationships)

"""清理资源"""
driver.close()

