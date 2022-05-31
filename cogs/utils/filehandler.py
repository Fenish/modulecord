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


class Locale:
    def __init__(self, language):
        self.language = language.lower().capitalize()
        self.default_locale = "English"

        locale_url = "https://raw.githubusercontent.com/Fenish/modulecord-modules/" \
                     f"main/locales/{self.language}.json"

        default_locale_url = "https://raw.githubusercontent.com/Fenish/modulecord-modules/" \
                             "main/locales/English.json"

        self.locale_file = JsonFromUrl(locale_url)
        self.default_locale_file = JsonFromUrl(default_locale_url)

    def __getitem__(self, item):
        if not self.locale_file.get(item):
            return self.default_locale_file.get(item)
        return self.locale_file.get(item)
