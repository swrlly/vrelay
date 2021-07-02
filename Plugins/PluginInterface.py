
"""
Here is an interface for Plugin classes.
"""
class PluginInterface:

    hooks = {}
    load = False
    defaultState = False

    def getAuthor(self) -> str:
        return ""

    def getCommands(self) -> list:
        return []