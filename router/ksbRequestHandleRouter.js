const express = require("express");
const router = express.Router();
const fsPromises = require('fs').promises;
const path = require('path');
const { execSync } = require("child_process");
const wrapAsyncFn = require('../util/wrapAsyncFn');

router.get(
    "/ksb/metadata", 
    wrapAsyncFn(async (req, res) => {
        console.log('got /ksb/metadata request');

        const subject = req.query.subject;
        if(subject === undefined) {
            res.state(404).send({error: 'need \"subject\" value'});
            return;
        }


        const dataDir = path.resolve('python', process.env[`PATH_METADATA_${subject}`]);
        const fileList = await fsPromises.readdir(dataDir);
        const latestFileName = fileList
            .filter(v => v.startsWith(subject))
            .sort((a,b) => b - a)
            [0];
        if(latestFileName === undefined) {
            console.error('cannot find metadata file');
            res.state(404).send({error: 'metadata not prepared'});
            return;
        }

        const scriptPath = path.resolve('python', 'main.py');
        const pythonResult = execSync(`python3 ${scriptPath} ${subject}`).toString();
        if(pythonResult.startsWith('0')) {
            const processedDataPath = path.resolve('python', process.env[`PATH_PROCESSED_DATA_${subject}`], pythonResult.slice(2));
            const processedData = (await fsPromises.readFile(processedDataPath)).toString();
            //TODO : 데이터를 KSB로 업로드하기

            res.status(200).send({
                data: [
                    {
                        id: new Date().toISOString(),
                    },
                ],
            });
            await fsPromises.unlink(processedDataPath);
        } else {
            const errorLog = pythonResult.slice(2);
            console.error(errorLog);

            res.status(500).send(
                {
                    errors: [
                        {
                            message: `there was an error with python processor\n\n${errorLog}`,
                        },
                    ],
                }
            )
        }
    })
);

module.exports = router;