import random

def assign_memes_to_students(cursor):
    # Get the total number of students and memes
    cursor.execute("SELECT student_id FROM Students")
    students = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT meme_id FROM Memes")
    memes = [row[0] for row in cursor.fetchall()]
    
    # Shuffle memes to ensure random distribution
    random.shuffle(memes)
    
    meme_assignment_count = {meme_id: 0 for meme_id in memes}
    assignments = []

    for student_id in students:
        assigned_memes = random.sample([meme_id for meme_id in memes if meme_assignment_count[meme_id] < 5], 10)
        for meme_id in assigned_memes:
            assignments.append((student_id, meme_id))
            meme_assignment_count[meme_id] += 1

    # Insert assignments into the Assignments table
    cursor.executemany("""
        INSERT INTO Assignments (student_id, meme_id)
        VALUES (:1, :2)
    """, assignments)

    # Commit the transaction to save changes
    cursor.connection.commit()

# Example of using the function
assign_memes_to_students(cursor)
