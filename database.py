import sqlite3


def get_connection():
    try:
        # IF Multithreading error comes then change with below code 
        # conn = sqlite3.connect("Quiz.db", check_same_thread=False)  # Enable thread safety
        conn = sqlite3.connect("Quiz.db")
        print("Database connection established")
        return conn
    except sqlite3.Error as e:
        print(f"Error occurred while connecting to the database: {e}")
        return None
    

def delete_all_records():
    conn = get_connection()
    cobj = conn.cursor()
    cobj.execute("DELETE FROM STUDENT_DATA")
    conn.commit()
    conn.close()

def create_table_if_not_exists():
    # Create the table if it does not exist
    try:
        conn = get_connection()
        cobj = conn.cursor()
        table = """
        CREATE TABLE IF NOT EXISTS STUDENT_DATA(
            student_id TEXT,
            wallet_address TEXT,
            exam_title TEXT,
            city TEXT,
            center_name TEXT,
            booklet TEXT,
            start_time TEXT,
            que_ans TEXT,
            suspicious_activity_detected TEXT,
            end_time TEXT,
            transaction_id TEXT
        )
        """
        
        cobj.execute(table)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error occurred while creating the table: {e}")
        conn.rollback()

def drop_table():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DROP TABLE STUDENT_DATA")

    conn.commit()
    conn.close()

    print("Dropped STUDENT table")

def add_student_data(data):
    try:
        student_id = data.get("student_id")
        wallet_address = data.get("wallet_address")
        exam_title = data.get("exam_title")
        city = data.get("city")
        center_name = data.get("center_name")
        booklet = data.get("booklet")
        start_time = data.get("start_time")
        que_ans = data.get("que_ans")
        suspicious_activity_detected = data.get("suspicious_activity_detected")
        end_time = data.get("end_time")
        transaction_id = data.get("transaction_id")

        if not all(
            [student_id, wallet_address, exam_title, city, center_name, booklet, start_time, que_ans, end_time, transaction_id]
        ):
            return {"error": "Missing parameters"}
        conn = get_connection()
        cobj = conn.cursor()
        cobj.execute(
            """INSERT INTO STUDENT_DATA (student_id, wallet_address, exam_title, city, center_name, booklet, start_time, que_ans, suspicious_activity_detected, end_time, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                student_id,
                wallet_address,
                exam_title,
                city,
                center_name,
                booklet,
                start_time,
                que_ans,
                suspicious_activity_detected,
                end_time,
                transaction_id,
            ),
        )
        conn.commit()
        conn.close()
        return {"success": "Student data added successfully"}
    except sqlite3.Error as e:
        print(f"Error occurred while adding student data: {e}")
        conn.rollback()
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    result = add_student_data({
        "student_id": "12345",
        "wallet_address": "0xabc123",
        "exam_title": "Math",
        "city": "Springfield",
        "center_name": "Central School",
        "booklet": "A",
        "start_time": "09:00",
        "que_ans": "1-A",
        "suspicious_activity_detected": "No",
        "end_time": "10:00",
        "transaction_id": "tx123456"
    })
    print(result)
