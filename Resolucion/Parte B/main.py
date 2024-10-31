from fastapi import FastAPI
import uvicorn

#Creamos la instancia
app = FastAPI()


@app.get("/")
def read_root():
    return {"message" : "Proyecto para Bootcamp de EDVAI"}

@app.get("/prediccion")
def predict_fraud_customer():
    return {"message" : "Devuelve la prediccion"}

#Segmento uvicorn
#_Corre en http://127.0.0.1:8000

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000) #prueba local
    #uvicorn.run(app, host='0.0.0.0', port=7860) #produccion