# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KUrLcNsR3blC7uJ2qom08V-_k17gI2oZ
"""

from google.colab import files
import pandas as pd

# Subir el archivo
uploaded = files.upload()

# Cargar el archivo como DataFrame
data = pd.read_excel("cancer.xlsx")

# Mostrar las primeras filas para verificar
print(data.head())

# -*- coding: utf-8 -*-
"""
Proyecto de clasificación de datos con múltiples clasificadores en Python
Este código implementa una clase `Clasificadores` que entrena y evalúa múltiples modelos de clasificación
basados en la librería scikit-learn. El enfoque sigue el paradigma de programación orientada a objetos.
Requisitos:
  - Regresión Logística
  - k-Nearest Neighbors (KNN)
  - Máquinas de Soporte Vectorial (SVM)
  - Árboles de Decisión
  - Random Forest
El programa se ejecuta en Google Colab y utiliza conjuntos de datos en formato `.xlsx`.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

class Clasificadores:
    """
    Clase para manejar múltiples clasificadores.
    """
    def __init__(self):
        self.modelos = {
            "Regresión Logística": LogisticRegression(max_iter=1000, random_state=42),
            "K-Nearest Neighbors": KNeighborsClassifier(),
            "SVM": SVC(probability=True, random_state=42),
            "Árbol de Decisión": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
        }
        self.resultados = {}

    def entrenar_modelos(self, X_train, y_train):
        """
        Entrena cada modelo utilizando los datos de entrenamiento.
        """
        for nombre, modelo in self.modelos.items():
            try:
                modelo.fit(X_train, y_train)
            except Exception as e:
                print(f"Error entrenando el modelo {nombre}: {e}")

    def evaluar_modelos(self, X_test, y_test):
        """
        Evalúa cada modelo con los datos de prueba y almacena los resultados.
        """
        for nombre, modelo in self.modelos.items():
            try:
                predicciones = modelo.predict(X_test)
                probas = modelo.predict_proba(X_test)[:, 1] if hasattr(modelo, 'predict_proba') else None

                # Métricas de evaluación
                precision = accuracy_score(y_test, predicciones)
                matriz = confusion_matrix(y_test, predicciones)
                reporte = classification_report(y_test, predicciones, zero_division=0)
                roc_auc = roc_auc_score(y_test, probas) if probas is not None else "No disponible"

                self.resultados[nombre] = {
                    "Precisión": precision,
                    "Matriz de Confusión": matriz,
                    "Reporte": reporte,
                    "ROC AUC": roc_auc,
                }
            except Exception as e:
                print(f"Error evaluando el modelo {nombre}: {e}")
        return self.resultados

    def mostrar_resultados(self):
        """
        Imprime y grafica los resultados de los modelos.
        """
        for nombre, resultado in self.resultados.items():
            print(f"\nModelo: {nombre}")
            print(f"Precisión: {resultado['Precisión']:.2f}")
            print(f"ROC AUC: {resultado['ROC AUC']}")
            print("Matriz de Confusión:")
            print(resultado["Matriz de Confusión"])
            print("Reporte de Clasificación:")
            print(resultado["Reporte"])

        # Gráfica de barras de precisión
        precisiones = {nombre: resultado["Precisión"] for nombre, resultado in self.resultados.items()}
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(precisiones.keys()), y=list(precisiones.values()))
        plt.title("Precisión de los Modelos")
        plt.ylabel("Precisión")
        plt.xlabel("Modelos")
        plt.xticks(rotation=45)
        plt.show()

# Configuración principal del programa
if __name__ == "__main__":
    # Cargar datos desde archivo
    ruta_archivo = "cancer.xlsx"  # Subir archivo a Colab o cambiar la ruta local
    datos = pd.read_excel(ruta_archivo)

    # Verificar valores únicos en la columna diagnosis
    print("Valores únicos en diagnosis:", datos["diagnosis"].unique())

    # Filtrar solo clases válidas (B y M)
    datos = datos[datos["diagnosis"].isin(["M", "B"])]

    # Separar características (X) y etiquetas (y)
    X = datos.drop(columns=["diagnosis"])
    y = datos["diagnosis"]

    # Codificar etiquetas (B = 0, M = 1)
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Verificar etiquetas
    print("Etiquetas únicas en y:", np.unique(y))

    # Imputar valores faltantes (rellenar NaN con la media de cada columna)
    X = X.fillna(X.mean())  # Reemplaza NaN con la media de cada columna

    # Escalar características
    scaler = StandardScaler()
    X = scaler.fit_transform(X)  # Escalar solo columnas numéricas

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Crear y entrenar clasificadores
    clf = Clasificadores()
    clf.entrenar_modelos(X_train, y_train)

    # Evaluar clasificadores
    resultados = clf.evaluar_modelos(X_test, y_test)

    # Mostrar resultados
    clf.mostrar_resultados()