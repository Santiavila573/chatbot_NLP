import tkinter as tk
import tkinter.font as font
from tkinter import scrolledtext
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json

# Asegúrate de descargar los recursos necesarios
nltk.download('punkt')
nltk.download('stopwords')

# Cargar preguntas y respuestas desde un archivo JSON
def cargar_datos(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return json.load(file)

# Base de datos de preguntas y respuestas
qa_pairs = cargar_datos('preguntas_respuestas.json')

# Función para obtener respuesta usando TF-IDF
def obtener_respuesta(pregunta):
    preguntas = list(qa_pairs.keys())
    respuestas = list(qa_pairs.values())
    preguntas.append(pregunta)

    tfidf_vectorizer = TfidfVectorizer().fit_transform(preguntas)
    tfidf_matrix = tfidf_vectorizer.toarray()

    cosine_similarities = linear_kernel(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
    
    indice_mejor_coincidencia = cosine_similarities.argmax()
    umbral_similitud = 0.2
    if cosine_similarities[indice_mejor_coincidencia] > umbral_similitud:
        return respuestas[indice_mejor_coincidencia]
    else:
        return "Lo siento, no tengo una respuesta para eso."

# Función para manejar la entrada del usuario
def enviar():
    pregunta_usuario = entrada.get()
    if pregunta_usuario.lower() == 'salir':
        ventana.quit()
    
    # Mostrar la pregunta del usuario en el chat
    texto_chat.config(state=tk.NORMAL)
    texto_chat.insert(tk.END, "Tú: " + pregunta_usuario + "\n")
    texto_chat.config(state=tk.DISABLED)
    
    # Limpiar la entrada
    entrada.delete(0, tk.END)
    
    # Simular un retraso en la respuesta
    ventana.after(1000, responder, pregunta_usuario)  # 1000 ms = 1 segundo

def responder(pregunta_usuario):
    respuesta = obtener_respuesta(pregunta_usuario)
    texto_chat.config(state=tk.NORMAL)
    texto_chat.insert(tk.END, "Bot: " + respuesta + "\n")
    texto_chat.config(state=tk.DISABLED)
    texto_chat.yview(tk.END)  # Desplazar hacia abajo automáticamente

# Función para limpiar el chat
def limpiar_chat():
    texto_chat.config(state=tk.NORMAL)
    texto_chat.delete(1.0, tk.END)
    texto_chat.config(state=tk.DISABLED)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Chatbot Asistente")
ventana.geometry("400x450")
ventana.configure(bg="#f5f5f5")  # Color de fondo suave

# Mensaje de bienvenida
texto_chat = scrolledtext.ScrolledText(ventana, state=tk.DISABLED, wrap=tk.WORD, height=15)
texto_chat.pack(pady=10, padx=10)
texto_chat.configure(bg="#ffffff", fg="#333333", font=("Arial", 10))  # Texto oscuro sobre fondo claro
texto_chat.config(state=tk.NORMAL)
texto_chat.insert(tk.END, "¡Hola! Soy tu asistente virtual. ¿Cómo puedo ayudarte hoy?\n")
texto_chat.config(state=tk.DISABLED)

# Crear entrada de texto
entrada = tk.Entry(ventana, width=50, font=("Arial", 10), bg="#e6e6e6", fg="#333333")
entrada.pack(pady=10, padx=10)
entrada.bind("<Return>", lambda event: enviar())

# Crear botones
frame_botones = tk.Frame(ventana, bg="#f5f5f5")
frame_botones.pack(pady=5)

boton_enviar = tk.Button(frame_botones, text="Enviar", command=enviar, bg="#4CAF50", fg="white", font=("Arial", 10), relief="flat")
boton_enviar.pack(side=tk.LEFT, padx=5)

boton_limpiar = tk.Button(frame_botones, text="Limpiar Chat", command=limpiar_chat, bg="#FF5733", fg="white", font=("Arial", 10), relief="flat")
boton_limpiar.pack(side=tk.LEFT, padx=5)

# Ejecutar la ventana
ventana.mainloop()