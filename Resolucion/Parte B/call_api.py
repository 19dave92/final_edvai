import requests

search_api_url = "http://127.0.0.1:8000"

# CASO 1 -> Tipo de fraude: 0/False
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

#Acceder al index / home:
#response = requests.get(url_root)
#print(response.json())

# Llamada al endpoint prediccion
#response = requests.get(search_api_url)
#print(response.json())

response = requests.post(search_api_url)
print(response.json())