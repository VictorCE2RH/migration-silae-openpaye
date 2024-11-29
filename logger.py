
class Colors:
    """Classe contenant les codes ANSI pour les couleurs"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'    # Pour réinitialiser la couleur


def _coloredStatement(string,color):
    return f"{color}{string}{Colors.END}"

def SuccessStatement(string):
    return _coloredStatement(string,Colors.GREEN+Colors.BOLD) 
def ErrorStatement(string):
    return _coloredStatement(string,Colors.RED+Colors.BOLD) 
def WarningStatement(string):
    return _coloredStatement(string,Colors.YELLOW)
def ProgressStatement(string):
    return _coloredStatement(string,Colors.CYAN)
def StatisticStatement(string):
    return _coloredStatement(string,Colors.BLUE)


def printErr(string):
    print(ErrorStatement(string))
def printSuccess(string):
    print(SuccessStatement(string))
def printProgress(string):
    print(ProgressStatement(string))
def printStat(string):
    print(StatisticStatement(string))