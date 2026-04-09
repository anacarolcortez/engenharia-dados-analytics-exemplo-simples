import duckdb

class DuckDBClient:
    def __init__(self, path="data/processed/processos.parquet"):
        self.path = path
        self.con = duckdb.connect()

    def query(self, sql: str):
        return self.con.execute(sql).fetchdf()