const express = require("express");
const router = express.Router();
const middleware = require("../middleware/middleware");
const {ungzip} = require("node-gzip");
const fsPromises = require('fs').promises;
const path = require('path');
const { execSync } = require("child_process");
const wrapAsyncFn = require('../util/wrapAsyncFn');

const IFTTT_GISAID_FIELD = process.env.IFTTT_ACTION_GISAID_FIELD_NAME;
const IFTTT_WHO_FIELD = process.env.IFTTT_ACTION_WHO_FIELD_NAME;
const decompressString = async (gzipCompressed) => (await ungzip(Buffer.from(gzipCompressed, 'base64') ) ).toString();

router.use(middleware.checkIftttServiceKey);
router.post(
    "/ifttt/v1/actions/upload_gisaid_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_GISAID_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got gisaid trigger");

        const metaDataList = await decompressString(req.body.actionFields[IFTTT_GISAID_FIELD]);
        const dataSaveDir = path.resolve('python', process.env.PATH_METADATA_GISAID);
        const fileSavePath = path.join(dataSaveDir, `GISAID_${new Date().getTime()}.txt`);
        await fsPromises.writeFile(fileSavePath, metaDataList);
    })
);

router.post(
    "/ifttt/v1/actions/upload_who_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_WHO_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got who trigger");

        const metaDataList = await decompressString(req.body.actionFields[IFTTT_WHO_FIELD]);
        const dataSaveDir = path.resolve('python', process.env.PATH_METADATA_WHO);
        const fileSavePath = path.join(dataSaveDir, `WHO_${new Date().getTime()}.txt`);
        await fsPromises.writeFile(fileSavePath, metaDataList);
    })
);

module.exports = router;
