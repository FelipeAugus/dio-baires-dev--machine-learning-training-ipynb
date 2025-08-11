# **OBSERVAÇÃO:**
# Esse notebook não executa no colab, pois precisa de acesso ao microfone e a saida de áudio do computador.
# É possivel adaptar o script adicionando funções que executam JS para obter e reproduzir audio.

# pip install -q pyttsx3 SpeechRecognition pygame pyaudio wikipedia

import os
import pyttsx3
import random
import speech_recognition as sr
import unicodedata
import webbrowser
import wikipedia
wikipedia.set_lang('pt')

from pygame import mixer
from datetime import datetime

# ----- FUNÇÕES BÁSICAS -----
# "LÊ" o texto que voce passou

def get_id_voz_pt():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "brazil" in voice.name.lower() or "portuguese" in voice.id.lower():
            engine.stop()
            return voice.id
    engine.stop()
    return None
ID_VOZ_PT = get_id_voz_pt()

def fala(text):
    engine = pyttsx3.init()
    if(ID_VOZ_PT): engine.setProperty('voice', ID_VOZ_PT)
    print(f"Falando: {text}")
    engine.say(text)
    engine.runAndWait()

# Obtem a solicitação do usuario e converte para texto
def remove_acentos(txt):
    nfkd = unicodedata.normalize('NFKD', txt)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def escuta():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            print("Ouvindo...")
            audio = r.listen(source)
            said = r.recognize_google(audio, language='pt-BR')
            return remove_acentos(said.lower())
        except sr.UnknownValueError: fala("Desculpe, não entendi.")
        except sr.RequestError: fala("Desculpe, o serviço de voz não está disponível.")
    return ""

# ----- FUNCIONALIDADES DO ASSISTENTE -----
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

def stopmusic():
    mixer.music.stop()

def piada():
    piadas = [
        "Por que o computador foi ao médico? Porque ele estava com um vírus!",
        "O que o bit disse para o byte? “Você é tão grande!”",
        "Por que o programador sempre confunde Halloween com Natal? Porque OCT 31 = DEC 25.",
        "Por que os computadores não podem mentir? Porque eles têm muitos bits de verdade.",
        "O que um cabo USB falou para o outro? “Conecte-se comigo!”",
        "Por que o Wi-Fi foi ao psicólogo? Porque ele estava sem conexão.",
        "Qual a comida preferida do navegador? Cookies.",
        "Por que o JavaScript é tão triste? Porque ele não sabe lidar com tipos.",
        "Qual a comida preferida do computador? Chips.",
        "O que o Google disse para o usuário? “Eu sei tudo sobre você.”",
        "Qual a piada favorita dos engenheiros de software? “Isso vai rodar em produção.”",
        "Por que o programador foi pego? Porque ele quebrou a regra do “try-catch”.",
        "Qual hoobie do computador? Fazer bits.",
        "O que a impressora falou para o papel? “Você é meu tipo.”",
        "Por que o computador não pode jogar futebol? Porque ele tem medo de perder o controle.",
        "Qual o doce favorito dos programadores? Cookie.",
        "O que o algoritmo disse para o programador? “Me resolve isso aí!”",
        "Qual é a banda favorita dos programadores? Linkin Park (porque tem o link).",
        "Por que o código foi ao psicólogo? Porque ele tinha muitos problemas não tratados.",
        "Por que o computador não leva desaforo pra casa? Porque ele tem um processador poderoso!",
        "O que o software disse para o hardware? “Você me completa.”",
        "Por que o firewall é tão bom em volei? Porque ele sabe bloquear tudo!",
        "O que o robô disse para a impressora? “Isso é impressão sua!”"
    ]
    return random.choice(piadas)

def respond(text):
    print("Texto obtido: " + text)
    try:
        if 'youtube' in text:
            fala("O que você gostária de assistir?")
            keyword = escuta()
            if keyword!= '':
                url = f"https://www.youtube.com/results?search_query={keyword}"
                webbrowser.get().open(url)
                fala(f"Aqui está o que encontrei para {keyword} no youtube")
        elif 'pesquise' in text:
            fala("O que você gostaria que eu pesquisasse?")
            query = escuta()
            if query !='':
                result = wikipedia.summary(query, sentences=3)
                fala("De acordo com a wikipedia")
                fala(result)
        elif 'piada' in text:
            fala(piada())
        elif 'quantas horas' in text:
            strTime = datetime.today().strftime("%H:%M %p")
            print(strTime)
            fala(strTime)
        elif 'tocar musica' in text:
            fala("Agora tocando música!")           
            music_dir = os.path.join(os.environ['USERPROFILE'], "Music")
            songs = [f for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
            print(songs)
            playmusic(music_dir + "\\" + songs[0])
        elif 'parar musica' in text:
            fala("Parando música!")
            stopmusic()
        elif 'sair' in text or 'tchau' in text:
            fala("Falou valeu! Até mais.")
            return True
    except Exception as e:
        print(e)
        fala("Ocorreu algum erro. Tente novamente, por favor!")


while True:
    text = escuta()
    if(text):
        ret = respond(text)
        if ret: break
