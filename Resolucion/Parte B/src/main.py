from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel
import pickle
import pandas as pd
from fastapi.encoders import jsonable_encoder

import os

#Creamos la instancia
app = FastAPI()

#Cargamos el modelo de predicción 
#with open("../../../model/modelo_proyecto_final.pkl", 'rb') as f:     #Local
with open("../model/modelo_proyecto_final.pkl", 'rb') as f:      #Docker
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)


#COLUMNS_PATH = "../../../model/categories_ohe_without_fraudulent.pickle"    #Local
COLUMNS_PATH = "../model/categories_ohe_without_fraudulent.pickle"    #Docker
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

#BINS_ORDER = os.path.join("../../../model/saved_bins_order.pickle") #Local
BINS_ORDER = os.path.join("../model/saved_bins_order.pickle") #Docker
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

#BINS_TRANSACTION = os.path.join("../../../model/saved_bins_transaction.pickle") #Local
BINS_TRANSACTION = os.path.join("../model/saved_bins_transaction.pickle") #Docker
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)

## Ajustamos lo que tenemos como json a un dataframe

class Answer(BaseModel):
    orderAmount : float
    orderState : str
    paymentMethodRegistrationFailure : str
    paymentMethodType : str
    paymentMethodProvider : str
    paymentMethodIssuer : str
    transactionAmount : int
    transactionFailed : bool
    emailProvider : str
    emailDomain : str
    customerIPAddressSimplified : str
    sameCity : str

@app.get("/")
def read_root():
    return {"message" : "Proyecto para Bootcamp de EDVAI----"}

@app.post("/prediccion")
def predict_fraud_customer(answer: Answer):
    
    answer_dict = jsonable_encoder(answer)

    for key, value in answer_dict.items():
        answer_dict[key] = [value]

    single_instance = pd.DataFrame.from_dict(answer_dict)
    
    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
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
    
    return response

#Segmento uvicorn
#_Corre en http://127.0.0.1:8000

if __name__ == '__main__':
    #uvicorn.run(app, host='127.0.0.1', port=8000) #prueba local
    uvicorn.run(app, host='0.0.0.0', port=7860) #produccion