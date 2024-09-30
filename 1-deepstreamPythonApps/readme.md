# 🌟 1-deepstreamPythonApps

Bem-vindo ao **1-deepstreamPythonApps**! Neste projeto, exploramos como usar o DeepStream da NVIDIA com Python para construir aplicativos de inferência em vídeo de forma eficiente. Vamos conferir os detalhes! 🎉

## 📁 Estrutura do Projeto

Aqui está a estrutura de diretórios do projeto:

```
C:.
│   readme.md
│
├───mari-deepstream-app
│   │   config_infer_primary_mari.txt
│   │   config_infer_primary_peoplenet.yml
│   │   deepstream_test_1.py
│   │   mari.py
│   │   out_people_mari.mp4
│   │   pipeline.png
│   │   pipeline_dot.dot
│   │   README
│   │
│   └───peopleNet
│           labels.txt
│           nvinfer_config.txt
│           resnet34_peoplenet_int8.onnx
│           resnet34_peoplenet_int8.onnx_b1_gpu0_int8.engine
│           resnet34_peoplenet_int8.onnx_b2_gpu0_int8.engine
│           resnet34_peoplenet_int8.onnx_b4_gpu0_int8.engine
│           resnet34_peoplenet_int8.txt
│
└───mari-learn-gstreamer
        audio-video-tutorial.py
        basic-tutorial-2.py
        basic-tutorial-3.py
        basic-tutorial-4.py
        basic-tutorial-5.py
        out.mp4
        pads-examples.py
```

## 🎯 Objetivo do Projeto

Este projeto é dividido em duas partes principais:

1. **mari-deepstream-app**: Um aplicativo que utiliza o modelo **PeopleNet** dentro do DeepStream e plugins GStreamer para criar um pipeline que exibe duas câmeras RTSP do escritório lado a lado, enquanto realiza inferências nas imagens.
2. **mari-learn-gstreamer**: Uma coleção de tutoriais e exemplos da documentação do GStreamer, que serve como base para os plugins Python do DeepStream e funcionam de maneira similar. Você pode conferir a documentação [aqui](https://gstreamer.freedesktop.org/documentation/tutorials/basic/index.html?gi-language=python). 📚

## 🛠️ Como Rodar

### 1. **Configuração do Ambiente**

Certifique-se de ter o **DeepStream SDK** e o **GStreamer** instalados corretamente. 

### 2. **Executando o Aplicativo DeepStream**

Para rodar o aplicativo que utiliza o modelo PeopleNet, você deve usar o arquivo `mari.py` ou `deepstream_test_1.py`. Abaixo está um exemplo de como executar o aplicativo:

```bash
python mari.py
```

### 3. **Visualizando a Pipeline**

A estrutura da pipeline que foi criada pode ser visualizada no arquivo `pipeline.png`. Aqui você pode ver como as câmeras estão conectadas e como as inferências estão sendo realizadas.

### 4. **Tutoriais GStreamer**

No diretório **mari-learn-gstreamer**, você encontrará vários tutoriais básicos que podem ajudá-lo a entender melhor como funciona o GStreamer. Cada arquivo contém exemplos práticos que podem ser executados diretamente!

## 🔗 Referências

- [DeepStream Python Apps GitHub](https://github.com/NVIDIA-AI-IOT/deepstream_python_apps)
- [Introdução aos Plugins do DeepStream](https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_plugin_Intro.html)

