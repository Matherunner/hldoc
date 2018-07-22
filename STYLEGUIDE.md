# STYLE GUIDE FOR HLPR

## General

Note that 1 px = 0.75 pt on the web as defined [here](https://www.w3.org/TR/css3-values/#absolute-lengths), but 1 px = 1 pt in Illustrator. Convert appropriately. The web is always assumed to be in 96 ppi as implied in the document.

## Images

All images should be captioned.

All PNG files must be optimised by the `optipng` program.

All GIF files must be optimised using the provided `optigif` script.

All SVG files must be optimised using the `svgo` program.

Images should preferably not exceed 625px in width. The height should preferably be within a screen height, but for some diagrams such as flow charts exceeding one screen is unavoidable.

### Screenshots

Photos or screenshots should be served in JPEG format. While 2x resolution is desirable, this requirement is optional if the degradation in quality is not too severe. If 2x resolution is used, the :scale: 50% attribute must be specified.

### Technical drawings

Recommended drawing programs:

- Adobe Illustrator (general purpose, and essential for producing SVGs with embedded fonts)
- OmniGraffle (for flowcharts)
- TikZ (for mathematical and precise drawings, and possibly flowcharts)
- Asymptote/Metapost (alternative to TikZ)
- matplotlib (for graphs)

Drawings should be ideally served be as SVG files. This is so that a line that is supposed to be 1px thick will actually appear so. If PNG is created, the line widths will be scaled up instead.

The background should usually be transparent unless a different background colour has a significant meaning or provides clearer presentation.

Texts should generally be set in Baskerville or its variants.

Arrowheads should preferrably be "Arrow 9" in Illustrator.

Lines should have a minimum stroke width of 1px.

Dotted lines should have 2px dashes and 2px gaps.

Font sizes in SVG files must be specified at 125% of the intended web `pt` size for reasons already explained earlier. For example, if a text of size 13pt is desired, it must be specified at 17pt in Illustrator.

Use the provided `hlpr.ait` template if Illustrator is used. To create flowcharts, it's recommended to use OmniGraffle and `hlpr-flowchart.gtemplate`.

If other vector graphics programs are used, unless they support converting text to outline *at the export step*, independent of source file, do not export SVGs from them. Instead, export to PDF or EPS, and then export as SVG from Illustrator.

To output an SVG file in Illustrator, go to Files -> Export -> Export for Screens, then:

- select "Full Document"
- untick "Open Location after Export"
- click on the gear icon to go to settings, go to SVG, then
  - select "Convert To Outlines" for Font
  - select "Embed" for Images
  - select "Minimal" for Object IDs
  - untick "Responsive"
- make sure there is only one entry for "Formats", and the format is "SVG"

The "Convert To Outlines" is crucial to allow the SVG to be read everywhere. Note that we must not embed any fonts because the `<font>` attribute has very limited browser support at the time of writing. The output SVG must then be processed using the `svgo` to further reduce the file size. In case Illustrator makes this feature difficult, or if Illustrator is not available, ghostscript has a `-dNoOutputFonts` parameter for PDFs.

#### TikZ

Always use `bp` instead of `pt` whenever TeX is involved. This is very important.

### Font size series

13, 16

