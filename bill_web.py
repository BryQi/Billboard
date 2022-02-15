#importar librerias
from cmath import e

from pyexpat import features

import streamlit as st
import pickle
import pandas as pd
import numpy as np

import streamlit as st
import plotly.figure_factory as ff
import numpy as np

#Extrar los archivos pickle
#varaible vacia para almacenar probabilidad
decision_tree = ''

with open('lin_reg.pkl', 'rb') as li:
    lin_reg = pickle.load(li)

with open('log_reg.pkl', 'rb') as lo:
    log_reg = pickle.load(lo)


with open('decision_treeE.pkl', 'rb') as sv:
    decision_tree = pickle.load(sv)


#funcion para clasificar las plantas 
def classify(num):
    if num == 0:
        return 'No llegó al Top'
    elif num == 1:
        return 'Llegó al Top'

def main():
    #titulo
    st.image(
    "https://phantom-marca.unidadeditorial.es/772232b91f820ff4d5aaf3eae6dc4c31/resize/1320/f/jpg/assets/multimedia/imagenes/2020/10/15/16027188459256.jpg",
    width=None,) 

    # Título
    html_temp = """
    <h1 style="color:#2A759D;text-align:center;">¿Probabilidad de llegar al TOP 1 del Premio Billboard Hot 100</h1>
    El Billboard Hot 100 es una gran lista de éxitos musicales de los 100 sencillos más vendidos en Estados Unidos, 
    que ayuda a promover la industria musical nacional e internacional, y se define como la más importante de las listas de
     Billboard junto con la Billboard 200.
    <br>
    Variables de anális:
    <br>
    <br>
    </div>

    """
    st.markdown(html_temp,unsafe_allow_html=True)
    #titulo de sidebar
    st.sidebar.header('Parámetros de entrada')

    #funcion para poner los parametrso en el sidebar
    def user_input_parameters():    
        mood =estado_Animo = st.sidebar.slider('Estado de animo', 0, 6, 6 )
        tempo =tiempo = st.sidebar.slider('Tiempo', 0, 2, 2)
        gen = genero = st.sidebar.slider('Genero', 0, 4, 4)
        tipo = tipo_Artista = st.sidebar.slider('Tipo artista', 0, 3, 3)
        eda = edad = st.sidebar.slider('Edad', 0, 4, 4)
        dura= duracion = st.sidebar.slider('Duración', 0, 6, 6)
        data = {'Estado de ánimo': estado_Animo,
                'Tiempo': tiempo,
                'Género': genero,
                'Tipo de artista': tipo_Artista,
                'Edad': edad,
                'Duración': duracion,
                }
        features = pd.DataFrame(data, index=[0])
###### datos estáticos quemados
### Estado de ánimo
    
        st.subheader('Estado de ánimo')
        if mood == 6:
                st.caption('Energizar - Potenciar')
        elif mood == 5:
                st.caption('Fresco - Emocionado - Entusiasmado - Agitado - Animado')
        elif mood == 4:
               st.caption('Sofisticado - Agresivo - Ardiente - Alborotador - Sentimental - Melancólico - Inquietante')
        elif mood == 3:
                st.caption('Desafiante')
        elif mood == 2: 
                st.caption('Sensual - Romantico')
        elif mood == 1:
                st.caption('Tranquilo')
        
### tiempo
        st.subheader('Tiempo')
        if tempo == 0:
            st.write('Tiempo lento')
        elif tempo == 1:
            st.write('Tiempo medio')
        elif tempo == 2:
            st.write('Tiempo rápido')
        
### género
        st.subheader('Género')
        if gen == 0:
            st.write(' Banda sonora - Jazz - Otros')
        elif gen == 1:
            st.write('Alternativa - Punk - Electrónica - Rock')
        elif gen == 2:
            st.write('Tradicional')
        elif gen == 3:
            st.write('Pop')
        elif gen == 4:
            st.write('Urbano') 
### tipo de artista
        st.subheader('Tipo de artista')
        if tipo == 0:
            st.write(' ')
        elif tipo == 1:
            st.write('Mixto')
        elif tipo == 2:
            st.write('Mujer')
        elif tipo == 3:
            st.write('Hombre')

### edad
        st.subheader('Edad')
        if  eda == 0:
            st.write('Menor a 21 años')
        elif  eda == 1:
            st.write('De 22 a 26 años')
        elif  eda == 2:
            st.write('De 27 a 30 años')
        elif  eda == 3:
            st.write('De 31 a 40 años')
        elif  eda== 4:
            st.write('Mayor a 41 años')
### edad
        st.subheader('Duración')
        if dura == 0:
            st.write('Menor a 150 segundos')
        elif dura == 1:
            st.write('De 151 a 180 segundos')
        elif dura == 2:
            st.write('De 181 a 210 segundos')
        elif dura == 3:
            st.write('De 211 a 240 segundos')
        elif dura == 4:
            st.write('De 241 a 270 segundos')
        elif dura == 5:
            st.write('De 271 a 300 segundos')
        elif dura== 6:
            st.write('Mayor a 301 segundos')

        return features 

    df = user_input_parameters()

        
    #escoger el modelo preferido
    option = [ 'Árbol de decisión']

    model = st.sidebar.selectbox('Algoritmo?', option)


    #st.subheader('Parámetros de entrada')
    st.subheader(model)
    st.write(df)

    if st.button('EJECUTAR PARA PREDECIR'):
        x_i = np.asarray(df).reshape(1,-1)
        if model == 'Linear Regression':
            st.success(classify(lin_reg.predict(df)))
            x_i = np.asarray(df).reshape(1,-1)  
            st.success('La probabilidad del acierto es: {}'.format(probabilidad[:,1]*100))

        elif model == 'Logistic Regression':
            st.success(classify(log_reg.predict(df)))
            x_i=np.asarray(df).reshape(1,-1)
            st.success('La probabilidad del Acierto es: {}'.format(probabilidad[:,1]*100))
        else:
            st.success(classify(decision_tree.predict(df)))
            x_i=np.asarray(df).reshape(1,-1)
            probabilidad = decision_tree.predict_proba(x_i)
            st.success('La probabilidad del acierto es: {}'.format(probabilidad[:,1]*100))
            
if __name__ == '__main__':
    main()
    