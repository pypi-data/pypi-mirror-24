from IPython.display import HTML


class Viewer:
    def __init__(self):
        self.port = 51001
        return HTML("""<iframe src=http://localhost:%d width=700 height=350></iframe>""" % self.port)
