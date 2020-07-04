const fs = require('fs');
const { JSDOM } = require("jsdom");
const { mjpage } = require('mathjax-node-page');

/**
 * Remove the <script> tag that loads MathJax.js from the CDN.
 * @param {string} html 
 */
function removeMathJaxScript(html) {
    const dom = new JSDOM(html);
    for (const script of dom.window.document.getElementsByTagName('script')) {
        const src = script.getAttribute('src');
        if (src && src.includes('MathJax.js')) {
            script.remove();
            break;
        }
    }
    return dom.serialize();
}

async function processFile(file) {
    console.log(`Processing ${file}`);
    const content = fs.readFileSync(file).toString();
    mjpage(content, { format: ['TeX'] }, { html: true }, (output) => {
        const html = removeMathJaxScript(output);
        fs.writeFileSync(file, html);
        console.log(`${file} done`);
    })
}

async function main() {
    const files = process.argv.slice(2);

    // This is not truely multiprocessing, but it turns out running this script
    // in parallel on each of the file provides little gain.
    Promise.all(files.map(processFile));
}

main()
