from tabulate import tabulate


class BaseModel:
    def __repr__(self):
        items = [(k, v) for k, v in self.__dict__.items()]
        return "\n" + tabulate(items, headers=("attribute", "value"), tablefmt="pipe")

    def __eq__(self, other):
        return all(
            [self.__dict__[k] == other.__dict__[k] for k in self.__dict__.keys()]
        )
