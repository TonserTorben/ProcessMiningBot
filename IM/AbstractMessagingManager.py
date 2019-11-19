import abc

class AbstractMessagingManager(abc.ABC):

    @abc.abstractmethod
    def send_message(self, message):
        pass

    @abc.abstractmethod
    def send_file(self):
        pass

    @abc.abstractmethod
    def receive_message(self):
        pass

    @abc.abstractmethod
    def receive_file(self):
        pass