from ruamel.yaml import YAML

yaml = YAML()


class YamlFile:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as stream:
            self.data = yaml.load(stream)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def add_data(self, new_dict: dict):
        yaml_data = self.data
        yaml_data.update(new_dict)
        with open(self.file, 'w') as file:
            yaml.dump(yaml_data, file)
