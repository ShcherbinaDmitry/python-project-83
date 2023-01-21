import pytest
from page_analyzer import app;

@pytest.fixture()
def create_app():
    app_instance = app()
    app_instance.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app_instance

#     # clean up / reset resources here

# @pytest.fixture()
# def client(app_instance):
#     return app_instance.test_client()


# @pytest.fixture()
# def runner(app_instance):
#     return app_instance.test_cli_runner()

# def test_index_page(client):
#     response = client.get("/")
#     assert "Hello, World!" in response.data

def test_index_page():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, World!'
