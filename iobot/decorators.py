
def singleton(cls):
    """ http://www.python.org/dev/peps/pep-0318/#examples """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

