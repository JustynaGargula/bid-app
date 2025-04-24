
class Tender {
    constructor(tender_name, company, description, tender_start_time, tender_finish_time, max_budget, id = null) {
        this.id = id;
        this.tender_name = tender_name;
        this.company = company;
        this.description = description;
        this.tender_start_time = tender_start_time;
        this.tender_finish_time = tender_finish_time;
        this.max_budget = max_budget;

    }
    toArray() {
        return [
            this.tender_name,
            this.company,
            this.description,
            this.tender_start_time,
            this.tender_finish_time,
            this.max_budget
        ];
    }
}

module.exports = Tender