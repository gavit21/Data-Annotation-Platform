import os
import oracledb

class Database:
    def __init__(self):
        try:
            self.user = "admin"
            self.dsn = "memed_high"
            self.pw = "password"
            self.wallet_pw = "password"

            self.con = oracledb.connect(
                user=self.user,
                password=self.pw,
                dsn=self.dsn,
                config_dir=r"/home/deepeshg/Desktop/DB/deep_wallet",
                wallet_location=r"/home/deepeshg/Desktop/DB/deep_wallet",
                wallet_password=self.wallet_pw
            )
            self.cursor = self.con.cursor()
        except oracledb.DatabaseError as e:
            print("There was a problem connecting to the database:", e)

    def insert_meme(self, meme_image_filename):
        try:
            self.cursor.execute("""
                INSERT INTO Memes (meme_image_path)
                VALUES (:meme_image_path)
            """, {'meme_image_path': meme_image_filename})  # Insert only the filename, not the full path
            self.con.commit()  # Make sure to use self.con for commit
            print(f"Inserted meme filename: {meme_image_filename}")
        except oracledb.DatabaseError as e:  # Changed cx_Oracle to oracledb
            print(f"Error inserting meme filename {meme_image_filename}: {e}")

    def close(self):
        try:
            self.cursor.close()
            self.con.close()  # Make sure to use self.con for connection close
            print("Database connection closed.")
        except oracledb.DatabaseError as e:  # Changed cx_Oracle to oracledb
            print("Error closing the connection:", e)

def insert_memes_from_folder(db, folder_path):
    # Get all image files from the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Insert each image file into the Memes table
    for image_file in image_files:
        # Insert only the filename into the database
        db.insert_meme(image_file)

if __name__ == "__main__":
    # Initialize the database connection
    db = Database()
    
    # Specify the folder where the meme images are stored
    folder_path = "static/memes"  # Make sure this is the relative folder path used by your Flask app
    
    # Insert the meme filenames into the database
    insert_memes_from_folder(db, folder_path)

    # Close the database connection
    db.close()
