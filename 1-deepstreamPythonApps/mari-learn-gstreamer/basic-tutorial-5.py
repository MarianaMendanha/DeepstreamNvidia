##### WORKING
import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main():
    # Inicializando GStreamer
    Gst.init(None)

    # Criando os elementos
    audio_source = Gst.ElementFactory.make("audiotestsrc", "audio_source")
    tee = Gst.ElementFactory.make("tee", "tee")
    audio_queue = Gst.ElementFactory.make("queue", "audio_queue")
    audio_convert = Gst.ElementFactory.make("audioconvert", "audio_convert")
    audio_resample = Gst.ElementFactory.make("audioresample", "audio_resample")
    audio_sink = Gst.ElementFactory.make("autoaudiosink", "audio_sink")
    video_queue = Gst.ElementFactory.make("queue", "video_queue")
    visual = Gst.ElementFactory.make("wavescope", "visual")
    video_convert = Gst.ElementFactory.make("videoconvert", "csp")
    video_sink = Gst.ElementFactory.make("autovideosink", "video_sink")

    # Criando o pipeline vazio
    pipeline = Gst.Pipeline.new("test-pipeline")

    if not pipeline or not audio_source or not tee or not audio_queue or not audio_convert or not audio_resample or not audio_sink or not video_queue or not visual or not video_convert or not video_sink:
        print("Not all elements could be created.")
        return -1

    # Configurando os elementos
    audio_source.set_property("freq", 215.0)
    visual.set_property("shader", 0)
    visual.set_property("style", 1)

    # Adicionando e vinculando os elementos que podem ser automaticamente vinculados porque eles têm pads "Always"
    pipeline.add(audio_source)
    pipeline.add(tee)
    pipeline.add(audio_queue)
    pipeline.add(audio_convert)
    pipeline.add(audio_resample)
    pipeline.add(audio_sink)
    pipeline.add(video_queue)
    pipeline.add(visual)
    pipeline.add(video_convert)
    pipeline.add(video_sink)

    if not audio_source.link(tee):
        print("Elements could not be linked.")
        return -1

    if not audio_queue.link(audio_convert) or not audio_convert.link(audio_resample)  or not audio_resample.link(audio_sink):
        print("Elements could not be linked.")
        return -1

    if not video_queue.link(visual) or not visual.link(video_convert) or not video_convert.link(video_sink):
        print("Elements could not be linked.")
        return -1

    # Vinculando manualmente o Tee, que tem pads "Request"
    tee_audio_pad = tee.request_pad_simple("src_%u")
    print("Obtained request pad %s for audio branch." % tee_audio_pad.get_name())
    queue_audio_pad = audio_queue.get_static_pad("sink")
    tee_video_pad = tee.request_pad_simple("src_%u")
    print("Obtained request pad %s for video branch." % tee_video_pad.get_name())
    queue_video_pad = video_queue.get_static_pad("sink")

    if tee_audio_pad.link(queue_audio_pad) != Gst.PadLinkReturn.OK or tee_video_pad.link(queue_video_pad) != Gst.PadLinkReturn.OK:
        print("Tee could not be linked.")
        return -1

    # Iniciando a reprodução do pipeline
    ret = pipeline.set_state(Gst.State.PLAYING)

    # Aguardando até erro ou EOS
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Falha ao iniciar a reprodução.")
        sys.exit(1)
    
    pipeline.set_state(Gst.State.NULL)
    # Liberando os pads de requisição do Tee, e desreferenciando-os
    tee.release_request_pad(tee_audio_pad)
    tee.release_request_pad(tee_video_pad)
    
    # Liberando recursos
    bus.unref()
    pipeline.unref()
    
    

if __name__ == '__main__':
    main()
