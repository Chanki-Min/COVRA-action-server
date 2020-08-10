const express = require('express');
const bodyParser = require('body-parser');
const app = express();

require('dotenv').config();
const router = require('./route.js');

//request의 body를 json으로 받아들인다.
app.use(bodyParser.json());

//라우터 적용
app.use('/',router);

const listener = app.listen(process.env.PORT, function() {
    console.log('Your app is listening on port ' + listener.address().port);
});