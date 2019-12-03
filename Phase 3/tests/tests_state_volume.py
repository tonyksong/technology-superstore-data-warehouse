# import mydbconfig as mydb
import pytest
import auxFunctions as aux
import app as app
def test_db_connect():
    """
    GIVEN db credentials
    CONNECT with DB and return true if successful
    :return:
    """
    (state, dbconn) = aux.get_connection()
    assert state == True

@pytest.fixture
def test_client():
    flask_app = app.create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()



def test_assignments():
    SQL_MANAGER_ASSIGNMENTS_WITH_EMAIL = "SELECT storeNumber AS `Store Number`, managerName AS `Manager`, Manages.emailAddress AS `Manager Email` FROM Manages JOIN Manager ON Manages.emailAddress = Manager.emailAddress ORDER BY Manages.storeNumber, managerName;"
    dataFrayme = aux.get_df(SQL_MANAGER_ASSIGNMENTS_WITH_EMAIL)
    assert (dataFrayme)

def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/hello')
    assert response.status_code == 200

def test_holidays(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/holidays')
    assert response.status_code == 200