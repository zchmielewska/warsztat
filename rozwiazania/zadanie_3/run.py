import os
from cashflower import run
from settings import settings


if __name__ == "__main__":
    output, diagnostic, log = run(settings=settings, path=os.path.dirname(__file__))
