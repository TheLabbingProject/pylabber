from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from research.models.procedure_step import ProcedureStep


class ProcedureManager(models.QuerySet):
    def from_dict(self, definition: dict):
        title = definition["title"]
        description = definition["description"]
        try:
            procedure = self.get(title=title)
        except ObjectDoesNotExist:
            procedure = self.create(title=title, description=description)
        else:
            if procedure.description != description:
                procedure.description = description
                procedure.save()
        if "steps" in definition:
            ProcedureStep.objects.from_list(procedure, definition["steps"])
        return procedure

    def from_list(self, definitions: list) -> list:
        return [self.from_dict(definition) for definition in definitions]
