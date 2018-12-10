import abc

from flask import render_template, request, redirect, url_for


class AbstractPage(abc.ABC):
    """Abstract class that will represent a webpage"""

    def __init__(self):
        """Constructor"""
        pass

    @abc.abstractmethod
    def process(self, *args):
        raise NotImplementedError

class MainPage(AbstractPage):
    """Main page of the site, where we can send a link"""

    def __init__(self):
        """Constructor"""
        AbstractPage.__init__(self)

    def process(self):
        return render_template("main_page.html")

class ResultPage(AbstractPage):
    """Result page of the site"""

    def __init__(self):
        """Constructor"""
        AbstractPage.__init__(self)

    def process(self, database):
        if request.method == 'POST':
            if 'link' not in request.form:
                return redirect(url_for("error_page?code=1000"))
            else:
                link = request.form['link']

                # Send the link to another part of the program for processing

                return render_template("results.html", link=link)
        else:
            return redirect(url_for("error_page?code=1000"))


class ErrorPage(AbstractPage):
    """Error page of the site"""

    def __init__(self):
        """Constructor"""
        AbstractPage.__init__(self)

    def process(self):
        return render_template("error.html")