from django.conf import settings


#: The settings key used to set count filtering mode.
COUNT_FILTERING_KEY: str = "ENABLE_COUNT_FILTERING"

#: Default value for the count filtering setting.
COUNT_FILTERING_DEFAULT: bool = False


def get_count_filtering_configuration() -> bool:
    """
    Returns the value of the :attr:`COUNT_FILTERING_KEY` setting, or
    :attr:`COUNT_FILTERING_DEFAULT` if not set.

    Returns
    -------
    bool
        Whether to enable filtering and ordering based on related model counts,
        default is :attr:`COUNT_FILTERING_DEFAULT`
    """
    return getattr(settings, COUNT_FILTERING_KEY, COUNT_FILTERING_DEFAULT)


ENABLE_COUNT_FILTERING: bool = get_count_filtering_configuration()
