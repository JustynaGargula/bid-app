var express = require('express');
var router = express.Router();
var databaseController = require('../controllers/database-controller')
const Tender = require(("../models/Tender"))
const data = require("bootstrap/js/src/dom/data");

router.use(express.urlencoded({ extended: true }));
router.use(express.json());


// GET pages
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Przetargi' });
});

router.get('/tenders-list', (req, res) => {
  databaseController.getTenders((err, rows) => {
    if(err){
      return res.status(500).send("Błąd pobierania danych");
    } else {
        res.render('./pages/tenders-list', {'data': rows});
    }
  })
});

router.get('/finished-tenders-list', (req, res) => {
  databaseController.getFinishedTenders((err, rows) => {
    if(err) {
      return res.status(500).send("Błąd pobierania danych")
    } else {
      res.render('./pages/finished-tenders-list', { data: rows});
    }
  })

});

router.get('/new-tender', (req, res) => {
  res.render('./pages/new-tender');
});

// handling database operations
router.post('/save-tender', (req, res) => {
  const {tender_name, company, description, tender_start_time, tender_finish_time, max_budget} = req.body
  let tender = new Tender(tender_name, company, description, tender_start_time, tender_finish_time, max_budget)
  databaseController.addTender(tender, (err) => {
    if(err){
      return res.status(500).send("Błąd dodawania danych");
    } else {
      res.redirect("/tenders-list");

    }
  })
});

router.get('/tenders-list/:id', (req, res) => {
  const id = req.params.id;
  databaseController.getTenderDetails(id, (err, row) => {
    if(err) {
      res.status(500).send("Błąd pobierania danych");
    } else {
      res.render("./pages/tender-details", {id: id, data: row, current_time: new Date(), finish_time: new Date(row.tender_finish_time) });
    }
  })

})

router.get('/tenders-list/:id/new-bid', (req, res) => {
  const id = req.params.id
  databaseController.getTenderDetails(id, (err, row) => {
    if(err) {
      res.status(500).send("Błąd pobierania danych");
    } else {
      res.render("./pages/new-bid", {id: id, data: row});
    }
  })
})

module.exports = router;
