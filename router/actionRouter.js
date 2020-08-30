const express = require("express");
const router = express.Router();
const middleware = require("../middleware/middleware");
const { ungzip } = require("node-gzip");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const spawn = require("child_process").execSync;

const IFTTT_GISAID_FIELD = process.env.IFTTT_ACTION_GISAID_FIELD_NAME;
const IFTTT_WHO_FIELD = process.env.IFTTT_ACTION_WHO_FIELD_NAME;

const wrapAsyncFn = (asyncFn) => {
    return async (req, res, next) => {
        try {
            return await asyncFn(req, res, next);
        } catch (error) {
            return next(error);
        }
    };
};
const decompressString = async (gzipCompressed) =>
    (await ungzip(Buffer.from(gzipCompressed, "base64"))).toString();

const deleteFileEndsWithExtension = (dirPath, extension) => {
    const fileNameList = fs.readdirSync(dirPath);
    fileNameList.forEach((fileName) => {
        if (fileName.endsWith(extension)) {
            const filePath = path.join(dirPath, fileName);
            fs.unlinkSync(filePath);
            console.log(`${filePath} deleted`);
        }
    });
};

router.use(middleware.checkIftttServiceKey);
router.post(
    "/ifttt/v1/actions/upload_gisaid_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_GISAID_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got gisaid trigger");

        const metaDataList = await decompressString(
            req.body.actionFields[IFTTT_GISAID_FIELD]
        );
        const processedDataDirPath = path.resolve(
            "python",
            process.env.PATH_PROCESSED_DATA_GISAID
        );
        const dataSaveDir = path.resolve(
            "python",
            process.env.PATH_METADATA_GISAID
        );
        const fileSavePath = path.join(
            dataSaveDir,
            `gisaid_data_${new Date().getTime()}.txt`
        );
        try {
            deleteFileEndsWithExtension(processedDataDirPath, ".txt");
            deleteFileEndsWithExtension(dataSaveDir, ".txt");
        } catch (error) {
            console.warn(
                `Error occured while cleaning ${process.env.PATH_METADATA_GISAID} and ${process.env.PATH_PROCESSED_DATA_GISAID}`
            );
        }
        fs.writeFileSync(fileSavePath, metaDataList);

        const scriptPath = path.resolve("python", "main.py");
        const pythonResult = execSync(
            `python3 ${scriptPath} gisaid`
        ).toString();
        console.log(pythonResult);

        if (pythonResult.startsWith("0")) {
            const processedDataPath = path.join(
                processedDataDirPath,
                pythonResult.slice(2).trim()
            );

            const processedData = fs.readFileSync(processedDataPath).toString();
            //TODO : 데이터를 KSB로 업로드하기

            res.status(200).send({
                data: [
                    {
                        id: new Date().toISOString(),
                    },
                ],
            });
        } else {
            const errorLog = pythonResult.slice(2).trim();
            console.error(errorLog);

            res.status(500).send({
                errors: [
                    {
                        message: `there was an error with python processor\n\n${errorLog}`,
                    },
                ],
            });
        }
    })
);

router.post(
    "/ifttt/v1/actions/upload_who_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_WHO_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got who trigger");

        const metaDataList = await decompressString(
            req.body.actionFields[IFTTT_WHO_FIELD]
        );
        const processedDataDirPath = path.resolve(
            "python",
            process.env.PATH_PROCESSED_DATA_WHO
        );
        const originalDataDirPath = path.resolve(
            "python",
            process.env.PATH_METADATA_WHO
        );
        const originalDatafilePath = path.join(
            originalDataDirPath,
            `who_data_${new Date().getTime()}.txt`
        );

        try {
            deleteFileEndsWithExtension(processedDataDirPath, ".txt");
            deleteFileEndsWithExtension(originalDataDirPath, ".txt");
        } catch (error) {
            console.warn(
                `Error occured while cleaning ${process.env.PATH_METADATA_WHO} and ${process.env.PATH_PROCESSED_DATA_WHO}`
            );
        }
        fs.writeFileSync(originalDatafilePath, metaDataList);

        const scriptPath = path.resolve("python", "main.py");
        const pythonResult = execSync(`python3 ${scriptPath} who`).toString();
        console.log(pythonResult);

        if (pythonResult.startsWith('0')) {
            const processedDataPath = path.join(
                processedDataDirPath,
                pythonResult.slice(2).trim()
            );

            const processedData = fs.readFileSync(processedDataPath).toString();
            //TODO : 데이터를 KSB로 업로드하기

            res.status(200).send({
                data: [
                    {
                        id: new Date().toISOString(),
                    },
                ],
            });
        } else {
            const errorLog = pythonResult.slice(2).trim();
            console.error(errorLog);

            res.status(500).send({
                errors: [
                    {
                        message: `there was an error with python processor\n\n${errorLog}`,
                    },
                ],
            });
        }
    })
);

module.exports = router;
