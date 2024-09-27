import sys
sys.path.append('../')
import os
import gi
gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gst, Gst, GLib
from common.bus_call import bus_call
import pyds

def pad_added_handler(src, new_pad, convert, convertvideo):
    # Obtendo o pad do sink AUDIO
    sink_pad_audio = convert.get_static_pad("sink")
    # Obtendo o pad do sink VIDEO
    sink_pad_video = convertvideo.get_static_pad("sink")
    print("Recebido novo pad '%s' de '%s':" % (new_pad.get_name(), src.get_name()))

    # Se nosso conversor já estiver conectado, não temos nada a fazer aqui
    if sink_pad_audio.is_linked() and sink_pad_video.is_linked():
        print("Já estamos conectados com audio e video. Ignorando.")
        return

    # Checando o tipo do novo pad
    new_pad_caps = new_pad.get_current_caps()
    if not new_pad_caps:
        new_pad_caps = new_pad.query_caps()
    
    new_pad_struct = new_pad_caps.get_structure(0)
    new_pad_type = new_pad_struct.get_name()

    # media = new_pad_struct.get_string("media")
    
    if new_pad_type == "audio/x-raw":
        # Tentando a conexão
        ret = new_pad.link(sink_pad_audio)
        if ret != Gst.PadLinkReturn.OK:
            print("O tipo é '%s' mas a conexão falhou." % new_pad_type)
        else:
            print("Conexão bem sucedida (tipo '%s')." % new_pad_type)
            
    elif new_pad_type == "video/x-raw":
        # Tentando a conexão
        ret = new_pad.link(sink_pad_video)
        if ret != Gst.PadLinkReturn.OK:
            print("O tipo é '%s' mas a conexão falhou." % new_pad_type)
        else:
            print("Conexão bem sucedida (tipo '%s')." % new_pad_type)
            
    print("SOURCE PAD--------------------------------------------------------------------")
    print(new_pad_caps)
    print("CONVERT SINK PAD---------------------------------------------------------------")
    print(convertvideo.get_static_pad("sink").get_current_caps())
    print("-------------------------------------------------------------------------------")
    


def main():
    # Inicializando GStreamer
    Gst.init(None)

    # Criando os elementos
    print("Criando elementos")
    source = Gst.ElementFactory.make("uridecodebin", "source")
    convert = Gst.ElementFactory.make("audioconvert", "convert")
    resample = Gst.ElementFactory.make("audioresample", "resample")
    sink = Gst.ElementFactory.make("autoaudiosink", "sink")
    
    capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
    convertvideo = Gst.ElementFactory.make("videoconvert", "convertvideo")
    sinkvideo = Gst.ElementFactory.make("autovideosink", "sinkvideo")
    

    # Criando o pipeline vazio
    print("Criando pipeline")
    pipeline = Gst.Pipeline.new("test-pipeline")
    
    # CAPS
    caps = Gst.Caps.from_string("video/x-raw, format=NV12")
    capsfilter.set_property("caps", caps)

    if not pipeline or not source or not convert or not resample or not sink or not convertvideo or not sinkvideo:
        print("Não foi possível criar todos os elementos.")
        exit(-1)

    # Construindo o pipeline. Note que NÃO estamos conectando a fonte neste
    # ponto. Faremos isso mais tarde.
    print("Construindo pipeline")
    pipeline.add(source, convert, resample, sink, convertvideo, sinkvideo)
    
    # Definindo a URI para reproduzir
    print("Setando URI")
    source.props.uri = "https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm"

    # Conectando ao sinal pad-added
    print("Conectando pad")
    source.connect("pad-added", pad_added_handler, convert, convertvideo)
    
    if not convert.link(resample) or not resample.link(sink) or not convertvideo.link(sinkvideo):
        print("Os elementos não puderam ser conectados.")
        sys.exit(1)
    
    # create an event loop and feed gstreamer bus mesages to it
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)

    # Começando a reprodução
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Não foi possível mudar o estado do pipeline para PLAYING.")
        sys.exit(1)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass
        # cleanup
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main())