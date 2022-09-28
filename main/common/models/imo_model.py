from main.common.models.base_model import BaseModel


class ImoModelSearch(BaseModel):
    def __init__(self, **kwargs):
        self.imo_code = kwargs.get("imo_code")
        self.title = kwargs.get("title")
        self.icd9 = kwargs.get("icd9")
        self.more_icd9 = kwargs.get("more_icd9")
        self.icd10 = kwargs.get("icd10")
        self.more_icd10 = kwargs.get("more_icd10")
        self.snomed = kwargs.get("snomed")
        self.snomed_description = kwargs.get("snomed_description")
        self.hcc_community_factors = kwargs.get("hcc_community_factors")


class ImoModel(BaseModel):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.code = kwargs.get("code")
        self.description = kwargs.get("description")
        self.icd9_ids = kwargs.get("icd9_ids")
        self.icd9_codes = kwargs.get("icd9_codes")
        self.icd9_descriptions = kwargs.get("icd9_descriptions")
        self.icd10_ids = kwargs.get("icd10_ids")
        self.icd10_codes = kwargs.get("icd10_codes")
        self.icd10_descriptions = kwargs.get("icd10_descriptions")
        self.snomed = kwargs.get("snomed")
        self.snomed_description = kwargs.get("snomed_description")
        self.hcc_codes = kwargs.get("hcc_codes")
