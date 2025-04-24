var express = require('express');
var router = express.Router();
var databaseController = require('../controllers/database-controller')
const Tender = require(("../models/Tender"))

router.use(express.urlencoded({ extended: true }));
router.use(express.json());


// GET pages
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Przetargi' });
});

router.get('/tenders-list', (req, res) => {
  res.render('./pages/tenders-list');
});

router.get('/finished-tenders-list', (req, res) => {
  res.render('./pages/finished-tenders-list');
});

router.get('/new-tender', (req, res) => {
  res.render('./pages/new-tender');
});

// handling database operations
router.post('/save-tender', (req, res) => {
  const {name, company, description, tender_start_time, tender_finish_time, max_budget} = req.body
  let tender = new Tender(name, company, description, tender_start_time, tender_finish_time, max_budget)
  databaseController.addTender(tender, (err) => {
    if(err){
      return res.status(500).send("Błąd dodawania danych");
    } else {
      res.redirect("/");
    }
  })
});

module.exports = router;
