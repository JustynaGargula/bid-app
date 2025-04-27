var express = require('express');
var router = express.Router();
var databaseController = require('../controllers/database-controller')
const Tender = require(("../models/Tender"))
const Bid = require("../models/bid");

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
  let {tender_name, company, description, tender_start_time, tender_finish_time, max_budget} = req.body
  tender_start_time = tender_start_time.replace('T', ' ') + ':00';
  tender_finish_time = tender_finish_time.replace('T', ' ') + ':00';
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
      databaseController.getBids(id, (err, rows) => {
        if(err) {
          res.status(500).send("Błąd pobierania danych o ofertach");
        } else {
          res.render("./pages/tender-details", {id: id, data: row, current_time: new Date(), start_time: new Date(row.tender_start_time), finish_time: new Date(row.tender_finish_time), bids: rows });
        }

      });
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

router.post('/save-bid', (req, res) => {
  let {tender_id, bid_name, bid_value, bid_time} = req.body;
  let bid = new Bid(tender_id, bid_name, bid_value, bid_time);
  databaseController.saveBid(bid, (err) => {
    if(err) {
      res.status(500).send("Błąd zapisywania danych");
    } else {
      res.redirect("/tenders-list/"+tender_id)
    }
  })
})

module.exports = router;
