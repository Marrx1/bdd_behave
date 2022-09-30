from main.common.models.base_model import BaseModel


class TestModel(BaseModel):
    """One of example how to create model of api endpoint
    in this example **kwargs is data from response.json().
     for the similar purposes you can use data classes
    or Dict from addict  BUT in this implementation you can add own methods and setup more
    flexible behaviour in you model"""
    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.title = kwargs.get("title")
        self.icd = kwargs.get("icd")
        self.more_icd = kwargs.get("more_icd")
        self.description = kwargs.get("description")
        self.community_factors = kwargs.get("community_factors")
