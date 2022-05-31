import requests
from ruamel.yaml import YAML

yaml = YAML()


class YamlFile:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as stream:
            self.data = yaml.load(stream)

    def set_data(self, new_dict: dict):
        yaml_data = self.data
        yaml_data.update(new_dict)
        with open(self.file, "w") as file:
            yaml.dump(yaml_data, file)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.set_data({key: value})

    def __iter__(self) -> iter:
        return iter(self.data)

    def __str__(self) -> str:
        return str(self.data)


class JsonFromUrl:
    def __init__(self, url):
        self.url = url
        self.data = {}
        response = requests.get(url)
        if response.status_code != 404:
            self.data = response.json()

    def get(self, item):
        return self.data.get(item)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self) -> iter:
        return iter(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def __len__(self) -> int:
        return len(self.data)
