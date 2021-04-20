from typing import Dict, List, Tuple

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from research.models.event import Event


class ProcedureStepManager(models.QuerySet):
    def from_tuple(
        self, procedure, index: int, definition: Tuple[str, Dict[str, str]]
    ):
        event_class = apps.get_model(
            app_label="research", model_name=definition[0]
        )
        title = definition[1]["title"]
        description = definition[1]["description"]
        try:
            event = event_class.objects.get(title=title)
        except ObjectDoesNotExist:
            event = event_class.objects.create(
                title=title, description=description
            )
        else:
            if event.description != description:
                event.description = description
                event.save()
        try:
            step = self.get(procedure=procedure, index=index)
        except ObjectDoesNotExist:
            step = self.create(procedure=procedure, index=index, event=event)
        else:
            if step.event != event:
                step.event = event
                step.save()
        return step

    def from_list(
        self, procedure, definitions: List[Tuple[str, Dict[str, str]]]
    ) -> list:
        return [
            self.from_tuple(procedure, index, definition)
            for index, definition in enumerate(definitions)
        ]
