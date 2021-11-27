from __future__ import division

# Librerías estándar
import timeit

# Importaciones externas
import numpy as np
 
import matplotlib.pyplot as plt  

from sympy import Symbol, symbols,\
    S, sin, cos, tan, log, exp, ln, sqrt,  oo, latex, pprint, init_printing,\
    Integral, Derivative, factor, simplify, sets, solve, expand, cancel, lambdify,\
    solveset, Eq, apart, re, gamma, im, collect, apart, trigsimp, pi, cse, Interval

from sympy.calculus.util import continuous_domain as dominio
from sympy.calculus.util import function_range as rango
from sympy import Rational as Frac

from pylatex import Document, \
    Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command, NoEscape, Package

from pylatex.utils import italic

# Pasa una expresión de sympy a formato latex
def puntos(len, set, doc, tipo):
    with doc.create(Subsection(f"Puntos {tipo} ")):   
        if len <= 0: doc.append(f"No hay puntos {tipo}. ")

        else: 
            i = int(0)        
            doc.append(f"La función tiene puntos {tipo} en: ")
                
            for p_critico in set: 
                doc.append(NoEscape(f"${latex(p_critico)}$" ))
                i += 1
                        
                if i < len: doc.append(", ")
                else: doc.append(". ")         

def main():
    no_hay_rango = False

# Declaración de símbolos
    x, y, l, w, h, d, dy, dx, theta, alpha, R, V = symbols('x y l w h d dy dx \theta \alpha R V', real=True)
   
# Request and input validation
    f = input(f"Inserta la función: \nf = ")
   
    no_es_valido = True
    while no_es_valido:  
        try:
            f = eval(f)
            no_es_valido = False
        except: 
            f = input(f"\nError: Inserta de nuevo la función. \n f = ")

# Counter
    inicio = timeit.default_timer()

# Obtención de dominio y rango: 
    no_hay_rango = bool(False)
    
    dom = dominio(f, x, S.Reals)

    print("dom: ", dom)
    
    try: 
        ran = rango(f, x, S.Reals)
        hay_rango = True    

    except: 
        hay_rango = False

    if hay_rango and dom == ran: 
        ran = dom
    
    elif hay_rango and str(type(ran)) == "<class 'sympy.sets.sets.Interval'>": 
        ran2 = []
        for args in ran.args: 
            ran2.append(cancel(args))
        ran = Interval(ran2[0], ran2[1])
        
# Primera y segunda derivada: 
    f_prime = cancel(trigsimp(Derivative(f, x).doit()))
    print("fprime: ", f_prime)

    f_double_prime = cancel(trigsimp(Derivative(f_prime, x).doit()))
    print("fdoubleprime: ",f_double_prime)

# Máximos y minimos
    max_y_min = solve((f_prime), x)
    print("Puntos críticos: ", max_y_min)
    
    min = []
    max = []

    if len(max_y_min) > 0: 
        for point in max_y_min:
    
            slope = re(f_double_prime.subs(x, point))
            xy = (point, expand(f.subs(x, point)))
            
            if  slope > 0:
                min.append(xy)
            
            elif slope < 0: 
                max.append(xy)
        
# Creación del document's basic layout 
    doc = Document('Article')

    formato = {"tmargin": "0.5in", "lmargin": "1in"}
    doc = Document(geometry_options=formato)
    doc.preamble.append(Command('title', NoEscape('$ \mbox{' + 'Información de ' + '}' + latex(f) + ' $')) )
    doc.preamble.append(Command('author', 'Diego Coglievina Díaz'))
    doc.preamble.append(Command('date', '2021'))
    doc.append(NoEscape(r'\maketitle'))

# Generación del documento
# Dom y ran
    with doc.create(Section("Dominio y rango: ")): 
        dom = "dom \ f = \left\{ x \ | \ x \in " + latex(dom) + '\\right\}'
        doc.append(NoEscape(f" Se determinó que el domino de $f(x)$ está dado por el conjunto: $${dom}$$"))
        
        if hay_rango: 
            ran = " ran \ f = \left\{ y \ | \ y \in " + latex(ran) + '\\right\}'
            doc.append(NoEscape(f"Por otro lado, el rango puede ser descrito con el conjunto: $${ran}$$ "))
        else: 
            doc.append("El rango no pudo determinarse. ")

# Derivadas
    with doc.create(Section("Derivadas: ")):
        d_dx = str(latex(d/dx) + "\left[ " + latex(f) + " \\right]" + " = " + latex(factor(f_prime)))
        d2_dx2 = str(latex(d**2/dx**2) + "\left[ " + latex(f) + " \\right]" + " = " + latex(factor(f_double_prime)))

        doc.append(NoEscape("La primera y segunda derivadas de la función son: "))
        doc.append(NoEscape(f"$${d_dx}$$ $${d2_dx2}$$" ))

# Graficar: 
    
    len_max_y_min = len(max_y_min) 
    try: 
        g = lambdify(x, f, "numpy") 
        y = np.arange(-10, 10, 0.05)
        plt.ylim(-10, 10)
        plt.plot(y, g(y))
        if len(min) > 0: 
            for minimum in min: 
                plt.plot(minimum[0], minimum[1], marker="o", markersize=5, markeredgecolor="red")

        if len(max) > 0: 
            for maximum in max: 
                plt.plot(maximum[0], maximum[1], marker="o", markersize=5, markeredgecolor="red")

        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.grid()
        plt.savefig('fig', dpi=800)

        if len_max_y_min == 0: 
            doc.append(NoEscape(r"\begin{center}"))
            doc.append(NoEscape(r"  \includegraphics[width=0.5\textwidth]{fig.png}"))
            doc.append(NoEscape(r"\end{center}"))
        else: 
            doc.append(NoEscape(r"\begin{wrapfigure}{l}{0.5\textwidth}"))
            doc.append(NoEscape(r"  \includegraphics[width=0.49\textwidth]{fig.png}"))
            doc.append(NoEscape(r"\end{wrapfigure}"))
    except: 
        pass
# Puntos críticos 
    

    if len_max_y_min > 0: 
        with doc.create(Section("Puntos críticos: ")):
            
            if len_max_y_min > 0: 
                i = int(0)
                doc.append("La función tiene puntos críticos en: ")
            
                for p_critico in max_y_min: 
                    doc.append(NoEscape(f"$x={latex(p_critico)}$" ))
                    i += 1
                    
                    if i < len_max_y_min: doc.append(", ")
                    else: doc.append(". ")
                
                puntos(len(min), min, doc, 'mínimos')
                puntos(len(max), max, doc, 'máximos')

# Adición de paquetes para símbolos matemáticos
    doc.packages.append(Package('wrapfig'))
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('graphicx'))
    doc.generate_pdf('proyecto',  clean=True, clean_tex=False)
    final = timeit.default_timer()
    print('Tiempo: ', final - inicio)  

if __name__ == '__main__':
    main()
    