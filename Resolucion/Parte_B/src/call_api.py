import requests

#search_api_url = "http://127.0.0.1:8000/prediccion"
#search_api_url = "http://0.0.0.0:7860/prediccion"
search_api_url = "http://localhost:7860/prediccion"


# CASO 1 -> Tipo de fraude: 0/False
data1 = {
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


# CASO 2 -> Tipo de fraude: 1/True
data2 = {
    "orderAmount" : 26.0,
    "orderState" : "fulfilled",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "bitcoin",
    "paymentMethodProvider" : "VISA 16 digit",
    "paymentMethodIssuer" : "Solace Banks",
    "transactionAmount" : 26,
    "transactionFailed" : False,
    "emailProvider" : "yahoo",
    "emailDomain" : "com",
    "customerIPAddressSimplified" : "only_letters",
    "sameCity" : "no"
}

#Acceder al index / home:
#response = requests.get(url_root)
#print(response.json())

# Llamada al endpoint prediccion
#response = requests.get(search_api_url)
#print(response.json())

response = requests.post(search_api_url, json=data2)
print(response.json())