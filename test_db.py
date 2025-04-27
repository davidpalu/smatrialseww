import sqlite3

def test_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('study.db')
        cur = conn.cursor()
        
        # Test subjects table
        print("\nSubjects in database:")
        cur.execute("SELECT * FROM subjects")
        subjects = cur.fetchall()
        for subject in subjects:
            print(f"ID: {subject[0]}, Name: {subject[1]}")
        
        # Test materials table
        print("\nMaterials in database:")
        cur.execute("SELECT m.id, s.name, m.title, m.file_path, m.uploaded_on FROM materials m JOIN subjects s ON m.subject_id = s.id")
        materials = cur.fetchall()
        for material in materials:
            print(f"ID: {material[0]}, Subject: {material[1]}, Title: {material[2]}, File: {material[3]}, Uploaded: {material[4]}")
        
        conn.close()
        print("\nDatabase connection successful!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_database() 