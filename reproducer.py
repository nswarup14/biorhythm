import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_default_size(1200, 800)
        self.set_title("Reproducer")

        self.connect("delete-event", Gtk.main_quit)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self._plot = FigureCanvas(self.figure)
        self._plot.set_size_request(800, 600)
        self.axes = self.figure.add_subplot(111)

        self.click = False

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)

        container = Gtk.Box()
        container.pack_start(self._plot, True, True, 0)
        container.pack_start(button, False, True, 0)

        self._plot.connect("draw", self._draw_cb)

        sw = Gtk.ScrolledWindow()
        sw.set_border_width(10)
        sw.add_with_viewport(container)
        self.add(sw)
        self.show_all()

    def _draw_cb(self, widget, cr):
        self.axes.clear()
        t = np.arange(0.0, 3.0, 0.01)
        if self.click:
            s = np.sin(2*np.pi*t)
        else:
            s = np.cos(2*np.pi*t)
        self.axes.plot(t, s)

    def on_click_me_clicked(self, btn):
        self._plot.queue_draw()
        if self.click:
            self.click = False
        else:
            self.click = True


if __name__ == "__main__":
    win = Window()
    Gtk.main()