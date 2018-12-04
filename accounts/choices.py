from pylabber.utils import ChoiceEnum


class Title(ChoiceEnum):
    NONE = ''
    BSC = 'B.Sc.'
    MSC = 'M.Sc.'
    PHD = 'Ph.D.'
    PROF = 'Prof.'


class Position(ChoiceEnum):
    NONE = ''
    RA = 'Research Assistant'
    MSC = 'M.Sc. Student'
    PHD = 'Ph.D. Candidate'
    POST = 'Postdoctoral Researcher'
    MAN = 'Lab Manager'
    HEAD = 'Principle Investigator'
