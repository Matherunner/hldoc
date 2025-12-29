import { Worker } from 'node:worker_threads'
import os from 'node:os'
import path from 'node:path'

async function main() {
    const files = process.argv.slice(2)
    if (!files.length) {
        return
    }

    const maxWorkers = Math.min(os.cpus().length, files.length)
    let active = 0
    let index = 0

    await new Promise((resolve, reject) => {
        const spawnNext = () => {
            if (index >= files.length && !active) {
                resolve()
                return
            }

            while (active < maxWorkers && index < files.length) {
                const file = files[index++]
                active++

                const worker = new Worker(path.join(import.meta.dirname, './mjrender.worker.mjs'), {
                    workerData: { file }
                })

                worker.on('message', msg => {
                    if (msg.ok) {
                        console.log(`Finished ${msg.file}`)
                    } else {
                        console.error(`Error in ${msg.file}:`, msg.error)
                    }
                })

                worker.on('error', reject)

                worker.on('exit', code => {
                    active--
                    if (code) {
                        reject(new Error(`Worker exited with code ${code}`))
                    } else {
                        spawnNext()
                    }
                })
            }
        }

        spawnNext()
    })
}

main().catch(err => {
    console.error(err)
    process.exit(1)
})
