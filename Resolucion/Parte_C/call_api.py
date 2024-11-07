from gradio_client import Client

client = Client("http://127.0.0.1:7860/")

caso_1 = client.predict(
		param_0=18.0,
		param_1="pending",
		param_2="True",
		param_3="card",
		param_4="JCB 16 digit",
		param_5="Citizens First Banks",
		param_6=18,
		param_7="False",
		param_8="yahoo",
		param_9="com",
		param_10="only_letters",
		param_11="yes",
		api_name="/run/prediccion"
)

caso_2 = client.predict(
		param_0=26.0,
		param_1="fullfiled",
		param_2="True",
		param_3="bitcoin",
		param_4="VISA 16 digit",
		param_5="Solace Banks",
		param_6=26,
		param_7="False",
		param_8="yahoo",
		param_9="com",
		param_10="only_letters",
		param_11="no",
		api_name="/run/prediccion"
)
print("Tipo de fraude:", caso_2['label'])