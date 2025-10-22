from abc import ABC, abstractmethod

class DBOperations(ABC):

    @abstractmethod
    def getVisitorCount(self):
        pass

    @abstractmethod
    def clearVisitorCount(self):
        pass

    @abstractmethod
    def incrementVisitorCountandReturn(self):
        pass

    @abstractmethod
    def logVisitTimestamp(self):
        pass

    @abstractmethod
    def fetchAllTimestamps(self):
        pass