from de.sphrilix.holy_greetings.dto.greet import Greet


class User:
    """
    Wrapper class for a dc user with greetings.
    """

    def __init__(self, u_id: str, greets: list[Greet]):
        """
        Construct a new user instance with the given user id and its corresponding greetings.
        :param u_id: The given user id.
        :param msgs: The given greetings.
        """
        self.u_id = u_id
        self.greets = greets

    def __str__(self) -> str:
        """
        Construct a str representation.
        :return: Returns the str representation.
        """
        return str(self.to_json())

    def __eq__(self, other) -> bool:
        """
        If the user ids of two users are same the user are equal.
        :param other: The instance which the actual is compared.
        :return: Return self.u_id == other.u_id
        """
        return isinstance(other, User) and self.u_id == other.u_id

    def to_json(self) -> dict:
        """
        Construct a valid JSON representation of an user.
        :return: Returns the JSON representation.
        """
        return {"u_id": self.u_id,
                "msgs": [greet.to_json() for greet in self.greets]}
