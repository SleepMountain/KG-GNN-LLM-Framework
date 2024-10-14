import sys
sys.path.append('..')
from neo4j import GraphDatabase
from env_loader import GetEnv

uri = GetEnv("neo4j_uri")
username = GetEnv("neo4j_user")
password = GetEnv("neo4j_password")

driver = GraphDatabase.driver(uri, auth=(username, password))

def action(tx, query):
    return tx.run(query)
def excute(query):
    with driver.session() as session:
        return session.write_transaction(action, query)
