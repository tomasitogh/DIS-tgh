# Plataforma de Herramientas Estadísticas

## 📊 Descripción
Plataforma web desarrollada en Streamlit que integra múltiples herramientas estadísticas especializadas para análisis de datos, control de calidad e inferencia estadística.

## 🚀 Cómo ejecutar el proyecto

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## 🛠️ Herramientas Disponibles

### 1. 📈 Distribución Binomial Inversa
Calcula el parámetro **p** de una distribución binomial dada la probabilidad acumulada.

**Funcionalidad:**
- Encuentra p tal que P(X ≤ r) = A
- Inputs: Probabilidad acumulada (A), tamaño de muestra (n), número de éxitos (r)
- Usa algoritmo de búsqueda binaria para alta precisión
- Verifica resultados automáticamente

**Ejemplo:**
- A = 0.95, n = 600, r = 149 → p ≈ 0.2210495

### 2. 🎯 Plan de Muestreo (Bernoulli)
Diseña planes de muestreo óptimos para procesos de Bernoulli.

**Algoritmo Mejorado (v2.0):**
- ✅ Minimiza el tamaño de muestra (n)
- ✅ Maximiza el uso de errores permitidos (α y β)
- ✅ Encuentra la solución más eficiente según criterios estadísticos estándar
- ✅ Coincide con resultados de cálculos manuales expertos

**Verificación:**
- Error Tipo I: α = P(X ≥ r | n, p₀) = 1 - F(r-1 | n, p₀) ≤ α₀
- Error Tipo II: β = P(X < r | n, p₁) = F(r-1 | n, p₁) ≤ β₀

**Ejemplo:**
```
Input:  p₀ = 0.05, α = 0.2, p₁ = 0.07, β = 0.1
Output: n = 638, r = 37
        α_real = 0.19925 ≤ 0.2 ✓
        β_real = 0.09997 ≤ 0.1 ✓
```

### 3. χ² Pruebas de Chi-Cuadrado ⭐ NUEVO
Realiza pruebas de chi-cuadrado con tablas dinámicas y editables.

**Características:**
- 🔄 Tablas dinámicas (2×2 hasta 10×10)
- 📝 Editor interactivo de datos (st.data_editor mejorado)
- 🧮 Cálculos automáticos de totales y frecuencias esperadas
- 📊 Visualización de resultados detallados
- ✅ Decisión estadística automática

**Tipos de Pruebas:**

#### a) Bondad de Ajuste
Verifica si una distribución observada se ajusta a una distribución esperada.
- H₀: Los datos siguen la distribución esperada
- χ² = Σ[(O - E)² / E]
- gl = k - 1 (k = número de categorías)

#### b) Prueba de Consistencia (Homogeneidad)
Verifica si varias poblaciones tienen la misma distribución.
- H₀: Las poblaciones son homogéneas
- χ² = ΣΣ[(O[i,j] - E[i,j])² / E[i,j]]
- gl = (R - 1) × (C - 1)
- E[i,j] = (Total_fila[i] × Total_columna[j]) / Total_general

#### c) Prueba de Independencia
Verifica si dos variables categóricas son independientes.
- H₀: Las variables son independientes
- Misma fórmula que prueba de consistencia
- gl = (R - 1) × (C - 1)

**Ejemplo Práctico:**
```
Tabla 3×3 de contingencia:
         Grupo 1  Grupo 2  Grupo 3
Cat 1      20       30       10
Cat 2      15       25       20
Cat 3      25       15       30

Resultados:
χ²obs = 16.076
χ²crit(0.05, 4) = 9.488
Decisión: Rechazar H₀ (las variables están asociadas)
```

**Mejoras en st.data_editor:**
- ✅ Los datos persisten al editar y presionar Enter
- ✅ Manejo correcto del estado con session_state
- ✅ Reinicio automático al cambiar dimensiones
- ✅ Botón "Limpiar Tabla" para reiniciar manualmente
- ✅ Keys únicos para evitar conflictos

Ver documentación detallada en:
- [GUIA_CHI_CUADRADO.md](GUIA_CHI_CUADRADO.md) - Guía de uso
- [EJEMPLO_CHI_CUADRADO.md](EJEMPLO_CHI_CUADRADO.md) - Ejemplos prácticos
- [CORRECCIONES_DATA_EDITOR.py](CORRECCIONES_DATA_EDITOR.py) - Detalles técnicos

### 4. 🧮 Calculadora CASIO FX-95ES
Calculadora científica con soporte para:
- Operaciones básicas (+, -, ×, ÷)
- Fracciones (1/2, 3/4, etc.)
- Paréntesis y expresiones complejas
- Funciones científicas (sqrt, sin, cos, tan, log, ln)
- Constantes (π, e)
- Historial de cálculos

## 📁 Estructura del Proyecto

```
STREAMLIT_DIS/
├── app.py                          # Aplicación principal
├── binomial_inverse.py             # Distribución binomial inversa
├── sampling_plan.py                # Plan de muestreo
├── chi_square.py                   # Pruebas de chi-cuadrado ⭐
├── calculator.py                   # Calculadora científica
├── requirements.txt                # Dependencias
├── README.MD                       # Este archivo
├── GUIA_CHI_CUADRADO.md           # Guía de uso chi-cuadrado
├── EJEMPLO_CHI_CUADRADO.md        # Ejemplos prácticos
├── CORRECCIONES_DATA_EDITOR.py    # Documentación técnica
└── test_chi_cuadrado.py           # Tests de verificación

```

## 🧪 Testing

### Pruebas de Chi-Cuadrado:
```bash
python test_chi_cuadrado.py
```

Verifica:
- Cálculo correcto de χ² observado
- Frecuencias esperadas
- Grados de libertad
- Tablas de diferentes dimensiones

## 🔧 Tecnologías
- Python 3.x
- Streamlit (framework web)
- NumPy (cálculos numéricos)
- SciPy (distribuciones estadísticas)
- Pandas (manejo de datos)

## 📚 Documentación Adicional

- **test_chi_cuadrado.py**: Script de verificación con 3 casos de prueba
- **GUIA_CHI_CUADRADO.md**: Guía completa de uso con fórmulas y ejemplos
- **EJEMPLO_CHI_CUADRADO.md**: Ejemplos paso a paso con interpretación
- **CORRECCIONES_DATA_EDITOR.py**: Documentación técnica de las correcciones

## 🎯 Casos de Uso

1. **Control de Calidad**: Diseño de planes de muestreo para inspección
2. **Análisis de Datos**: Pruebas de hipótesis chi-cuadrado
3. **Investigación**: Verificar independencia entre variables
4. **Educación**: Herramienta didáctica para aprender estadística
5. **Industria**: Validación de procesos y distribuciones

## 🔄 Historial de Versiones

- **v3.0** (Nov 2024): Agregado módulo de pruebas de chi-cuadrado con tablas editables
- **v2.0** (Nov 2024): Mejorado algoritmo de plan de muestreo
- **v1.0** (Nov 2024): Versión inicial con 3 herramientas

## 📄 Licencia
Proyecto académico - Uso educativo

## 👨‍💻 Autor
Desarrollado para el curso de Diseño de Inferencia Estadística