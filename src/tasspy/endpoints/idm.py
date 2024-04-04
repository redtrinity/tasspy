from typing import Optional

from .. import TassConnector


class IdM(TassConnector):
    def __init__(
        self, app_code: str, api_vers: str, cmpy_code: str, token: str, base_url: Optional[str] = None
    ) -> None:
        self.app_code = app_code
        self.api_vers = api_vers
        self.cmpy_code = cmpy_code
        self.token = token
        super().__init__(base_url=base_url)

    def get_students(self, user_code: str, **kwargs) -> Optional[dict]:
        """Get students IdM details.
        :param user_code: student id or 'all'
        :param **kwargs: optional student params"""
        kwargs.update({"api_method": "getStudents", "user_code": user_code})
        print(f"idm.get_students: {kwargs=}")
        return self.get(**kwargs)

    def set_student(self, user_code: str, **kwargs) -> Optional[dict]:
        """Set values related to IdM entries for students.
        :param user_code: student id
        :param **kwargs: optional student params"""
        kwargs.update({"api_method": "SetStudent", "user_code": user_code})
        return self.post(**kwargs)
