# 🎉 Projetos de DeepStream e Detecção com YOLO

Bem-vindo ao repositório de projetos que explorei durante meu aprendizado em DeepStream da NVIDIA e detecção de objetos com YOLO! Aqui você encontrará três projetos, cada um focando em técnicas de inferência de imagem e vídeo usando tecnologias avançadas de inteligência artificial. Vamos dar uma olhada em cada um deles! 🚀

## 📁 Estrutura do Repositório

```
C:.
├───0-testDeepstreamCLI
│       (Conteúdo do primeiro projeto)
│
├───1-deepstreamPythonApps
│       (Conteúdo do segundo projeto)
│
└───2-testYoloPython
        (Conteúdo do terceiro projeto)
```

## 🔍 Projetos

### 0-testDeepstreamCLI

Neste projeto, eu aprendi a executar o DeepStream usando o comando CLI `deepstream-app`. Ele inclui exemplos do SDK com 30 e 4 fontes de vídeo, além de um pipeline personalizado que desenvolvi do zero. Você encontrará configurações de inferência e saída gravadas em MP4. 

- **Arquivos principais**: 
  - `deepstream_app_source1_peoplenet_mari.yml`: Arquivo de configuração para o pipeline.
  - `peoplenet_test.sh`: Script para executar o pipeline.
  - `out_people_mari.mp4`: Saída do pipeline com as inferências.

### 1-deepstreamPythonApps

Este projeto explora a integração do modelo PeopleNet no DeepStream usando Python. Ele utiliza plugins GStreamer para formar uma pipeline com duas câmeras RTSP, exibindo-as lado a lado enquanto as inferências ocorrem. O projeto inclui tutoriais e exemplos de GStreamer, que é a base para os plugins Python do DeepStream.

- **Arquivos principais**: 
  - `deepstream_test_1.py`: Script para testar a pipeline do DeepStream.
  - `mari.py`: Programa que utiliza o modelo PeopleNet.
  - `pipeline.png`: Visualização da estrutura do pipeline.

### 2-testYoloPython

Neste projeto, foco na detecção de Equipamentos de Proteção Individual (PPE) utilizando a arquitetura YOLO com Python. O projeto inclui um programa para realizar inferências em imagens e vídeos usando o modelo YOLO da biblioteca Ultralytics. Os resultados são armazenados em gifs, permitindo uma visualização clara das detecções realizadas.

- **Arquivos principais**: 
  - `image_detection.py`: Script para detecção em imagens.
  - `video_detection.py`: Script para detecção em vídeos.
  - `output/gifs/output_video.gif`: Saída da detecção.

## 🎯 Contribuições e Aprendizados

Esses projetos são o resultado de muitos testes e aprendizados sobre a aplicação de tecnologias de IA em tarefas de visão computacional. Sinta-se à vontade para explorar cada projeto, experimentar e contribuir com melhorias!
