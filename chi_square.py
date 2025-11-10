import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2

def show_chi_square():
    """Interfaz principal para pruebas de chi-cuadrado"""
    
    st.title("χ² Pruebas de Chi-Cuadrado")
    st.markdown("---")
    
    # Selector de tipo de prueba
    tipo_prueba = st.selectbox(
        "Selecciona el tipo de prueba:",
        ["Bondad de Ajuste", "Prueba de Consistencia (Homogeneidad)", "Prueba de Independencia"]
    )
    
    st.markdown("---")
    
    if tipo_prueba == "Bondad de Ajuste":
        prueba_bondad_ajuste()
    elif tipo_prueba == "Prueba de Consistencia (Homogeneidad)":
        prueba_consistencia()
    else:
        prueba_independencia()


def prueba_bondad_ajuste():
    """Prueba de bondad de ajuste con tabla editable"""
    
    st.markdown("### Prueba de Bondad de Ajuste")
    st.markdown("""
    Esta prueba verifica si una distribución observada se ajusta a una distribución esperada.
    - **H₀**: Los datos siguen la distribución esperada
    - **H₁**: Los datos no siguen la distribución esperada
    """)
    
    # Parámetros
    col1, col2 = st.columns(2)
    with col1:
        num_categorias = st.number_input(
            "Número de categorías:", 
            min_value=2, 
            max_value=20, 
            value=4, 
            step=1,
            key="bondad_num_cat"
        )
    
    with col2:
        alpha = st.number_input(
            "Nivel de significancia (α):", 
            min_value=0.001, 
            max_value=0.999, 
            value=0.05, 
            step=0.01,
            format="%.3f",
            key="bondad_alpha"
        )
    
    st.markdown("---")
    st.markdown("### Ingresa los datos:")
    
    # Botón para limpiar tabla
    if st.button("🔄 Limpiar Tabla", key="bondad_limpiar"):
        st.session_state.bondad_data = pd.DataFrame({
            'Categoría': [f'Categoría {i+1}' for i in range(num_categorias)],
            'Frecuencia Observada': [0] * num_categorias,
            'Frecuencia Esperada': [0] * num_categorias
        })
        st.rerun()
    
    # Inicializar o reiniciar cuando cambia el tamaño
    if 'bondad_num_cat_prev' not in st.session_state:
        st.session_state.bondad_num_cat_prev = num_categorias
    
    if st.session_state.bondad_num_cat_prev != num_categorias:
        st.session_state.bondad_num_cat_prev = num_categorias
        if 'bondad_data' in st.session_state:
            del st.session_state.bondad_data
    
    # Crear tabla editable solo si no existe
    if 'bondad_data' not in st.session_state:
        st.session_state.bondad_data = pd.DataFrame({
            'Categoría': [f'Categoría {i+1}' for i in range(num_categorias)],
            'Frecuencia Observada': [0] * num_categorias,
            'Frecuencia Esperada': [0] * num_categorias
        })
    
    # Editor de datos - usar directamente el session_state
    edited_df = st.data_editor(
        st.session_state.bondad_data,
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        key="bondad_editor"
    )
    
    # Actualizar el estado solo si hay cambios
    if not edited_df.equals(st.session_state.bondad_data):
        st.session_state.bondad_data = edited_df
    
    # Calcular
    if st.button("Calcular Chi-Cuadrado", type="primary"):
        O = edited_df['Frecuencia Observada'].values
        E = edited_df['Frecuencia Esperada'].values
        
        # Validaciones
        if np.any(E <= 0):
            st.error("⚠️ Las frecuencias esperadas deben ser mayores que 0")
            return
        
        if np.sum(O) == 0:
            st.error("⚠️ Debes ingresar frecuencias observadas")
            return
        
        # Calcular Chi-cuadrado observado
        chi_cuadrado_obs = calcular_chi_cuadrado(O, E)
        
        # Grados de libertad
        gl = num_categorias - 1
        
        # Valor crítico
        chi_critico = chi2.ppf(1 - alpha, gl)
        
        # Mostrar resultados
        mostrar_resultados_bondad(edited_df, O, E, chi_cuadrado_obs, chi_critico, gl, alpha)


def prueba_consistencia():
    """Prueba de consistencia/homogeneidad con tabla dinámica"""
    
    st.markdown("### Prueba de Consistencia (Homogeneidad)")
    st.markdown("""
    Esta prueba verifica si varias poblaciones tienen la misma distribución.
    - **H₀**: Las poblaciones son homogéneas (consistentes)
    - **H₁**: Las poblaciones no son homogéneas
    """)
    
    # Parámetros
    col1, col2, col3 = st.columns(3)
    with col1:
        num_filas = st.number_input(
            "Número de filas (categorías):", 
            min_value=2, 
            max_value=10, 
            value=3, 
            step=1,
            key="consist_num_filas"
        )
    
    with col2:
        num_columnas = st.number_input(
            "Número de columnas (grupos):", 
            min_value=2, 
            max_value=10, 
            value=3, 
            step=1,
            key="consist_num_cols"
        )
    
    with col3:
        alpha = st.number_input(
            "Nivel de significancia (α):", 
            min_value=0.001, 
            max_value=0.999, 
            value=0.05, 
            step=0.01,
            format="%.3f",
            key="consist_alpha"
        )
    
    st.markdown("---")
    st.markdown("### Tabla de Frecuencias Observadas:")
    
    # Botón para limpiar tabla
    if st.button("🔄 Limpiar Tabla", key="consist_limpiar"):
        columnas = [f'Grupo {i+1}' for i in range(num_columnas)]
        filas = [f'Categoría {i+1}' for i in range(num_filas)]
        st.session_state.consistencia_data = pd.DataFrame(
            np.zeros((num_filas, num_columnas), dtype=int),
            columns=columnas,
            index=filas
        )
        st.rerun()
    
    # Detectar cambio de dimensiones y reiniciar
    if 'consist_dims_prev' not in st.session_state:
        st.session_state.consist_dims_prev = (num_filas, num_columnas)
    
    if st.session_state.consist_dims_prev != (num_filas, num_columnas):
        st.session_state.consist_dims_prev = (num_filas, num_columnas)
        if 'consistencia_data' in st.session_state:
            del st.session_state.consistencia_data
        st.info(f"📝 Tabla reiniciada a {num_filas}×{num_columnas}")
    
    # Crear tabla editable solo si no existe
    if 'consistencia_data' not in st.session_state:
        columnas = [f'Grupo {i+1}' for i in range(num_columnas)]
        filas = [f'Categoría {i+1}' for i in range(num_filas)]
        st.session_state.consistencia_data = pd.DataFrame(
            np.zeros((num_filas, num_columnas), dtype=int),
            columns=columnas,
            index=filas
        )
    
    # Editor de datos - usar directamente el session_state
    edited_df = st.data_editor(
        st.session_state.consistencia_data,
        use_container_width=True,
        key="consistencia_editor"
    )
    
    # Actualizar el estado solo si hay cambios
    if not edited_df.equals(st.session_state.consistencia_data):
        st.session_state.consistencia_data = edited_df
    
    # Calcular
    if st.button("Calcular Chi-Cuadrado", type="primary"):
        # Convertir a array numpy
        tabla_obs = edited_df.values
        
        if np.sum(tabla_obs) == 0:
            st.error("⚠️ Debes ingresar datos en la tabla")
            return
        
        # Calcular totales
        totales_fila = tabla_obs.sum(axis=1)
        totales_columna = tabla_obs.sum(axis=0)
        total_general = tabla_obs.sum()
        
        # Calcular frecuencias esperadas
        freq_esperadas = np.zeros_like(tabla_obs, dtype=float)
        for i in range(num_filas):
            for j in range(num_columnas):
                freq_esperadas[i, j] = (totales_fila[i] * totales_columna[j]) / total_general
        
        # Calcular Chi-cuadrado observado
        chi_cuadrado_obs = calcular_chi_cuadrado_tabla(tabla_obs, freq_esperadas)
        
        # Grados de libertad
        gl = (num_filas - 1) * (num_columnas - 1)
        
        # Valor crítico
        chi_critico = chi2.ppf(1 - alpha, gl)
        
        # Mostrar resultados
        mostrar_resultados_tabla(
            edited_df, tabla_obs, freq_esperadas, totales_fila, 
            totales_columna, total_general, chi_cuadrado_obs, 
            chi_critico, gl, alpha, "Consistencia"
        )


def prueba_independencia():
    """Prueba de independencia con tabla dinámica"""
    
    st.markdown("### Prueba de Independencia")
    st.markdown("""
    Esta prueba verifica si dos variables categóricas son independientes.
    - **H₀**: Las variables son independientes
    - **H₁**: Las variables están asociadas (no son independientes)
    """)
    
    # Parámetros
    col1, col2, col3 = st.columns(3)
    with col1:
        num_filas = st.number_input(
            "Número de filas (categorías Variable 1):", 
            min_value=2, 
            max_value=10, 
            value=3, 
            step=1,
            key="indep_num_filas"
        )
    
    with col2:
        num_columnas = st.number_input(
            "Número de columnas (categorías Variable 2):", 
            min_value=2, 
            max_value=10, 
            value=4, 
            step=1,
            key="indep_num_cols"
        )
    
    with col3:
        alpha = st.number_input(
            "Nivel de significancia (α):", 
            min_value=0.001, 
            max_value=0.999, 
            value=0.05, 
            step=0.01,
            format="%.3f",
            key="indep_alpha"
        )
    
    st.markdown("---")
    st.markdown("### Tabla de Contingencia (Frecuencias Observadas):")
    
    # Botón para limpiar tabla
    if st.button("🔄 Limpiar Tabla", key="indep_limpiar"):
        columnas = [f'Variable 2 - Cat {i+1}' for i in range(num_columnas)]
        filas = [f'Variable 1 - Cat {i+1}' for i in range(num_filas)]
        st.session_state.independencia_data = pd.DataFrame(
            np.zeros((num_filas, num_columnas), dtype=int),
            columns=columnas,
            index=filas
        )
        st.rerun()
    
    # Detectar cambio de dimensiones y reiniciar
    if 'indep_dims_prev' not in st.session_state:
        st.session_state.indep_dims_prev = (num_filas, num_columnas)
    
    if st.session_state.indep_dims_prev != (num_filas, num_columnas):
        st.session_state.indep_dims_prev = (num_filas, num_columnas)
        if 'independencia_data' in st.session_state:
            del st.session_state.independencia_data
        st.info(f"📝 Tabla reiniciada a {num_filas}×{num_columnas}")
    
    # Crear tabla editable solo si no existe
    if 'independencia_data' not in st.session_state:
        columnas = [f'Variable 2 - Cat {i+1}' for i in range(num_columnas)]
        filas = [f'Variable 1 - Cat {i+1}' for i in range(num_filas)]
        st.session_state.independencia_data = pd.DataFrame(
            np.zeros((num_filas, num_columnas), dtype=int),
            columns=columnas,
            index=filas
        )
    
    # Editor de datos - usar directamente el session_state
    edited_df = st.data_editor(
        st.session_state.independencia_data,
        use_container_width=True,
        key="independencia_editor"
    )
    
    # Actualizar el estado solo si hay cambios
    if not edited_df.equals(st.session_state.independencia_data):
        st.session_state.independencia_data = edited_df
    
    # Calcular
    if st.button("Calcular Chi-Cuadrado", type="primary"):
        # Convertir a array numpy
        tabla_obs = edited_df.values
        
        if np.sum(tabla_obs) == 0:
            st.error("⚠️ Debes ingresar datos en la tabla")
            return
        
        # Calcular totales
        totales_fila = tabla_obs.sum(axis=1)
        totales_columna = tabla_obs.sum(axis=0)
        total_general = tabla_obs.sum()
        
        # Calcular frecuencias esperadas
        freq_esperadas = np.zeros_like(tabla_obs, dtype=float)
        for i in range(num_filas):
            for j in range(num_columnas):
                freq_esperadas[i, j] = (totales_fila[i] * totales_columna[j]) / total_general
        
        # Calcular Chi-cuadrado observado
        chi_cuadrado_obs = calcular_chi_cuadrado_tabla(tabla_obs, freq_esperadas)
        
        # Grados de libertad
        gl = (num_filas - 1) * (num_columnas - 1)
        
        # Valor crítico
        chi_critico = chi2.ppf(1 - alpha, gl)
        
        # Mostrar resultados
        mostrar_resultados_tabla(
            edited_df, tabla_obs, freq_esperadas, totales_fila, 
            totales_columna, total_general, chi_cuadrado_obs, 
            chi_critico, gl, alpha, "Independencia"
        )


def calcular_chi_cuadrado(O, E):
    """
    Calcula el estadístico chi-cuadrado
    χ² = Σ[(O - E)² / E]
    """
    return np.sum((O - E)**2 / E)


def calcular_chi_cuadrado_tabla(tabla_obs, tabla_esp):
    """
    Calcula el estadístico chi-cuadrado para una tabla de contingencia
    χ² = ΣΣ[(O_ij - E_ij)² / E_ij]
    """
    return np.sum((tabla_obs - tabla_esp)**2 / tabla_esp)


def mostrar_resultados_bondad(df, O, E, chi_obs, chi_crit, gl, alpha):
    """Muestra los resultados de la prueba de bondad de ajuste"""
    
    st.markdown("---")
    st.markdown("### Resultados")
    
    # Tabla de cálculos
    st.markdown("#### Tabla de Cálculos:")
    
    resultados = df.copy()
    resultados['(O - E)'] = O - E
    resultados['(O - E)²'] = (O - E)**2
    resultados['(O - E)² / E'] = (O - E)**2 / E
    
    st.dataframe(resultados, use_container_width=True, hide_index=True)
    
    # Totales
    st.markdown(f"**Total Observado:** {np.sum(O):.0f}")
    st.markdown(f"**Total Esperado:** {np.sum(E):.2f}")
    
    # Resultados principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("χ² Observado", f"{chi_obs:.6f}")
    
    with col2:
        st.metric(f"χ² Crítico (1-{alpha}; {gl} gl)", f"{chi_crit:.6f}")
    
    with col3:
        st.metric("Grados de Libertad", gl)
    
    # Decisión
    st.markdown("---")
    st.markdown("### Decisión:")
    
    if chi_obs > chi_crit:
        st.error(f"❌ **Rechazar H₀**")
        st.markdown(f"Como χ²obs ({chi_obs:.6f}) > χ²crítico ({chi_crit:.6f}), hay evidencia significativa para rechazar la hipótesis nula.")
        st.markdown("**Conclusión:** Los datos NO siguen la distribución esperada.")
    else:
        st.success(f"✅ **No rechazar H₀**")
        st.markdown(f"Como χ²obs ({chi_obs:.6f}) ≤ χ²crítico ({chi_crit:.6f}), no hay evidencia suficiente para rechazar la hipótesis nula.")
        st.markdown("**Conclusión:** Los datos son consistentes con la distribución esperada.")
    
    # P-valor
    p_valor = 1 - chi2.cdf(chi_obs, gl)
    st.markdown(f"**p-valor:** {p_valor:.6f}")


def mostrar_resultados_tabla(df, tabla_obs, tabla_esp, tot_fila, tot_col, 
                             tot_gral, chi_obs, chi_crit, gl, alpha, tipo):
    """Muestra los resultados de pruebas de consistencia e independencia"""
    
    st.markdown("---")
    st.markdown("### Resultados")
    
    # Tabla de frecuencias observadas con totales
    st.markdown("#### Frecuencias Observadas:")
    tabla_obs_display = df.copy()
    tabla_obs_display['Total'] = tot_fila
    tabla_totales_col = pd.DataFrame([np.append(tot_col, tot_gral)], 
                                     columns=list(tabla_obs_display.columns),
                                     index=['Total'])
    tabla_obs_completa = pd.concat([tabla_obs_display, tabla_totales_col])
    st.dataframe(tabla_obs_completa, use_container_width=True)
    
    # Tabla de frecuencias esperadas con totales
    st.markdown("#### Frecuencias Esperadas:")
    tabla_esp_df = pd.DataFrame(tabla_esp, 
                                columns=df.columns, 
                                index=df.index)
    tabla_esp_df['Total'] = tot_fila
    tabla_esp_completa = pd.concat([tabla_esp_df, tabla_totales_col])
    st.dataframe(tabla_esp_completa.style.format("{:.4f}"), use_container_width=True)
    
    # Tabla de contribuciones (O - E)² / E
    st.markdown("#### Contribuciones al Chi-Cuadrado [(O - E)² / E]:")
    contribuciones = (tabla_obs - tabla_esp)**2 / tabla_esp
    contrib_df = pd.DataFrame(contribuciones, 
                             columns=df.columns, 
                             index=df.index)
    st.dataframe(contrib_df.style.format("{:.6f}"), use_container_width=True)
    
    # Resultados principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("χ² Observado", f"{chi_obs:.6f}")
    
    with col2:
        st.metric(f"χ² Crítico (1-{alpha}; {gl} gl)", f"{chi_crit:.6f}")
    
    with col3:
        st.metric("Grados de Libertad", f"{gl}")
    
    st.markdown(f"**Fórmula grados de libertad:** gl = (R - 1) × (C - 1) = ({len(tot_fila)} - 1) × ({len(tot_col)} - 1) = {gl}")
    
    # Decisión
    st.markdown("---")
    st.markdown("### Decisión:")
    
    if chi_obs > chi_crit:
        st.error(f"❌ **Rechazar H₀**")
        st.markdown(f"Como χ²obs ({chi_obs:.6f}) > χ²crítico ({chi_crit:.6f}), hay evidencia significativa para rechazar la hipótesis nula.")
        if tipo == "Consistencia":
            st.markdown("**Conclusión:** Las poblaciones NO son homogéneas (no hay consistencia).")
        else:
            st.markdown("**Conclusión:** Las variables NO son independientes (están asociadas).")
    else:
        st.success(f"✅ **No rechazar H₀**")
        st.markdown(f"Como χ²obs ({chi_obs:.6f}) ≤ χ²crítico ({chi_crit:.6f}), no hay evidencia suficiente para rechazar la hipótesis nula.")
        if tipo == "Consistencia":
            st.markdown("**Conclusión:** Las poblaciones son homogéneas (hay consistencia).")
        else:
            st.markdown("**Conclusión:** No se pudo demostrar que las variables no son independientes (no hay asociación significativa).")
    
    # P-valor
    p_valor = 1 - chi2.cdf(chi_obs, gl)
    st.markdown(f"**p-valor:** {p_valor:.6f}")
