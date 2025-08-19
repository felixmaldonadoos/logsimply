from .logger import Logger

def main():
    log = Logger(level="INFO")
    log.info("logsimply CLI is working ✨")
