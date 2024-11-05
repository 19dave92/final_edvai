import gradio as gr
import pickle
import os
import pandas as pd



#Cargamos el modelo de predicción 
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'modelo_proyecto_final.pkl')
with open(MODEL_PATH, 'rb') as f:
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)

#Columnas
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'categories_ohe_without_fraudulent.pickle')
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

#Puntos de corte 'orders'
BINS_ORDER = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'saved_bins_order.pickle') 
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

#Puntos de corte 'transactions'
BINS_TRANSACTION = os.path.join(os.path.dirname(__file__), '..', '..', 'model','saved_bins_transaction.pickle') 
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)

#Mapeamos las variables del data frame en una lista
PARAMS_NAME=[
    "orderAmount",
    "orderState",
    "paymentMethodRegistrationFailure",
    "paymentMethodType",
    "paymentMethodProvider",
    "paymentMethodIssuer",
    "transactionAmount",
    "transactionFailed",
    "emailProvider",
    "emailDomain",
    "customerIpAddress",
    "sameCity"
]

def predict(*args):
    
    #Creamos un diccionario que contendra las KEY=PARAMS_NAME y los VALUE seran todos
    #los parametros seteados por el usuario en el frontend
    answer_dict = {}

    #Llenamos el diccionario.
    for i in range(len(PARAMS_NAME)):
        answer_dict[PARAMS_NAME[i]]=[args[i]]

    #Obtenemos un pandas dataframe a partir del diccionario
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

    # Cast numpy.int64 to just a int
    type_of_fraud = int(prediction[0])

    # Adaptación respuesta
    #response = "Error parsing value"
    if type_of_fraud == 0:
        response = "False"
    if type_of_fraud == 1:
        response = "True"
    if type_of_fraud == 2:
        response = "Warning"

    return response

    ####################__Comienzo Front End

with gr.Blocks() as demo:

    with gr.Row():

        with gr.Column():

            gr.Markdown("## Predecir si un cliente es fraudulento o no.")

            orderAmount = gr.Slider(label="Order Amount",
                                    minimum=10,
                                    maximum=353,
                                    step=1,
                                    randomize=True
                                    )
            
            orderState = gr.Radio(label="Order State",
                                  choices=["failed","fullfiled","pending"],
                                  value="failed"
                                  )
            
            paymentMethodRegistrationFailure = gr.Radio(label="Payment method registration failure",
                                                        choices=["True","False"],
                                                        value="True"
                                                        )
            
            paymentMethodType = gr.Radio(label="Payment Method Type",
                                         choices=["apple pay","bitcoin","card","paypal"],
                                         value="apple pay"
                                         )
            
            paymentMethodProvider = gr.Dropdown(label="Payment Method Provider",
                                                choices=[
                                                    "American Express",
                                                    "Diners Club / Carte Blanche",
                                                    "Discover",
                                                    "JCB 15 digit",
                                                    "JCB 16 digit",
                                                    "Maestro",
                                                    "Mastercard",
                                                    "VISA 13 digit",
                                                    "VISA 16 digit",
                                                    "Voyager",
                                                ],
                                                multiselect=False,
                                                value="American Express"
                                                )
            
            
            paymentMethodIssuer = gr.Dropdown(label="Payment Method Issuer",
                                                choices=[
                                                    "Bastion Banks",
                                                    "Bulwark Trust Corp.",
                                                    "Citizens First Banks",
                                                    "Fountain Financial Inc.",
                                                    "Grand Credit Corporation",
                                                    "Her Majesty Trust",
                                                    "His Majesty Bank Corp.",
                                                    "Rose Bancshares",
                                                    "Solace Banks",
                                                    "Vertex Bancorp",
                                                    "weird",
                                                ],
                                                multiselect=False,
                                                value="Bastion Banks"
                                                )
            
            transactionAmount = gr.Slider(label="Transaction amount",
                                    minimum=10,
                                    maximum=353,
                                    step=1,
                                    randomize=True
                                    )
            
            transactionFailed = gr.Radio(label="Transaction failed",
                                         choices=["True", "False"],
                                         value="False"
                                         )
            
            emailProvider = gr.Radio(label="Email provider",
                                         choices=["gmail","hotmail","yahoo","weird","other"],
                                         value="gmail"
                                         )
            
            emailDomain = gr.Radio(label="Email domain",
                                         choices=["biz","com","info","net","org","weird"],
                                         value="com"
                                         )
            
            customerIpAddress = gr.Radio(label="Customer IP Address",
                                         choices=["digits_and_letters","only_letters"],
                                         value="only_letters"
                                         )
            
            sameCity = gr.Radio(label="Same city \n(Representa si la compra y el envio corresponden a la misma ciudad)",
                                         choices=["no","yes","unknown"],
                                         value="unknown"
                                         )
            
        with gr.Column():

            gr.Markdown("## Predicción")

            label = gr.Label(label="Tipo de fraude")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
                predict,
                inputs=[
                    orderAmount,
                    orderState,
                    paymentMethodRegistrationFailure,
                    paymentMethodType,
                    paymentMethodProvider,
                    paymentMethodIssuer,
                    transactionAmount,
                    transactionFailed,
                    emailProvider,
                    emailDomain,
                    customerIpAddress,
                    sameCity,
                ],
                outputs=[label],
                api_name="prediccion"
            )

    gr.Markdown(
        """
        <p style='text-align: center'> 
            Desarrollado por <a href='https://www.linkedin.com/in/david-espejo-/ target='_blank'>David Espejo</a>        
        </p>
        """
    )


demo.launch()