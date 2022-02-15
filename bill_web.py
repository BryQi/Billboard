#importar librerias
from cmath import e
import streamlit as st
import pickle
import pandas as pd
import numpy as np

import streamlit as st
import plotly.figure_factory as ff
import numpy as np

#Extrar los archivos pickle
with open('lin_reg.pkl', 'rb') as li:
    lin_reg = pickle.load(li)

with open('log_reg.pkl', 'rb') as lo:
    log_reg = pickle.load(lo)

with open('decision_treeE.pkl', 'rb') as sv:
    decision_tree = pickle.load(sv)

#funcion para clasificar las plantas 
def estadoA(mood):
    if mood == 6:
        return 'Empowering'
    elif mood == 100:
        return 'Cool'

#funcion para clasificar las plantas 
def classify(num):
    if num == 0:
        return 'No llegó al Top'
    elif num == 1:
        return 'Llegó al Top'




def main():
    #titulo
    st.title('Modelamiento')
    #titulo de sidebar
    st.sidebar.header('User Input Parameters')

    #funcion para poner los parametrso en el sidebar
    def user_input_parameters():
        d=estado_Animo = st.sidebar.slider('Estado de animo', 0, 6, 0 )
        st.write('Estado de animo')   
        if d == 6:
            st.write('Empowering')
        elif d == 5:
            st.write('Cool')
        elif d== 4:
            st.write('Yearning')
        elif d== 3:
            st.write('Gritty')
        elif d== 2: 
            st.write('Sensual')
        elif d== 1:
            st.write('Easygoing')

        e=tiempo = st.sidebar.slider('Tiempo', 0, 2, 0)
        if e == 0:
            st.write('Fast Tempo')
        elif e == 1:
            st.write('Slow Tempo')
        elif e== 2:
            st.write('Medium Tempo')
        
        genero = st.sidebar.slider('Genero', 0, 4, 0)
        if e == 0:
            st.write('Soundtrack - Jazz - Other')
        elif e == 1:
            st.write('Alternative - Punk - Electronica - Rock')
        elif e== 2:
            st.write('Traditional')
        elif e== 3:
            st.write('Pop')
        elif e== 4:
            st.write('Urban')

        tipo_Artista = st.sidebar.slider('Tipo artista', 0, 3, 0)
        if e == 0:
            st.write(' ')
        elif e == 1:
            st.write('Mixed')
        elif e== 2:
            st.write('Female')
        elif e== 3:
            st.write('Male')
        

        edad = st.sidebar.slider('Edad', 0, 4, 0)
        if e == 0:
            st.write('Monor a 21 años')
        elif e == 1:
            st.write('De 22 a 26 años')
        elif e== 2:
            st.write('De 27 a 30 años')
        elif e== 3:
            st.write('De 31 a 40 años')
        elif e== 4:
            st.write('Mayor a 41 años')

        duracion = st.sidebar.slider('Duración', 0, 6, 0)
        if e == 0:
            st.write('Monor a 150 segundos')
        elif e == 1:
            st.write('De 151 a 180 segundos')
        elif e== 2:
            st.write('De 181 a 210 segundos')
        elif e== 3:
            st.write('De 211 a 240 segundos')
        elif e== 4:
            st.write('De 241 a 270 segundos')
        elif e== 5:
            st.write('De 271 a 300 segundos')
        elif e== 6:
            st.write('Mayor a 301 segundos')

        data = {'Estado de ánimo': estado_Animo,
                'Tiempo': tiempo,
                'Genero': genero,
                'Tipo de artista': tipo_Artista,
                'Edad': edad,
                'Duracion': duracion,
                }
        features = pd.DataFrame(data, index=[0])
        return features
    
    df = user_input_parameters()

    
    #escoger el modelo preferido
    option = ['Linear Regression', 'Logistic Regression', 'Árbol']
    model = st.sidebar.selectbox('Which model you like to use?', option)

    st.subheader('Parámetros de entrada')
    st.subheader(model)
    st.write(df)

    if st.button('EJECUTAR PARA PREDECIR'):
        if model == 'Linear Regression':
            st.success(classify(lin_reg.predict(df)))
        elif model == 'Logistic Regression':
            st.success(classify(log_reg.predict(df)))
        else:
            st.success(classify(decision_tree.predict(df)))
    

    

if __name__ == '__main__':
    main()
    