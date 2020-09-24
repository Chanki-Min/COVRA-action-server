const express = require("express");
const router = express.Router();
const middleware = require("../middleware/middleware");

const IFTTT_GISAID_FIELD = process.env.IFTTT_ACTION_GISAID_FIELD_NAME;
const IFTTT_WHO_FIELD = process.env.IFTTT_ACTION_WHO_FIELD_NAME;

//상태 조회
router.get("/ifttt/v1/status", (req, res) => {
    res.status(200).send();
});

//IFTTT test 라우팅
router.post("/ifttt/v1/test/setup", (req, res) => {
    res.status(200).send({
        //임의 data object를 보낸다
        data: {
            samples: {
                actions: {
                    upload_gisaid_covid19_data_to_ksb: {
                        [IFTTT_GISAID_FIELD]: [
                            {
                                strain: "USA/FL-BPHL-0772/2020",
                                virus: "ncov",
                                gisaid_epi_isl: "EPI_ISL_512677",
                                genbank_accession: "?",
                                date: "2020-06-29",
                                region: "North America",
                                country: "USA",
                                division: "Florida",
                                location: "",
                                region_exposure: "North America",
                                country_exposure: "USA",
                                division_exposure: "Florida",
                                segment: "genome",
                                length: "29513",
                                host: "Human",
                                age: "?",
                                sex: "?",
                                pangolin_lineage: "B.1.1",
                                GISAID_clade: "G",
                                originating_lab:
                                    "Florida Bureau of Public Health Laboratories",
                                submitting_lab:
                                    "Florida Bureau of Public Health Laboratories",
                                authors: "Sarah Schmedes et al",
                                url: "https://www.gisaid.org",
                                title: "?",
                                paper_url: "?",
                                date_submitted: "2020-08-11",
                            },
                        ],
                    },
                    upload_who_covid19_data_to_ksb: {
                        [IFTTT_WHO_FIELD]: [
                            {
                                Date_reported: "2020-08-18",
                                Country_code: "AF",
                                Country: "Afghanistan",
                                WHO_region: "EMRO",
                                New_cases: "3",
                                Cumulative_cases: "37599",
                                New_deaths: "0",
                                Cumulative_deaths: "1375",
                            },
                        ],
                    },
                },
            },
        },
    });
});

module.exports = router;
