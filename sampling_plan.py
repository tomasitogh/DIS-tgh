import streamlit as st
import numpy as np
from scipy.stats import binom, norm

def normal_approximation(p0, alpha, p1, beta):
    """Calcular aproximación inicial usando distribución normal"""
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(1 - beta)
    
    numerator = (z_alpha * np.sqrt(p0 * (1 - p0)) + z_beta * np.sqrt(p1 * (1 - p1)))**2
    denominator = (p1 - p0)**2
    
    n_approx = int(np.ceil(numerator / denominator))
    r_approx = int(np.ceil(n_approx * p0 + z_alpha * np.sqrt(n_approx * p0 * (1 - p0))))
    
    return n_approx, r_approx

def find_exact_solution(n_start, r_start, p0, alpha, p1, beta, progress_callback=None):
    """
    Encontrar la solución exacta buscando sistemáticamente desde la aproximación normal
    """
    n = n_start
    max_iterations = 50000
    
    for iteration in range(max_iterations):
        best_r = None
        min_violation = float('inf')
        
        r_min = max(1, int(n * p0 * 0.5))
        r_max = min(n, int(n * p1 * 2))
        
        for r in range(r_min, r_max + 1):
            # Calcular probabilidades
            prob_type1 = 1 - binom.cdf(r - 1, n, p0)
            prob_type2 = binom.cdf(r - 1, n, p1)
            
            violation_alpha = prob_type1 - alpha
            violation_beta = prob_type2 - beta
            
            total_violation = max(0, violation_alpha) + max(0, violation_beta)
            
            if total_violation < min_violation:
                min_violation = total_violation
                best_r = r
                best_probs = (prob_type1, prob_type2)
            
            if prob_type1 <= alpha and prob_type2 <= beta:
                return n, r, prob_type1, prob_type2
        
        n += 1
        
        if progress_callback and iteration % 100 == 0:
            progress = 30 + (iteration / max_iterations) * 60
            progress_callback(min(90, progress))
    
    if best_r is not None:
        return n-1, best_r, best_probs[0], best_probs[1]
    
    return None

def show_sampling_plan():
    st.title("📊 Plan de Muestreo - Procesos de Bernoulli")
    st.markdown("### Caso 1: H₀: p ≤ p₀  vs  H₁: p > p₀")
    
    st.markdown("""
    Esta herramienta calcula el **plan de muestreo óptimo** para pruebas de hipótesis 
    en procesos de Bernoulli, determinando el tamaño de muestra (n) y el valor crítico (r).
    """)
    
    # Parámetros de entrada
    st.markdown("### Parámetros de Entrada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        p0 = st.number_input(
            "p₀ (Probabilidad bajo H₀)",
            min_value=0.0001,
            max_value=0.9999,
            value=0.05,
            step=0.01,
            format="%.4f",
            help="Probabilidad bajo la hipótesis nula"
        )
        
        p1 = st.number_input(
            "p₁ (Probabilidad bajo H₁)",
            min_value=0.0001,
            max_value=0.9999,
            value=0.06,
            step=0.01,
            format="%.4f",
            help="Probabilidad bajo la hipótesis alternativa (debe ser > p₀)"
        )
    
    with col2:
        alpha = st.number_input(
            "α (Nivel de significancia)",
            min_value=0.0001,
            max_value=0.9999,
            value=0.01,
            step=0.01,
            format="%.4f",
            help="Probabilidad de error tipo I"
        )
        
        beta = st.number_input(
            "β (Error tipo II)",
            min_value=0.0001,
            max_value=0.9999,
            value=0.05,
            step=0.01,
            format="%.4f",
            help="Probabilidad de error tipo II"
        )
    
    # Validación
    valid = True
    if p1 <= p0:
        st.error("⚠️ p₁ debe ser mayor que p₀ para el caso 1")
        valid = False
    
    if valid and st.button("Calcular Plan de Muestreo", type="primary"):
        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Aproximación normal
        status_text.text("Calculando aproximación normal...")
        progress_bar.progress(10)
        
        n_approx, r_approx = normal_approximation(p0, alpha, p1, beta)
        
        st.markdown("### Aproximación por Distribución Normal")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("n (aproximado)", f"{n_approx:,}")
        with col2:
            st.metric("r crítico (aproximado)", f"{r_approx:,}")
        
        # Búsqueda exacta
        status_text.text("Buscando valores exactos...")
        progress_bar.progress(30)
        
        def update_progress(value):
            progress_bar.progress(int(value))
        
        result = find_exact_solution(n_approx, r_approx, p0, alpha, p1, beta, update_progress)
        
        progress_bar.progress(100)
        status_text.text("✅ Cálculo completado")
        
        if result:
            n_exact, r_exact, actual_alpha, actual_beta = result
            
            st.markdown("---")
            st.markdown("## 🎯 Plan de Muestreo Óptimo")
            
            # Métricas principales
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "📏 Tamaño de muestra (n)", 
                    f"{n_exact:,}",
                    delta=f"{n_exact - n_approx:,} vs aproximación"
                )
            with col2:
                st.metric(
                    "🎲 Valor crítico (r)", 
                    f"{r_exact:,}",
                    delta=f"{r_exact - r_approx:,} vs aproximación"
                )
            
            # Regla de decisión
            st.markdown("### 📋 Regla de Decisión")
            st.info(
                f"**Se rechazará H₀** si al realizar **{n_exact:,} pruebas** "
                f"se obtienen **{r_exact:,} o más éxitos**."
            )
            
            # Probabilidades de error
            st.markdown("### 📊 Probabilidades de Error")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Error Tipo I (α)",
                    f"{actual_alpha:.10f}",
                    delta=f"{actual_alpha - alpha:.2e}",
                    delta_color="inverse"
                )
                st.caption(f"Objetivo: {alpha}")
                
            with col2:
                st.metric(
                    "Error Tipo II (β)",
                    f"{actual_beta:.10f}",
                    delta=f"{actual_beta - beta:.2e}",
                    delta_color="inverse"
                )
                st.caption(f"Objetivo: {beta}")
            
            # Verificación
            st.markdown("### ✓ Verificación")
            check1 = "✅" if actual_alpha <= alpha else "❌"
            check2 = "✅" if actual_beta <= beta else "❌"
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"{check1} α calculado ≤ α objetivo: **{actual_alpha <= alpha}**")
            with col2:
                st.write(f"{check2} β calculado ≤ β objetivo: **{actual_beta <= beta}**")
            
            # Interpretación
            with st.expander("ℹ️ Interpretación de Resultados"):
                st.markdown(f"""
                **Interpretación del Plan de Muestreo:**
                
                - La probabilidad de **rechazar H₀ cuando es verdadera** (Error Tipo I) es de **{actual_alpha:.6f}**
                - La probabilidad de **no rechazar H₀ cuando p = {p1}** (Error Tipo II) es de **{actual_beta:.6f}**
                - La **potencia de la prueba** es de **{1-actual_beta:.6f}** (probabilidad de detectar p₁ = {p1})
                
                **Aplicación Práctica:**
                
                Para aplicar este plan de muestreo:
                1. Realizar {n_exact:,} pruebas independientes
                2. Contar el número de éxitos obtenidos
                3. Si se obtienen {r_exact:,} o más éxitos → Rechazar H₀ (evidencia de que p > {p0})
                4. Si se obtienen menos de {r_exact:,} éxitos → No rechazar H₀
                """)
        else:
            st.error("❌ No se pudo encontrar una solución válida. Intenta ajustar los parámetros.")
    
    # Ejemplos de uso
    with st.expander("📝 Ejemplo de Uso"):
        st.markdown("""
        **Escenario: Control de Calidad**
        
        Una fábrica quiere detectar si la tasa de defectos ha aumentado:
        
        - **p₀ = 0.05**: Tasa de defectos aceptable (5%)
        - **p₁ = 0.06**: Tasa de defectos que queremos detectar (6%)
        - **α = 0.01**: Nivel de confianza 99% (1% de falsos positivos)
        - **β = 0.05**: Potencia 95% (5% de no detectar el aumento)
        
        El programa calculará:
        - Cuántas muestras inspeccionar (n)
        - Cuántos defectos justifican detener producción (r)
        """)
