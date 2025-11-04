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
    Encontrar la solución óptima que minimiza n y maximiza el uso de α y β permitidos.
    
    El algoritmo busca el par (n, r) que:
    1. Cumple las restricciones: α_real <= α y β_real <= β
    2. Minimiza n (menor tamaño de muestra)
    3. Maximiza α_real y β_real (estar lo más cerca posible de los límites permitidos)
    """
    # Buscar en un rango razonable alrededor de la aproximación normal
    # Reducimos el rango para hacerlo más eficiente
    n_min = max(10, int(n_start * 0.85))
    n_max = int(n_start * 1.15)
    
    best_solution = None
    best_score = float('inf')
    
    total_iterations = n_max - n_min
    
    # Buscar de menor a mayor n para encontrar el mínimo primero
    for idx, n in enumerate(range(n_min, n_max + 1)):
        # Actualizar progreso
        if progress_callback and idx % 5 == 0:
            progress = 30 + (idx / total_iterations) * 60
            progress_callback(min(90, progress))
        
        # Rango de búsqueda para r (optimizado)
        r_min = max(1, int(n * p0 * 0.6))
        r_max = min(n, int(n * p1 * 1.8))
        
        found_valid = False
        
        for r in range(r_min, r_max + 1):
            # Calcular probabilidades de error
            # Error tipo I: P(rechazar H0 | H0 es cierto) = P(X >= r | p0)
            prob_type1 = 1 - binom.cdf(r - 1, n, p0)
            # Error tipo II: P(no rechazar H0 | H1 es cierto) = P(X < r | p1)
            prob_type2 = binom.cdf(r - 1, n, p1)
            
            # Verificar que cumple las restricciones
            if prob_type1 <= alpha and prob_type2 <= beta:
                found_valid = True
                # Calcular score: queremos minimizar n y maximizar cercanía a límites
                # Penalizar fuertemente n más grande
                # Recompensar estar cerca de los límites de α y β
                score = (
                    n * 1000 +  # Penalización por tamaño de muestra (factor dominante)
                    (alpha - prob_type1)**2 * 1000 +  # Queremos α cercano al límite
                    (beta - prob_type2)**2 * 1000     # Queremos β cercano al límite
                )
                
                if score < best_score:
                    best_score = score
                    best_solution = (n, r, prob_type1, prob_type2)
        
        # Si ya encontramos una solución válida y el siguiente n sería peor,
        # podemos terminar (optimización)
        if found_valid and best_solution and n > best_solution[0] + 5:
            break
    
    return best_solution

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
            
            # Fórmulas exactas con G y F binomial
            st.markdown("### 📐 Valores Exactos Calculados")
            st.info(f"""
**Fórmulas con los valores óptimos encontrados:**

• **Gᵦ(rc={r_exact}, n={n_exact}, p₀={p0})** = {actual_alpha:.10f}  
• **Fᵦ(rc={r_exact-1}, n={n_exact}, p₁={p1})** = {actual_beta:.10f}

Donde:
- **Gᵦ** = 1 - Fᵦ(r | n, p) = P(X > r) = Probabilidad de rechazar H₀
- **Fᵦ** = P(X ≤ r) = Función de distribución acumulada binomial
            """)
            
            # Verificación
            st.markdown("### ✓ Verificación")
            
            # Verificación usando G y F binomial (notación del profesor)
            G_binomial = 1 - binom.cdf(r_exact, n_exact, p0)
            F_binomial = binom.cdf(r_exact - 1, n_exact, p1)
            
            col1, col2 = st.columns(2)
            with col1:
                check1 = "✅" if actual_alpha <= alpha else "❌"
                st.write(f"{check1} α calculado ≤ α objetivo: **{actual_alpha <= alpha}**")
                st.caption(f"P(X ≥ r | n, p₀) = 1 - F(r-1 | n, p₀) ≤ α")
            with col2:
                check2 = "✅" if actual_beta <= beta else "❌"
                st.write(f"{check2} β calculado ≤ β objetivo: **{actual_beta <= beta}**")
                st.caption(f"P(X < r | n, p₁) = F(r-1 | n, p₁) ≤ β")
            
            # Información adicional con notación G y F
            with st.expander("📐 Verificación Detallada (Notación G y F Binomial)"):
                st.markdown(f"""
                **Notación:**
                - **F(k | n, p)** = P(X ≤ k) = Función de distribución acumulada
                - **G(k | n, p)** = P(X > k) = 1 - F(k | n, p) = Función de supervivencia
                
                **Condiciones que debe cumplir el plan de muestreo:**
                
                1. **Error Tipo I (α):**
                   - α = P(rechazar H₀ | H₀ es cierto) = P(X ≥ r | n, p₀)
                   - α = 1 - P(X ≤ r-1 | n, p₀) = 1 - F(r-1 | n, p₀)
                   - α = {actual_alpha:.10f} ≤ {alpha} ✓
                
                2. **Error Tipo II (β):**
                   - β = P(no rechazar H₀ | H₁ es cierto) = P(X < r | n, p₁)
                   - β = P(X ≤ r-1 | n, p₁) = F(r-1 | n, p₁)
                   - β = {actual_beta:.10f} ≤ {beta} ✓
                
                **Usando notación alternativa:**
                - G({r_exact} | {n_exact}, {p0}) = P(X > {r_exact}) = {G_binomial:.10f}
                - F({r_exact-1} | {n_exact}, {p1}) = P(X ≤ {r_exact-1}) = {F_binomial:.10f}
                
                **Nota:** El algoritmo busca minimizar n mientras se mantiene lo más cerca
                posible de los límites permitidos de α y β, aprovechando al máximo los
                errores permitidos para obtener el plan de muestreo más eficiente.
                """)
            
            
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
