import pytest
from restaurant_webapp import create_app
from flask import current_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application
    # configured for testing
    testing_client = flask_app.test_client()

    # Establish an application context
    ctx = flask_app.app_context()

    # Push the application context to the application context stack
    ctx.push()

    current_app.logger.info('In the test_client fixture')    #push the application context to the stack before accessing the logger

    # Pop the application context from the stack
    ctx.pop()

    # or instead use this
    # with flask_app.app_context():
    # current_app.logger.info('In the test_client fixture')

    return testing_client