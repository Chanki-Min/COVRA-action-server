const express = require("express");
const router = express.Router();
const middleware = require("../middleware/middleware");
const {ungzip} = require("node-gzip");

const IFTTT_GISAID_FIELD = process.env.IFTTT_ACTION_GISAID_FIELD_NAME;
const IFTTT_WHO_FIELD = process.env.IFTTT_ACTION_WHO_FIELD_NAME;

const wrapAsyncFn = asyncFn => {
      return (async (req, res, next) => {
        try {
          return await asyncFn(req, res, next)
        } catch (error) {
          return next(error)
        }
      })  
    }
const decompressString = async (gzipCompressed) => (await ungzip(Buffer.from(gzipCompressed, 'base64') ) ).toString();

router.use(middleware.checkIftttServiceKey);

router.post(
    "/ifttt/v1/actions/upload_gisaid_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_GISAID_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got gisaid trigger");

        const metaDataList = await decompressString(req.body.actionFields[IFTTT_GISAID_FIELD]);

        console.log(
            `metaDataList type : ${typeof metaDataList} len = ${
                metaDataList.length
            }`
        );

        //TODO : 데이터를 KSB로 업로드하기

        res.status(200).send({
            data: [
                {
                    id: new Date().toISOString(),
                },
            ],
        });
    })
);

router.post(
    "/ifttt/v1/actions/upload_who_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_WHO_FIELD]),
    wrapAsyncFn(async (req, res) => {
        console.log("got who trigger");

        const metaDataList = await decompressString(req.body.actionFields[IFTTT_WHO_FIELD]);

        console.log(
            `metaDataList type : ${typeof metaDataList} len = ${
                metaDataList.length
            }`
        );

        //TODO : 데이터를 KSB로 업로드하기

        res.status(200).send({
            data: [
                {
                    id: new Date().toISOString(),
                },
            ],
        });
    })
);

module.exports = router;
