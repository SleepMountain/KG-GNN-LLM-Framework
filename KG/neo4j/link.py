from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Neo4j数据库的URI
username = "neo4j"              # 数据库用户名
password = "czxczx3224039710"           # 数据库密码

# 创建连接
driver = GraphDatabase.driver(uri, auth=(username, password))
