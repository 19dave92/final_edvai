from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import pandas as pd
import pickle
import os
from funpymodeling import status, freq_tbl

#Cargamos el modelo de predicción 
#with open("D:/EDVai/Bootcamp/final_edvai/model/modelo_proyecto_final.pkl", 'rb') as f:
with open("C:/Users/Usuario/Documents/FINAL/final_edvai/model/modelo_proyecto_final.pkl", 'rb') as f:    
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)

#COLUMNS_PATH = "D:/EDVai/Bootcamp/final_edvai/model/categories_ohe_without_fraudulent.pickle"
COLUMNS_PATH = "C:/Users/Usuario/Documents/FINAL/final_edvai/model/categories_ohe_without_fraudulent.pickle"
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

#BINS_ORDER = os.path.join("D:/EDVai/Bootcamp/final_edvai/model/saved_bins_order.pickle")
BINS_ORDER = os.path.join("C:/Users/Usuario/Documents/FINAL/final_edvai/model/saved_bins_order.pickle")
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

#BINS_TRANSACTION = os.path.join("D:/EDVai/Bootcamp/final_edvai/model/saved_bins_transaction.pickle")
BINS_TRANSACTION = os.path.join("C:/Users/Usuario/Documents/FINAL/final_edvai/model/saved_bins_transaction.pickle")
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)

data = {
    "orderAmount" : 18.0,
    "orderState" : "pending",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "card",
    "paymentMethodProvider" : "JCB 16 digit",
    "paymentMethodIssuer" : "Citizens First Banks",
    "transactionAmount" : 18,
    "transactionFailed" : False,
    "emailProvider" : "yahoo",
    "emailDomain" : "com",
    "customerIPAddressSimplified" : "only_letters",
    "sameCity" : "yes"
}

answer_dict = jsonable_encoder(data)

for key, value in answer_dict.items():
        answer_dict[key] = [value]

single_instance = pd.DataFrame.from_dict(answer_dict)

#Convierte la columna en float
single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
#categoriza la variable según 
single_instance["orderAmount"] = pd.cut(single_instance['orderAmount'],
                                    bins=new_saved_bins_order, 
                                    include_lowest=True)

single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
single_instance["transactionAmount"] = pd.cut(single_instance['transactionAmount'],
                                    bins=new_saved_bins_order, 
                                    include_lowest=True)

# One hot encoding
single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)

prediction = model.predict(single_instance_ohe)

type_of_fraud = int(prediction[0])

response = {"Tipo de fraude": type_of_fraud}

print(response)