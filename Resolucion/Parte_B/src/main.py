from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel
import pickle
import pandas as pd
from fastapi.encoders import jsonable_encoder

import os

#Creamos la instancia
app = FastAPI()

path = os.getcwd()
last_part = os.path.basename(path)

print(">>>>>>>>>>>>>>>>> ",last_part)

if (last_part == "final_edvai" or last_part == "src"):
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'modelo_proyecto_final.pkl')
    COLUMNS_PATH = os.path.join(os.path.dirname(__file__), '..','..', '..', 'model', 'categories_ohe_without_fraudulent.pickle')
    BINS_ORDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'saved_bins_order.pickle') 
    BINS_TRANSACTION = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model','saved_bins_transaction.pickle') 
else: 
    MODEL_PATH = "/app/model/modelo_proyecto_final.pkl"
    COLUMNS_PATH = "/app/model/categories_ohe_without_fraudulent.pickle"
    BINS_ORDER = "/app/model/saved_bins_order.pickle"
    BINS_TRANSACTION = "/app/model/saved_bins_transaction.pickle"

#Cargamos el modelo de predicción 
#MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'modelo_proyecto_final.pkl')
with open(MODEL_PATH, 'rb') as f:
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)

#Columnas
#COLUMNS_PATH = os.path.join(os.path.dirname(__file__), '..','..', '..', 'model', 'categories_ohe_without_fraudulent.pickle')
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

#Puntos de corte 'orders'
#BINS_ORDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'saved_bins_order.pickle') 
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

#Puntos de corte 'transactions'
#BINS_TRANSACTION = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model','saved_bins_transaction.pickle') 
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
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7860) #_Se accede con localhost:7860