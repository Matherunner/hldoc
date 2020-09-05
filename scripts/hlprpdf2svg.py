#!/usr/bin/env python

import os
import inkex
import inkex.command

class MyExtension(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--file', help='File name to save the plain SVG')

    def effect(self):
        if not self.options.file:
            inkex.errormsg('Please specify an output file')
            return

        scale = self.svg.uutounit(1, 'px')
        new_width = self.svg.width * scale
        new_height = self.svg.height * scale
        self.svg.set('viewBox', '0 0 {} {}'.format(new_width, new_height))
        self.svg.set('width', new_width)
        self.svg.set('height', new_height)
        self.document = inkex.load_svg(
            inkex.command.inkscape_command(
                self.svg, verbs=['FitCanvasToDrawing']))

        try:
            # Need to remove existing file or write_svg will fail silently
            os.remove(self.options.file)
        except:
            pass
        inkex.command.write_svg(self.document, self.options.file)

if __name__ == '__main__':
    MyExtension().run()
