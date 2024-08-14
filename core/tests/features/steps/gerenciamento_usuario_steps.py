from behave import given, when, then
import requests

BASE_URL = 'http://localhost:5000'

@given('eu estou autenticado')
def step_given_authenticated(context):
    data = {
        'username': 'teste1',
        'email': 'teste1@example.com',
        'password': '4210'
    }
    user_response = requests.post(f'{BASE_URL}/user', json=data)
    assert user_response.status_code == 201
    context.user_id = user_response.json().get('id', None)
    
    login_data = {
        'email': 'teste1@example.com',
        'password': '4210'
    }
    login_response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert login_response.status_code == 200
    context.token = login_response.json().get('access_token', None)

@given('eu forneço dados de atualização válidos')
def step_given_valid_update_data(context):
    context.data = {
        'username': 'usuario_atualizado',
        'password': 'nova_senha'
    }

@when('eu envio uma solicitação PUT para "/user"')
def step_when_put_user(context):
    response = requests.put(f'{BASE_URL}/user', json=context.data, headers={'Authorization': f'Bearer {context.token}'})
    context.response = response

@when('eu envio uma solicitação DELETE para "/user"')
def step_when_delete_user(context):
    response = requests.delete(f'{BASE_URL}/user', json={'uid': context.user_id}, headers={'Authorization': f'Bearer {context.token}'})
    context.response_delete = response

@then('as informações do usuário devem ser atualizadas')
def step_then_user_updated(context):
    assert context.response.status_code == 201

@then('o usuário deve ser deletado')
def step_then_user_deleted(context):
    assert context.response_delete.status_code == 201
