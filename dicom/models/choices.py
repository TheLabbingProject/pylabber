from pylabber.utils import ChoiceEnum


class Sex(ChoiceEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class DataSourceType(ChoiceEnum):
    SMB = 'SMB'
