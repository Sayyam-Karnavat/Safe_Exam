from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import sqlite3
import threading
from deploy_file import Blockchain
from collections import deque
import time
import subprocess
import sys
import metadata

app = Flask(__name__)
CORS(app=app)
socketApp = SocketIO(app, cors_allowed_origins="*")

# Global variables initialization
blockchain_obj = Blockchain(user_id="admin")
queue_obj = None
stop_Event = threading.Event()

############################################################################

# Exam title , Start and End-Time

Exam_Name = metadata.Exam_Title
exam_start_time = metadata.exam_start_time
exam_end_time = metadata.exam_end_time


# Exam question and answer data
question_answer_data = metadata.quiz_data

#############################################################################


def kill_background_terminal():
    script_path = 'kill-conhost.ps1'
    command = [
        'powershell.exe',
        '-ExecutionPolicy', 'ByPass',
        '-File', script_path
    ]
    try:
        subprocess.Popen(command)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    sys.exit(0)

class TaskQueue:
    def __init__(self):
        self.task_queue = deque()

    def add_task(self, student_json_data):
        self.task_queue.appendleft(student_json_data)
        return 1

    def write_data_to_blockchain(self, json_student_data):
        student_id = json_student_data.get('student_id', "-")
        exam_title = json_student_data.get('exam_title', "-")
        city = json_student_data.get('city', "-")
        center_name = json_student_data.get('center_name', "-")
        booklet = json_student_data.get('booklet', "-")
        start_time = json_student_data.get('start_time', "-")
        que_ans = json_student_data.get('que_ans', "-")
        end_time = json_student_data.get('end_time', "-")
        suspicious_activity_detected = json_student_data.get('suspicious_activity_detected', "-")
        wallet_address = json_student_data.get('wallet_address', "-")
        user_mnemonic = json_student_data.get("user_mnemonic" , "-")

        transaction_id, wallet_address = blockchain_obj.deploy_data(
            student_id=student_id,
            exam_title=exam_title,
            city=city,
            center_name=center_name,
            suspicious_activity_detected=suspicious_activity_detected,
            start_time=start_time,
            end_time=end_time,
            booklet=booklet,
            que_ans=que_ans,
            user_mnemonic=user_mnemonic
        )
        
        json_student_data['transaction_id'] = transaction_id
        json_student_data['wallet_address'] = wallet_address


        ##################################################################################################################
        # Retry logic by append the data again to queue.
        
        if transaction_id == -1 and wallet_address == -1:
            # Error occured (possibly timeout error ) , hence again append the data to queue
            self.add_task(student_json_data= json_student_data)
        ##################################################################################################################
        else:
            try:
                with sqlite3.connect("Quiz.db", check_same_thread=False) as conn:
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
                print("Data written to local database!")
            except sqlite3.Error as e:
                print(f"Error occurred while adding student data: {e}")

    def get_all_tasks(self):
        return list(self.task_queue)

def complete_task(queue_obj):
    global stop_Event
    while not stop_Event.is_set():
        time.sleep(1)  # Avoid busy waiting
        if queue_obj.task_queue:
            task_json_data = queue_obj.task_queue.pop()
            if task_json_data:
                queue_obj.write_data_to_blockchain(task_json_data)

def get_quiz_db_connection():
    return sqlite3.connect("Quiz.db", check_same_thread=False)

@app.route("/")
def index():
    return "Socket server is running!"


@app.route("/get_question_answer" , methods =['GET'])
def get_question_answer():
    return question_answer_data
    

@app.route("/exam_data", methods=['GET'])
def exam_start():
    global exam_end_time, Exam_Name
    try:
        exam_json = {
            "exam_start_time": exam_start_time,
            "exam_name": Exam_Name,
            "exam_end_time": exam_end_time
        }
        socketApp.emit("exam_start", exam_json)
        return jsonify(exam_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/send_data_to_blockchain", methods=['POST'])
def receive_student_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data received"}), 400
    queue_obj.add_task(data)
    return '', 200

@app.route("/get_all_quiz_data")
def get_quiz_data():
    try:
        conn = get_quiz_db_connection()
        cursor = conn.cursor()
        all_rows = cursor.execute("SELECT * FROM STUDENT_DATA").fetchall()
        student_data = [
            {
                "student_id": row[0],
                "wallet_address": row[1],
                "exam_title": row[2],
                "city": row[3],
                "center_name": row[4],
                "booklet": row[5],
                "start_time": row[6],
                "que_ans": row[7],
                "suspicious_activity_detected": row[8],
                "end_time": row[9],
                "transaction_id": row[10],
            }
            for row in all_rows
        ]
        return jsonify(student_data), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_wallet_data/<wallet_address>", methods=['GET'])
def get_wallet_data(wallet_address):
    try:
        conn = get_quiz_db_connection()
        cursor = conn.cursor()
        all_rows = cursor.execute("SELECT * FROM STUDENT_DATA WHERE wallet_address=?", (wallet_address,)).fetchall()
        student_data = [
            {
                "student_id": row[0],
                "wallet_address": row[1],
                "exam_title": row[2],
                "city": row[3],
                "center_name": row[4],
                "booklet": row[5],
                "start_time": row[6],
                "que_ans": row[7],
                "suspicious_activity_detected": row[8],
                "end_time": row[9],
                "transaction_id": row[10],
            }
            for row in all_rows
        ]
        return jsonify(student_data), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_starttime_AI_data/", methods=['GET'])
def get_specific_time_and_AI_data():
    try:
        conn = get_quiz_db_connection()
        cursor = conn.cursor()
        all_rows = cursor.execute('SELECT student_id , wallet_address ,start_time , suspicious_activity_detected, end_time , transaction_id FROM STUDENT_DATA WHERE start_time <> "-" or end_time <> "-" or suspicious_activity_detected= "yes"').fetchall()
        student_data = [
            {
                "student_id": row[0],
                "wallet_address": row[1],
                "start_time": row[2],
                "suspicious_activity_detected": row[3],
                "end_time": row[4],
                "transaction_id": row[5],
            }
            for row in all_rows
        ]


        return jsonify(student_data), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_crash_exam_index_answers/<application_id>", methods=['GET'])
def get_crashed_exam_details(application_id):
    try:
        # Pass the captured student_id to the method
        resume_index, question_answer_data = blockchain_obj.get_crash_exam_details(application_id=application_id)
        return jsonify({"resume_index": resume_index, "question_answer_data": question_answer_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def create_table_if_not_exists():
    try:
        with get_quiz_db_connection() as conn:
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
    except sqlite3.Error as e:
        print(f"Error occurred while creating the table: {e}")

def delete_all_records():
    try:
        with get_quiz_db_connection() as conn:
            cobj = conn.cursor()
            cobj.execute("DELETE FROM STUDENT_DATA")
            conn.commit()
            print("All records deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error occurred while deleting all records: {e}")

if __name__ == "__main__":
    create_table_if_not_exists()
    queue_obj = TaskQueue()
    thread = threading.Thread(target=complete_task, args=(queue_obj,))
    thread.start()
    try:
        print("Quiz socket running !!!!")
        socketApp.run(app, host="0.0.0.0", port=2222, debug=False)
        while len(queue_obj.task_queue) > 0:
            print("Tasks pending in queue !!!")
            time.sleep(1)
        stop_Event.set()
        thread.join()  # Gracefully stop the thread
    except Exception as e:
        print("Error occurred !!!", e)
    finally:
        kill_background_terminal()
        print("Server stopped.")
