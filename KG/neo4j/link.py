from neo4j import GraphDatabase
import sys
sys.path.append('..')
from env_loader import GetEnv

uri = GetEnv("neo4j_uri")
username = GetEnv("neo4j_user")
password = GetEnv("neo4j_password")

# 创建连接
driver = GraphDatabase.driver(uri, auth=(username, password))
