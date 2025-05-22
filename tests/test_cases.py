import unittest

newTenderId = 0

class OpenHomePage(unittest.TestCase):
    pass

class OpenTenderListPage(unittest.TestCase):
    pass

class OpenFinishedTenderListPage(unittest.TestCase):
    pass

class OpenNewTenderPage(unittest.TestCase):
    pass

class OpenTenderWithId1Page(unittest.TestCase):
    pass

class OpenNewBidForId1Page(unittest.TestCase):
    pass

class OpenNewBidPageForNewId(unittest.TestCase):
    pass

class OpenTenderPageForWrongId(unittest.TestCase):
    pass

class OpenNewBidPageForWrongId(unittest.TestCase):
    pass

class AddNewTender(unittest.TestCase):
    pass

class AddNewBidForNewId(unittest.TestCase):
    pass

class AddNewBidForFinishedTender(unittest.TestCase):
    pass

class AddNewTenderWithoutBudget(unittest.TestCase):
    pass

class AddNewTenderWithoutInstytutionName(unittest.TestCase):
    pass

class AddNewTenderWithoutDescription(unittest.TestCase):
    pass

class AddNewTenderWithoutStartDate(unittest.TestCase):
    pass

class AddNewTenderWithoutFinishDate(unittest.TestCase):
    pass

class AddNewBidForNewIdWithoutName(unittest.TestCase):
    pass

class AddNewBidForNewIdWithoutValue(unittest.TestCase):
    pass

class ReadHomePageDescription(unittest.TestCase):
    pass

class ReadTenderListElements(unittest.TestCase):
    pass

class ReadFinishedTenderListElements(unittest.TestCase):
    pass

class ReadTenderWithId1Details(unittest.TestCase):
    pass

class ReadTenderWithId1WinningBid(unittest.TestCase):
    # no winner here
    pass

class ReadTenderWithId6WinningBid(unittest.TestCase):
    # first bid on the list
    pass

class GoToHomePageByClickingOnNavbar(unittest.TestCase):
    pass

class GoToTenderListPageByClickingOnNavbar(unittest.TestCase):
    pass

class GoToFinishedTenderListPageByClickingOnNavbar(unittest.TestCase):
    pass

class GoToNewTenderPageByClickingOnNavbar(unittest.TestCase):
    pass

class GoToTenderDetailsPageByClickingOnNameOfTendreWithId1(unittest.TestCase):
    pass