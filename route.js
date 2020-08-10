const express = require("express");
const router = express.Router();
const IFTTT_SERVICE_KEY = process.env.IFTTT_SERVICE_KEY;

//서비스 키를 확인하는 미들웨어 추가
router.use(function (req, res, next) {
  if (req.get("IFTTT-Service-Key") !== IFTTT_SERVICE_KEY) {
    res.status(401).send({
      errors: [
        {
          message: "Channel/Service key is not correct",
        },
      ],
    });
    return;
  } else {
    next();
  }
});

//상태 조회
router.get("/ifttt/v1/status", (req, res) => {
  const a = req.get("IFTTT-Service-Key");

  res.status(200).send();
});

//IFTTT test 라우팅
router.post("/ifttt/v1/test/setup", (req, res) => {
  res.status(200).send({
    //임의 data object를 보낸다
    data: {
      samples: {
        actionRecordSkipping: {
          upload_gisaid_data_to_ksb: { invalid: "true" },
        },
      },
    },
  });
});

router.post("/ifttt/v1/actions/upload_gisaid_data_to_ksb", (req, res) => {
  console.log("got trigger");

  console.log(`body : \n${JSON.stringify(req.body, undefined, 2)}`);

  const metaDataList = req.body.actionFields.value1;

  console.log(`metaDataList = ${metaDataList}`)

  //TODO : 데이터를 KSB로 업로드하기

  res.status(200).send({
    data: [
      {
        id: new Date().toISOString(),
      },
    ],
  });
});

module.exports = router;
