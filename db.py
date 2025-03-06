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
                config_dir=r"path/directory/wallet",
                wallet_location=r"path/directory/wallet",
                wallet_password=self.wallet_pw
            )
            self.cursor = self.con.cursor()
        except oracledb.DatabaseError as e:
            print("There was a problem connecting to the database:", e)


    def insert_student(self, name, roll_no, email, password):
        try:
            self.cursor.execute("""
                INSERT INTO Students (student_name, roll_no, student_email, student_password)
                VALUES (:name, :roll_no, :email, :password)
            """, {'name': name, 'roll_no': roll_no, 'email': email, 'password': password})
            self.con.commit()  # Use self.con.commit() instead of self.connection.commit()
            return 1
        except oracledb.IntegrityError:
            return 0
        except oracledb.DatabaseError as e:
            print("Error inserting student:", e)
            return 0

    def authenticate(self, email, password):
        try:
            self.cursor.execute("""
                SELECT student_id FROM Students WHERE student_email = :email AND student_password = :password
            """, {'email': email, 'password': password})
            student = self.cursor.fetchone()
            return student is not None
        except oracledb.DatabaseError as e:
            print("Error authenticating user:", e)
            return False

    def get_student_id(self, email):
        try:
            self.cursor.execute("""
                SELECT student_id FROM Students WHERE student_email = :email
            """, {'email': email})
            student = self.cursor.fetchone()
            return student[0] if student else None
        
        except oracledb.DatabaseError as e:
            print("Error getting student ID:", e)
            return None

    def get_assigned_memes(self, student_id):
        try:
            self.cursor.execute("""
                SELECT m.meme_id, m.meme_image_path 
                FROM Memes m
                JOIN Assignments a ON m.meme_id = a.meme_id
                WHERE a.student_id = :student_id AND a.is_completed = 0
            """, {'student_id': student_id})
            return self.cursor.fetchall()
        except oracledb.DatabaseError as e:
            print("Error getting assigned memes:", e)
            return None

    def submit_rating(self, student_id, meme_id, rating, comment_1, classification_1):
        try:
            self.cursor.execute("""
                UPDATE Assignments
                SET rating = :rating, comment_1 = :comment_1, classification_1 = :classification_1, is_completed = 1
                WHERE student_id = :student_id AND meme_id = :meme_id
            """, {'rating': rating, 'comment_1': comment_1, 'classification_1': classification_1, 'student_id': student_id, 'meme_id': meme_id})
            self.con.commit()  # Use self.con.commit() instead of self.connection.commit()
        except oracledb.DatabaseError as e:
            print("Error submitting rating:", e)
