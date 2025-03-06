import cx_Oracle

# Establish the database connection
connection = cx_Oracle.connect(
    user="admin",
    password="88050@Deepesh",
    dsn="(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.ap-mumbai-1.oraclecloud.com))(connect_data=(service_name=g2f9d4fc79267ca_memetag_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"
)
cursor = connection.cursor()

print("Checking memes...")
cursor.execute("""
    SELECT * FROM Memes WHERE meme_id = 3318
""")
memes = cursor.fetchall()
print("Memes:", memes)