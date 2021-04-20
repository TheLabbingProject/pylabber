from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from research.models.procedure import Procedure


class StudyManager(models.QuerySet):
    def from_dict(self, definition: dict):
        title = definition["title"]
        description = definition["description"]
        try:
            study = self.get(title=title)
        except ObjectDoesNotExist:
            study = self.create(title=title, description=description)
        else:
            if study.description != description:
                study.description = description
                study.save()
        if "procedures" in definition:
            procedures = Procedure.objects.from_list(definition["procedures"])
            study.procedures.set(procedures)
        return study

    def from_list(self, definitions: List[dict]) -> list:
        return [self.from_dict(definitions) for definitions in definitions]
