import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Plataforma Estadística",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.sidebar.title("📊 Plataforma Estadística")
st.sidebar.markdown("---")

# Menú de navegación
st.sidebar.markdown("### Herramientas Disponibles")

menu_options = {
    "🏠 Inicio": "home",
    "📈 Distribución Binomial Inversa": "binomial",
    "🎯 Plan de Muestreo (Bernoulli)": "sampling",
    "χ² Pruebas de Chi-Cuadrado": "chi_square",
    "⍺ Probability Distribution":"distributions"
}

# Selector de página
selection = st.sidebar.radio(
    "Selecciona una herramienta:",
    list(menu_options.keys()),
    label_visibility="collapsed"
)

selected_page = menu_options[selection]

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Acerca de")
st.sidebar.info("""
**Plataforma Estadística**

Conjunto de herramientas para:
- Cálculos de distribución binomial
- Diseño de planes de muestreo
- Inferencia estadística
""")

# Renderizar la página seleccionada
if selected_page == "home":
    st.title("🏠 Plataforma de Herramientas Estadísticas")
    st.markdown("---")
    
    st.markdown("""
    ### Bienvenido a la Plataforma Estadística
    
    Esta plataforma integra múltiples herramientas estadísticas para facilitar 
    cálculos y análisis en procesos de control de calidad e inferencia estadística.
    """)
    
    # Tarjetas de herramientas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📈 Distribución Binomial Inversa
        
        Calcula el parámetro **p** de una distribución binomial dado:
        - Probabilidad acumulada izquierda (A)
        - Tamaño de muestra (n)
        - Número de éxitos (r)
        
        **Casos de uso:**
        - Análisis retrospectivo de datos
        - Estimación de parámetros poblacionales
        - Calibración de modelos estadísticos
        """)
        
        if st.button("➡️ Ir a Distribución Binomial Inversa", key="btn_binomial"):
            st.session_state.page = "binomial"
            st.rerun()
    
    with col2:
        st.markdown("""
        #### 🎯 Plan de Muestreo (Bernoulli)
        
        Diseña planes de muestreo óptimos para procesos de Bernoulli:
        - Determina tamaño de muestra (n)
        - Calcula valor crítico (r)
        - Controla errores Tipo I y Tipo II
        
        **Casos de uso:**
        - Control de calidad en manufactura
        - Diseño de experimentos
        - Pruebas de hipótesis estadísticas
        """)
        
        if st.button("➡️ Ir a Plan de Muestreo", key="btn_sampling"):
            st.session_state.page = "sampling"
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        #### χ² Pruebas de Chi-Cuadrado
        
        Realiza pruebas de chi-cuadrado con tablas dinámicas:
        - Bondad de ajuste
        - Prueba de consistencia (homogeneidad)
        - Prueba de independencia
        
        **Casos de uso:**
        - Verificar distribuciones teóricas
        - Comparar poblaciones
        - Analizar asociaciones entre variables
        """)
        
        if st.button("➡️ Ir a Pruebas Chi-Cuadrado", key="btn_chi"):
            st.session_state.page = "chi_square"
            st.rerun()
    
    st.markdown("---")
    
    # Sección de características
    st.markdown("### ✨ Características de la Plataforma")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Precisión**
        - Algoritmos optimizados
        - Alta precisión numérica
        - Validación de resultados
        """)
    
    with col2:
        st.markdown("""
        **⚡ Rapidez**
        - Cálculos eficientes
        - Interfaz responsiva
        - Resultados inmediatos
        """)
    
    with col3:
        st.markdown("""
        **📊 Visualización**
        - Resultados claros
        - Gráficos interactivos
        - Interpretación detallada
        """)
    
    st.markdown("---")
    st.caption("Desarrollado con Streamlit, NumPy y SciPy")

elif selected_page == "binomial":
    # Importar y ejecutar la app de binomial inversa
    from binomial_inverse import find_p_from_cumulative
    
    st.title("📈 Calculadora de Distribución Binomial Inversa")
    st.markdown("### Encuentra el parámetro *p* dada la probabilidad acumulada")
    
    st.markdown("""
    Esta aplicación calcula el valor de **p** en una distribución binomial dado:
    - **A**: Probabilidad acumulada izquierda F_b(r|n,p) = P(X ≤ r)
    - **n**: Tamaño de muestra
    - **r**: Número de éxitos
    """)
    
    # Crear columnas para los inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        A = st.number_input(
            "Probabilidad Acumulada (A)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.95,
            step=0.01,
            format="%.4f",
            help="Probabilidad acumulada izquierda P(X ≤ r)"
        )
    
    with col2:
        n = st.number_input(
            "Tamaño de muestra (n)", 
            min_value=1, 
            value=600,
            step=1,
            help="Número de ensayos"
        )
    
    with col3:
        r = st.number_input(
            "Número de éxitos (r)", 
            min_value=0, 
            value=149,
            step=1,
            help="Número de éxitos observados"
        )
    
    # Validación
    if r > n:
        st.error("⚠️ El número de éxitos (r) no puede ser mayor que el tamaño de muestra (n)")
    else:
        if st.button("Calcular p", type="primary"):
            from scipy.stats import binom
            
            with st.spinner("Calculando..."):
                p_result = find_p_from_cumulative(A, n, r)
                
                if p_result is not None:
                    st.success("✅ Cálculo completado")
                    
                    # Mostrar resultado principal
                    st.markdown("### Resultado")
                    st.metric(label="Valor de p", value=f"{p_result:.10f}")
                    
                    # Verificación
                    prob_verificacion = binom.cdf(r, n, p_result)
                    st.markdown("### Verificación")
                    st.info(f"P(X ≤ {r}) con n={n} y p={p_result:.10f} = **{prob_verificacion:.10f}**")
                    
                    error = abs(prob_verificacion - A)
                    st.caption(f"Error: {error:.2e}")
                    
                    # Información adicional
                    import numpy as np
                    with st.expander("ℹ️ Información adicional"):
                        st.write(f"**Media esperada (np):** {n * p_result:.2f}")
                        st.write(f"**Desviación estándar:** {np.sqrt(n * p_result * (1 - p_result)):.2f}")
                        st.write(f"**Varianza:** {n * p_result * (1 - p_result):.2f}")
                else:
                    st.error("❌ No se pudo encontrar una solución. Verifica los valores ingresados.")
    
    # Ejemplos
    with st.expander("📝 Ver ejemplos de uso"):
        st.markdown("""
        **Ejemplo 1:**
        - A = 0.95, n = 600, r = 149 → p ≈ 0.2210495
        
        **Ejemplo 2:**
        - A = 0.05, n = 600, r = 150 → p ≈ 0.2807915
        
        **Ejemplo 3:**
        - A = 0.975, n = 20, r = 1 → p ≈ 1.234818
        """)

elif selected_page == "sampling":
    # Importar y ejecutar la app de plan de muestreo
    from sampling_plan import show_sampling_plan
    show_sampling_plan()

elif selected_page == "chi_square":
    # Importar y ejecutar las pruebas de chi-cuadrado
    from chi_square import show_chi_square
    show_chi_square()

elif selected_page == "distributions":
    from prob_distribution import render
    render()
