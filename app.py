import streamlit as st
import PIL.Image
import random
import spacy
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from streamlit_extras.let_it_rain import rain
import prompts


# Variables para guardar datos de sesión

if 'puntaje_mas_alto' not in st.session_state:
    st.session_state.puntaje_mas_alto = 0

if 'puntaje_guardado' not in st.session_state:
    st.session_state.puntaje_guardado = 0
    


# Parámetros
puntaje_mayor = 0


st.set_page_config(
    page_title="Herramientas AI - Qüid Lab",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Parametros NLP
#nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("en_core_web_sm")



# Oculto botones de Streamlit
hide_streamlit_style = """
				<style>
				#MainMenu {visibility: hidden;}

				footer {visibility: hidden;}
				</style>
				"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Funciones
def success():
	rain(
		emoji="🎈",
		font_size=54,
		falling_speed=5,
		animation_length=1, #'infinite'
	)





def adivinar_prompt(prompt_adivinado, prompt_real):
    frase1 = prompt_adivinado
    frase2 = prompt_real
    fra1 = nlp(frase1)
    fra2 = nlp(frase2)
    similitud_frases = fra1.similarity(fra2)
    puntaje_actual = similitud_frases
    return puntaje_actual


# Logo sidebar
image = PIL.Image.open('logo_blanco.png')
st.sidebar.image(image, width=None, use_column_width=None)

with st.sidebar:
    selected = option_menu(
        menu_title="Selecciona",  # required
        options=["Home", "Imagen", "Texto", "Audio", "Listado", "Contacto"],  # required
        icons=["house", "caret-right-fill", "caret-right-fill","caret-right-fill",
                        "caret-right-fill", "envelope"],  # optional
        menu_icon="upc-scan",  # optional
        default_index=0,  # optional
    )



if selected == "Home":
	st.title("Herramientas AI - Qüid Lab")
	st.write("Esta aplicación te permitirá acceder a algunas herramientas relacionadas con Inteligencia Artificial que pueden ser útiles para tu día a día.\n \n Tenla siempre a mano porque seguramente será de mucha utilidad.\n\n\n\n")
	st.write(' ')
	st.write("**Instrucciones:** \n Selecciona en el menú de la izquierda la sección de tu preferencia.")
	"""
	* Imágenes: Incluye actividades para practicar la redacción de prompts.
		* Herramienta 1: Adivina el prompt
		* Herramienta 2: La imagen más parecida
	* Texto: Incluye las herramientas para la generación de ideas.
		* Consultor positivo: Generación de ideas para solucionar un problema
		* Consultor negativo: Generación de ideas para hacer más grave un problema
	* Listado: Incluye las herramientas para la generación de imágenes y textos.
		* Para generar imágenes
		* Para generar textos
		* Recomendaciones para la inclusión


	"""


if selected == "Imagen":
	st.title(f"Seleccionaste la opción {selected}")


	actividad_select = st.sidebar.selectbox('Herramienta', ('Selecciona','Herramienta 1', 'Herramienta 2'))
	if actividad_select=="Selecciona":

		st.write(' ')
		st.write(' ')
		st.write("Ahora selecciona una opción dentro de la lista desplegable ubicada en la parte inferior de la barra lateral izquierda (debajo del menú).")
		
	if actividad_select == "Herramienta 1":
		st.title(f"{actividad_select} - Adivina el prompt")
		col1,col2= st.columns(2)
		imagen_select = col1.selectbox('Selecciona una imagen', prompts.Archivos_actividad1.keys())
		url_imagen_select = prompts.Archivos_actividad1.get(imagen_select)
		image = PIL.Image.open(url_imagen_select)
		col2.image(image, width=None, use_column_width=True)
		prompt_imagen_select = prompts.Actividad1_ListaPrompts.get(imagen_select)
		
		prompt_adivinado = col1.text_input('¿Cuál crees que es el prompt de esta imagen?', " ")
		boton_adivinar = col1.button("Adivinar")

		if boton_adivinar:
			puntaje_actual = adivinar_prompt(prompt_adivinado, prompt_imagen_select)
			diferencia_con_anterior = puntaje_actual - st.session_state.puntaje_guardado
			st.session_state.puntaje_guardado = puntaje_actual
			
			puntaje_mas_alto = st.session_state.puntaje_mas_alto
			diferencia_con_mas_alto = puntaje_actual - puntaje_mas_alto
				
			if puntaje_actual > puntaje_mas_alto:
				success()
				st.session_state.puntaje_mas_alto = puntaje_actual
			st.session_state.puntaje_guardado = puntaje_actual

			col1.metric(
				label="Puntaje actual y diferencia con puntaje anterior: 🌟",
				value=(numerize(puntaje_actual)),
				delta=numerize(diferencia_con_anterior),
			)

			col1.metric(
				label="Puntaje más alto: 🏆",
				value=(numerize(st.session_state.puntaje_mas_alto)),
			)

		#Ver el prompt real
		ver_prompt = st.checkbox('Ver el prompt 🚫(Sólo en caso de emergencia...)🚫')
		if ver_prompt:
			st.write('Prompt real:')
			st.write(prompt_imagen_select)

	if actividad_select == "Herramienta 2":
		st.title(f"Actividad 2 - La imagen más parecida")
		st.write("Esta actividad consiste en hacer una imagen lo más parecida posible a la imagen presentada.")

		col1,col2= st.columns(2)
		imagen_select = col1.selectbox('Selecciona una imagen', prompts.Archivos_actividad2.keys())
		url_imagen_select = prompts.Archivos_actividad2.get(imagen_select)
		image = PIL.Image.open(url_imagen_select)
		col2.image(image, width=None, use_column_width=True)
		prompt_imagen_select = prompts.Actividad2_ListaPrompts.get(imagen_select)
		col1.write("1. Analiza la imagen y redacta un prompt para generar una imagen lo más parecida posible")
		col1.write("2. Ingresa a Lexica.art y genera una imagen")
		body = '<a href="https://lexica.art/aperture">https://lexica.art/aperture</a>'
		col1.markdown(body, unsafe_allow_html=True)	
		col1.write("3. Comparte el resultado y compáralo con el de los demás")

		#Ver el prompt real
		ver_prompt = st.checkbox('Ver el prompt 🚫(Sólo en caso de emergencia...)🚫')
		if ver_prompt:
			st.write('Prompt real:')
			st.write(prompt_imagen_select)

if selected == "Texto":
	actividad_select = st.sidebar.selectbox('Herramientas para', ('Selecciona','Consultor Positivo', 'Consultor Negativo'))

	if actividad_select=="Selecciona":
		st.title(f"Seleccionaste la opción {selected}")

		st.write(' ')
		st.write(' ')
		st.write("Ahora selecciona una opción dentro de la lista desplegable ubicada en la parte inferior de la barra lateral izquierda (debajo del menú).")
		

	if actividad_select == "Consultor Positivo":
		st.title(f"Herramienta:  {actividad_select}")
		image =  PIL.Image.open('angel.jfif')
		st.image(image,width=500, use_column_width=True )
		# Get user input


		url = "https://ora.ai/sufficient-white-9rfn/consultor-virtual"

		st.markdown(f'''
		<div style="text-align:center">
		<a href={url}><button style="
		background-color:#ff4b4b;
		color:#ffff;
		">Contactar al Consultor Virtual Positivo</button></a>
		</div>
		''',
		unsafe_allow_html=True)


	if actividad_select == "Consultor Negativo":
		st.title(f"Herramienta:  {actividad_select}")
		image =  PIL.Image.open('bad.jfif')
		st.image(image,width=500, use_column_width=True )
		# Get user input


		url = "https://ora.ai/sufficient-white-9rfn/consultor-tóxico"

		st.markdown(f'''
		<div style="text-align:center">
		<a href={url}><button style="
		background-color:#ff4b4b;
		color:#ffff;
		">Contactar al Consultor Virtual Negativo</button></a>
		</div>
		''',
		unsafe_allow_html=True)



if selected == "Listado":
	actividad_select = st.sidebar.selectbox('Herramientas para', ('Selecciona','Imágenes', 'Texto', 'Accesibilidad'))

	if actividad_select=="Selecciona":
		st.title(f"Seleccionaste la opción {selected}")
		st.write(' ')
		st.write(' ')
		st.write("Ahora selecciona una opción dentro de la lista desplegable ubicada en la parte inferior de la barra lateral izquierda (debajo del menú).")
		
	
	if actividad_select=="Imágenes":
		st.title(f"Herramientas IA para la generación de imágenes")
		st.write("Algunas herramientas:")
		"""
		* Herramientas que pueden ayudar en la estructuración de prompts:
				
			* Herramientas que me permiten buscar prompts como referencia
				* http://lexica.art 
				* https://prompthero.com/ 

			* Herramientas que me permiten estructurar un prompt
				* https://www.dallelist.com/ 
				* https://promptomania.com/prompt-builder/ 
				* https://prompt.noonshot.com/ 

				
		* Herramientas para generar imágenes a partir de prompts:

			* Stable Diffusion
				* https://stablediffusionweb.com/#demo 
			* Lexica ART
				* https://lexica.art/aperture
			* Midjourney
				* http://midjourney.com/ 
				* Discord Server: https://discord.gg/midjourney 
			* https://www.bluewillow.ai/ 
				* Discord Server: https://discord.gg/UrgFx5RS 
			* Bing Image Creator (Dall-e)
				* https://www.bing.com/images/create 
			* Scribble Diffusion 
				* https://scribblediffusion.com/
			* ControlNet 
				* https://stablediffusionweb.com/ControlNet#demo
			* Dream by Wombo
				* https://dream.ai/create
			* Leonardo AI
				* https://leonardo.ai/


		"""
	if actividad_select=="Texto":
		st.title(f"Herramientas IA para la generación de texto")
		st.write("Algunas herramientas:")
		"""
		* Herramientas que pueden ayudar en la estructuración de prompts:
				
			* Herramientas que me permiten buscar prompts como referencia
				* https://chat.openai.com/chat 
				* https://bing.com/chat 


			

		"""

	if actividad_select=="Accesibilidad":
		st.title(f"Herramientas para asegurar la accesibilidad")
		st.write("Algunas herramientas:")
		"""
		* Guía para la creación de contenidos accesibles (Fundación Saldarriaga Concha):	
			* https://www.saldarriagaconcha.org/wp-content/uploads/2022/08/2022-08-Agosto-Guia-para-la-innovacion-educativa-y-la-creaccion-de-contenidos-accesibles.pdf


				


		"""






if selected == "Contacto":
	st.title(f"Seleccionaste la opción {selected}")
	st.write(' ')
	st.write(' ')

	st.title(f"Contacto y créditos")
	st.subheader("Jorge O. Cifuentes")
	body = '<a href="https://www.quidlab.co">https://www.quidlab.co</a>'
	st.markdown(body, unsafe_allow_html=True)
	st.write('Email: *jorge@quidlab.co* :heart: :fleur_de_lis:')
	st.write("Quid Lab AI tools")
	st.write("Version 1.0")
	st.text("")







