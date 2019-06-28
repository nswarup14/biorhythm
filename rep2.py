import gi
gi.require_version('Gtk', '3.0')
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

        self.figure = Figure()
        self._plot = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.sine = False
        self.replot()

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)

        container = Gtk.Box()
        container.pack_start(self._plot, True, True, 0)
        container.pack_start(button, False, True, 0)

        self.add(container)

        self.show_all()

    def replot(self):
        self.axes.clear()
        t = np.arange(0.0, 3.0, 0.01)
        if self.sine:
            s = np.sin(2*np.pi*t)
        else:
            s = np.cos(2*np.pi*t)
        self.axes.plot(t, s)
        self._plot.queue_draw()

    def on_click_me_clicked(self, btn):
        self.sine = not self.sine
        self.replot()


if __name__ == "__main__":
    win = Window()
    Gtk.main()