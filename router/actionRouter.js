const express = require("express");
const router = express.Router();
const middleware = require('../middleware/middleware');

const IFTTT_GISAID_FIELD = process.env.IFTTT_ACTION_GISAID_FIELD_NAME;
const IFTTT_WHO_FIELD = process.env.IFTTT_ACTION_WHO_FIELD_NAME;

router.use(middleware.checkIftttServiceKey);


router.post(
    "/ifttt/v1/actions/upload_gisaid_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_GISAID_FIELD]),
    (req, res) => {
        console.log("got gisaid trigger");

        const metaDataList = req.body.actionFields[IFTTT_GISAID_FIELD];

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
    }
);

router.post(
    "/ifttt/v1/actions/upload_who_covid19_data_to_ksb",
    middleware.checkIsRequiredFieldExist([IFTTT_WHO_FIELD]),
    (req, res) => {
        console.log("got who trigger");

        const metaDataList = req.body.actionFields[IFTTT_WHO_FIELD];

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
    }
);

module.exports = router;
