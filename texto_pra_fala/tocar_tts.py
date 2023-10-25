# Text to Speech (TTS): texto pra fala e tradução incluido
import os
import io
import pyaudio

from google.cloud import texttospeech
from pydub import AudioSegment
from translate import Translator

# Chave do '.json' pra acessar a API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "texto_pra_fala/json/quixotic-tesla-402716-cec4cfa9b718.json"

def traduzir(texto: str=None):
    """
    Função pra traduzir texto
    por @LeyyGarcia
    """
    translator = Translator(to_lang="pt-br")
    translation = translator.translate(texto)
    return translation

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



