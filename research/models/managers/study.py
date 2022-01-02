from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from research.models.managers.utils import (
    STUDY_SUBJECTS_AGGREGATION,
    STUDY_SUBJECTS_ANNOTATION,
)
from research.models.procedure import Procedure
from research.utils import get_subject_model


class StudyManager(QuerySet):
    def with_counts(self) -> QuerySet:
        return self.alias(**STUDY_SUBJECTS_AGGREGATION).annotate(
            **STUDY_SUBJECTS_ANNOTATION
        )

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

    def query_associated_subjects(self) -> QuerySet:
        """
        Returns a queryset of subjects associated with these studies.

        See Also
        --------
        * :func:`subject_set`

        Returns
        -------
        models.QuerySet
            Subjects associated with these studies
        """
        Subject = get_subject_model()
        subjects = Subject.objects.none()
        for study in self.all():
            subjects |= study.query_associated_subjects()
        return subjects
