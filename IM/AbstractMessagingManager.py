import abc

class AbstractMessagingManager(abc.ABC):

    @abc.abstractmethod
    def handle_message(self, message):
        pass

    @abc.abstractmethod
    def send_message(self, message):
        pass

    @abc.abstractmethod
    def send_photo(self, message):
        pass

    @abc.abstractmethod
    def send_video(self, message):
        pass

    @abc.abstractmethod
    def start_bot(self):
        pass

    @abc.abstractmethod
    def receive_message(self, message):
        pass