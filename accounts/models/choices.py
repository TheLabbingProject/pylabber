"""
Subclasses of the :class:`~pylabber.utils.ChoiceEnum` class used to represent
raw and human-readable values for choices within the :mod:`accounts.models` module.

"""

from pylabber.utils import ChoiceEnum


class Title(ChoiceEnum):
    BSC = "B.Sc."
    MSC = "M.Sc."
    PHD = "Ph.D."
    PROF = "Prof."


class Role(ChoiceEnum):
    RA = "Research Assistant"
    MSC = "M.Sc. Student"
    PHD = "Ph.D. Candidate"
    POST = "Postdoctoral Researcher"
    AFF = "Research Affiliate"
    MAN = "Lab Manager"
    PI = "Principle Investigator"
