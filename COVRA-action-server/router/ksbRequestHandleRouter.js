const express = require("express");
const router = express.Router();
const fs = require('fs');
const path = require('path');
const { execSync } = require("child_process");
const wrapAsyncFn = require('../util/wrapAsyncFn');

router.get(
    "/ksb/metadata", 
    wrapAsyncFn(async (req, res) => {
        console.log('got /ksb/metadata request');

        const subject = req.query.subject;
        if(subject === undefined) {
            res.set(404).send({error: 'need \"subject\" value'});
            return;
        }

        const path = await getLatestProcessedDataPath(subject);
        const fileStream = fs.createReadStream(path);

        fileStream.pipe(res);
    })
);

const getLatestProcessedDataPath = async (subject) => {
    const dataDirPath = path.resolve('python', 'processed_data', subject);
    const fileList = await fs.promises.readdir(dataDirPath);
    return path.join(dataDirPath, fileList.filter(s => (path.extname(s) == '.txt') || (path.extname(s) == '.json'))
        .sort((a,b) => b-a)[0]);    
}

module.exports = router;