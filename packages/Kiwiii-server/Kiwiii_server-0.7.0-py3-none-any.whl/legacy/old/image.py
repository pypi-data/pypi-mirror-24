#coding: UTF-8

"""
Image util module
"""

import io
import cairo
from gi.repository import Pango
from gi.repository import PangoCairo


def resize_by_height(raw_img, height):
    """Proportional resize by height (width is floored)

    Args:
      raw_img: bytearray of PNG format data
      height: int
    Returns:
      bytearray of resized image
    """
    input_ = io.StringIO(raw_img)
    input_.seek(0)  # rewind
    surface = cairo.ImageSurface.create_from_png(input_)
    input_.close()
    size = (surface.get_width(), surface.get_height())
    scale = height / float(size[1])
    new_surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, int(size[0] * scale), height)
    ctx = cairo.Context(new_surface)
    ctx.scale(scale, scale)
    ctx.set_source_surface(surface, 0, 0)
    ctx.paint()
    output = io.StringIO()
    new_surface.write_to_png(output)
    resized_img = bytearray(output.getvalue())
    output.close()
    return resized_img


def get_size(raw_img):
    """Get size of the image

    Args:
      raw_img: bytearray of PNG format data
    Returns:
      width, height
    """
    input_ = io.StringIO(raw_img)
    input_.seek(0)  # rewind
    surface = cairo.ImageSurface.create_from_png(input_)
    input_.close()
    return surface.get_width(), surface.get_height()


def render_text(string, size, fontstyle="Sans 14", fontcolor=(1, 0, 0)):
    """Generate rectangle image with text

    Args:
      string: text to be rendered
      size: (width, height)
    Returns:
      bytearray of PNG image
    """
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, size[0], size[1])
    context = cairo.Context(surface)

    context.rectangle(0, 0, size[0], size[1])
    context.set_source_rgb(1, 1, 1)
    context.fill()

    pangocairo_context = PangoCairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    layout = pangocairo_context.create_layout()
    font = Pango.FontDescription(fontstyle)
    layout.set_font_description(font)

    layout.set_text(string)
    context.set_source_rgb(*fontcolor)
    (w, h) = [e / Pango.SCALE for e in layout.get_size()]
    context.translate((size[0] - w) / 2, (size[1] - h) / 2)
    pangocairo_context.update_layout(layout)
    pangocairo_context.show_layout(layout)

    buf = io.StringIO()
    surface.write_to_png(buf)
    img = bytearray(buf.getvalue())
    buf.close()
    return img


def main():
    with open("cairo_text.png", "wb") as image_file:
        image_file.write(render_text("ほげほげ", (300, 300)))

    #data = bytearray(open("cairo_text2.png", "rb").read())
    #output = resize_by_height(data, 150)
    #with open("cairo_text3.png", "wb") as image_file:
    #    image_file.write(output)

if __name__ == "__main__":
    main()
