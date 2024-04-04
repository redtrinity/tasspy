from dataclasses import dataclass

from . import KwargsValidator, KwargValueValidator


@dataclass
class Campus(KwargValueValidator):
    """Validate student parameter 'campus'"""

    name = "campus"
    types = str
    valid_values = ("ARI", "ARN")


@dataclass
class CommType(KwargValueValidator):
    """Validate student parameter 'commtype'"""

    name = "commtype"
    valid_values = ("all", "aca", "att", "ec", "gen", "lw", "tkco")


@dataclass
class IncludePhoto(KwargValueValidator):
    """Validate student parameter 'includephoto'"""

    name = "includephoto"
    types = bool


@dataclass
class PCTutorGroup(KwargValueValidator):
    """Validate student parameter 'pc_tutor_group'"""

    name = "pc_tutor_group"
    all_digits = False
    max_length = 5
    types = str


@dataclass
class CurrentStatus(KwargValueValidator):
    """Validate student status parameter 'currentstatus'"""

    name = "currentstatus"
    valid_values = ("current", "future", "past", "noncurrent")


@dataclass
class Code(KwargValueValidator):
    """Validate student parameter 'code'"""

    name = "code"
    all_digits = True
    length = 6
    types = (int, str)


@dataclass
class StudClass(KwargValueValidator):
    """Validate student parameter 'studclass' (converted to 'class' post validation)"""

    name = "studclass"
    types = str


@dataclass
class Thumbnail(KwargValueValidator):
    """Validate student parameter 'includephoto'"""

    name = "includephoto"
    types = bool


@dataclass
class UpdateOn(KwargValueValidator):
    """Validate student parameter 'updaet_on'"""

    name = "update_on"
    types = str
    date_formatg = "%d/%m/%Y"


@dataclass
class UpdateOnFrom(KwargValueValidator):
    """Validate student parameter 'update_on_from'"""

    name = "update_on_from"
    types = str
    date_formatg = "%d/%m/%Y"


@dataclass
class UpdateOnTo(KwargValueValidator):
    """Validate student parameter 'update_on_to'"""

    name = "update_on_to"
    types = str
    date_formatg = "%d/%m/%Y"


@dataclass
class YearGroup(KwargValueValidator):
    """Validate student parameter 'year_group'"""

    name = "year_group"
    types = (int, str)
    valid_values = tuple([n for n in range(0, 13)])


@dataclass
class UDAreaCode(KwargValueValidator):
    """Validate student paramter 'areacode'"""

    name = "areacode"
    types = (int, str)
    valid_values = tuple([n for n in range(0, 500)])


@dataclass
class GetStudentsDetails(KwargsValidator):
    valid_kwargs = (
        Code(),
        CurrentStatus(),
        IncludePhoto(),
        Thumbnail(),
        Campus(),
        PCTutorGroup(),
        StudClass(),
        YearGroup(),
        UpdateOn(),
        UpdateOnFrom(),
        UpdateOnTo(),
    )
    required_kwargs = (CurrentStatus(),)


@dataclass
class GetStudentUD(KwargsValidator):
    valid_kwargs = (
        Code(),
        CurrentStatus(),
    )
    conditional_kwargs = (Code(), CurrentStatus(),)


@dataclass
class GetStudentUDArea(KwargsValidator):
    valid_kwargs = (
        Code(),
        UDAreaCode(),
    )
    required_kwargs = (Code(), UDAreaCode(),)


@dataclass
class GetCommunicationRulesDetails(KwargsValidator):
    valid_kwargs = (
        Code(),
        CurrentStatus(),
        CommType(),
    )
    required_kwargs = (
        CurrentStatus(),
        CommType(),
    )
