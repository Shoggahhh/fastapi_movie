from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """ """

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        return password from username if found
        :param username: name user
        :return: password from user if found
        """

    @classmethod
    def check_password_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Check password for matches
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Check a password
        :param username: whose password
        :param password: check password with what is in the database
        :return: True if is match, else False
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_password_match(
            password1=db_password,
            password2=password,
        )
