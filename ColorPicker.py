"""
========================
Visualizing named colors
========================

Simple plot example with the named colors and its visual representation.
Left Mouse Button on color copies its name to the clipboard
Right Button: copies its HEX value (double right click copies rgb values as a string)

"""

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import matplotlib as mpl
import pyperclip

class ColorPicker():

    def __init__(self):

        #remove toolbars
        mpl.rcParams['toolbar'] = 'None'

        # get colors from matplotlib module
        self.colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

        # Sort colors by hue, saturation, value and name.
        # Source: "https://matplotlib.org/3.3.1/gallery/color/named_colors.html"
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in self.colors.items())
        self.sorted_names = [name for hsv, name in by_hsv]

        # dictionary for saving colors and coordinates in the grid
        self.color_cords = {}

        # define grid parameters
        n = len(self.sorted_names)
        self.ncols = 4
        self.nrows = n // self.ncols + 1

        # draw window
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.fig.canvas.set_window_title('Color Picker')

        # connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self)

        # draw the grid
        self.draw_color_grid()


    def draw_color_grid(self):
        # Get height and width
        X, Y = self.fig.get_dpi() * self.fig.get_size_inches()
        h = Y / (self.nrows + 1)
        w = X / self.ncols

        #iterate through sorted names list
        for i, name in enumerate(self.sorted_names):
            col = i % self.ncols
            row = i // self.ncols
            y = Y - (row * h) - h

            xi_line = w * (col + 0.05)
            xf_line = w * (col + 0.25)
            xi_text = w * (col + 0.3)

            self.ax.text(xi_text, y, name, fontsize=(h * 0.8),
                    horizontalalignment='left',
                    verticalalignment='center')

            self.ax.hlines(y + h * 0.1, xi_line, xf_line,
                      color=self.colors[name], linewidth=(h * 0.6))

            # update dictionary that will be queried by the mouse events in order to get hex and rgb values
            self.color_cords[name] = (int(xi_text), int(y+h))

        self.ax.set_xlim(0, X)
        self.ax.set_ylim(0, Y)
        self.ax.set_axis_off()

        self.fig.subplots_adjust(left=0, right=1,
                            top=1, bottom=0,
                            hspace=0, wspace=0)
        plt.show()

    # The mouse event button self.fig.canvas.mpl_connect('button_press_event', SELF) calls SELF (the main class: ColorPicker)
    # as the class is already instantiated __call__ is called instead of __init__
    def __call__(self, event):
        print(event)
        for color in self.color_cords:
            if abs(self.color_cords[color][0] - event.xdata) < 50 \
                    and abs(self.color_cords[color][1] - event.ydata - 10) < 5:
                output = ''
                if event.button == 1:
                    output = color
                elif event.button == 3:
                    if event.dblclick == 1:
                        output = str((int(mcolors.to_rgb(color)[0]*255), int(mcolors.to_rgb(color)[1]*255), int(mcolors.to_rgb(color)[2]*255)))
                    elif event.dblclick == 0:
                        output = mcolors.to_hex(color)
                print(output)
                pyperclip.copy(output)

if __name__ == '__main__':
    picker = ColorPicker()
    plt.close(fig=None)
