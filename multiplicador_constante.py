import streamlit as st
import pandas as pd

# Configuración para pantalla completa
st.set_page_config(layout="wide")

# Función para realizar las operaciones
def multiplicador_constante(constante, semilla1, iteraciones):
    # Lista para almacenar los resultados
    resultados = []
    
    for i in range(iteraciones):
        # Calcula el producto de la semilla
        producto = semilla1 * constante
        longitud = len(str(producto))
        
        # Asegurándonos de que producto tenga 0 a la izquierda si es necesario
        if longitud <= 8:
            producto = f"{producto:08}"
        elif longitud <= 16:
            producto = f"{producto:016}"
        elif longitud <= 32:
            producto = f"{producto:032}"
        
        # Tomando los 4 dígitos de en medio según la longitud
        if longitud <= 8:
            medio = producto[2:6]
        elif longitud <= 16:
            medio = producto[6:10]
        elif longitud <= 32:
            medio = producto[14:18]
        
        # Convirtiendo a int()
        medio = int(medio)
        
        # Obteniendo ri
        ri = medio / 10000
        
        # Guardamos los resultados en una lista
        resultados.append({
            'Iteración': i+1,
            'Semilla 1': semilla1,
            'Constante': constante,
            'Producto': producto,
            'Longitud': longitud,
            'Medio': medio,
            'ri': ri
        })
                
        # La nueva semilla será el valor de 'medio' calculado en esta iteración
        semilla1 = medio
        
    return resultados

# Interfaz gráfica con Streamlit
st.title("Generador Multiplicador Constante")

# Crear columnas para organizar el diseño (entrada en la izquierda y resultados en la derecha)
col1, espacio, col2 = st.columns([2, 0.5, 3])

# Captura de datos
with col1:
    semilla1_input = st.text_input("Ingresa tu semilla (número de dígitos pares y mayor a 0):")
    constante_input = st.text_input("Ingresa tu constante (número de dígitos pares y mayor a 0):")
    iteraciones_input = st.text_input("Ingresa las iteraciones:")

# Si ambos inputs están llenos, hacer las validaciones y mostrar los resultados
if semilla1_input and constante_input and iteraciones_input:
    try:
        semilla1 = int(semilla1_input)  # Convertir la semilla a entero
        constante = int(constante_input)  # Convertir la semilla a entero
        iteraciones = int(iteraciones_input)  # Convertir las iteraciones a entero

        # Validación de las condiciones de entrada
        if semilla1 > 0 and len(str(semilla1)) % 2 == 0 and constante > 0 and len(str(constante)) % 2 == 0 and iteraciones > 0:
            # Obtener los resultados de las operaciones
            resultados = multiplicador_constante(constante, semilla1, iteraciones)
            
            # Convertir la lista de resultados en un DataFrame de Pandas
            df = pd.DataFrame(resultados)
            
            # Eliminando una columna 
            df = df.drop(df.columns[0], axis=1)  # Elimina la primera columna
                        
            # Mostrar la tabla en la columna derecha
            with col2:
                st.header("Tabla Generada")
                st.dataframe(df, use_container_width=True)
                
                with st.expander("Hecho por:"):
                    st.write("Rodrigo González López S4A")
        else:
            st.error("Recuerda que la semilla debe tener un número de dígitos pares y mayor a 0, y las iteraciones deben ser mayores a 0.")
    except ValueError:
        st.error("Por favor, ingresa valores numéricos válidos para la semilla y las iteraciones.")
