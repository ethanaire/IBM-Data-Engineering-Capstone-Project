# This program requires the python module ibm-db to be installed.
# Install it using the below command
# python3 -m pip install ibm-db

# Install the connection using this command: pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3

# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to DB2
import ibm_db

# Connect to MySQL
connection = mysql.connector.connect(user='root', password='4UqHQRfJd74cj2f97qEB6ngU',host='172.21.54.124',database='sales')
if (connection):
	print("Connected to MySQL")
# create cursor
cursor = connection.cursor()

# connection details

dsn_hostname = "21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "mqv21447"        # e.g. "abc12345"
dsn_pwd = "zWgQ0yQXIiTsmqOC"      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "31864"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"

# Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# create connection
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

# Find out the last rowid from DB2 data warehouse
def get_last_rowid():
    SQL = "SELECT MAX(ROWID) FROM sales_data"
    stmt = ibm_db.exec_immediate(conn, SQL)
    res = ibm_db.fetch_both(stmt)
    print(res)
    return int(res[0])

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# Find out the lastest rowid from MySQL data warehouse
def get_latest_records(rowid):
    SQL = "SELECT * FROM sales_data WHERE rowid > %s"
    cursor.execute(SQL, [rowid])
    new_recs = cursor.fetchall()
    # for row in new_recs: print(row)
    return new_recs

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 data warehouse.
def insert_records(records):
    SQL = "INSERT INTO sales_data(rowid,product_id,customer_id,quantity) VALUES(?,?,?,?);"
    stmt = ibm_db.prepare(conn, SQL)

    for record in records:
        ibm_db.execute(stmt, record)

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))


# disconnect from mysql warehouse
connection.close()

# disconnect from DB2 data warehouse
ibm_db.close(conn)

# End of program
print("End of program")
