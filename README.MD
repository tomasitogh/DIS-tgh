# Plataforma de Herramientas Estadísticas

## 📊 Descripción
Plataforma web desarrollada en Streamlit que integra múltiples herramientas estadísticas especializadas.

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

### 3. 🧮 Calculadora CASIO FX-95ES
Calculadora científica con soporte para:
- Operaciones básicas (+, -, ×, ÷)
- Fracciones (1/2, 3/4, etc.)
- Paréntesis y expresiones complejas
- Funciones científicas (sqrt, sin, cos, tan, log, ln)
- Constantes (π, e)
- Historial de cálculos

## 📝 Ejemplo de Uso - Plan de Muestreo

**Caso de prueba:**
- p₀ = 0.05, α = 0.2
- p₁ = 0.07, β = 0.1

**Resultado:**
- n = 638 (tamaño de muestra)
- r = 37 (valor crítico)
- α_real = 0.19925 ≤ 0.2 ✓
- β_real = 0.09997 ≤ 0.1 ✓

## 🔧 Tecnologías
- Python 3.x
- Streamlit
- NumPy
- SciPy

## 📄 Licencia
Proyecto académico - Uso educativo