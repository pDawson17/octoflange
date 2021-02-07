class Data_Consumer:
    def __init__(self):
        self.global_data = {}

    def set_data(self, data, key):
        print("setting", data)
        self.global_data[key] = data

    def get_data(self, key):
        if key not in self.global_data:
            return []
        return self.global_data[key]

    #def remove_data(self, key):
    #    self.global_data
