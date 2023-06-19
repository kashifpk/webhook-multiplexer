import json
from .config import get_settings


class ForwardsData:

    _data = {}

    def __init__(self):
        self.settings = get_settings()

    def load_data(self):
        cls = self.__class__

        if self.settings.data_file.exists():
            print(f"Loading forwards data from {self.settings.data_file}")
            cls._data = json.load(open(self.settings.data_file))


    def save_data(self):
        cls = self.__class__

        json.dump(cls._data, open(self.settings.data_file, 'w'))


forwards_data = ForwardsData()