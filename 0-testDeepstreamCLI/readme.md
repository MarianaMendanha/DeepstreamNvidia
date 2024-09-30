# 🚀 0-testDeepstreamCLI

Bem-vindo ao **0-testDeepstreamCLI**! Este projeto foi criado enquanto eu aprendia a usar o DeepStream da NVIDIA para rodar aplicativos de inferência em vídeo. Vamos mergulhar nos detalhes! 🌊

## 📁 Estrutura do Projeto

Aqui está a estrutura de diretórios do projeto:

```
C:.
├───mari
│       deepstream_app_source1_peoplenet_mari.yml
│       out_people_2.mp4
│       out_people_mari.mp4
│       peoplenet_test.sh
│       readme.md
│       source_tao_app_mari.csv
│
└───modifiedSamples
    ├───30sources-sample
    │       source30_1080p_dec_infer-resnet_tiled_display_int8.yml
    │       source30_1080p_dec_preprocess_infer-resnet_tiled_display_int8.txt
    │       sources_30.csv
    │
    ├───4sources-sample
    │       source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.yml
    │       source4_1080p_dec_preprocess_infer-resnet_preprocess_sgie_tiled_display_int8.txt
    │       sources_4.csv
    │
    ├───config
    │       config_infer_primary.txt
    │       config_infer_primary.yml
    │       config_infer_secondary_vehiclemake.txt
    │       config_infer_secondary_vehiclemake.yml
    │       config_infer_secondary_vehicletypes.txt
    │       config_infer_secondary_vehicletypes.yml
    │       config_tracker_IOU.yml
    │       config_tracker_NvDCF_accuracy.yml
    │       config_tracker_NvDCF_max_perf.yml
    │       config_tracker_NvDCF_perf.yml
    │       config_tracker_NvDeepSORT.yml
    │       config_tracker_NvSORT.yml
    │
    └───output
            out.mp4
```

## 🎯 Objetivo do Projeto

Este projeto demonstra como rodar o DeepStream utilizando o comando CLI `deepstream-app`. Eu selecionei dois exemplos do SDK: um com **30 fontes de vídeo** e outro com **4 fontes**. Sugiro que depois de conseguir rodar um app com sucesso, modifique os parâmetros do arquivo ``source.yml`` e veja o que isso altera no produto final. Olhe a documentação ou outros exemplos dentro do deepstream para saber o que cada parâmetro significa. 

## 🛠️ Como Rodar

### 1. **Configuração do Ambiente**

Certifique-se de que você está **dentro do container DeepStream** para que o projeto funcione corretamente. 

### 2. **Alteração de Paths no YAML**

Os caminhos dentro do arquivo `deepstream_app_source1_peoplenet_mari.yml` devem ser ajustados de acordo com a posição do seu app `mari` no projeto. Por exemplo, a linha:

```yaml
config-file: ../nvinfer/config_infer_primary_peoplenet.yml
```

deve apontar para o arquivo `config_infer_primary_peoplenet.yml` com relação à posição do arquivo `.yml`.

### 3. **Executando o Pipeline**

Para rodar o seu pipeline personalizado, use o arquivo `peoplenet_test.sh`, que contém o seguinte comando:

```bash
deepstream-app -c deepstream_app_source1_peoplenet_mari.yml
```

🎉 E pronto! Agora você pode visualizar a saída do seu pipeline em `out_people_mari.mp4`!

## 📝 Conclusão

Espero que este README tenha ajudado você a entender como usar o DeepStream com o comando CLI. Divirta-se explorando a inferência de vídeo! 🎥✨

