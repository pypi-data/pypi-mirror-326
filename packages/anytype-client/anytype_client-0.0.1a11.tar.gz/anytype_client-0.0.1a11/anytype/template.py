class Template:
    def __init__(self):
        self._headers: dict = {}
        self.type = ""
        self.id = ""
        self.name = ""
        self.icon = ""

    def __repr__(self):
        return f"<Template(name={self.name}, icon={self.icon})>"
