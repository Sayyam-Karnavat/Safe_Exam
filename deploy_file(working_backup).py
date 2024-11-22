import base64
from artifact_file import HelloWorldClient
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import account, mnemonic, transaction


class Blockchain:
    def __init__(self):
        # Create the client
        self.algod_address = "https://testnet-api.algonode.cloud"
        self.algod_token = "a" * 64
        self.indexer_add = "https://testnet-idx.algonode.cloud"
        self.algod_client = AlgodClient(self.algod_token, self.algod_address)
        self.indexer_client = IndexerClient("", self.indexer_add)
        self.private_key, self.address = account.generate_account()
        self.new_mnemonic = mnemonic.from_private_key(self.private_key)
        self.deployer = algokit_utils.get_account_from_mnemonic(self.new_mnemonic)
        print(
            f"Deployer address: {self.deployer.address}\nDeployer privateKey: {self.deployer.private_key}"
        )
        self.app_client = HelloWorldClient(
            self.algod_client, creator=self.deployer, indexer_client=self.indexer_client
        )
        # Funded Account
        self.master_wallet = mnemonic.to_private_key(
            "banner enlist wide have awake rail resource antique arch tonight pilot abuse file metal canvas beyond antique apart giant once slight ice beef able uncle"
        )
        self.master_addr = account.address_from_private_key(self.master_wallet)
        self.amount_microalgos = int(1 * 1e6)
        self.suggested_params = self.algod_client.suggested_params()
        self.txn = transaction.PaymentTxn(
            sender=self.master_addr,
            receiver=self.deployer.address,
            amt=self.amount_microalgos,
            sp=self.suggested_params,
        )
        self.signed_txn = self.txn.sign(self.master_wallet)
        self.txid = self.algod_client.send_transaction(self.signed_txn)
        print(f"Account Funded...  Transaction ID:- {self.txid}")
        self.wallet_address = self.deployer.address
        self.app_client.deploy(
            on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
            on_update=algokit_utils.OnUpdate.AppendApp,
        )
        # app_client.app_id = 675696144
        self.deployed_app = self.app_client.app_id
        print("App ID:", self.app_client.app_id)

    def deploy_data(
        self,
        student_id,
        exam_title,
        city,
        center_name,
        booklet,
        start_time,
        que_ans,
        suspicious_activity_detected,
        end_time,
    ):
        try:

            self.response = self.app_client.quiz_data(
                student_id=student_id,
                exam_title=exam_title,
                city=city,
                center_name=center_name,
                booklet=booklet,
                start_time=start_time,
                end_time=end_time,
                que_ans=que_ans,
                suspicious_activity_detected=suspicious_activity_detected,
                wallet_address=self.wallet_address,
            )
            self.transaction_id = self.response.tx_id
            self.sender_wallet = self.response.tx_info["txn"]["txn"]["snd"]
            if "yes" in str(suspicious_activity_detected):

                print(f"!!! Malicicous activity Transaction !!!:- https://app.dappflow.org/explorer/transaction/{self.transaction_id}")
            else:
                print(f"Exam Transaction :- https://app.dappflow.org/explorer/transaction/{self.transaction_id}")
            return self.transaction_id, self.sender_wallet
        except Exception as e :
            print("Error writing data to blockchain !!!")
            return -1 , -1 

    def get_all_transactions(self, wallet_address, appId):
        print(f"Getting all transactions for {wallet_address} - in App:- {appId}")
        self.response = self.indexer_client.search_transactions(
            address=wallet_address, application_id=appId
        )
        all_transactions = self.response["transactions"]

        for single_transaction in all_transactions:
            if "global-state-delta" in single_transaction:
                global_state_delta = single_transaction["global-state-delta"]
                for single_delta in global_state_delta:
                    print(single_delta)
                    attribute = single_delta["key"]
                    value = single_delta["value"]["bytes"]
                    print(
                        f"Attribute:- {base64.b64decode(attribute).decode('utf-8')} ||| Value:-  {base64.b64decode(value).decode('utf-8')}"
                    )
                print("-" * 64)

    def check_unleft_exam(self):
        """
        This functions checks if software crashed while user was giving exam and returns the question index number
        where the user left the exam.
        """
        try:

            max_index = 0
            # We are picking wallet address and appid from deploy locale file which is imported in this folder
            question_answer_data = {}
            response = self.indexer_client.search_transactions(
                address=self.wallet_address, application_id=self.deployed_app
            )
            all_transactions = response["transactions"]

            for single_transaction in all_transactions:
                if "global-state-delta" in single_transaction:
                    global_state_delta = single_transaction["global-state-delta"]
                    for single_delta in global_state_delta:
                        try:
                            attribute = single_delta.get("key")
                            value = single_delta.get("value").get("bytes")
                            decoded_attribute = base64.b64decode(attribute).decode("utf-8")
                            decoded_value = base64.b64decode(value).decode("utf-8")
                            # print(f"{decoded_attribute} :- {decoded_value}")
                            # Since sequentially data is retrieved if user has selected multiple answer for same question traversing back and forth then
                            # The latest answer will be overwritten automatically
                            if (
                                decoded_attribute == "global_que_ans"
                                and value.strip() != "-"
                            ):
                                question_num, answer = decoded_value.strip().split("-")
                                if question_num.strip().isdigit():
                                    if not question_answer_data.get(question_num.strip()):
                                        question_answer_data[question_num.strip()] = (
                                            answer.strip()
                                        )
                        except:
                            continue
                    # print("-"*64)
            print("Question answer data:-" , question_answer_data)
            if question_answer_data:
                # # IF using sorting on dictonary then we can use pop directly after sorting to get max index
                # question_answer_data_sorted = sorted(question_answer_data.items(), key=lambda item: item[0])
                max_index = max(question_answer_data, key=lambda item: item[0])
            return max_index, question_answer_data
        except Exception as e:
            print("Error in deploy file (testnet)" , e)


# if __name__ == "__main__":
#     data = Blockchain()
#     wallet_address = "VYO6EHVAW4GBWV2DSQV6LW2ZH4FFQXCESWODBXD7KRI3SHABD55GPYBCLE"
#     student_id = "1234"
#     exam_title = "Bank Exam"
#     city = "Surat"
#     center_name = "VNSGU"
#     booklet = "A"
#     start_time = "14 : 47 : 43"
#     que_ans = "1:D"
#     suspicious_activity_detected = "No"
#     end_time = "14 : 47 : 43"
#     data.deploy_data(wallet_address,student_id,exam_title,city,center_name,booklet,start_time,que_ans,suspicious_activity_detected,end_time)
#     data.get_all_transactions("VYO6EHVAW4GBWV2DSQV6LW2ZH4FFQXCESWODBXD7KRI3SHABD55GPYBCLE","1001")
