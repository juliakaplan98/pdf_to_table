""" Startup point for PDF Manipulator"""

from pdfmanipulator.index import main

if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    main()
