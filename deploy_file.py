import base64
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import account, mnemonic, transaction
from artifact_file import HelloWorldClient


class Blockchain:


    def __init__(self , user_id ,user_already_exist = False , user_json_data = None ):

        ########################################################################
        # Create the client
        self.algod_address = "https://testnet-api.algonode.cloud"
        self.algod_token = "a" * 64
        self.indexer_add = "https://testnet-idx.algonode.cloud"
        self.algod_client = AlgodClient(self.algod_token, self.algod_address)
        self.indexer_client = IndexerClient("", self.indexer_add)


        ################################################################################
        self.UserID = user_id

        if not user_already_exist:
            # User's data (User is the deployer of app)
            self.private_key , self.address = self.generate_account()
            self.new_mnemonic = mnemonic.from_private_key(self.private_key)
            self.deployer = algokit_utils.get_account_from_mnemonic(self.new_mnemonic)
            self.__fund_account()
            self.app_client , self.deployed_app = self.deploy_app()

        else:
            # Check if the json data of already existing user is provided or not
            if user_json_data:
                self.private_key , self.address = user_json_data['user_private_key'] , user_json_data['user_wallet_address']
                self.new_mnemonic = mnemonic.from_private_key(self.private_key)
                self.deployer = algokit_utils.get_account_from_mnemonic(self.new_mnemonic)
                self.app_client = HelloWorldClient(
                self.algod_client, creator=self.deployer, indexer_client=self.indexer_client
                )
                self.deployed_app = user_json_data['app_id']
            else:
                print("User Json Data not provided !!!")


    @staticmethod
    def generate_account():
        private_key,wallet_address = account.generate_account()
        return (private_key , wallet_address)


    def __fund_account(self):
        # Funded Account
        self.master_wallet = mnemonic.to_private_key(
            "toss transfer sure frozen real jungle mouse inch smoke derive floor alter ten eagle narrow perfect soap weapon payment chaos amateur height estate absent cabbage"
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
        print(f"Account {self.deployer.address} Funded !!!!")



    def deploy_app(self):

        app_client = HelloWorldClient(
            self.algod_client, creator=self.deployer, indexer_client=self.indexer_client
        )

        app_client.deploy(
            on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
            on_update=algokit_utils.OnUpdate.AppendApp,
        )
        

        print(
            f" APP deployed at :- {app_client.app_id}"
        )
        return app_client , app_client.app_id
    

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
        user_mnemonic,
    ):
        try:
            deployer = algokit_utils.get_account_from_mnemonic(user_mnemonic)

            app_client = HelloWorldClient(
            self.algod_client, creator=deployer, indexer_client=self.indexer_client
        )
            response = app_client.quiz_data(
                student_id=f"{student_id}",
                exam_title=exam_title,
                city=city,
                center_name=center_name,
                booklet=booklet,
                start_time=start_time,
                end_time=end_time,
                que_ans=que_ans,
                suspicious_activity_detected=suspicious_activity_detected,
                wallet_address=deployer.address,
            )

            transaction_id = response.tx_id
            sender_wallet = response.tx_info["txn"]["txn"]["snd"]


            # if "yes" in str(suspicious_activity_detected):

            #     print(f"!!! Malicicous activity Transaction !!!:- https://app.dappflow.org/explorer/transaction/{transaction_id}")
            # else:
                # print(f"Exam Transaction :- https://app.dappflow.org/explorer/transaction/{transaction_id}")
            print(f"Exam Transaction :- https://lora.algokit.io/testnet/transaction/{transaction_id}")
            return transaction_id, sender_wallet
        except Exception as e :
            print("Error writing data to blockchain !!!" , e)
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


    def get_crash_exam_details(self,  application_id):
        """
        This functions checks if software crashed while user was giving exam and returns the question index number
        where the user left the exam.
        """
        try:

            max_index = 0
            # We are picking wallet address and appid from deploy locale file which is imported in this folder
            question_answer_data = {}
            response = self.indexer_client.search_transactions(
                application_id=application_id
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
            if question_answer_data:
                # # IF using sorting on dictonary then we can use pop directly after sorting to get max index
                # question_answer_data_sorted = sorted(question_answer_data.items(), key=lambda item: item[0])
                # max_index = max(question_answer_data, key=lambda item: item[0])
                return question_answer_data
            else:
                return {}
        except Exception as e:
            print("Error in deploy file (testnet)" , e)


    def get_generated_user_details(self):
        return {
                "userID":self.UserID,
                "user_wallet_address" : self.deployer.address,
                "user_private_key" : self.deployer.private_key,
                "user_mnemonic" : self.new_mnemonic,
                "app_id" : self.deployed_app
            }