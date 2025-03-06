import random
import oracledb

class Database:
    def __init__(self):
        try:
            self.user = "admin"
            self.dsn = "memed_high"
            self.pw = "370822@Deepesh"
            self.wallet_pw = "370822@Deepesh"

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

    def fetch_unassigned_memes(self):
        try:
            self.cursor.execute("""
                SELECT meme_id
                FROM Memes
                WHERE meme_id NOT IN (
                    SELECT meme_id
                    FROM Assignments
                )
            """)
            return [row[0] for row in self.cursor.fetchall()]
        except oracledb.DatabaseError as e:
            print("Error fetching unassigned memes:", e)
            return []

    def fetch_students(self):
        try:
            self.cursor.execute("SELECT student_id FROM Students")
            return [row[0] for row in self.cursor.fetchall()]
        except oracledb.DatabaseError as e:
            print("Error fetching students:", e)
            return []

    def assign_memes_to_students(self, student_ids, meme_ids):
        assignments = []
        student_meme_count = {student_id: 0 for student_id in student_ids}
        
        for student_id in student_ids:
            assigned_memes = set()
            while len(assigned_memes) < 100 and meme_ids:
                meme_id = meme_ids.pop(0)  # Take a meme from the list
                assigned_memes.add(meme_id)
                assignments.append((student_id, meme_id))

            if len(assigned_memes) < 100:
                print(f"Not enough memes to assign 100 memes to student {student_id}.")
                break

        try:
            self.cursor.executemany("""
                INSERT INTO Assignments (student_id, meme_id)
                VALUES (:1, :2)
            """, assignments)
            self.con.commit()
            print(f"Assigned {len(assignments)} memes to students.")
        except oracledb.DatabaseError as e:
            print("Error assigning memes:", e)


dbo = Database()

def assign_memes():
    # Fetch unassigned memes and students
    unassigned_memes = dbo.fetch_unassigned_memes()
    students = dbo.fetch_students()
    
    # Fetch current assignments to prevent reassigning
    existing_assignments = {}
    try:
        dbo.cursor.execute("""
            SELECT student_id, COUNT(meme_id) 
            FROM Assignments
            GROUP BY student_id
        """)
        existing_assignments = {row[0]: row[1] for row in dbo.cursor.fetchall()}
    except oracledb.DatabaseError as e:
        print("Error fetching existing assignments:", e)

    # Filter students who need more memes to reach 100
    eligible_students = [student_id for student_id in students if existing_assignments.get(student_id, 0) < 100]
    
    if not eligible_students:
        print("No eligible students for assignment.", "warning")
        return

    # Assign memes to eligible students if there are memes and eligible students available
    if unassigned_memes:
        dbo.assign_memes_to_students(eligible_students, unassigned_memes)
        print("Memes have been assigned to eligible students.", "success")
    else:
        print("No memes available for assignment.", "warning")


assign_memes()
