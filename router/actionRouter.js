const express = require("express");
const router = express.Router();
const got = require('got');
const zlib = require('zlib');

const util = require('util');
const stream = require('stream');
const pipeline = util.promisify(stream.pipeline);

const fs = require('fs');
const path = require('path');
const exec = require("child_process").exec;
const execPromise = util.promisify(exec);

const wrapAsyncFn = require('../util/wrapAsyncFn');

router.post(
    "/ifttt/v1/actions/preprocess_data",
    wrapAsyncFn(async (req, res) => {
        console.log("got data update trigger");

        const gisaidURL = req.body.actionFields.gisaid_data_url;
        const whoURL = req.body.actionFields.who_data_url;
        
        const gisaidSavePath = path.resolve('python', 'data', 'gisaid');
        const whoSavePath = path.resolve('python', 'data', 'who');
        const gisaidProcessedPath = path.resolve('python', 'processed_data', 'gisaid');
        const whoProcessedPath = path.resolve('python', 'processed_data', 'who');
        const scriptPath = path.resolve('python', 'main.py');

        await clearDir(gisaidSavePath);
        await clearDir(whoSavePath);

        const gisaidDownload = downloadByStream(gisaidURL, path.join(gisaidSavePath, `GISAID_DATA_${new Date().getTime()}.txt`));
        const whoDownload = downloadByStream(whoURL, path.join(whoSavePath, `WHO_DATA_${new Date().getTime()}.txt`));   
        await Promise.all([gisaidDownload, whoDownload]);
        
        const gisaidProcess = execPromise(`python3 ${scriptPath} gisaid`);
        const whoProcess = execPromise(`python3 ${scriptPath} who`);
        await Promise.all([gisaidProcess, whoProcess]);

        const gisaidResult = (await gisaidProcess).stdout;
        const whoResult = (await whoProcess).stdout;

        if(gisaidResult.startsWith('0')) {
            const resultFile = gisaidResult.slice(2);
            await clearDir(gisaidProcessedPath, [resultFile]);
        } else {
            console.error(`preprocess script error : ${gisaidResult}`)
        }

        if(whoResult.startsWith('0')) {
            const resultFile = whoResult.slice(2);
            await clearDir(whoProcessedPath, [resultFile]);
        } else {
            console.error(`preprocess script error : ${whoResult}`)
        }

        res.set(200).send({
            "data": [
                {
                  "id": new Date().getTime(),
                }
              ]
        })
    })
);

const downloadByStream = (url, savePath) => {
    const GunzipPipe = zlib.createGunzip();  
    const downloadStream = got.stream(url);
    const fileWriterStream = fs.createWriteStream(savePath);

    downloadStream
        .on("error", (error) => {
        console.error(`Download failed: ${error.message}`);
        });
  
    fileWriterStream
        .on("error", (error) => {
        console.error(`Could not write file to system: ${error.message}`);
        })
        .on('finish', () => {
            console.log(`new metadata download complete, url : ${url}`);
        })


    return pipeline(
        downloadStream,
        GunzipPipe,
        fileWriterStream
    )    
}


/**
 * 
 * @param {String} dirPath : 비울 디렉토리 경로 
 * @param {String} exceptionFiles : 삭제하지 않을 파일 이름 배열
 */
const clearDir = async (dirPath, exceptionFiles) => {
    const dir = await fs.promises.readdir(dirPath);
    const unlinkPromises = dir.map(file => {
        if(exceptionFiles instanceof Array) {
            if(exceptionFiles.filter(name => name == file).length === 0 && path.extname(file) == '.txt')
                fs.promises.unlink(path.resolve(dirPath, file));

        } else if (exceptionFiles === undefined)
            if(path.extname(file) == '.txt')
                fs.promises.unlink(path.resolve(dirPath, file))
    });
    return Promise.all(unlinkPromises);
}

module.exports = router;
