"""  Repository fixtures
"""
from pytest_shutil.workspace import Workspace


def pytest_funcarg__svn_repo(request):
    """ Function-scoped fixture to create a new svn repo in a temporary workspace.
    
        Attributes
        ----------
        uri (str) :  SVN repo uri.
        .. also inherits all attributes from the `workspace` fixture 
        
    """
    return request.cached_setup(
        setup=SVNRepo,
        teardown=lambda p: p.teardown(),
        scope='function',
    )


class SVNRepo(Workspace):
    """
    Creates an empty SVN repository in a temporary workspace.
    Cleans up on exit.

    Attributes
    ----------
    uri : `str`
        repository base uri
    """
    def __init__(self):
        super(SVNRepo, self).__init__()
        self.run('svnadmin create .', capture=True)
        self.uri = "file://%s" % self.workspace
