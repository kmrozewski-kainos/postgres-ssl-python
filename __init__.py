import psycopg2 as pg
from os.path import abspath

# Constants
pg_host = "localhost"
pg_port = int(5432)
pg_name = "postgres"
pg_user = "postgres"
pg_pass = "postgres"
root_cert = abspath("./postgres-keys/root.crt")
client_pub_cert = abspath("./postgres-keys/postgresql.crt")
client_priv_key = abspath("./postgres-keys/postgresql.key")

# Queries
query = {
    "create": "create table if not exists names(id serial primary key, name varchar(20))",
    "count": "select count(*) as cnt from names",
    "insert": "insert into names(name) values (%s)",
    "get": "select id, name from names",
    "delete": "delete from names returning *"
}

# DB connection
db_conn = pg.connect(host = pg_host, port = pg_port, user = pg_user, password = pg_pass, dbname = pg_name,
               sslmode = "verify-ca", sslrootcert = root_cert, sslcert = client_pub_cert, sslkey = client_priv_key)

# Wrapper
def execute_queries(db_conn, fn):
    with db_conn:
        with db_conn.cursor() as cursor:
            return fn(cursor)

# Functions with database operations
def get_table_count(cursor):
    cursor.execute(query["create"])
    cursor.execute(query["count"])
    return int(cursor.fetchone()[0])

def add_name(cursor):
        print "Executing:\n\t%s" % cursor.mogrify(query["insert"], ("Konrad", ))
        cursor.execute(query["insert"], ("Konrad",))

def select_from_names(cursor):
    cursor.execute(query["get"])
    return map(lambda record: record, cursor)

def delete_all_from_names(cursor):
    cursor.execute(query["delete"])
    deleted = map(lambda record: record, cursor)
    print "Deleted %s rows" % str(len(deleted))
    return deleted

# Execute queries
print "\n\nCreate table 'names'"
print execute_queries(db_conn, get_table_count)
print "\n\nInsert values to the table 'names'"
print execute_queries(db_conn, add_name)
print "\n\nPull data from table 'names'"
print execute_queries(db_conn, select_from_names)
print "\n\nDelte all rows from the table 'names'"
print execute_queries(db_conn, delete_all_from_names)

# Close connection at the end of the script
# using 'with pg.connect() as db_conn' won't close db connection at the end
# of the 'with' block
db_conn.close()
