from typing import Optional

from .. import TassConnector
from ..decorators import (
    rename_class_param,
    validate_kwargs,
)
from ..validators.students import (
    GetCommunicationRulesDetails,
    GetStudentsDetails,
    GetStudentUD,
    GetStudentUDArea,
)


class StudentDetails(TassConnector):
    def __init__(
        self, app_code: str, api_vers: str, cmpy_code: str, token: str, base_url: Optional[str] = None
    ) -> None:
        self.app_code = app_code
        self.api_vers = api_vers
        self.cmpy_code = cmpy_code
        self.token = token
        super().__init__(base_url=base_url)

    @validate_kwargs(GetCommunicationRulesDetails)
    def get_communication_rule_details(self, **kwargs) -> Optional[dict]:
        """Get communication rules for students.
        :param currentstatus: student status, 'current', 'future', 'past', or 'noncurrent'
        :param commtype: communication rules to return in the result
        :param **kwargs: optional student params"""
        kwargs.update({"api_method": "getCommunicationRulesDetails"})

        return self.get(**kwargs)

    @validate_kwargs(GetStudentsDetails)
    @rename_class_param("studclass")
    def get_student_details(self, **kwargs) -> Optional[dict]:
        """Get student details.
        Note: The TASS API documentation indicates 'class' is a parameter that can be passed to the API method,
              however this is a reserved word in Python so use 'studclass' instead. This will get adjusted by
              the 'rename_class_param' decorator.
        :param currentstatus: student status, 'current', 'future', 'past', or 'noncurrent'
        :param **kwargs: optional student params"""
        kwargs.update({"api_method": "getStudentsDetails"})

        return self.get(**kwargs)

    @validate_kwargs(GetStudentUD)
    def get_student_ud(self, **kwargs) -> Optional[dict]:
        """Get student UD data.
        :param code: required if 'currentstatus' parameter not provided
        :param currentstatus: required if 'code' parameter not provided"""
        kwargs.update({"api_method": "getStudentUD"})

        return self.get(**kwargs)

    @validate_kwargs(GetStudentUDArea)
    def get_student_ud_area(self, **kwargs) -> Optional[dict]:
        """Get student UD data.
        :param code: student id code (required)
        :param areacode: UD area code (required)"""
        kwargs.update({"api_method": "getStudentUD"})

        return self.get(**kwargs)

    @validate_kwargs(GetStudentsDetails)
    def missing_photo_report(self, currentstatus: str, **kwargs) -> Optional[dict]:
        """Get details of students missing an ID photo.
        :param currentstatus: student status, 'current', 'future', 'past', or 'noncurrent'
        :param **kwargs: optional student params"""
        inc_photo_params = {"includephoto": True}

        def _has_photo(s: dict) -> bool:
            """Test student has photo.
            :param s: dictionary object representing a student."""
            try:
                sp = s["general_details"]["student_photo"]
                fn = sp["file_info"]["file_name"]

                return not fn.lower() == "unavailable.gif"
            except KeyError:
                return False

            return False

        if not kwargs:
            kwargs = inc_photo_params
        else:
            kwargs.update(inc_photo_params)

        if (result := self.get_student_details(currentstatus=currentstatus, **kwargs)) and (
            students := result.get("students")
        ):
            result["students"] = [*filter(lambda s: not _has_photo(s), students)]

            return result
