const fs = require('fs');
const { JSDOM } = require("jsdom");
const { mjpage } = require('mathjax-node-page');
const htmlMinify = require('html-minifier-terser').minify;
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

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
    return new Promise(resolve => {
        const content = fs.readFileSync(file).toString();
        mjpage(content, { format: ['TeX'] }, { html: true }, (output) => {
            let html = removeMathJaxScript(output);
            html = htmlMinify(html, {
                collapseWhitespace: true,
                removeComments: true,
                minifyCSS: true,
                minifyJS: true,
                removeRedundantAttributes: true,
                removeScriptTypeAttributes: true,
                removeStyleLinkTypeAttributes: true,
            });
            fs.writeFileSync(file, html);
            resolve();
        })
    })
}

function main() {
    if (cluster.isMaster) {
        const files = process.argv.slice(2);
        for (let i = 0; i < Math.min(numCPUs, files.length); ++i) {
            const worker = cluster.fork();
            worker.on('message', msg => {
                if (msg.message === 'completed') {
                    const newFileIdx = files.findIndex(file => !!file);
                    if (newFileIdx !== -1) {
                        worker.send({ message: 'newFile', newFile: files[newFileIdx], newFileIdx })
                        files[newFileIdx] = undefined;
                    } else {
                        worker.kill();
                    }
                }
            })
            worker.send({ message: 'newFile', newFile: files[i], newFileIdx: i });
            files[i] = undefined;
        }
    } else {
        process.on('message', async msg => {
            if (msg.message === 'newFile') {
                console.log(`Processing ${msg.newFile}`);
                await processFile(msg.newFile, msg);
                console.log(`${msg.newFile} done`);
                process.send({ message: 'completed', fileIdx: msg.newFileIdx })
            }
        })
    }
}

main()
