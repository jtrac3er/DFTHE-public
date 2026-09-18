import sympy as sp

def check_derivable(t1_expr, t2_expr, z1_expr, z2_expr, s1_expr=None, s2_expr=None):
    """
    Prüft, ob Z=[z1, z2] aus T=[t1, t2] (und optional S=[s1, s2]) 
    durch punktweise Op (+,-,*,/) und Transposition herleitbar ist.
    """
    # Symbole definieren
    t1, t2 = sp.symbols('t1 t2')
    vars_list = [t1, t2]
    
    if s1_expr is not None:
        s1, s2 = sp.symbols('s1 s2')
        vars_list.extend([s1, s2])

    # Die Ziel-Ausdrücke in SymPy-Objekte umwandeln
    z1 = sp.sympify(z1_expr)
    z2 = sp.sympify(z2_expr)

    # Wir definieren die erlaubten Transformationen der Inputs:
    # Jedes Argument in z1 kann entweder t1, t2, s1 oder s2 sein.
    # Wenn in z1 an einer Stelle x steht, muss in z2 an der 
    # gleichen Stelle der "Partner" y stehen.
    
    # Partner-Mapping:
    # T -> T^T bedeutet: t1 wird zu t2, t2 wird zu t1
    # S -> S^T bedeutet: s1 wird zu s2, s2 wird zu s1
    # Identität: t1 bleibt t1, t2 bleibt t2 (wenn wir nicht transponieren)
    
    # Wir prüfen, ob z2 hervorgeht aus z1, indem wir 
    # t1 <-> t2 und s1 <-> s2 tauschen.
    z1_swapped = z1.subs({t1: t2, t2: t1})
    if s1_expr is not None:
        z1_swapped = z1_swapped.subs({s1: s2, s2: s1})

    # Überprüfung auf algebraische Identität
    if sp.simplify(z1_swapped - z2) == 0:
        return True, "Möglich: z2 ist die transponierte Struktur von z1."
    
    # Spezialfall: Wenn z1 und z2 völlig identisch sind UND keine 
    # Kopplung verletzen (z.B. nur t1+t2 in beiden), ist es auch möglich.
    if sp.simplify(z1 - z2) == 0:
        # Prüfen, ob der Ausdruck selbst-symmetrisch unter Transposition ist
        if sp.simplify(z1 - z1_swapped) == 0:
            return True, "Möglich: Struktur ist symmetrisch."
            
    return False, "Nicht möglich: Unterschiedliche Rechenwege pro Kanal."

# --- TESTFÄLLE ---

# Beispiel 1: T + S^T -> [t1 + s2, t2 + s1]
print(f"Test 1: {check_derivable('t1', 't2', 't1 + s2', 't2 + s1', 's1', 's2')}")

# Beispiel 2: [t1*s1, t2+s2] (Links Multiplikation, rechts Addition)
print(f"Test 2: {check_derivable('t1', 't2', 't1 * s1', 't2 + s2', 's1', 's2')}")

# Beispiel 3: [t1, t1] (Informationen von links nach rechts kopieren ohne Partner)
print(f"Test 3: {check_derivable('t1', 't2', 't1', 't1', 's1', 's2')}")