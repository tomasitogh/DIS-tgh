import streamlit as st
import numpy as np
import scipy.stats as stats



# Selección del modelo
modelos = [
    "Fisher-Snedecor (F)"
]
def render():
    # Título de la app
    st.title("Probability Distributions - Fisher-Snedecor (F)")
    modelo_seleccionado = st.selectbox("Selecciona un modelo de distribución:", modelos)

    # Función para calcular la probabilidad
    def calcular_probabilidad(modelo, params, x, lado, prob):
        try:
            if modelo == "Fisher-Snedecor (F)":
                df1, df2 = params['df1'], params['df2']
                dist = stats.f(dfn=df1, dfd=df2)
            
            if lado == "Izquierda" and modelo == "Fisher-Snedecor (F)":
                return dist.ppf(prob)
            elif lado == "Derecha" and modelo == "Fisher-Snedecor (F)":
                return dist.ppf(prob)
        except Exception as e:
            return f"Error en cálculo: {e}"

    # Inputs de parámetros según el modelo (usando number_input para entrada manual)
    params = {}
    if modelo_seleccionado == "Fisher-Snedecor (F)":
        params['df1'] = st.number_input("Grados de libertad numerador (df1)", min_value=1, value=5)
        params['df2'] = st.number_input("Grados de libertad denominador (df2)", min_value=1, value=10)
        prob = st.number_input("Probabilidad", min_value=0.000, max_value=1.0, value=0.5, format="%0.6f")

    # Input para x y selección de lado
    x = st.number_input("Valor de x", value=0.0, format="%0.6f")

    lado = st.selectbox("Selecciona el lado de la probabilidad:", ["Izquierda", "Derecha"])

    # Botón para calcular
    if st.button("Calcular Probabilidad"):
        prob = calcular_probabilidad(modelo_seleccionado, params, x, lado, prob)
        if isinstance(prob, str):
            st.error(prob)
        else:
            st.write(f"**Probabilidad {lado.lower()} en x={x}:** {prob:.8f}")
