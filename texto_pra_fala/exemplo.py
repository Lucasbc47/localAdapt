# Arquivo pra testar TTS
from texto_pra_fala.tocar_tts import traduzir, falar

texto_em_ing = 'Text to test our text to speech code'
texto_em_port = traduzir(texto=texto_em_ing)

falar(
    texto=texto_em_port, 
    tocar=True 
    # False: salva o arquivo
)
