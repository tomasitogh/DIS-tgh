import streamlit as st
import numpy as np
import scipy.stats as stats



# Selección del modelo
modelos = [
    "Proceso de Bernoulli - Modelo Binomial",
    "Proceso de Poisson - Poisson",
    "Exponencial",
    "Weibull",
    "Gumbel del min",
    "Gumbel del max",
    "Pareto",
    "Normal",
    "Log Normal",
    "Gamma - Poisson",
    "Gamma - Empírica"
]
def render():
    # Título de la app
    st.title("Probability Distributions - Cálculo de Probabilidades")
    modelo_seleccionado = st.selectbox("Selecciona un modelo de distribución:", modelos)

    # Función para calcular la probabilidad
    def calcular_probabilidad(modelo, params, x, lado):
        try:
            if modelo == "Proceso de Bernoulli - Modelo Binomial":
                n, p = params['n'], params['p']
                dist = stats.binom(n, p)
                cdf = dist.cdf(x)
            elif modelo == "Proceso de Poisson - Poisson":
                lam = params['lambda']
                dist = stats.poisson(lam)
                cdf = dist.cdf(x)
            elif modelo == "Exponencial":
                lam = params['lambda']
                dist = stats.expon(scale=1/lam)
                cdf = dist.cdf(x)
            elif modelo == "Weibull":
                k, lam = params['k'], params['lambda']
                dist = stats.weibull_min(c=k, scale=lam)
                cdf = dist.cdf(x)
            elif modelo == "Gumbel del min":
                mu, beta = params['mu'], params['beta']
                dist = stats.gumbel_l(loc=mu, scale=beta)
                cdf = dist.cdf(x)
            elif modelo == "Gumbel del max":
                mu, beta = params['mu'], params['beta']
                dist = stats.gumbel_r(loc=mu, scale=beta)
                cdf = dist.cdf(x)
            elif modelo == "Pareto":
                alpha, xm = params['alpha'], params['xm']
                dist = stats.pareto(b=alpha, scale=xm)
                cdf = dist.cdf(x)
            elif modelo == "Normal":
                mu, sigma = params['mu'], params['sigma']
                dist = stats.norm(loc=mu, scale=sigma)
                cdf = dist.cdf(x)
            elif modelo == "Log Normal":
                mu, sigma = params['mu'], params['sigma']
                dist = stats.lognorm(s=sigma, scale=np.exp(mu))
                cdf = dist.cdf(x)
            elif modelo == "Gamma - Poisson":
                r, p = params['r'], params['p']
                dist = stats.nbinom(n=r, p=p)
                cdf = dist.cdf(x)
            elif modelo == "Gamma - Empírica":
                k, theta = params['k'], params['theta']
                dist = stats.gamma(a=k, scale=theta)
                cdf = dist.cdf(x)
            
            if lado == "Izquierda":
                return cdf
            elif lado == "Derecha":
                return 1 - cdf
        except Exception as e:
            return f"Error en cálculo: {e}"

    # Inputs de parámetros según el modelo (usando number_input para entrada manual)
    params = {}
    if modelo_seleccionado == "Proceso de Bernoulli - Modelo Binomial":
        params['n'] = st.number_input("Número de ensayos (n)", min_value=1, value=10)
        params['p'] = st.number_input("Probabilidad de éxito (p)", min_value=0.000, max_value=1.0, value=0.5, format="%0.6f")
    elif modelo_seleccionado == "Proceso de Poisson - Poisson":
        params['lambda'] = st.number_input("Tasa (λ o x raya)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Exponencial":
        params['lambda'] = st.number_input("Tasa (λ)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Weibull":
        params['k'] = st.number_input(f"Shape (k o  β)", min_value=0.100, value=1.0, format="%0.6f")
        params['lambda'] = st.number_input("Scale (λ o α)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado in ["Gumbel del min", "Gumbel del max"]:
        params['mu'] = st.number_input("Loc (μ o θ)", value=0.000, format="%0.6f")
        params['beta'] = st.number_input("Scale (β)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Pareto":
        params['alpha'] = st.number_input("Shape (α)", min_value=0.100, value=1.0, format="%0.6f")
        params['xm'] = st.number_input("Scale (x_m)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Normal":
        params['mu'] = st.number_input("Media (μ)", value=0.000, format="%0.6f")
        params['sigma'] = st.number_input("Desviación (σ)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Log Normal":
        params['mu'] = st.number_input("Media log (μ)", value=0.000, format="%0.6f")
        params['sigma'] = st.number_input("Desviación log (σ)", min_value=0.100, value=1.0, format="%0.6f")
    elif modelo_seleccionado == "Gamma - Poisson":
        params['r'] = st.number_input("Éxitos (r)", min_value=1, value=5)
        params['p'] = st.number_input("Probabilidad (p)", min_value=0.000, max_value=1.0, value=0.5, format="%0.6f")
    elif modelo_seleccionado == "Gamma - Empírica":
        params['k'] = st.number_input("Shape (k)", min_value=0.100, value=1.0, format="%0.6f")
        params['theta'] = st.number_input("Scale (θ)", min_value=0.100, value=1.0, format="%0.6f")

    # Input para x y selección de lado
    x = st.number_input("Valor de x", value=0.0, format="%0.6f")
    lado = st.selectbox("Selecciona el lado de la probabilidad:", ["Izquierda", "Derecha"])

    # Botón para calcular
    if st.button("Calcular Probabilidad"):
        prob = calcular_probabilidad(modelo_seleccionado, params, x, lado)
        if isinstance(prob, str):
            st.error(prob)
        else:
            st.write(f"**Probabilidad {lado.lower()} en x={x}:** {prob:.8f}")
