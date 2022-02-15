#importar las librerias necesarias
from re import A
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn import tree
from sklearn.model_selection import KFold
from subprocess import check_call
from PIL import Image, ImageDraw, ImageFont
from IPython.display import Image as PImage
import pickle

import pandas as pd
 
#cargar los datos en un dataset
bill = pd.read_csv("artists_billboard_fix3.csv")

#print(bill)

#data.head(10)


#bill = datasets.load_iris()
# El tempo (Tiempo) que puede ser lento, medio o rápido queda mapeado: 0-Rapido,
#  1-Lento, 2-Medio (por cantidad de canciones en cada tempo: el Medio es el que más tiene)


# Mood Mapping  (mapeo de los estados de animo)

bill['moodEncoded'] = bill['mood'].map( {'Energizing': 6, 
                                        'Empowering': 6,
                                        'Cool': 5, 
                                        'Yearning': 4, # anhelo, deseo, ansia
                                        'Excited': 5, #emocionado
                                        'Defiant': 3, 
                                        'Sensual': 2, 
                                        'Gritty': 3, #coraje 
                                        'Sophisticated': 4,
                                        'Aggressive': 4, # provocativo
                                        'Fiery': 4, #caracter fuerte
                                        'Urgent': 3, 
                                        'Rowdy': 4, #ruidoso alboroto
                                        'Sentimental': 4,
                                        'Easygoing': 1, # sencillo
                                        'Melancholy': 4, 
                                        'Romantic': 2, 
                                        'Peaceful': 1, 
                                        'Brooding': 4, # melancolico
                                        'Upbeat': 5, #optimista alegre
                                        'Stirring': 5, #emocionante
                                        'Lively': 5, #animado
                                        'Other': 0,'':0} ).astype(int)


# Genre Mapping (mapeo del género)
bill['genreEncoded'] = bill['genre'].map( {'Urban': 4, 
                                          'Pop': 3, 
                                          'Traditional': 2, 
                                          'Alternative & Punk': 1,
                                         'Electronica': 1, 
                                          'Rock': 1, 
                                          'Soundtrack': 0, 
                                          'Jazz': 0,
                                          'Other':0,'':0} 
                                       ).astype(int)

# artist_type Mapping 
bill['artist_typeEncoded'] = bill['artist_type'].map( {'Female': 2, 'Male': 3, 'Mixed': 1, '': 0} ).astype(int)


drop_elements = ['id','title','artist','mood','tempo','genre','artist_type','chart_date','anioNacimiento','durationSeg']
artists_encoded = bill.drop(drop_elements, axis = 1)

print (artists_encoded)


#Revisemos en tablas cómo se reparten los top=1 en los diversos atributos mapeados. 
#Sobre la columna sum, estarán los top, pues al ser valor 0 o 1, sólo se sumarán los que sí llegaron al número 1

artists_encoded[['moodEncoded', 'top']].groupby(['moodEncoded'], as_index=False).agg(['mean', 'count', 'sum'])

#La mayoría de top 1 los vemos en los estados de ánimo 5 y 6 con 46 y 43 canciones

artists_encoded[['artist_typeEncoded', 'top']].groupby(['artist_typeEncoded'], as_index=False).agg(['mean', 'count', 'sum'])
#Aqui están bastante repartidos, pero hay mayoría en tipo 3: artistas masculinos

artists_encoded[['genreEncoded', 'top']].groupby(['genreEncoded'], as_index=False).agg(['mean', 'count', 'sum'])
#Los géneros con mayoría son evidentemente los géneros 3 y 4 que corresponden con Urbano y Pop

##########################################

cv = KFold(n_splits=10) # Numero deseado de "folds" que haremos
accuracies = list()
max_attributes = len(list(artists_encoded))
depth_range = range(1, max_attributes + 1)
 
# Testearemos la profundidad de 1 a cantidad de atributos +1
for depth in depth_range:
    fold_accuracy = []
    tree_model = tree.DecisionTreeClassifier(criterion='entropy',
                                             min_samples_split=20,
                                             min_samples_leaf=5,
                                             max_depth = depth,
                                             class_weight={1:3.5})
    for train_fold, valid_fold in cv.split(artists_encoded):
        f_train = artists_encoded.loc[train_fold] 
        f_valid = artists_encoded.loc[valid_fold] 
 
        model = tree_model.fit(X = f_train.drop(['top'], axis=1), 
                               y = f_train["top"]) 
        valid_acc = model.score(X = f_valid.drop(['top'], axis=1), 
                                y = f_valid["top"]) # calculamos la precision con el segmento de validacion
        fold_accuracy.append(valid_acc)
 
    avg = sum(fold_accuracy)/len(fold_accuracy)
    accuracies.append(avg)
    
# Mostramos los resultados obtenidos
df = pd.DataFrame({"Max Depth": depth_range, "Average Accuracy": accuracies})
df = df[["Max Depth", "Average Accuracy"]]
print(df.to_string(index=False))
#Podmeos ver que en 4 niveles de splits tenemos el score más alto, con casi 65%.

############################################

# Crear arrays de entrenamiento y las etiquetas que indican si llegó a top o no 
y_train = artists_encoded['top']
x_train = artists_encoded.drop(['top'], axis=1).values 



lin_reg = LinearRegression()
log_reg = LogisticRegression()
# Crear Arbol de decision con profundidad = 4
decision_tree = tree.DecisionTreeClassifier(criterion='entropy',
                                            min_samples_split=20,
                                            min_samples_leaf=5,
                                            max_depth = 4,
                                            class_weight={1:3.5})

#entrenar modelos
lin_regr = lin_reg.fit(x_train, y_train)
log_regr = log_reg.fit(x_train, y_train)
decision_treeE = decision_tree.fit(x_train, y_train)

with open('lin_reg.pkl', 'wb') as li:
    pickle.dump(lin_regr, li)

with open('log_reg.pkl', 'wb') as lo:
    pickle.dump(log_regr, lo)

with open('decision_treeE.pkl', 'wb') as sv:
    pickle.dump(decision_treeE, sv)




