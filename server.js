require("dotenv").config();

const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const actionRouter = require("./router/actionRouter");
const boilerPlateRouter = require("./router/boilerPlateRouter");

//request의 body를 json으로 받아들인다.
app.use(bodyParser.json({ limit: "50mb" }));

//라우터 적용
app.use("/", actionRouter);
app.use("/", boilerPlateRouter);

const listener = app.listen(process.env.PORT, function () {
    console.log("Your app is listening on port " + listener.address().port);
});
