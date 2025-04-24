
class Tender {
    constructor(id = null, name, company, description, tender_start_time, tender_finish_time, max_budget) {
        this.id = id;
        this.name = name;
        this.company = company;
        this.description = description;
        this.tender_start_time = tender_start_time;
        this.tender_finish_time = tender_finish_time;
        this.max_budget = max_budget;

    }
    toArray() {
        return [
            this.name,
            this.company,
            this.description,
            this.tender_start_time,
            this.tender_finish_time,
            this.max_budget
        ];
    }
}

module.exports = Tender