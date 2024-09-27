#!/usr/bin/env python
import sys
import os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk

# The `GTK_Main` class sets up a simple GTK window with controls to play MPEG2 video files using
# GStreamer pipeline elements.
class GTK_Main(object):
    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Mpeg2-Player")
        window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        vbox.add(self.movie_window)
        window.show_all()
        
        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("filesrc", "file-source")
        demuxer = Gst.ElementFactory.make("mpegpsdemux", "demuxer")
        demuxer.connect("pad-added", self.demuxer_callback)
        video_decoder = Gst.ElementFactory.make("mpeg2dec", "video-decoder")
        audio_decoder = Gst.ElementFactory.make("decodebin", "audio-decoder")
        audioconv = Gst.ElementFactory.make("audioconvert", "converter")
        audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")
        videosink = Gst.ElementFactory.make("autovideosink", "video-output")
        self.queuea = Gst.ElementFactory.make("queue", "queuea")
        self.queuev = Gst.ElementFactory.make("queue", "queuev")
        colorspace = Gst.ElementFactory.make("videoconvert", "colorspace")
        
        if not source or not demuxer or not video_decoder or not audio_decoder or not audioconv or not audiosink or not videosink:
            print("Não foi possível criar todos os elementos.")
            exit(-1)
        
        self.player.add(source)
        self.player.add(demuxer)
        self.player.add(video_decoder)
        self.player.add(audio_decoder)
        self.player.add(audioconv)
        self.player.add(audiosink)
        self.player.add(videosink)
        self.player.add(self.queuea)
        self.player.add(self.queuev)
        self.player.add(colorspace)
        
        source.link(demuxer)
        
        self.queuev.link(video_decoder)
        video_decoder.link(colorspace)
        colorspace.link(videosink)
        
        self.queuea.link(audio_decoder)
        audio_decoder.link(audioconv)
        audioconv.link(audiosink)
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        
    def start_stop(self, w):
        """
        The function `start_stop` checks if a file path exists and plays the file if it does, otherwise
        it stops the player and resets the button label.
        
        :param w: In the provided code snippet, the `start_stop` method takes two parameters: `self` and
        `w`
        """
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.get_by_name("file-source").set_property("location", filepath)
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")
                
    def on_message(self, bus, message):
        """
        The `on_message` function handles different types of messages in a GStreamer pipeline, such as
        EOS and ERROR messages.
        
        :param bus: The `bus` parameter in the `on_message` function is typically a GStreamer bus
        object. The bus is used to receive messages from the pipeline, such as end-of-stream (EOS) or
        error messages. These messages can be used to handle different events in the GStreamer pipeline,
        like changing
        :param message: The `message` parameter in the `on_message` function is an object that
        represents a message received on a GStreamer bus. It contains information about the type of
        message and any associated data. In the provided code snippet, the function checks the type of
        the message (whether it is EOS or ERROR
        """
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            
    def on_sync_message(self, bus, message):
        """
        The function `on_sync_message` sets the window handle for an imagesink element in a Python
        program.
        
        :param bus: The `bus` parameter in the `on_sync_message` method represents the GStreamer bus
        that is used for communication between elements in a GStreamer pipeline. It is responsible for
        delivering messages such as errors, warnings, and state changes
        :param message: The `message` parameter in the `on_sync_message` function is an object that
        represents a message received on the bus. In this context, it is used to handle synchronization
        messages related to the video playback. The `message` object contains information about the
        message structure and its source
        """
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            xid = self.movie_window.get_property('window').get_xid()
            imagesink.set_window_handle(xid)
            
    def demuxer_callback(self, demuxer, pad):
        """
        The `demuxer_callback` function links pads based on their template names to corresponding queue
        pads.
        
        :param demuxer: The `demuxer_callback` function takes two parameters: `demuxer` and `pad`
        :param pad: The `pad` parameter in the `demuxer_callback` function is a pad object representing
        an input or output pad of a demuxer element in a GStreamer pipeline. Pads are used to connect
        elements in the pipeline and transfer data between them. In this context, the `pad`
        """
        if pad.get_property("template").name_template == "video_%02d":
            qv_pad = self.queuev.get_pad("sink")
            pad.link(qv_pad)
        elif pad.get_property("template").name_template == "audio_%02d":
            qa_pad = self.queuea.get_pad("sink")
            pad.link(qa_pad)
        
Gst.init(None)
GTK_Main()
GObject.threads_init()
Gtk.main()