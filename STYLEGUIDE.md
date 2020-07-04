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

### Generating SVG from PDF

The following method generates the smallest SVG files, while ensuring maximal browser compatibility by not using any advanced SVG features. The downside is the reliance of a proprietary software, Adobe Illustrator. In addition, as texts are outlined, if the graphic contains many characters, the file size can increase greatly.

1. Open Adobe Illustrator 2017
2. Open the PDF
3. Check that the width of the image is within limits
4. Go to File -> Export -> Export for Screens...
5. Choose output directory as `images/`
6. Choose "Full Document" under "Select"
7. Choose "SVG" as the only entry under Formats
8. Click on the gear icon to access SVG settings, set "Styling" to "Internal CSS", "Font" to "Convert to Outlines", "Images" to "Embed", "Object IDs" to "Minimal", "Decimal" to "2", and **un-check "Responsive"**.
9. Click "Export Artboard"
10. Double-check that the `width` attribute in the `svg` tag is within limits
11. Run `svgo` on the generated SVG

Steps 5 to 8 need to be done only once, unless the settings have been modified.

The "Convert To Outlines" is crucial to allow the SVG to be read everywhere. Note that we must not embed any fonts because the `<font>` attribute has very limited browser support at the time of writing. The output SVG must then be processed using the `svgo` to further reduce the file size. In case Illustrator makes this feature difficult, or if Illustrator is not available, ghostscript has a `-dNoOutputFonts` parameter for PDFs.

Alternatively, if Adobe Illustrator is not available:

1. Open Inkscape 0.9
2. Open the PDF, choose "Poppler/Cairo import" (do not use "Internal import" as the text will be messed up)
3. Go to File -> Document Properties..., set "Scale x" to 1 for "User units per px", then click "Resize page to drawing or selection" (in that order)
4. Check that the width of the image is within limits *in px*
5. Go to File -> Save As..., choose "Plain SVG" as the format
6. Run `svgo --multipass -p 2` on the generated SVG

The file size generated using this method will tend to be bigger. Nevertheless, each glyph is defined as a `<symbol>` and reused throughout by Inkscape, which implies that an image with many characters may be able to keep the file size small, compared to the Illustrator method. That is, as the number of characters increases, there may be a point at which Inkscape would generate smaller files than Illustrator.

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

Font sizes in SVG files must be specified at 125% of the intended web `pt` size for reasons already explained earlier. For example, if a text of size 13pt is desired, it must Abe specified at 17pt in Illustrator.

Use the provided `hlpr.ait` template if Illustrator is used. To create flowcharts, it's recommended to use OmniGraffle and `hlpr-flowchart.gtemplate`.

If other vector graphics programs are used, unless they support converting text to outline *at the export step*, independent of source file, do not export SVGs from them. Instead, export to PDF or EPS, and then export as SVG from Illustrator.

#### TikZ

Always use `bp` instead of `pt` whenever TeX is involved. This is very important.

Standard procedure for preparing a TikZ graphic:

1. Make sure Baskerville 10 Pro and Dark Modern typefaces are installed
2. Create a `.tex` file under `imgsrc/`
3. Use the `imgsrc/templates/hlprtikz` document class
4. Generate PDF by running with `lualatex`
5. Generate the production SVG by standard methods

#### Flowcharts

Draw flowcharts using TikZ or OmniGraffle only. There are a few guidelines to the style of flowcharts:

1. Flow charts should not have boxes drawn around them. While this runs counter how "professional" flowcharts are usually drawn, it has the benefits of reducing visual noise and make the entire figure more compact. Flowcharts may contain many nodes, and putting boxes in every node will dramatically bloat the size of the figure for little good. Another minor reason is that, while standardisation organisations like ISO has defined the meaning of different shapes in a flowchart, unless you are a flowchart expert, or made conscious effort to learn them, or are forced to learn them at some point, you wouldn't be able to tell the difference in meaning between a normal rectangle and a parallelogram, or a circle and a rounded rectangle.

2. Always expand vertically, never horizontally, because the screen is meant to be scrolled vertically. Go in horizontal directions only for short branches.

3. Prefer drawing arrows in horizontal or vertical directions. Diagonal arrows may be used for short branches.

4. If there is a need to loop back, and there are multiple points at which this can happen, draw a big continuous arrow starting the *lowest* node that loops back, and for all the nodes above that loop back, draw a horizontal arrow that touches the big arrow.


%%%%% NOTE: only put "on grid" for nodes that are left or right of, otherwise don't
  %%%%% Also, don't use "start branch", it just doesn't work well
  %%%%% If branching out and need to change direction, specify continue chain for the second node, or on chain on second and all the rest

  %%%%% Use near start for "yes" and "no"

### Screenshots

In game screenshots should have higher exposures, warmer tint, slightly desaturated, and sharpened. None of these effects should be overdone. The rationale is for the screenshots to fit the background colour of the documentation.

### Font size series

13, 16

### TikZ animations

Tikz animations can be created by generating a PDF with multiple pages, each page representing one frame, and then extracting the pages out into PNG files with ImageMagick. To create a new page, simply create a new `tikzpicture` environment. To generate multiple `tikzpicture` blocks iteratively, surround a `tikzpicture` with a `\foreach` construct. This is valid because `\foreach` is more powerful than repeating some draw commands -- it's a full-fledged command provided by `pgffor` that is independent of `tikzpicture`, and you can put anything inside the curly braces.

