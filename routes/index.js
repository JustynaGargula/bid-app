var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/bids-list', (req, res) => {
  res.render('./pages/bids-list');
});

router.get('/finished-bids-list', (req, res) => {
  res.render('./pages/finished-bids-list');
});

router.get('/new-bid', (req, res) => {
  res.render('./pages/new-bid');
});


module.exports = router;
