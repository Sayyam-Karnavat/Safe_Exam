import pandas as pd
import pickle

class ModelPredictor:
    def __init__(self):
        # Load all necessary components once during initialization
        self._load_resources()

    def _load_resources(self):
        # Load protocol encoder
        with open("pickle_files/protocol_encoder.pkl", 'rb') as f:
            self.protocol_encoder = pickle.load(f)

        # Load scaler
        with open("pickle_files/scaler.pkl", 'rb') as f:
            self.scaler = pickle.load(f)

        # Load the prediction model
        with open("pickle_files/RCF_model_prediction.pkl", 'rb') as f:
            self.rcf = pickle.load(f)

    def predict(self, data_sent):
        # Create a DataFrame from the data_sent dictionary
        pred_df = pd.DataFrame([data_sent])

        # Define columns to include for predictions
        columns_to_include = ['protocol', 'packet_length', 'flag', 'sequence', 'ack', 'window_size']

        # Reorder DataFrame columns to match the defined order
        pred_df = pred_df[columns_to_include]

        # Encode 'protocol' column using the loaded encoder
        pred_df['protocol'] = pred_df['protocol'].apply(lambda x: self.protocol_encoder[x])

        # Convert DataFrame to integer type
        pred_df = pred_df.astype("int64")

        # Scale 'packet_length' column using the loaded scaler
        pred_df['packet_length'] = self.scaler.transform(pred_df[['packet_length']])

        # Make predictions using the model
        y_pred = self.rcf.predict(pred_df)

        return y_pred[0]

if __name__ == "__main__":
    predictor = ModelPredictor()

    # Perform predictions as needed
    data_sent = {
        'protocol': 'TCP',
        'packet_length': 1500,
        'flag': 1,
        'sequence': 34567,
        'ack': 12345,
        'window_size': 512
    }

    prediction = predictor.predict(data_sent)
    print(prediction)
