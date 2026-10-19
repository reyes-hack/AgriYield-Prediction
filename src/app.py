import joblib
import pandas as pd
import gradio as gr

#Load Model
model_dict = joblib.load('../Models/RandomForestModel.joblib')
model = model_dict['modelo']
features = model_dict['variables']

#Variables del modelo
numero_variables = len(features)

if hasattr(model, 'feature_names_in_'):
    nombre_variables = list(model.feature_names_in_)

if len(nombre_variables) != numero_variables:
    print('El número de variables no coinicde con el modelo')
    
#Función de predicción
def predict(*valores):
    if len(valores) != numero_variables:
        raise ValueError('Número incorreco de variables')
    
    if any(valor is None for valor in valores):
        raise gr.Error("Completa todos los campos antes de predecir.")
    
    data = pd.DataFrame([valores], cols=features)
    
    prediction = model.predict(data)
    result = float(prediction[0])
    
    return result


#interfac
with gr.Blocks(title="Predicción con Random Forest") as demo:

    gr.Markdown("# Predicción con Random Forest")
    gr.Markdown(
        "Introduce los valores de las variables para "
        "estimar el resultado mediante el modelo entrenado."
    )

    entradas = []

    for nombre in nombre_variables:
        entrada = gr.Number(label=nombre,precision=6)
        entradas.append(entrada)

    boton = gr.Button("Realizar predicción", variant="primary")

    salida = gr.Number(
        label="Valor predicho",
        precision=6
    )

    boton.click(fn=predict, inputs=entradas, outputs=salida)

    gr.Markdown(
        "Nota: la predicción depende de los datos y del "
        "entrenamiento del modelo. No es una garantía del resultado real."
    )

if __name__ == "__main__":
    demo.launch()