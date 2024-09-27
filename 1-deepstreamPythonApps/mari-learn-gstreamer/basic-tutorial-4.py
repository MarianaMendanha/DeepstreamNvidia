import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Funções abaixo imprimem as Capacidades de forma amigável ao humano
def print_field(field, value, pfx):
    str = Gst.value_serialize(value)
    print("%s  %15s: %s" % (pfx, GLib.quark_to_string(field), str))

def print_caps(caps, pfx):
    if caps is None:
        return

    if caps.is_any():
        print("%sANY" % pfx)
        return
    if caps.is_empty():
        print("%sEMPTY" % pfx)
        return

    for i in range(caps.get_size()):
        structure = caps.get_structure(i)
        print("%s%s" % (pfx, structure.get_name()))
        structure.foreach(print_field, pfx)

# Imprime informações sobre um Pad Template, incluindo suas Capacidades
def print_pad_templates_information(factory):
    print("Pad Templates for %s:" % factory.get_longname())
    if factory.get_num_pad_templates() == 0:
        print("  none")
        return

    pads = factory.get_static_pad_templates()
    for padtemplate in pads:
        if padtemplate.direction == Gst.PadDirection.SRC:
            print("  SRC template: '%s'" % padtemplate.name_template)
        elif padtemplate.direction == Gst.PadDirection.SINK:
            print("  SINK template: '%s'" % padtemplate.name_template)
        else:
            print("  UNKNOWN!!! template: '%s'" % padtemplate.name_template)

        if padtemplate.presence == Gst.PadPresence.ALWAYS:
            print("    Availability: Always")
        elif padtemplate.presence == Gst.PadPresence.SOMETIMES:
            print("    Availability: Sometimes")
        elif padtemplate.presence == Gst.PadPresence.REQUEST:
            print("    Availability: On request")
        else:
            print("    Availability: UNKNOWN!!!")

        if padtemplate.static_caps.string is not None:
            print("    Capabilities:")
            caps = padtemplate.static_caps.get()
            print_caps(caps, "      ")

        print("\n")

# Mostra as capacidades ATUAIS do pad solicitado no elemento dado
def print_pad_capabilities(element, pad_name):
    pad = element.get_static_pad(pad_name)
    if not pad:
        print("Could not retrieve pad '%s'" % pad_name)
        return

    # Recupera capacidades negociadas (ou capacidades aceitáveis se a negociação ainda não estiver concluída)
    caps = pad.get_current_caps()
    if not caps:
        caps = pad.query_caps(None)

    # Imprime e libera
    print("Caps for the %s pad:" % pad_name)
    print_caps(caps, "      ")
    caps.unref()
    pad.unref()

def main():
    # Inicializa GStreamer
    Gst.init(None)

    # Cria as fábricas de elementos
    source_factory = Gst.ElementFactory.find("audiotestsrc")
    sink_factory = Gst.ElementFactory.find("autoaudiosink")
    if not source_factory or not sink_factory:
        print("Not all element factories could be created.")
        return -1

    # Imprime informações sobre os pad templates dessas fábricas
    print_pad_templates_information(source_factory)
    print_pad_templates_information(sink_factory)

    # Pede às fábricas para instanciar elementos reais
    source = source_factory.create("source")
    sink = sink_factory.create("sink")

    # Cria o pipeline vazio
    pipeline = Gst.Pipeline.new("test-pipeline")

    if not pipeline or not source or not sink:
        print("Not all elements could be created.")
        return -1

    # Constrói o pipeline
    pipeline.add(source)
    pipeline.add(sink)
    if not source.link(sink):
        print("Elements could not be linked.")
        return -1

    # Imprime capacidades negociadas iniciais (no estado NULL)
    print("In NULL state:")
    print_pad_capabilities(sink, "sink")

    # Começa a reprodução
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state (check the bus for error messages).")

    # Aguarda até erro, EOS ou Mudança de Estado
    bus = pipeline.get_bus()
    terminate = False
    while not terminate:
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS | Gst.MessageType.STATE_CHANGED)

        # Analisa mensagem
        if msg:
            if msg.type == Gst.MessageType.ERROR:
                err, debug_info = msg.parse_error()
                print("Error received from element %s: %s" % (msg.src.get_name(), err.message))
                print("Debugging information: %s" % (debug_info if debug_info else "none"))
                terminate = True
            elif msg.type == Gst.MessageType.EOS:
                print("End-Of-Stream reached.")
                terminate = True
            elif msg.type == Gst.MessageType.STATE_CHANGED:
                # Estamos interessados apenas em mensagens de mudança de estado do pipeline
                if msg.src == pipeline:
                    old_state, new_state, pending_state = msg.parse_state_changed()
                    print("\nPipeline state changed from %s to %s:" % (Gst.Element.state_get_name(old_state), Gst.Element.state_get_name(new_state)))
                    # Imprime as capacidades atuais do elemento sink
                    print_pad_capabilities(sink, "sink")

            msg.unref()

    # Libera recursos
    bus.unref()
    pipeline.set_state(Gst.State.NULL)
    pipeline.unref()
    source_factory.unref()
    sink_factory.unref()

if __name__ == '__main__':
    main()
