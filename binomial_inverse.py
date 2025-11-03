import numpy as np
from scipy.stats import binom
from scipy.optimize import brentq

def find_p_from_cumulative(A, n, r):
    """
    Encuentra el valor de p dado:
    A: Probabilidad acumulada izquierda Fb(r|n,p)
    n: Tamaño de muestra
    r: Número de éxitos
    
    Retorna el valor de p tal que P(X <= r) = A
    """
    def equation(p):
        if p <= 0 or p >= 1:
            return np.inf
        return binom.cdf(r, n, p) - A
    
    try:
        # Buscar p en el rango (0.0001, 0.9999)
        p_solution = brentq(equation, 0.0001, 0.9999, xtol=1e-10)
        return p_solution
    except ValueError:
        # Si no encuentra solución en el rango, intentar con límites extendidos
        try:
            p_solution = brentq(equation, 1e-6, 1-1e-6, xtol=1e-10)
            return p_solution
        except:
            return None
