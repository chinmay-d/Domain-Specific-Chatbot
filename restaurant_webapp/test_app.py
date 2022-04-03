def test_chatbot_page(test_client):
    '''
    Given a flask application when the '/chatbot' page is requested (GET) then check the response is valid
    '''
    response = test_client.get('/chatbot')
    assert response.status_code == 200
    assert b'Welcome!' in response.data