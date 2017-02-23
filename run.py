""" File to Start EMR App
"""

from app.application import initialize_app

app = initialize_app('development')

if __name__ == '__main__':
    app.run()

