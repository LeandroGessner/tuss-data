import psycopg2

# Replace with your Postgres credentials and host
conn = psycopg2.connect(
    host="localhost",  # Use the host machine's IP or hostname
    database="postgres",
    user="user",
    password="password"
)

cur = conn.cursor()

# Perform database operations
cur.execute("SELECT * FROM coco")
rows = cur.fetchall()
print(rows)

cur.close()
conn.close()
