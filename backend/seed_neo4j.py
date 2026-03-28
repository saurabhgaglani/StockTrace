#!/usr/bin/env python3
"""Neo4j Graph Seeding Script for StockTrace"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jSeeder:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def create_constraints(self):
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Company) REQUIRE n.ticker IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Country) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Supplier) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Material) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Region) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Commodity) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Organization) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Political) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Policy) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Market) REQUIRE n.name IS UNIQUE",
        ]
        with self.driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
            for c in constraints:
                session.run(c)
        print("✓ Constraints created")

    def clear_database(self):
        with self.driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("✓ Database cleared")

    def seed_graph(self):
        with self.driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
            # Companies
            session.run("""
                MERGE (tsla:Company {ticker: 'TSLA'}) SET tsla.name='Tesla', tsla.industry='Automotive/EV'
                MERGE (xom:Company {ticker: 'XOM'}) SET xom.name='ExxonMobil', xom.industry='Energy'
                MERGE (nvda:Company {ticker: 'NVDA'}) SET nvda.name='NVIDIA', nvda.industry='Semiconductors'
                MERGE (aapl:Company {ticker: 'AAPL'}) SET aapl.name='Apple', aapl.industry='Technology'
            """)
            print("✓ Companies created")

            # Tesla supply chain
            session.run("""
                MATCH (tsla:Company {ticker: 'TSLA'})
                MERGE (battery:Material {name: 'Battery Production'}) SET battery.type='Manufacturing'
                MERGE (lithium:Material {name: 'Lithium'}) SET lithium.type='Raw Material'
                MERGE (cobalt:Material {name: 'Cobalt'}) SET cobalt.type='Raw Material'
                MERGE (ganfeng:Supplier {name: 'Ganfeng Lithium'}) SET ganfeng.country='China'
                MERGE (glencore:Supplier {name: 'Glencore'}) SET glencore.country='Switzerland'
                MERGE (mali:Country {name: 'Mali'}) SET mali.region='West Africa', mali.stability='Low'
                MERGE (drc:Country {name: 'DRC'}) SET drc.region='Central Africa', drc.stability='Low'
                MERGE (tsla)-[:DEPENDS_ON]->(battery)
                MERGE (battery)-[:DEPENDS_ON]->(lithium)
                MERGE (battery)-[:DEPENDS_ON]->(cobalt)
                MERGE (lithium)-[:SUPPLIED_BY]->(ganfeng)
                MERGE (cobalt)-[:SUPPLIED_BY]->(glencore)
                MERGE (ganfeng)-[:MINES_IN]->(mali)
                MERGE (glencore)-[:MINES_IN]->(drc)
            """)
            print("✓ Tesla supply chain created")

            # ExxonMobil / Oil / Political chain
            session.run("""
                MATCH (xom:Company {ticker: 'XOM'})
                MERGE (crude:Commodity {name: 'Crude Oil'}) SET crude.type='Energy'
                MERGE (permian:Region {name: 'Permian Basin'}) SET permian.location='Texas'
                MERGE (gulf:Region {name: 'Gulf Coast'}) SET gulf.location='USA'
                MERGE (oil_markets:Market {name: 'Oil Markets'}) SET oil_markets.type='Global Commodity'
                MERGE (opec:Organization {name: 'OPEC'}) SET opec.type='Cartel'
                MERGE (middle_east:Region {name: 'Middle East'}) SET middle_east.stability='Medium'
                MERGE (china:Country {name: 'China'}) SET china.region='Asia', china.gdp_rank=2
                MERGE (oil_demand:Market {name: 'Oil Demand'}) SET oil_demand.type='Consumption'
                MERGE (trade_policy:Policy {name: 'Trade Policy'}) SET trade_policy.type='Tariffs'
                MERGE (trump:Political {name: 'Trump'}) SET trump.role='Policy Maker', trump.influence='High'
                MERGE (xom)-[:PRODUCES]->(crude)
                MERGE (xom)-[:OPERATES_IN]->(permian)
                MERGE (xom)-[:OPERATES_IN]->(gulf)
                MERGE (crude)-[:TRADED_IN]->(oil_markets)
                MERGE (oil_markets)-[:INFLUENCED_BY]->(opec)
                MERGE (opec)-[:OPERATES_IN]->(middle_east)
                MERGE (oil_markets)-[:DRIVEN_BY]->(oil_demand)
                MERGE (oil_demand)-[:AFFECTED_BY]->(china)
                MERGE (china)-[:SUBJECT_TO]->(trade_policy)
                MERGE (trade_policy)-[:CONTROLLED_BY]->(trump)
            """)
            print("✓ ExxonMobil/Oil/Political chain created")

            # NVIDIA supply chain
            session.run("""
                MATCH (nvda:Company {ticker: 'NVDA'})
                MERGE (gpu:Material {name: 'GPU Manufacturing'}) SET gpu.type='Production'
                MERGE (tsmc:Supplier {name: 'TSMC'}) SET tsmc.country='Taiwan'
                MERGE (ase:Supplier {name: 'ASE Technology'}) SET ase.country='Taiwan'
                MERGE (taiwan:Country {name: 'Taiwan'}) SET taiwan.region='Asia', taiwan.stability='Medium'
                MERGE (packaging:Material {name: 'Advanced Packaging'}) SET packaging.type='Processing'
                MERGE (nvda)-[:DEPENDS_ON]->(gpu)
                MERGE (gpu)-[:MANUFACTURED_BY]->(tsmc)
                MERGE (nvda)-[:DEPENDS_ON]->(packaging)
                MERGE (packaging)-[:SUPPLIED_BY]->(ase)
                MERGE (tsmc)-[:OPERATES_IN]->(taiwan)
                MERGE (ase)-[:OPERATES_IN]->(taiwan)
            """)
            print("✓ NVIDIA supply chain created")

            # Apple supply chain
            session.run("""
                MATCH (aapl:Company {ticker: 'AAPL'})
                MATCH (china:Country {name: 'China'})
                MERGE (assembly:Material {name: 'iPhone Assembly'}) SET assembly.type='Manufacturing'
                MERGE (display:Material {name: 'Display Supply'}) SET display.type='Component'
                MERGE (foxconn:Supplier {name: 'Foxconn'}) SET foxconn.country='Taiwan'
                MERGE (boe:Supplier {name: 'BOE Technology'}) SET boe.country='China'
                MERGE (zhengzhou:Region {name: 'Zhengzhou'}) SET zhengzhou.location='China'
                MERGE (aapl)-[:DEPENDS_ON]->(assembly)
                MERGE (aapl)-[:DEPENDS_ON]->(display)
                MERGE (assembly)-[:SUPPLIED_BY]->(foxconn)
                MERGE (display)-[:SUPPLIED_BY]->(boe)
                MERGE (foxconn)-[:OPERATES_IN]->(zhengzhou)
                MERGE (boe)-[:OPERATES_IN]->(china)
            """)
            print("✓ Apple supply chain created")

    def verify_paths(self):
        with self.driver.session(database=os.getenv("NEO4J_DATABASE")) as session:
            for (a, b, label) in [
                ("Mali", "TSLA", "Mali → TSLA"),
                ("Trump", "XOM", "Trump → XOM"),
                ("Taiwan", "NVDA", "Taiwan → NVDA"),
            ]:
                result = session.run(
                    "MATCH path = (a {name:$a})-[*]-(b:Company {ticker:$b}) RETURN path LIMIT 1",
                    a=a, b=b
                )
                print(f"{'✓' if result.single() else '✗'} {label} path exists")

            node_count = session.run("MATCH (n) RETURN count(n) as c").single()["c"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as c").single()["c"]
            print(f"\n📊 Graph Stats: {node_count} nodes, {rel_count} relationships")

def main():
    print("🌱 Seeding Neo4j Graph for StockTrace\n")
    seeder = Neo4jSeeder()
    try:
        seeder.create_constraints()
        seeder.clear_database()
        seeder.seed_graph()
        seeder.verify_paths()
        print("\n✅ Graph seeding complete!")
    finally:
        seeder.close()

if __name__ == "__main__":
    main()
