class BaseException(Exception):
    """
    The base class for exceptions.

    All the exceptions in this application should be inherited from this exception.
    """

    def __init__(self, title: str, details: dict) -> None:
        """
        Initialize the exception.

        Args:
            title (str): The display title.
            details (dict): Serializable dictionary with the details of the occured exception.
        """
        self.title = title
        self.details = details

    @property
    def representation(self) -> dict:
        """
        Convert the exception into a serializable dictionary.

        Used for JSON serialization.

        Returns:
            dict: The serializable representation of the base exception.
        """
        return {
            'title': self.title,
            'details': self.details,
        }
