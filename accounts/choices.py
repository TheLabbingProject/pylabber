from pylabber.utils import ChoiceEnum


class Title(ChoiceEnum):
    BSC = "B.Sc."
    MSC = "M.Sc."
    PHD = "Ph.D."
    PROF = "Prof."


class Position(ChoiceEnum):
    RA = "Research Assistant"
    MSC = "M.Sc. Student"
    PHD = "Ph.D. Candidate"
    POST = "Postdoctoral Researcher"
    AFF = "Research Affiliate"
    MAN = "Lab Manager"
    PI = "Principle Investigator"
