import requests

search_api_url = "http://127.0.0.1:8000/predict"

# CASO 1 -> Tipo de fraude: 0/False
data = {
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

response = requests.post(search_api_url, json=data)
print(response.json())