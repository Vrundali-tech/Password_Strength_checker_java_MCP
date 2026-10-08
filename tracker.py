from reportlab.lib.pagesizes import letter
from reportlab.platypus import Flowable

class PageTracker(Flowable):
    def __init__(self, name, tracker_dict):
        super().__init__()
        self.name = name
        self.tracker_dict = tracker_dict

    def draw(self):
        page = self.canv.getPageNumber()
        self.tracker_dict[self.name] = page
