from behave import given, when, then
import requests

BASE_URL = 'http://localhost:5000'

@given('eu forneço um e-mail e senha válidos')
def step_given_valid_login_data(context):
    context.data = {
        'email': 'admin@example.com',
        'password': '4210'
    }

@given(u'eu forneço um e-mail ou senha inválidos')
def step_given_invalid_login_data(context):
    context.data = {
        'email': 'admin@example.com',
        'password': 'invalid'
    }

@when('eu envio uma solicitação POST para "/login"')
def step_when_post_login(context):
    response = requests.post(f'{BASE_URL}/login', json=context.data)
    context.response = response

@then('a resposta deve conter um token de acesso')
def step_then_contains_access_token(context):
    print(context.response.json())
    assert 'access_token' in context.response.json()

@then('a resposta deve informar que o e-mail ou a senha é inválido')
def step_then_invalid_credentials(context):
    assert context.response.json()['message'] == 'Email ou senha invalidos'

@then('a resposta deve ter status code 200')
def step_then_status_code_200(context):
    assert context.response.status_code == 200

@then('a resposta deve ter status code 401')
def step_then_status_code_401(context):
    assert context.response.status_code == 401
