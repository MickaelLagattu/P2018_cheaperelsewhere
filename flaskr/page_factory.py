from .pages import *


class PageNotFoundException(Exception):
    pass


class PageFactory():
    """Class that will generate the pages"""

    @staticmethod
    def generate_page(page_name):
        """Generates a page"""

        if page_name == 'MAIN':
            return MainPage()
        elif page_name == 'RESULT':
            return ResultPage()
        elif page_name == 'ERROR':
            return ErrorPage()
        else:
            raise PageNotFoundException()