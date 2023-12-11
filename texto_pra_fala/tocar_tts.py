# Text to Speech (TTS): texto pra fala e tradução incluido
# Usuário pode escolher entre espeak, gcloud ou pyttsx3
import os
import io

import pyaudio
import subprocess
import pyttsx3

from google.cloud import texttospeech
from pydub import AudioSegment
from translate import Translator

# Chave do '.json' pra acessar a API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "texto_pra_fala/json/NOME_DO_ARQUIVO_JSON"

def substituicao(texto: str) -> str:
    nomes_classes = ['pessoa', 'bicicleta', 'carro', 'motocicleta', 'avião', 'ônibus', 'trem', 'caminhão', 'barco', 'semáforo', 'hidrante', 'placa de pare', 'parquímetro', 'banco', 'pássaro', 'gato', 'cachorro', 'cavalo', 'ovelha', 'vaca', 'elefante', 'urso', 'zebra', 'girafa', 'mochila', 'guarda-chuva', 'bolsa', 'gravata', 'mala', 'frisbee', 'esqui', 'snowboard', 'bola esportiva', 'pipa', 'taco de beisebol', 'luva de beisebol', 'skate', 'prancha de surfe', 'raquete de tênis', 'garrafa', 'taça de vinho', 'xícara', 'garfo', 'faca', 'colher', 'tigela', 'banana', 'maçã', 'sanduíche', 'laranja', 'brócolis', 'cenoura', 'cachorro-quente', 'pizza', 'rosquinha', 'bolo', 'cadeira', 'sofá', 'planta em vaso', 'cama', 'mesa de jantar', 'vaso sanitário', 'TV', 'laptop', 'mouse', 'controle remoto', 'teclado', 'celular', 'micro-ondas', 'forno', 'torradeira', 'pia', 'geladeira', 'livro', 'relógio', 'vaso', 'tesoura', 'ursinho de pelúcia', 'secador de cabelo', 'escova de dentes']
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    for i, item in enumerate(class_names):
        texto = texto.replace(item, nomes_classes[i])
    return texto

def traduzir(texto: str=None):
    """
    Função pra traduzir texto
    por @LeyyGarcia
    """
    translator = Translator(to_lang="pt-br")
    translation = translator.translate(texto)
    return translation

def falar_espeak(texto: str=None) -> None:
    """
    Função de falar texto utilizando espeak
    Opção alternativa I
    """
    # sudo apt-get install espeak
    subprocess.run(['espeak', texto])

def falar_ttsx(texto: str=None) -> None:
    """
    Função de falar texto utilizando pyttsx3
    Opção alternativa II
    """
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def falar(texto: str=None, tocar: bool=True) -> None:
    """
    Função pra falar com ajuda da API da Google Cloud

    """
    # Inicializamos o cliente, texto sintetizado da Google Cloud TTS
    cliente_tts = texttospeech.TextToSpeechClient()
    texto_sintetizado = texttospeech.SynthesisInput(text=texto)

    # Inicializamos o seletor de voz
    voz = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Config de audio
    configuracao_audio = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Chamada de API
    resposta = cliente_tts.synthesize_speech(
        input=texto_sintetizado, voice=voz, audio_config=configuracao_audio
    )
    bytes_da_resposta = resposta.audio_content

    if tocar:
        # Colocamos na memória com AudioSegment e lemos os bytes com io 
        audio = AudioSegment.from_file(
            io.BytesIO(bytes_da_resposta), format="mp3"
        )

        # Inicialização do pyaudio
        py_audio = pyaudio.PyAudio()

        # Inicialização da Stream com pyaudio.open
        stream = py_audio.open(
            format=py_audio.get_format_from_width(audio.sample_width),
            channels=audio.channels,
            rate=audio.frame_rate,
            output=True
        )

        # Toca sem salvar e fecha
        stream.write(audio.raw_data)
        stream.stop_stream()
        stream.close()

        py_audio.terminate()

    if not tocar:
        with open('saida.mp3', 'wb') as saida:
            saida.write(bytes_da_resposta)