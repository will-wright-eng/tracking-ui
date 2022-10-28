import configparser
import os
import pathlib


class ConfigHandler:
    def __init__(self, project_name: str = "tmp"):
        p = pathlib.Path.home()
        self.home_path = p
        self.config_path = p / ".config" / project_name
        self.config_file_path = self.config_path / "config"

        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file_path):
            self.config.read(self.config_file_path)
            print(f"project: {project_name}")
            print("-- config file exists --")
            print(self.print_configs())

    def export_configs(self):
        # export configs as environment variables
        for key, val in self.config.defaults().items():
            if key is not None:
                os.environ[key.upper()] = val

    def print_configs(self):
        # print('print configs')
        print(self.config.defaults())
        # self.config.read_file(
        for key, val in self.config.defaults().items():
            # if key is not None:
            # print(key.upper(),(20-int(len(key)))*' ', val)
            self.formatted_print(key, val)

    def write_config_file(self):
        # rewrite config file
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)

    def create_file_and_dir(self):
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.config_file_path.touch()

    def create_config_locally(self, secret_dict: dict):
        self.create_file_and_dir()
        self.write_config_file_from_dict(config_dict=secret_dict)
        return self.print_configs()

    def config_file_input(self, config_dict: dict, section: str = "DEFAULT"):
        """
        example:
        config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '8',}
        """
        self.config[section] = config_dict

    def write_config_file_from_dict(self, config_dict: dict):
        self.config_file_input(config_dict)
        self.write_config_file()

    def put_project(self, project_name):
        self.project_name = project_name
        self.config_path = self.home_path / ".config" / project_name
        self.config_file_path = self.config_path / "config"
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file_path):
            self.config.read(self.config_file_path)
            print("-- config file exists --")
            print(self.print_configs())
            return False
        else:
            print("-- new project --")
            return True

    def display_config_contents(self, file_path):
        print("\n-- ", file_path, " --")
        tmp = configparser.ConfigParser()
        tmp.read(file_path)
        for key, val in tmp.defaults().items():
            self.formatted_print(key, val)

    def list_config_dirs(self, secret_name: str = "all"):
        # list directories
        p = self.home_path / ".config"
        active = []
        other = []
        for x in p.iterdir():
            if x.is_dir():
                tmp = x / "config"
                if os.path.isfile(tmp):
                    active.append(tmp.resolve())
                    resp = "config file exists"
                else:
                    other.append(x.resolve())
                    resp = "no config file"
                if secret_name == "all":
                    self.formatted_print(x, resp, n=45)

        if secret_name == "all":
            for file_path in active:
                self.display_config_contents(file_path)
        else:
            secret_path = [path for path in active if secret_name in str(path)]
            if len(secret_path) > 1:
                print("multiple matches")
            else:
                self.display_config_contents(secret_path[0])

    def formatted_print(self, key, val, n=20):
        key = str(key)
        val = str(val)
        print(key, (n - int(len(key))) * ".", val)

    def get_configs(self):
        if os.path.isfile(self.config_file_path):
            return self.config.defaults()
        else:
            return None

    def check_config_exists(self):
        return os.path.isfile(self.config_file_path)


config_handler = ConfigHandler()
