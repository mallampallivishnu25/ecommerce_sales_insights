import argparse, os, glob
import duckdb

def run_sql_dir(db_path: str, sql_dir: str):
    con = duckdb.connect(db_path)
    files = sorted(glob.glob(os.path.join(sql_dir, "*.sql")))
    if not files:
        print(f"No SQL files found in {sql_dir}")
        return
    for f in files:
        print(f"Executing: {f}")
        with open(f, "r") as fh:
            sql = fh.read()
        con.execute(sql)
    con.close()
    print("Completed executing SQL files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb"))
    parser.add_argument("--run-sql", dest="sql_dir", default="src/transform/sql")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    run_sql_dir(args.db, args.sql_dir)
