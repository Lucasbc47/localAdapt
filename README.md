<p align="center">
  <h1 align="center">localAdapt</h1>
</p>

## Projeto feito para o Samsung Innovation Campus 2023
Se trata de um prótotipo pra ajudar deficientes visuais, consta um dispositivo móvel (RPI) conectada a uma câmera que detecta objetos e pessoas a frente, e envia as informações pra um fone via texto pra voz. Ele utiliza o **yolov5** pra código de detecção de objetos e dataset. Pode se ligar o dispositivo com um powerbank. A ideia era portar num cordão ou até mesmo em uma bengala.

## Itens utilizados
- Raspberry Pi 4B
- Raspberry Pi Camera Rev 1.3
- Powerbank
- Case impressa 3D (https://www.thingiverse.com/thing:3732714)
- Fone com fio

## Setup  
- Instale as bibliotecas necessárias e libcamera
- Vá na pasta **texto_pra_fala e siga o tutorial pra API da Google Cloud**
- Caso não consiga, utilize **espeak** ou **pyttsx3**, e altere na linha 187.
- Crie um arquivo na home chamado **rodar.sh** e insira:
```sh
#!/bin/bash
sleep 15
libcamera-vid --rotation 180 -n -t 0 --width 1280 --height 960 --framerate 1 -->
sleep 5
cd <local_do_yolov5>
python3 detect.py --source=tcp://127.0.0.1:8888
```
- Conecte a **Raspberry Pi Camera** cuidadosamente em seu **Raspberry Pi**
- Pra rodar ao ligar, crie um **service na /etc/systemd/system/** 
- Exemplo de arquivo service, **project.service**
```sh
[Unit]
Description=uma descricao pro seu projeto

[Service]
ExecStart=/home/pi/rodar.sh
Restart=always
User=pi

[Install]
WantedBy=default.target
```

- Após criar, reinicie o serviço com **sudo systemctl daemon-reload**.

```
# iniciar 
sudo systemctl start project
# ativar
sudo systemctl enable project
# status
sudo systemctl status project
```
