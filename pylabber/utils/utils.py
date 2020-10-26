"""
General utility classes and functions for the *pylabber*
`project <https://docs.djangoproject.com/en/2.2/ref/applications/#projects-and-applications>`_.
"""

from django.db import models
from enum import Enum
from questionnaire_reader import QuestionnaireReader
import msoffcrypto, io


class ChoiceEnum(Enum):
    """
    A Python `enum <https://docs.python.org/3/library/enum.html>`_ with
    a method to provide choices in the format that Django expects them.
    
    """

    @classmethod
    def choices(cls):
        """
        Returns a tuple of tuples containing the definition of choices for
        a given Django field. For more information see Django's 
        `model field reference <https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices>`_.
        
        Returns
        -------
        tuple
            Tuples representing actual values next to human-readable values.
        """
        return tuple((choice.name, choice.value) for choice in cls)


class CharNullField(models.CharField):
    """
    Subclass of the CharField that allows empty strings to be stored as NULL.
    """

    description = "CharField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection):
        """
        Gets value right out of the db and changes it if its ``None``.
        """

        if value is None:
            return ""
        else:
            return value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its ``None``.
        """

        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        if value is None:
            # If db has NULL, convert it to ''.
            return ""

        # Otherwise, just return the value.
        return value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """

        if value == "":
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value


class SubjectDataHandler:
    @classmethod
    def __init__(cls, path):
        cls.questionnaire = QuestionnaireReader(path=path)

    def open_password_protected_excel(
        self, filename: str, password: str
    ) -> io.BytesIO:
        """
        A method to open a password protected excel.

        Returns
        -------
        io.BytesIO
            Decrypted excel.
        """

        f = msoffcrypto.OfficeFile(open(filename, "rb"))
        f.load_key(password=password)
        decrypted = io.BytesIO()
        f.decrypt(decrypted)

        return decrypted
