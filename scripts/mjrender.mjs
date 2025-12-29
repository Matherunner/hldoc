import fs from 'fs'

import { minify as minifyHTML } from 'html-minifier-terser'

import { mathjax } from '@mathjax/src/js/mathjax.js';
import { TeX } from '@mathjax/src/js/input/tex.js';
import { CHTML } from '@mathjax/src/js/output/chtml.js';
import { liteAdaptor } from '@mathjax/src/js/adaptors/liteAdaptor.js';
import { RegisterHTMLHandler } from '@mathjax/src/js/handlers/html.js';
import '@mathjax/src/js/util/asyncLoad/esm.js';

import '@mathjax/src/js/input/tex/base/BaseConfiguration.js';
import '@mathjax/src/js/input/tex/ams/AmsConfiguration.js';
import '@mathjax/src/js/input/tex/newcommand/NewcommandConfiguration.js';
import '@mathjax/src/js/input/tex/noundefined/NoUndefinedConfiguration.js';

async function main() {
    const adaptor = liteAdaptor();
    RegisterHTMLHandler(adaptor);

    const files = process.argv.slice(2)
    for (const file of files) {
        console.log(`Server-side rendering of ${file}...`)

        const htmlFile = fs.readFileSync(file, 'utf-8')

        const tex = new TeX({
            packages: ['base', 'ams', 'newcommand', 'noundefined'],
            formatError(jax, err) { console.error(err.message); return jax.formatError(err) },
        })
        const chtml = new CHTML({
            fontURL: 'https://cdn.jsdelivr.net/npm/@mathjax/mathjax-newcm-font/chtml/woff2',
            displayOverflow: 'scroll',
        });

        const html = mathjax.document(htmlFile, { InputJax: tex, OutputJax: chtml })

        await html.renderPromise()

        // Remove CDN link to mathjax for unnecessary client-side rendering
        for (const elem of adaptor.head(html.document).children) {
            if (elem.kind === 'script' && elem.attributes.src?.includes('mathjax')) {
                adaptor.remove(elem)
                break
            }
        }

        var htmlStr = adaptor.doctype(html.document) + '\n' + adaptor.outerHTML(adaptor.root(html.document))

        htmlStr = await minifyHTML(htmlStr, {
            removeComments: true,
            minifyCSS: true,
            minifyJS: true,
            removeRedundantAttributes: true,
            removeScriptTypeAttributes: true,
            removeStyleLinkTypeAttributes: true,
        })

        fs.writeFileSync(file, htmlStr)
    }
}

main()
