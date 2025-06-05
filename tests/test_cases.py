
import time
import unittest

import selenium
import selenium.webdriver
from selenium.webdriver.common.by import By


newTenderId = 0
isNewTenderCreated = False

def open_page_set_up(url):
    options = selenium.webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = selenium.webdriver.Chrome(options=options)
    driver.get(url)
    return driver

class OpenHomePage(unittest.TestCase):
    url = "http://localhost:3000"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_home_page_title(self):
        self.assertIn("Przetargi", self.driver.title)

    def test_if_navbar_exists(self):
        self.assertIsNotNone(self.driver.find_element(By.CSS_SELECTOR, "nav"))    


class OpenTenderListPage(unittest.TestCase):
    url = "http://localhost:3000/tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_tenders_list_page_title(self):
        self.assertIn("Przetargi", self.driver.title)

class OpenFinishedTenderListPage(unittest.TestCase):
    url = "http://localhost:3000/finished-tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_finished_tenders_list_page_title(self):
        self.assertIn("Przetargi", self.driver.title)

class OpenNewTenderPage(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
       self.driver = open_page_set_up(self.url)

    def test_new_tender_page_title(self):
        self.assertIn("Przetargi", self.driver.title)

class OpenTenderWithId1Page(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/1"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_tender_with_id_1_page_title(self):
        self.assertIn("Przetargi", self.driver.title)

class OpenNewBidForId6Page(unittest.TestCase):
    # dla zakończonego przetargu nie powinno dać się stworzyć nowej oferty
    url = "http://localhost:3000/tenders-list/6/new-bid"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_new_bid_for_id_6_page_title(self):
        self.assertNotIn("Przetargi", self.driver.title)

class OpenNewBidPageForNewId(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/{newTenderId}/new-bid"
    def setUp(self):
        if isNewTenderCreated:
            self.driver = open_page_set_up(self.url)

    def test_new_bid_for_new_tender_page_title(self):
        if isNewTenderCreated:
            self.assertIn("Przetargi", self.driver.title)

class OpenTenderPageForWrongId(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/-1"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_tender_with_wrong_id_page_title(self):
        self.assertNotIn("Przetargi", self.driver.title)

class OpenNewBidPageForWrongId(unittest.TestCase):
    # nie powinno dać się stworzyć nowej oferty
    url = "http://localhost:3000/tenders-list/-1/new-bid"
    def setUp(self):
        self.driver = open_page_set_up(self.url)

    def test_new_bid__for_tender_with_wrong_id_page_title(self):
        self.assertNotIn("Przetargi", self.driver.title)

class AddNewTender(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "company").send_keys("Remony12")
        self.driver.find_element(By.ID, "description").send_keys("Remont schodów budynku Muzeum Miejskiego")
        self.driver.execute_script(
            "document.getElementById('tender-start-time').value = arguments[0]",
            "2025-06-05T10:30"
        )
        self.driver.execute_script(
            "document.getElementById('tender-finish-time').value = arguments[0]",
            "2025-06-07T10:30"
        )
        self.driver.find_element(By.ID, "max_budget").send_keys("30000")

        button = self.driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        button.click()

        time.sleep(1)
        self.assertEqual("http://localhost:3000/tenders-list", self.driver.current_url)
        self.isNewTenderCreated = True
        
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        last_row = rows[-1]
        self.newTenderId = last_row.find_element(By.TAG_NAME, "th").text

        selector = f'a[href="/tenders-list/{self.newTenderId}"]'
        link = self.driver.find_element(By.CSS_SELECTOR, selector)
        self.assertEqual(link.text, "Remont schodów")


class AddNewBidForNewId(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/{newTenderId}/new-bid"
    def setUp(self):
        if isNewTenderCreated:
            self.driver = open_page_set_up(self.url)
    def test_new_bid_for_new_id(self):
        if isNewTenderCreated:
            self.driver.find_element(By.ID, "bid_name").send_keys("Remont w mig")
            self.driver.find_element(By.ID, "bid_value").send_keys("29000")
            button = self.driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
            button.click()

            self.assertEqual(self.driver.current_url, "http://localhost:3000/tenders-list/{newTenderId}")
            # oferty nie można zobaczyć przed upływem końcowego terminu

class AddNewBidForFinishedTender(unittest.TestCase):
    # sprawdzam dla przetargu o id 6
    url = "http://localhost:3000/tenders-list/6/new-bid"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_bid_for_finished_tender(self):
        element1 = self.driver.find_element(By.ID, "bid_name")
        self.assertIsNone(element1)
        element2 = self.driver.find_element(By.ID, "bid_value")
        self.assertIsNone(element2)
        element3 = self.driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
        self.assertIsNone(element3)

def try_to_add_incomplete_tender(driver, testcase):
        button = driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        button.click()

        time.sleep(1)
        testcase.assertEqual("http://localhost:3000/save-tender", driver.current_url)
        testcase.assertEqual("Błąd dodawania danych", driver.find_element(By.CSS_SELECTOR, "body").text)

class AddNewTenderWithoutBudget(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "company").send_keys("Remony12")
        self.driver.find_element(By.ID, "description").send_keys("Remont schodów budynku Muzeum Miejskiego")
        self.driver.execute_script(
            "document.getElementById('tender-start-time').value = arguments[0]",
            "2025-06-05T10:30"
        )
        self.driver.execute_script(
            "document.getElementById('tender-finish-time').value = arguments[0]",
            "2025-06-07T10:30"
        )
        try_to_add_incomplete_tender(self.driver, self)

class AddNewTenderWithoutInstitutionName(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "description").send_keys("Remont schodów budynku Muzeum Miejskiego")
        self.driver.execute_script(
            "document.getElementById('tender-start-time').value = arguments[0]",
            "2025-06-05T10:30"
        )
        self.driver.execute_script(
            "document.getElementById('tender-finish-time').value = arguments[0]",
            "2025-06-07T10:30"
        )
        self.driver.find_element(By.ID, "max_budget").send_keys("30000")
        try_to_add_incomplete_tender(self.driver, self)

class AddNewTenderWithoutDescription(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "company").send_keys("Remony12")
        self.driver.execute_script(
            "document.getElementById('tender-start-time').value = arguments[0]",
            "2025-06-05T10:30"
        )
        self.driver.execute_script(
            "document.getElementById('tender-finish-time').value = arguments[0]",
            "2025-06-07T10:30"
        )
        self.driver.find_element(By.ID, "max_budget").send_keys("30000")
        try_to_add_incomplete_tender(self.driver, self)

class AddNewTenderWithoutStartDate(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "company").send_keys("Remony12")
        self.driver.find_element(By.ID, "description").send_keys("Remont schodów budynku Muzeum Miejskiego")
        self.driver.execute_script(
            "document.getElementById('tender-finish-time').value = arguments[0]",
            "2025-06-07T10:30"
        )
        self.driver.find_element(By.ID, "max_budget").send_keys("30000")
        try_to_add_incomplete_tender(self.driver, self)

class AddNewTenderWithoutFinishDate(unittest.TestCase):
    url = "http://localhost:3000/new-tender"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_add_new_tender(self):
        self.driver.find_element(By.ID, "tender_name").send_keys("Remont schodów")
        self.driver.find_element(By.ID, "company").send_keys("Remony12")
        self.driver.find_element(By.ID, "description").send_keys("Remont schodów budynku Muzeum Miejskiego")
        self.driver.execute_script(
            "document.getElementById('tender-start-time').value = arguments[0]",
            "2025-06-05T10:30"
        )
        self.driver.find_element(By.ID, "max_budget").send_keys("30000")
        try_to_add_incomplete_tender(self.driver, self)

class AddNewBidForNewIdWithoutName(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/{newTenderId}/new-bid"
    def setUp(self):
        if isNewTenderCreated:
            self.driver = open_page_set_up(self.url)
    def test_new_bid_for_new_id(self):
        if isNewTenderCreated:
            self.driver.find_element(By.ID, "bid_value").send_keys("29000")
            button = self.driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
            button.click()

            self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, "body").text, "Błąd zapisywania danych")

class AddNewBidForNewIdWithoutValue(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/{newTenderId}/new-bid"
    def setUp(self):
        if isNewTenderCreated:
            self.driver = open_page_set_up(self.url)
    def test_new_bid_for_new_id(self):
        if isNewTenderCreated:
            self.driver.find_element(By.ID, "bid_name").send_keys("Testowa oferta")
            button = self.driver.find_element(By.CSS_SELECTOR, ".btn.submit-button")
            button.click()

            self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, "body").text, "Błąd zapisywania danych")


class ReadHomePageDescription(unittest.TestCase):
    url = "http://localhost:3000"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_description(self):
        self.assertIsNotNone(self.driver.find_element(By.ID, "description"))
    def test_find_keyword_in_description(self):
        self.assertIn("Przetargi Online", self.driver.find_element(By.ID, "description").text)

class ReadTenderListElements(unittest.TestCase):
    url = "http://localhost:3000/tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_elements(self):
        self.assertIsNotNone(self.driver.find_element(By.CSS_SELECTOR, "thead"))
        self.assertGreaterEqual(len(self.driver.find_elements(By.CSS_SELECTOR, "tr")), 0)

class ReadFinishedTenderListElements(unittest.TestCase):
    url = "http://localhost:3000/finished-tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_elements(self):
        self.assertIsNotNone(self.driver.find_element(By.CSS_SELECTOR, "thead"))
        self.assertGreaterEqual(len(self.driver.find_elements(By.CSS_SELECTOR, "tr")), 0)

class ReadTenderWithId6Details(unittest.TestCase):
    url = "http://localhost:3000/tenders-list/6"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_elements(self):
        self.assertIsNotNone(self.driver.find_element(By.CSS_SELECTOR, "b"))
    def test_find_keyword_in_details(self):
        self.assertIn("Malowanie", self.driver.find_element(By.CSS_SELECTOR, "b").text)    

class ReadTenderWithId1WinningBid(unittest.TestCase):
    # no winner here
    url = "http://localhost:3000/tenders-list/1"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_bids(self):
        self.assertEqual(len(self.driver.find_elements(By.ID, "bid")), 0)
    def test_find_no_winner_message(self):
        self.assertEqual("Przetarg zakończono bez rozstrzygnięcia", self.driver.find_elements(By.CSS_SELECTOR, "b")[1].text)

class ReadTenderWithId6WinningBid(unittest.TestCase):
    # first bid on the list
    url = "http://localhost:3000/tenders-list/6"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_find_bids(self):
        self.assertGreaterEqual(len(self.driver.find_elements(By.ID, "bid")), 0)
    def test_find_winning_bid(self):
        bids = self.driver.find_elements(By.ID, "bid")
        self.assertIn('400', bids[0].text)

class GoToHomePageByClickingOnNavbar(unittest.TestCase):
    url = "http://localhost:3000/tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_go_to_homepage(self):
        self.driver.find_element(By.ID, "nav-home").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:3000/")

class GoToTenderListPageByClickingOnNavbar(unittest.TestCase):
    url = "http://localhost:3000/"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_go_to_tender_list(self):
        self.driver.find_element(By.ID, "nav-tenders").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:3000/tenders-list")

class GoToFinishedTenderListPageByClickingOnNavbar(unittest.TestCase):
    url = "http://localhost:3000/"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_go_to_finished_tender_list(self):
        self.driver.find_element(By.ID, "nav-finished-tenders").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:3000/finished-tenders-list")

class GoToNewTenderPageByClickingOnNavbar(unittest.TestCase):
    url = "http://localhost:3000/"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_go_to_new_tender_page(self):
        self.driver.find_element(By.ID, "nav-new-tender").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:3000/new-tender")

class GoToTenderDetailsPageByClickingOnNameOfTenderWithId1(unittest.TestCase):
    url = "http://localhost:3000/finished-tenders-list"
    def setUp(self):
        self.driver = open_page_set_up(self.url)
    def test_go_to_tender_details_page(self):
        selector = f'a[href="/tenders-list/1"]'
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        element.click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:3000/tenders-list/1")

loader = unittest.TestLoader()
open_suite = unittest.TestSuite()
open_suite.addTests(loader.loadTestsFromTestCase(cls) for cls in [
    OpenHomePage,
    OpenTenderListPage,
    OpenFinishedTenderListPage,
    OpenNewTenderPage,
    OpenTenderWithId1Page,
    OpenNewBidForId6Page,
    OpenNewBidPageForNewId,
    OpenTenderPageForWrongId,
    OpenNewBidPageForWrongId
])

add_suite = unittest.TestSuite()
add_suite.addTests(loader.loadTestsFromTestCase(cls) for cls in [
    AddNewTender,
    AddNewBidForNewId,
    AddNewBidForFinishedTender,
    AddNewTenderWithoutBudget,
    AddNewTenderWithoutInstitutionName,
    AddNewTenderWithoutDescription,
    AddNewTenderWithoutStartDate,
    AddNewTenderWithoutFinishDate,
    AddNewBidForNewIdWithoutName,
    AddNewBidForNewIdWithoutValue
])

read_suite = unittest.TestSuite()
read_suite.addTests(loader.loadTestsFromTestCase(cls) for cls in [
    ReadHomePageDescription,
    ReadTenderListElements,
    ReadFinishedTenderListElements,
    ReadTenderWithId6Details,
    ReadTenderWithId1WinningBid,
    ReadTenderWithId6WinningBid
])

goto_suite = unittest.TestSuite()
goto_suite.addTests(loader.loadTestsFromTestCase(cls) for cls in [
    GoToHomePageByClickingOnNavbar,
    GoToTenderListPageByClickingOnNavbar,
    GoToFinishedTenderListPageByClickingOnNavbar,
    GoToNewTenderPageByClickingOnNavbar,
    GoToTenderDetailsPageByClickingOnNameOfTenderWithId1
])
all_tests = unittest.TestSuite([open_suite, add_suite, read_suite, goto_suite])

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_tests)