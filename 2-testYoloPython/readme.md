# 🎉 2-testYoloPython

Bem-vindo ao **2-testYoloPython**! Neste projeto, exploramos a detecção de Equipamentos de Proteção Individual (PPE) utilizando a arquitetura YOLO (You Only Look Once) com Python. Vamos começar a jornada! 🚀

## 📁 Estrutura do Projeto

Aqui está a estrutura de diretórios do projeto:

```
C:.
├───data
│       imagem (2).jpg
│       imagem (3).jpg
│
├───models
│       readme.md
│
├───PPE-Detection-YOLO
│   │   .gitignore
│   │   README.md
│   │   requirements.txt
│   │
│   ├───data
│   │   ├───images
│   │   │       example_image.jpg
│   │   │
│   │   ├───models
│   │   │       PPE_Model.pt
│   │   │
│   │   └───videos
│   │           example_video.mp4
│   │
│   ├───output
│   │   └───gifs
│   │           output_video.gif
│   │
│   └───src
│           image_detection.py
│           video_detection.py
│
└───yolov8
    └───results
        ├───best
        │   └───inferencesize_640
        │           imagem (2).jpg
        │           imagem (3).jpg
        │
        ├───custom
        │   └───predict
        │           imagem (12).jpg
        │
        └───PPE
            └───inferencesize_640
                    imagem (2).jpg
                    imagem (3).jpg
```

## 🎯 Objetivo do Projeto

O objetivo deste projeto é realizar a detecção de Equipamentos de Proteção Individual (PPE) em imagens e vídeos usando o modelo YOLO. O diretório **PPE-Detection-YOLO** contém um programa que utiliza o modelo YOLO da biblioteca Ultralytics para realizar inferências de imagens.

## 🚀 Como Rodar

### 1. **Configuração do Ambiente**

Antes de executar o projeto, você precisará instalar as dependências necessárias. Use o arquivo `requirements.txt` para instalar tudo rapidamente:

```bash
pip install -r PPE-Detection-YOLO/requirements.txt
```

### 2. **Executando o Código**

Para realizar a detecção de imagens ou vídeos, utilize os scripts Python encontrados no diretório **src**.

- **Detecção em Imagens:**

```bash
python PPE-Detection-YOLO/src/image_detection.py --input data/imagem\ (2).jpg --output output/gifs/output_video.gif
```

- **Detecção em Vídeos:**

```bash
python PPE-Detection-YOLO/src/video_detection.py --input PPE-Detection-YOLO/data/videos/example_video.mp4 --output output/gifs/output_video.gif
```

### 3. **Resultados**

Os resultados das inferências serão armazenados na pasta `output/gifs`, onde você pode visualizar as detecções realizadas.

## 🔍 Modelos Utilizados

No diretório **yolov8/results**, você encontrará as saídas de testes com diferentes modelos YOLO para a detecção de PPE. A estrutura inclui resultados das inferências, bem como imagens e vídeos de exemplo para validação.


## 📚 Referências

- [YOLOv8](https://github.com/ultralytics/yolov5)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)

