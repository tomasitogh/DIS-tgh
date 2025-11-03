import streamlit as st
from fractions import Fraction
import re
import math

def show_calculator():
    st.title("🧮 Calculadora CASIO FX-95ES")
    st.markdown("### Calculadora científica con fracciones y paréntesis")
    
    # Inicializar historial en session state
    if 'calc_history' not in st.session_state:
        st.session_state.calc_history = []
    if 'calc_display' not in st.session_state:
        st.session_state.calc_display = ""
    
    # Display de la calculadora
    st.markdown("### 📟 Pantalla")
    display_value = st.text_input(
        "Expresión:",
        value=st.session_state.calc_display,
        key="calc_input",
        placeholder="Ingresa tu expresión matemática...",
        help="Ejemplos: 1/2 + 3/4, (2+3)*5, sqrt(16), 2^3"
    )
    st.session_state.calc_display = display_value
    
    # Botones de la calculadora
    st.markdown("### 🔢 Teclado")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("7", use_container_width=True):
            st.session_state.calc_display += "7"
            st.rerun()
        if st.button("4", use_container_width=True):
            st.session_state.calc_display += "4"
            st.rerun()
        if st.button("1", use_container_width=True):
            st.session_state.calc_display += "1"
            st.rerun()
        if st.button("0", use_container_width=True):
            st.session_state.calc_display += "0"
            st.rerun()
    
    with col2:
        if st.button("8", use_container_width=True):
            st.session_state.calc_display += "8"
            st.rerun()
        if st.button("5", use_container_width=True):
            st.session_state.calc_display += "5"
            st.rerun()
        if st.button("2", use_container_width=True):
            st.session_state.calc_display += "2"
            st.rerun()
        if st.button(".", use_container_width=True):
            st.session_state.calc_display += "."
            st.rerun()
    
    with col3:
        if st.button("9", use_container_width=True):
            st.session_state.calc_display += "9"
            st.rerun()
        if st.button("6", use_container_width=True):
            st.session_state.calc_display += "6"
            st.rerun()
        if st.button("3", use_container_width=True):
            st.session_state.calc_display += "3"
            st.rerun()
        if st.button("(", use_container_width=True):
            st.session_state.calc_display += "("
            st.rerun()
    
    with col4:
        if st.button("+", use_container_width=True):
            st.session_state.calc_display += "+"
            st.rerun()
        if st.button("-", use_container_width=True):
            st.session_state.calc_display += "-"
            st.rerun()
        if st.button("×", use_container_width=True):
            st.session_state.calc_display += "*"
            st.rerun()
        if st.button("÷", use_container_width=True):
            st.session_state.calc_display += "/"
            st.rerun()
    
    with col5:
        if st.button(")", use_container_width=True):
            st.session_state.calc_display += ")"
            st.rerun()
        if st.button("^", use_container_width=True):
            st.session_state.calc_display += "**"
            st.rerun()
        if st.button("⌫ DEL", use_container_width=True):
            st.session_state.calc_display = st.session_state.calc_display[:-1]
            st.rerun()
        if st.button("C", use_container_width=True, type="secondary"):
            st.session_state.calc_display = ""
            st.rerun()
    
    # Funciones científicas
    st.markdown("### 🔬 Funciones Científicas")
    col_fn1, col_fn2, col_fn3, col_fn4 = st.columns(4)
    
    with col_fn1:
        if st.button("√ (sqrt)", use_container_width=True):
            st.session_state.calc_display += "sqrt("
            st.rerun()
    
    with col_fn2:
        if st.button("sin", use_container_width=True):
            st.session_state.calc_display += "sin("
            st.rerun()
    
    with col_fn3:
        if st.button("cos", use_container_width=True):
            st.session_state.calc_display += "cos("
            st.rerun()
    
    with col_fn4:
        if st.button("tan", use_container_width=True):
            st.session_state.calc_display += "tan("
            st.rerun()
    
    col_fn5, col_fn6, col_fn7, col_fn8 = st.columns(4)
    
    with col_fn5:
        if st.button("log", use_container_width=True):
            st.session_state.calc_display += "log("
            st.rerun()
    
    with col_fn6:
        if st.button("ln", use_container_width=True):
            st.session_state.calc_display += "ln("
            st.rerun()
    
    with col_fn7:
        if st.button("π", use_container_width=True):
            st.session_state.calc_display += "pi"
            st.rerun()
    
    with col_fn8:
        if st.button("e", use_container_width=True):
            st.session_state.calc_display += "e"
            st.rerun()
    
    # Botón de cálculo
    st.markdown("---")
    col_calc1, col_calc2 = st.columns([3, 1])
    
    with col_calc1:
        if st.button("🟰 CALCULAR", use_container_width=True, type="primary"):
            if st.session_state.calc_display:
                try:
                    result = evaluate_expression(st.session_state.calc_display)
                    st.session_state.calc_history.insert(0, {
                        'expression': st.session_state.calc_display,
                        'result': result
                    })
                    # Mantener solo los últimos 10 cálculos
                    if len(st.session_state.calc_history) > 10:
                        st.session_state.calc_history = st.session_state.calc_history[:10]
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error en el cálculo: {str(e)}")
    
    with col_calc2:
        if st.button("🗑️ Borrar Todo", use_container_width=True):
            st.session_state.calc_display = ""
            st.session_state.calc_history = []
            st.rerun()
    
    # Mostrar resultado y historial
    if st.session_state.calc_history:
        st.markdown("### 📊 Resultado Actual")
        latest = st.session_state.calc_history[0]
        
        col_res1, col_res2 = st.columns([1, 1])
        with col_res1:
            st.info(f"**Expresión:** `{latest['expression']}`")
        with col_res2:
            st.success(f"**Resultado:** `{latest['result']}`")
        
        # Historial
        if len(st.session_state.calc_history) > 1:
            with st.expander("📜 Ver Historial de Cálculos"):
                for i, calc in enumerate(st.session_state.calc_history[1:], 1):
                    st.text(f"{i}. {calc['expression']} = {calc['result']}")
    
    # Instrucciones
    with st.expander("ℹ️ Instrucciones de Uso"):
        st.markdown("""
        **Operaciones básicas:**
        - Suma: `+`
        - Resta: `-`
        - Multiplicación: `*` o `×`
        - División: `/` o `÷`
        - Potencia: `^` o `**`
        
        **Fracciones:**
        - Escribe fracciones como: `1/2`, `3/4`, etc.
        - Ejemplo: `1/2 + 3/4 = 1.25` o `5/4`
        
        **Paréntesis:**
        - Usa paréntesis para agrupar: `(2+3)*5`
        
        **Funciones científicas:**
        - Raíz cuadrada: `sqrt(16)` → 4
        - Seno: `sin(30)` (en grados)
        - Coseno: `cos(60)`
        - Tangente: `tan(45)`
        - Logaritmo base 10: `log(100)` → 2
        - Logaritmo natural: `ln(e)` → 1
        - Pi: `pi` → 3.14159...
        - Número e: `e` → 2.71828...
        
        **Ejemplos:**
        - `1/2 + 3/4` → 1.25
        - `(2+3)*(4-1)` → 15
        - `sqrt(16) + 2^3` → 12
        - `sin(30) + cos(60)` → 1.0
        """)


def evaluate_expression(expr):
    """Evalúa una expresión matemática con soporte para fracciones"""
    # Limpiar y preparar la expresión
    expr = expr.strip()
    
    # Reemplazar operadores visuales
    expr = expr.replace('×', '*')
    expr = expr.replace('÷', '/')
    expr = expr.replace('^', '**')
    
    # Reemplazar funciones
    expr = expr.replace('sqrt', 'math.sqrt')
    expr = expr.replace('sin', 'math.sin')
    expr = expr.replace('cos', 'math.cos')
    expr = expr.replace('tan', 'math.tan')
    expr = expr.replace('log', 'math.log10')
    expr = expr.replace('ln', 'math.log')
    expr = expr.replace('pi', 'math.pi')
    
    # Reemplazar 'e' solo si no es parte de otra palabra
    expr = re.sub(r'\be\b', 'math.e', expr)
    
    # Convertir ángulos de grados a radianes para funciones trigonométricas
    expr = re.sub(r'math\.(sin|cos|tan)\(([^)]+)\)', 
                  lambda m: f'math.{m.group(1)}(math.radians({m.group(2)}))', expr)
    
    try:
        # Evaluar la expresión
        result = eval(expr, {"__builtins__": {}}, {"math": math, "Fraction": Fraction})
        
        # Formatear el resultado
        if isinstance(result, (int, float)):
            # Si es un número entero, mostrarlo sin decimales
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            # Si es un float, formatearlo con precisión razonable
            elif isinstance(result, float):
                # Intentar expresar como fracción si es simple
                frac = Fraction(result).limit_denominator(1000)
                if abs(float(frac) - result) < 1e-10:
                    return f"{result:.10g} (≈ {frac.numerator}/{frac.denominator})"
                return f"{result:.10g}"
            return str(result)
        else:
            return str(result)
    except Exception as e:
        raise ValueError(f"Expresión inválida: {str(e)}")
