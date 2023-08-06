# coding: UTF-8

import cStringIO

import cairo
import pango
import pangocairo


def getPngImage():
    canvas_width = 200
    canvas_height = 200
    text = u"hogehoge"

    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, canvas_width, canvas_height)
    context = cairo.Context(surface)

    context.rectangle(0, 0, canvas_width, canvas_height)
    context.set_source_rgb(1, 1, 1)
    context.fill()

    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    layout = pangocairo_context.create_layout()
    font = pango.FontDescription("Sans 14")
    layout.set_font_description(font)

    layout.set_text(text)
    context.set_source_rgb(1, 0, 0)
    (w, h) = [e / pango.SCALE for e in layout.get_size()]
    context.translate((canvas_width - w) / 2, (canvas_height - h) / 2)
    pangocairo_context.update_layout(layout)
    pangocairo_context.show_layout(layout)

    buf = cStringIO.StringIO()
    surface.write_to_png(buf)
    img = buf.getvalue()
    buf.close()
    return img



input_ = bytearray(open("cairo_text.png", "rb").read())
output = png_resize(input_, (150, 150))

#img = getPngImage()
with open("cairo_text2.png", "wb") as image_file:
    image_file.write(output)
