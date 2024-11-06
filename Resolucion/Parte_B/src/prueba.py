import os
import pickle

path = os.getcwd()
last_part = os.path.basename(path)

print(">>>>>>>>>>>>>>>>> ",last_part)

if (last_part != "final_edvai"):
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'modelo_proyecto_final.pkl')
    COLUMNS_PATH = os.path.join(os.path.dirname(__file__), '..','..', '..', 'model', 'categories_ohe_without_fraudulent.pickle')
    BINS_ORDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model', 'saved_bins_order.pickle') 
    BINS_TRANSACTION = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'model','saved_bins_transaction.pickle') 
else:
    MODEL_PATH = "/app/model/modelo_proyecto_final.pkl"
    COLUMNS_PATH = "/app/model/categories_ohe_without_fraudulent.pickle"
    BINS_ORDER = "/app/model/saved_bins_order.pickle"
    BINS_TRANSACTION = "/app/model/saved_bins_transaction.pickle"




with open(MODEL_PATH, 'rb') as f:
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)