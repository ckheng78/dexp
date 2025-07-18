from db import dexp_db

def test():
    db = dexp_db()
    try:
        # Example query to test the connection
        result = db.execute_query("SELECT * FROM actor LIMIT 5")
        for row in result:
            print(row)
    finally:
        db.close()