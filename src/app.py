
import joblib
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
import math
from pathlib import Path

# =========================================
# 1. CARGA DEL MODELO
# =========================================

MODEL_PATH = Path("../Models/RandomForestModel.joblib")

model_dict = joblib.load(MODEL_PATH)

model = model_dict["modelo"]
features = list(model_dict["variables"])

numero_variables = len(features)

if numero_variables == 0:
    raise ValueError("El modelo no tiene variables registradas.")

# Obtener los nombres de las variables
# y comprobar que coincidan con el entrenamiento.
if hasattr(model, "feature_names_in_"):
    nombre_variables = list(model.feature_names_in_)

    if set(nombre_variables) != set(features):
        raise ValueError(
            "Las variables guardadas no coinciden "
            "con las del modelo entrenado."
        )
else:
    nombre_variables = features.copy()


# =========================================
# 2. FUNCIÓN DE PREDICCIÓN
# =========================================

def predict(*valores):

    if len(valores) != numero_variables:
        raise gr.Error(
            "El número de valores no coincide con "
            "las variables del modelo."
        )

    if any(valor is None for valor in valores):
        raise gr.Error(
            "Completa todos los campos antes de predecir."
        )

    if any(
        not math.isfinite(float(valor))
        for valor in valores
    ):
        raise gr.Error(
            "Introduce únicamente valores numéricos válidos."
        )

    # Construir el DataFrame con los nombres correctos
    data = pd.DataFrame(
        [valores],
        columns=features
    )

    # Respetar el orden utilizado en el entrenamiento
    if hasattr(model, "feature_names_in_"):
        data = data[nombre_variables]

    try:
        prediction = model.predict(data)
        result = float(prediction[0])
    except Exception as error:
        raise gr.Error(
            f"No se pudo realizar la predicción: {error}"
        )

    # Mensaje de resultado
    mensaje = (
        "Predicción calculada correctamente. "
        "El resultado es una estimación del modelo."
    )

    return result, mensaje


# =========================================
# 3. GRÁFICA DE IMPORTANCIA DE VARIABLES
# =========================================

def plot_importance():

    if not hasattr(model, "feature_importances_"):
        return None

    importancia = model.feature_importances_

    df_importancia = pd.DataFrame({
        "Variable": nombre_variables,
        "Importancia": importancia
    }).sort_values(
        "Importancia",
        ascending=True
    )

    fig, ax = plt.subplots(
        figsize=(9, max(4, len(df_importancia) * 0.35))
    )

    ax.barh(
        df_importancia["Variable"],
        df_importancia["Importancia"],
        color="#39805C"
    )

    ax.set_title("Importancia de las variables")
    ax.set_xlabel("Importancia relativa")
    ax.set_ylabel("Variable")
    ax.grid(axis="x", alpha=0.2)

    fig.tight_layout()

    return fig


# =========================================
# 4. ESTILOS VISUALES
# =========================================

css = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

#hero {
    background: linear-gradient(120deg, #173F32, #347653);
    color: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

#hero h1, #hero p {
    color: white;
}

h3 {
    color: #959697
}

#predict-button {
    min-height: 48px;
    font-weight: 600;
}

#result-panel {
    border: 1px solid #39805C;
    border-radius: 14px;
    padding: 16px;
}
"""


# =========================================
# 5. CONSTRUCCIÓN DEL DASHBOARD
# =========================================

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="lime"
    ),
    css=css,
    title="CebaTech | Predicción agrícola"
) as demo:

    with gr.Column(elem_id="hero"):
        gr.Markdown("""
        # 🌾 CebaTech
        ### Plataforma de predicción del rendimiento de cebada

        Sistema de apoyo a la estimación agrícola mediante
        Machine Learning y Random Forest.
        """)

    with gr.Row():

        # PANEL DE ENTRADA
        with gr.Column(scale=6):

            gr.Markdown("## 1. Datos de la parcela")

            gr.Markdown(
                "Introduce los valores de las variables "
                "utilizadas durante el entrenamiento."
            )

            entradas = []

            for nombre in nombre_variables:
                entrada = gr.Number(
                    label=nombre,
                    precision=6,
                    value=None
                )
                entradas.append(entrada)

            with gr.Row():
                boton = gr.Button(
                    "🌱 Calcular predicción",
                    variant="primary",
                    elem_id="predict-button"
                )

                limpiar = gr.Button(
                    "Limpiar campos",
                    variant="secondary"
                )

        # PANEL DE RESULTADOS
        with gr.Column(scale=5, elem_id="result-panel"):

            gr.Markdown("## 2. Resultado")

            gr.Markdown(
                "Rendimiento estimado por el modelo entrenado."
            )

            salida = gr.Number(
                label="Predicción del rendimiento",
                precision=6,
                interactive=False
            )

            estado = gr.Textbox(
                label="Estado de la predicción",
                interactive=False,
                lines=3
            )

            gr.Markdown("""
            **Interpretación:** la predicción corresponde
            a la variable objetivo y a la unidad utilizadas
            al entrenar el modelo.
            """)

    gr.Markdown("---")

    # IMPORTANCIA DE VARIABLES
    with gr.Accordion(
        "📊 Análisis del modelo",
        open=True
    ):

        if hasattr(model, "feature_importances_"):
            gr.Markdown(
                "### Importancia de las variables\n"
                "Muestra la contribución relativa que el "
                "modelo asigna a cada variable."
            )

            grafica = gr.Plot(
                value=plot_importance(),
                label="Importancia de variables"
            )
        else:
            gr.Markdown(
                "Este estimador no expone "
                "`feature_importances_`."
            )

    gr.Markdown("""
    ---
    **Modelo:** Random Forest

    **Aplicación:** Estimación del rendimiento de parcelas de cebada

    **Nota:** las predicciones son estimaciones del modelo.
    Su precisión depende de los datos de entrenamiento y
    de las condiciones de aplicación.
    """)

    # EVENTO DE PREDICCIÓN
    boton.click(
        fn=predict,
        inputs=entradas,
        outputs=[salida, estado]
    )

    # EVENTO PARA LIMPIAR LOS CAMPOS
    limpiar.click(
        fn=lambda: [None] * (numero_variables + 2),
        inputs=[],
        outputs=entradas + [salida, estado]
    )


# =========================================
# 6. EJECUCIÓN
# =========================================

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", 
                server_port=int(os.environ.get("PORT", 10000)))
