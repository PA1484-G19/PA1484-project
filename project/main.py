from debug_log import log
import sys

from app import App

app: App

def main():
    global app
    try:
        app = App()
    except Exception as error:
        log("FATAL: %r" % (error,))
        sys.print_exception(error)
        raise

if __name__=='__main__':
    main()
