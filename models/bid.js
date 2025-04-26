
class Bid {
    constructor(tender_id, bid_name, bid_value, bid_time, id= null) {
        this.id = id;
        this.tender_id = tender_id;
        this.bid_name = bid_name;
        this.bid_value = bid_value;
        this.bid_time = bid_time;
    }

    toArray() {
        return [
            this.tender_id,
            this.bid_name,
            this.bid_value,
            this.bid_time
        ];
    }
}

module.exports = Bid