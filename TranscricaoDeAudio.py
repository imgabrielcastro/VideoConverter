import azure.cognitiveservices.speech as speechsdk
import os
import subprocess
import time
from datetime import datetime, timedelta
import openai
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import threading
import sys


dll_path = r"C:\Users\joseg\AppData\Local\Programs\Python\Python312\Lib\site-packages\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll"

ffmpeg_path = r"C:\Users\joseg\Desktop\VideoConverter\ffmpeg\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    print("FFmpeg encontrado!")
else:
    print("FFmpeg não encontrado!")



# Adicionando o caminho da DLL ao sistema
os.environ['PATH'] = dll_path + ";" + os.environ['PATH']

# Caminho do ffmpeg
if hasattr(sys, '_MEIPASS'):
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg", "bin", "ffmpeg.exe")
else:
    ffmpeg_path = r"C:\Users\joseg\Desktop\VideoConverter\ffmpeg\ffmpeg.exe"



# Função para localizar o FFmpeg
def localizar_ffmpeg():
    if hasattr(sys, '_MEIPASS'):
        # Caminho do FFmpeg no modo empacotado
        ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg", "bin", "ffmpeg.exe")
    else:
        # Caminho do FFmpeg no modo desenvolvimento (local)
        ffmpeg_path = r"C:\Users\joseg\Desktop\VideoConverter\ffmpeg\bin\ffmpeg.exe"

    # Verifica se o FFmpeg existe no caminho
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"FFmpeg não encontrado no caminho: {ffmpeg_path}")

    return ffmpeg_path

# Exemplo de uso no seu código
ffmpeg_path = localizar_ffmpeg()
print(f"Caminho do FFmpeg: {ffmpeg_path}")


# Configuração das credenciais da Azure
api_key_azure = "SUA API KEY"
region = "brazilsouth"

# Configuração da API OpenAI
openai.api_key = "SUA API KEY"

class RedirectedOutput:
    """Classe para redirecionar o stdout para a área de texto"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.last_message_id = None  # Para controlar a atualização de mensagens de tempo decorrido

    def write(self, message):
        if "Tempo decorrido" in message:
            # Atualiza o tempo decorrido em uma única linha
            if self.last_message_id:
                self.text_widget.delete(self.last_message_id, "end")
            self.last_message_id = self.text_widget.index("end-1c linestart")
            self.text_widget.insert(self.last_message_id, message)
        else:
            self.text_widget.insert("end", message)
        self.text_widget.see("end")

    def flush(self):
        pass

# Variável para controlar o cancelamento do processo
cancelar_processo = False

def verificar_arquivo_convertido(converted_audio_path):
    """Verifica se o arquivo convertido já existe e pergunta se o usuário deseja excluí-lo."""
    if os.path.exists(converted_audio_path):
        resposta = messagebox.askyesno("Arquivo Existente", "O arquivo convertido já existe. Deseja apagá-lo?")
        if resposta:
            try:
                os.remove(converted_audio_path)
                print(f"Arquivo existente removido: {converted_audio_path}")
            except Exception as e:
                print(f"Erro ao remover o arquivo existente: {e}")
        else:
            print("O arquivo existente será reutilizado.")

def converter_mp4_para_wav(input_path, output_path, speed=1.3):
    global cancelar_processo
    print("Convertendo o arquivo MP4 para WAV...")
    try:
        subprocess.run(
            [
                ffmpeg_path,
                "-i", input_path,
                "-ar", "16000",
                "-ac", "1",
                "-b:a", "64k",
                "-filter:a", f"atempo={speed}",
                output_path
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,  # Evita a abertura do CMD
        )
        if cancelar_processo:
            print("Processo cancelado pelo usuário.")
            return
        print(f"Arquivo convertido e ajustado com sucesso: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao converter e ajustar o arquivo MP4 para WAV: {e}")
        exit()

def transcrever_audio_com_timestamps(audio_path):
    global cancelar_processo
    print("Configurando o Azure...")
    speech_config = speechsdk.SpeechConfig(subscription=api_key_azure, region=region)
    speech_config.speech_recognition_language = "pt-BR"
    audio_input = speechsdk.AudioConfig(filename=audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    transcricao_com_timestamps = []
    done = False

    def stop_cb(evt):
        nonlocal done
        done = True

    def processar_resultado(evt):
        nonlocal transcricao_com_timestamps
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            inicio_segundos = result.offset / 10**7
            timestamp = str(timedelta(seconds=int(inicio_segundos)))
            transcricao_com_timestamps.append(f"{timestamp} - {result.text}")

    speech_recognizer.recognized.connect(processar_resultado)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Iniciando transcrição com timestamps...")
    start_time = datetime.now()
    speech_recognizer.start_continuous_recognition()

    # Cronômetro para exibir o tempo decorrido em uma única linha
    last_message = ""
    while not done:
        if cancelar_processo:
            print("Processo cancelado pelo usuário.")
            speech_recognizer.stop_continuous_recognition()
            return []
        elapsed_time = datetime.now() - start_time
        current_message = f"Tempo decorrido: {str(elapsed_time).split('.')[0]}"
        if current_message != last_message:
            print(f"\r{current_message}", end="")
            last_message = current_message
        time.sleep(1)

    # Finaliza a transcrição
    speech_recognizer.stop_continuous_recognition()
    elapsed_time = datetime.now() - start_time
    print(f"\nTranscrição concluída em: {str(elapsed_time).split('.')[0]}")
    return transcricao_com_timestamps

def enviar_ao_chatgpt(transcricao_com_timestamps):
    print("Enviando a transcrição ao ChatGPT para formatação...")

    template = """
    Treinamento Inicial realizado com Nome do Cliente

    TREINAMENTO@COMPUTADOR

    Modelo de Negócio do cliente:
    Uma descrição breve de como o cliente identifica seu negócio e sobre os processos do dia a dia. Inclua as minutagens reais baseadas na transcrição.

    Configurações Realizadas por o Cliente:
    - Configuração 1 realizada: Apenas a configuração e o número da minutagem que é citada;
    - Configuração 2 realizada: Apenas a configuração e o número da minutagem que é citada;
    - …    

    Itens abordados durante o treinamento:
    - Tópico 1: descrição resumida e a minutagem;
    - Tópico 2: descrição resumida e a minutagem;
    - …

    Comportamento do cliente durante o treinamento:
    Um bloco de texto de como foram as interações do cliente com o consultor e suas reações durante o treinamento, com as minutagens corretas;

    Alinhamento final:
    - Comprometimento 1: Ponto com breve descrição do que o cliente se comprometeu a executar, com as minutagens corretas;
    - Comprometimento 2: Ponto com breve descrição do que o cliente se comprometeu a executar, com as minutagens corretas;
    - …
    """

    transcricao_formatada = "\n".join(transcricao_com_timestamps)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente que organiza transcrições de treinamentos seguindo um modelo específico."},
                {"role": "user", "content": f"Baseado no seguinte log de treinamento com timestamps:\n\n{transcricao_formatada}\n\n{template}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erro ao enviar ao ChatGPT: {e}")
        return f"Erro ao processar a transcrição: {e}"

def iniciar_processo(input_audio_path, output_widget):
    global cancelar_processo
    cancelar_processo = False  # Reseta o estado de cancelamento
    try:
        # Limpar o widget de saída
        output_widget.delete(1.0, tk.END)

        converted_audio_path = "./audio_convertido.wav"

        # Verificar se o arquivo já existe
        verificar_arquivo_convertido(converted_audio_path)

        # Converter o arquivo
        converter_mp4_para_wav(input_audio_path, converted_audio_path)

        # Transcrever o áudio
        transcricao_com_timestamps = transcrever_audio_com_timestamps(converted_audio_path)

        if cancelar_processo:
            print("Processo cancelado pelo usuário.")
            return

        # Enviar ao ChatGPT
        resposta_gpt = enviar_ao_chatgpt(transcricao_com_timestamps)

        # Caminho para a área de trabalho e a pasta de transcrições
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pasta_transcricoes = os.path.join(desktop_path, "Transcrições Realizadas")

        # Verifica se a pasta "Transcrições Realizadas" existe, caso contrário, cria
        if not os.path.exists(pasta_transcricoes):
            os.makedirs(pasta_transcricoes)

        # Caminho completo para salvar o arquivo .txt dentro da pasta criada
        base_name = os.path.basename(input_audio_path).replace(".mp4", "")
        caminho_arquivo_txt = os.path.join(pasta_transcricoes, f"{base_name}_resposta_formatada.txt")

        # Salvar resultado no arquivo
        with open(caminho_arquivo_txt, "w", encoding="utf-8") as arquivo:
            arquivo.write(resposta_gpt)

        print(f"Resposta formatada salva em: {caminho_arquivo_txt}")

        # Excluir o arquivo .wav temporário após salvar
        if os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)
            print(f"Arquivo temporário {converted_audio_path} excluído com sucesso.")

    except Exception as e:
        print(f"Erro ao processar: {e}")

def cancelar_processo_button():
    global cancelar_processo
    cancelar_processo = True

def escolher_arquivo(output_widget):
    filepath = filedialog.askopenfilename(filetypes=[("Arquivos de Áudio", "*.mp4;*.wav")])
    if filepath:
        threading.Thread(target=iniciar_processo, args=(filepath, output_widget), daemon=True).start()

# Interface Gráfica
def criar_interface():
    app = tk.Tk()
    app.title("Transcrição de Áudio")
    app.geometry("600x600")
    app.configure(bg="#833AB4")

    style = ttk.Style()
    style.configure("TButton", background="#833AB4", foreground="black", font=("Comfortaa ", 12), padding=10)
    style.map("TButton", background=[("active", "#833AB4")])

    label = tk.Label(app, text="Transcrição de Áudio", font=("Comfortaa ", 16, "bold"), bg="#833AB4", fg="white")
    label.pack(pady=10)

    output_widget = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Comfortaa ", 12), bg="#EDEDED", fg="black", height=20)
    output_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    button_frame = tk.Frame(app, bg="#833AB4")
    button_frame.pack(pady=20)

    botao_selecionar = ttk.Button(button_frame, text="Selecionar Arquivo", command=lambda: escolher_arquivo(output_widget))
    botao_selecionar.grid(row=0, column=0, padx=10)

    botao_cancelar = ttk.Button(button_frame, text="Cancelar Processo", command=cancelar_processo_button)
    botao_cancelar.grid(row=0, column=1, padx=10)

    sys.stdout = RedirectedOutput(output_widget)

    app.mainloop()

if __name__ == "__main__":
    criar_interface()
