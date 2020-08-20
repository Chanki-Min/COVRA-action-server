const IFTTT_SERVICE_KEY = process.env.IFTTT_SERVICE_KEY;

module.exports = {
    /**
     * req의 header에 있는 IFTTT service key가 일치하는지 검사하는 미들웨어 함수
     *
     * @param {*} req
     * @param {*} res
     * @param {*} next
     */
    checkIftttServiceKey: function (req, res, next) {
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
    },

    /**
     * 요구되는 필드 리스트를 검사하는 미들웨어 함수를 만드는 고계함수
     *
     * @param {Array} requiredFieldList : 요구되는 IFTTT 필드 리스트
     * @returns {(req, res, next) => void} : express middleware function
     */
    checkIsRequiredFieldExist: function (requiredFieldList) {
        //generate MiddleWare function
        return (req, res, next) => {
            if (
                req.body.actionFields === undefined ||
                requiredFieldList
                    .map((field) => req.body.actionFields[field] === undefined)
                    .reduce((pre, curr) => pre && curr)
            ) {
                res.status(400).send({
                    errors: [
                        {
                            status: "SKIP",
                            message: `Action field is undefined. required : req.body.actionFields and ${JSON.stringify(
                                requiredFieldList
                            )}`,
                        },
                    ],
                });
                return;
            } else {
                next();
            }
        };
    },
};
