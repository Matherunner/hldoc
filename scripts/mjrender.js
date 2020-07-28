const fs = require('fs');
const { JSDOM } = require("jsdom");
const { mjpage } = require('mathjax-node-page');
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

function processFile(file) {
    console.log(`Processing ${file}`);
    const content = fs.readFileSync(file).toString();
    mjpage(content, { format: ['TeX'] }, { html: true }, (output) => {
        const html = removeMathJaxScript(output);
        fs.writeFileSync(file, html);
        console.log(`${file} done`);
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
        process.on('message', msg => {
            if (msg.message === 'newFile') {
                processFile(msg.newFile);
                process.send({ message: 'completed', fileIdx: msg.newFileIdx })
            }
        })
    }    
}

main()
