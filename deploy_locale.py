import base64
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from artifact_file import HelloWorldClient


# pip install algokit-utils py-algorand-sdk


class Blockchain:

    def __init__(self):
        self.algod_address = "http://localhost:4001"
        self.algod_token = "a" * 64
        self.indexer_add = "http://localhost:8980"
        self.algod_client = AlgodClient(self.algod_token, self.algod_address)
        self.indexer_client = IndexerClient(self.algod_token, self.indexer_add)


        # Gets the default account from localnet 
        self.deployer = algokit_utils.get_localnet_default_account(self.algod_client)


        self.app_client = HelloWorldClient(
            self.algod_client,
            creator=self.deployer,
            indexer_client=self.indexer_client,
        )

        # This wallet address is used in QnA and Login page to filter transactions and to resume quiz
        self.wallet_address = self.deployer.address
        self.app_client.deploy(
            on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
            on_update=algokit_utils.OnUpdate.AppendApp,
        )
        
        self.deployed_app = self.app_client.app_id

    def deploy_data(self,student_id,exam_title,city,center_name,booklet,start_time,que_ans,suspicious_activity_detected,end_time):
        self.response = self.app_client.quiz_data(student_id=student_id , 
                                        exam_title=exam_title ,
                                        city=city,
                                        center_name=center_name,
                                        booklet=booklet,
                                        start_time=start_time,
                                        end_time=end_time,
                                        que_ans=que_ans,
                                        suspicious_activity_detected=suspicious_activity_detected,
                                        wallet_address=self.wallet_address)
        self.transaction_id = self.response.tx_id
        print(f"Sender wallet {self.wallet_address}")

        if "yes" in str(suspicious_activity_detected).lower():
            print(f"!!! Unusual Activity detected !!!\n Transaction :- https://lora.algokit.io/localnet/transaction/{self.transaction_id}")
        else:
            print(f" ### EXAM TRANSACTTION ### :- https://lora.algokit.io/localnet/transaction/{self.transaction_id}")
        return self.transaction_id , self.wallet_address


    def get_all_transactions(self, wallet_address ,appId):
        print(f"Getting all transactions for {wallet_address} - in App:- {appId}")
        self.response = self.indexer_client.search_transactions(address=wallet_address , application_id=appId)
        all_transactions = self.response['transactions']

        for single_transaction in all_transactions:
            if "global-state-delta" in single_transaction:
                global_state_delta = single_transaction['global-state-delta']
                for single_delta in global_state_delta:
                    print(single_delta)
                    attribute = single_delta['key']
                    value = single_delta['value']['bytes']
                    print(f"Attribute:- {base64.b64decode(attribute).decode('utf-8')} ||| Value:-  {base64.b64decode(value).decode('utf-8')}")
                print("-"*64)

    def check_unleft_exam(self):
            '''
            This functions checks if software crashed while user was giving exam and returns the question index number
            where the user left the exam.
            '''
            max_index = 0
            # We are picking wallet address and appid from deploy locale file which is imported in this folder
            question_answer_data = {}
            response = self.indexer_client.search_transactions(address=self.wallet_address , application_id=self.deployed_app)
            all_transactions = response['transactions']
    
            for single_transaction in all_transactions:
                if "global-state-delta" in single_transaction:
                    global_state_delta = single_transaction['global-state-delta']
                    for single_delta in global_state_delta:
                        try:
                            attribute = single_delta.get('key')
                            value = single_delta.get('value').get('bytes')
                            decoded_attribute = base64.b64decode(attribute).decode('utf-8')
                            decoded_value = base64.b64decode(value).decode('utf-8')
                            # print(f"{decoded_attribute} :- {decoded_value}")
                            # Since sequentially data is retrieved if user has selected multiple answer for same question traversing back and forth then
                            # The latest answer will be overwritten automatically
                            if decoded_attribute == "global_que_ans" and value.strip() !="-":
                                question_num , answer = decoded_value.strip().split("-")
                                if question_num.strip().isdigit():
                                    if not question_answer_data.get(question_num.strip()):
                                        question_answer_data[question_num.strip()] = answer.strip()
                        except:
                            continue
                    # print("-"*64)
            if question_answer_data:
                # # IF using sorting on dictonary then we can use pop directly after sorting to get max index
                # question_answer_data_sorted = sorted(question_answer_data.items(), key=lambda item: item[0])
                max_index = max( question_answer_data, key= lambda item : item[0])
            return max_index , question_answer_data