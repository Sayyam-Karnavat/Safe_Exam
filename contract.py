from algopy import ARC4Contract, String,subroutine
from algopy.arc4 import abimethod


class HelloWorld(ARC4Contract):
    @abimethod()
    def quiz_data(
        self,
        wallet_address: String,
        student_id: String,
        exam_title: String,
        city: String,
        center_name: String,
        booklet: String,
        start_time: String,
        que_ans: String,
        suspicious_activity_detected: String,
        end_time: String,
    ) -> None:
        self.reset_global_state()
        self.global_wallet_address = wallet_address
        self.global_student_id = student_id
        self.global_exam_title = exam_title
        self.global_city = city
        self.global_center_name = center_name
        self.global_booklet = booklet
        self.global_start_time = start_time
        self.global_que_ans = que_ans
        self.global_suspicious_activity_detected = suspicious_activity_detected
        self.global_end_time = end_time

    @subroutine
    def reset_global_state(self) -> None:
        self.global_wallet_address = String("")
        self.global_student_id = String("")
        self.global_exam_title = String("")
        self.global_city = String("")
        self.global_center_name = String("")
        self.global_booklet = String("")
        self.global_start_time = String("")
        self.global_que_ans = String("")
        self.global_suspicious_activity_detected = String("")
        self.global_end_time = String("")
