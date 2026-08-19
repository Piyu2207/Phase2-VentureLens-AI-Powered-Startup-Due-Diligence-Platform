from neo4j import GraphDatabase

from backend.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

class Neo4jStore:

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def verify(self):
        self.driver.verify_connectivity()

    def clear(self):
        with self.driver.session(database=NEO4J_DATABASE) as s:
            s.run("MATCH (n) DETACH DELETE n")

    def insert_startups(self, startups):
        query = """
        MERGE (s:Startup {id:$id})
        SET s.name=$name, s.sector=$sector
        WITH s
        UNWIND $founders AS x
        MERGE (f:Founder {name:x}) MERGE (f)-[:FOUNDED]->(s)
        WITH s
        UNWIND $investors AS x
        MERGE (i:Investor {name:x}) MERGE (i)-[:INVESTED_IN]->(s)
        WITH s
        UNWIND $competitors AS x
        MERGE (c:Startup {name:x}) MERGE (s)-[:COMPETES_WITH]->(c)
        WITH s
        UNWIND $partners AS x
        MERGE (p:Organization {name:x}) MERGE (s)-[:PARTNERED_WITH]->(p)
        """
        with self.driver.session(database=NEO4J_DATABASE) as s:
            for x in startups:
                s.run(query, id=x["id"], name=x["name"], sector=x["sector"],
                      founders=x["founders"], investors=x["investors"],
                      competitors=x["competitors"], partners=x["partners"]).consume()

    def count_nodes_edges(self):
        with self.driver.session(database=NEO4J_DATABASE) as s:
            n = s.run("MATCH (x) RETURN count(x) AS c").single()["c"]
            e = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
            return n, e

    def query_graph(self, name):
        q = """
        MATCH (s:Startup) WHERE toLower(s.name)=toLower($name)
        OPTIONAL MATCH (s)-[r]-(other)
        RETURN s.name AS startup, type(r) AS relationship,
               labels(other) AS other_labels, coalesce(other.name,other.id) AS connected_entity
        ORDER BY relationship, connected_entity
        """
        with self.driver.session(database=NEO4J_DATABASE) as s:
            return [dict(x) for x in s.run(q, name=name)]
