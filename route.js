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
        actions : {
          upload_gisaid_data_to_ksb : {
            value1 : [
              {
                "strain": "USA/FL-BPHL-0772/2020",
                "virus": "ncov",
                "gisaid_epi_isl": "EPI_ISL_512677",
                "genbank_accession": "?",
                "date": "2020-06-29",
                "region": "North America",
                "country": "USA",
                "division": "Florida",
                "location": "",
                "region_exposure": "North America",
                "country_exposure": "USA",
                "division_exposure": "Florida",
                "segment": "genome",
                "length": "29513",
                "host": "Human",
                "age": "?",
                "sex": "?",
                "pangolin_lineage": "B.1.1",
                "GISAID_clade": "G",
                "originating_lab": "Florida Bureau of Public Health Laboratories",
                "submitting_lab": "Florida Bureau of Public Health Laboratories",
                "authors": "Sarah Schmedes et al",
                "url": "https://www.gisaid.org",
                "title": "?",
                "paper_url": "?",
                "date_submitted": "2020-08-11"
              }
            ]
          }
        }
      },
    },
  });
});

router.post("/ifttt/v1/actions/upload_gisaid_data_to_ksb", (req, res) => {
  console.log("got trigger");

  if(req.body.actionFields === undefined || req.body.actionFields.value1 === undefined) {
    console.log('no data from request body');
    res.status(400).send({
      errors: [
        {
          "status": "SKIP",
          message :  "Requst.body.vaule1 is undefined"
        }
      ]
    });
    return;
  }

  const metaDataList = req.body.actionFields.value1;

  console.log(`metaDataList type : ${typeof metaDataList} len = ${metaDataList.length}`)

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
