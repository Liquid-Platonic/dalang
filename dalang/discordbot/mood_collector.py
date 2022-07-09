from collections import defaultdict


class MoodCollector:
    def __init__(self):
        self.data_dict = defaultdict(list)

    def add(self, data, guild):
        if data:
            self.data_dict[guild].insert(0, data)

    def get(self, guild):
        return self.data_dict[guild]


mood_collector = MoodCollector()
