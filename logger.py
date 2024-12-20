from datetime import datetime
import logging

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
    return _coloredStatement(string,Colors.YELLOW+Colors.BOLD)
def ProgressStatement(string):
    return _coloredStatement(string,Colors.CYAN)
def StatisticStatement(string):
    return _coloredStatement(string,Colors.BLUE)

PRINT_ERR=True
PRINT_SUCCESS=True
PRINT_PROG=True
PRINT_STAT=True
PRINT_WARN=True
PRINT_LOG=True
PRINT_DEBUG=False

# Configuration du logger pour le fichier
file_logger = logging.getLogger('FileLogger')
file_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('application.log')
file_handler.setFormatter(formatter)
file_logger.addHandler(file_handler)

def _log_to_file(message):
    """Fonction utilitaire pour enregistrer dans le fichier de log"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_logger.info(message)

def error(string):
    if PRINT_ERR:
        print(ErrorStatement(" ERROR: " + string))
        _log_to_file(f"ERROR: {string}")

def success(string):
    if PRINT_SUCCESS:
        print(SuccessStatement(" SUCCESS: " + string))
        _log_to_file(f"SUCCESS: {string}")

def progress(string):
    if PRINT_PROG:
        print(ProgressStatement(string))
        _log_to_file(f"PROGRESS: {string}")

def statistic(string):
    if PRINT_STAT:
        print(StatisticStatement(string))
        _log_to_file(f"STAT: {string}")

def warning(string):
    if PRINT_WARN:
        print(WarningStatement(" WARNING: " + string))
        _log_to_file(f"WARNING: {string}")

def log(string):
    if PRINT_LOG:
        print(string)
        _log_to_file(string)

def debug(string):
    if PRINT_DEBUG:
        print(string)
        _log_to_file(f"DEBUG : {string}")