import sys
sys.path.append("../")
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from common.bus_call import bus_call

# Inicializar o GStreamer
Gst.init(None)

# Criar o pipeline
pipeline = Gst.Pipeline.new("pipeline")

# Criar o elemento nvmultiurisrcbin
src = Gst.ElementFactory.make("nvmultiurisrcbin", "src")
src.set_property("port", 9000)
src.set_property("ip-address", "localhost")
src.set_property("batched-push-timeout", 33333)
src.set_property("max-batch-size", 10)
src.set_property("drop-pipeline-eos", 1)
src.set_property("live-source", 1)
uri_list = "file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_1080p_h264.mp4,file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_1080p_h265.mp4"
src.set_property("uri-list", uri_list)
# src.set_property("enable-padding", True)
src.set_property("width", 920)
src.set_property("height", 420)
pipeline.add(src)

# Criar o elemento nvmultistreamtiler
tiler = Gst.ElementFactory.make("nvmultistreamtiler", "tiler")
tiler.set_property("square-seq-grid", True)
tiler.set_property("width", 920)  # Largura da saída em pixels
tiler.set_property("height", 580)  # Altura da saída em pixels

pipeline.add(tiler)
src.link(tiler)

# Criar o elemento nveglglessink
sink = Gst.ElementFactory.make("nveglglessink", "sink")
pipeline.add(sink)
tiler.link(sink)

loop = GLib.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_call, loop)

# Iniciar o pipeline
print("Now playing...")
pipeline.set_state(Gst.State.PLAYING)

# Rodar o loop principal
try:
    loop.run()
except:
    pass
# cleanup
print("Exiting app\n")
pipeline.set_state(Gst.State.NULL)


# # Definir as URIs dos vídeos
# uris = [
#     "file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_720p.mp4",
#     "file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_1080p_h264.mp4"
# ]





# import threading
# import sys
# sys.path.append('../')
# import gi
# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GLib

# Gst.init(None)

# def on_pad_added(decodebin, pad, sink):
#     print(f"New pad added: {pad.get_name()}")
#     caps = pad.query_caps(None)
#     name = caps.to_string()
    
#     print(name)
#     if name.startswith("video/"):
#         sink_pad = sink.get_static_pad("sink")
#         pad.link(sink_pad)

# def run_pipeline(uri):
#     pipeline = Gst.Pipeline.new("pipeline")
#     source = Gst.ElementFactory.make("uridecodebin", "source")
#     source.props.uri = uri

#     sink = Gst.ElementFactory.make("nveglglessink", "sink")
#     source.connect("pad-added", on_pad_added, sink)

#     pipeline.add(source)
#     pipeline.add(sink)

#     pipeline.set_state(Gst.State.PLAYING)
#     loop = GLib.MainLoop()
#     loop.run()

# # Rodar dois pipelines em paralelo
# uri1 = "file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_720p.mp4"
# uri2 = "file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_1080p_h264.mp4"

# thread1 = threading.Thread(target=run_pipeline, args=(uri1,))
# thread2 = threading.Thread(target=run_pipeline, args=(uri2,))

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()




# import sys
# sys.path.append('../')
# import gi
# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GLib

# Gst.init(None)

# def on_pad_added(decodebin, pad, converter):
#     print(f"New pad added: {pad.get_name()}")
#     caps = pad.query_caps(None)
#     name = caps.to_string()
    
#     print(name)
#     if name.startswith("video/"):
#         sink_pad = converter.get_static_pad("sink")
#         if not sink_pad.is_linked():
#             pad.link(sink_pad)

# pipeline = Gst.Pipeline.new("pipeline")
# source = Gst.ElementFactory.make("uridecodebin", "source")
# source.props.uri = "https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm"
# queue = Gst.ElementFactory.make("queue", "queue")
# decoder = Gst.ElementFactory.make('avdec_h264', "decoder")
# converter = Gst.ElementFactory.make('videoconvert', "converter")
# capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
# caps = Gst.Caps.from_string("video/x-raw, format=I420")
# capsfilter.set_property("caps", caps)
# sink = Gst.ElementFactory.make("autovideosink", "sink")

# if not pipeline or not source or not queue or not decoder or not converter or not capsfilter or not sink:
#     print("Not all elements could be created.")
#     sys.exit(1)

# pipeline.add(source)
# pipeline.add(queue)
# pipeline.add(decoder)
# pipeline.add(converter)
# pipeline.add(capsfilter)
# pipeline.add(sink)

# source.connect("pad-added", on_pad_added, queue)
# queue.link(decoder)
# decoder.link(converter)
# converter.link(capsfilter)
# capsfilter.link(sink)

# ret = pipeline.set_state(Gst.State.PLAYING)
# if ret == Gst.StateChangeReturn.FAILURE:
#     print("Unable to set the pipeline to the playing state.")
#     sys.exit(1)

# loop = GLib.MainLoop()
# loop.run()





# # (Request Pads)
# import gi
# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GObject

# Gst.init(None)

# pipeline = Gst.Pipeline.new("pipeline")
# source = Gst.ElementFactory.make("videotestsrc", "source")
# tee = Gst.ElementFactory.make("tee", "tee")
# queue1 = Gst.ElementFactory.make("queue", "queue1")
# queue2 = Gst.ElementFactory.make("queue", "queue2")
# sink1 = Gst.ElementFactory.make("autovideosink", "sink1")
# sink2 = Gst.ElementFactory.make("autovideosink", "sink2")

# pipeline.add(source)
# pipeline.add(tee)
# pipeline.add(queue1)
# pipeline.add(queue2)
# pipeline.add(sink1)
# pipeline.add(sink2)

# source.link(tee)
# tee.link(queue1)
# tee.link(queue2)
# queue1.link(sink1)
# queue2.link(sink2)

# pipeline.set_state(Gst.State.PLAYING)
# GObject.MainLoop().run()


