import cx_Oracle
import os

try:
    # Establish the connection to the Oracle Database
    connection = cx_Oracle.connect(
        user="admin",
        password="88050@Deepesh",
        dsn="(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.ap-mumbai-1.oraclecloud.com))(connect_data=(service_name=g2f9d4fc79267ca_memetag_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"
    )
    print("Successfully connected to the Oracle Database")
    
    # Create a cursor
    cursor = connection.cursor()
    
    # Execute a simple query to check the connection
    cursor.execute("SELECT SYSDATE FROM DUAL")
    result = cursor.fetchone()
    print("Current database date and time:", result[0])

    # Define the directory where images are stored
    meme_directory = 'static/memes'

    for filename in os.listdir(meme_directory):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Add more extensions if needed
            # Insert image path into the Memes table
            cursor.execute("""
                INSERT INTO Memes (meme_image_path) 
                VALUES (:image_path)
            """, {'image_path': filename})  # Store only filename

    # Commit the transaction to save changes
    connection.commit()
    
except cx_Oracle.DatabaseError as e:
    # Handle any errors that occur during the database operations
    print("There was an error with the Oracle Database operation:", e)

finally:
    # Ensure resources are closed even if an error occurs
    if cursor:
        cursor.close()
    if connection:
        connection.close()
