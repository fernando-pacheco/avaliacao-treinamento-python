from behave import given, when, then
import requests
import json

BASE_URL = "http://127.0.0.1:5000/user"

@given('eu forneço os dados de registro válidos')
def step_given_valid_registration_data(context):
    context.data = {
        "username": "novo_usuario",
        "email": "novo@dominio.com",
        "password": "senha_forte"
    }

@given('um usuário com nome de usuário "{username}" já está registrado')
def step_given_existing_username(context, username):
    context.existing_username = username

@given('eu forneço os dados de registro com o mesmo nome de usuário')
def step_given_registration_with_existing_username(context):
    context.data = {
        "username": context.existing_username,
        "email": "novo@dominio.com",
        "password": "senha_forte"
    }

@given('um usuário com e-mail "{email}" já está registrado')
def step_given_existing_email(context, email):
    context.existing_email = email

@given('eu forneço os dados de registro com o mesmo e-mail')
def step_given_registration_with_existing_email(context):
    context.data = {
        "username": "novo_usuario",
        "email": context.existing_email,
        "password": "senha_forte"
    }

@when('eu envio uma solicitação POST para "/user"')
def step_when_send_post_request(context):
    response = requests.post(BASE_URL, json=context.data)
    print(context.data)
    print(response.json())
    context.response = response

@then('a resposta deve informar que o nome de usuário já está em uso')
def step_then_username_already_in_use(context):
    assert context.response.json().get("message") == "Username ja esta em uso"

@then('a resposta deve informar que o e-mail já está em uso')
def step_then_email_already_in_use(context):
    assert context.response.json().get("message") == "Email ja esta em uso"

@then('o usuário deve ser registrado com sucesso')
def step_then_user_registered_successfully(context):
    assert context.response.json().get("message") == "Cadastro realizado com sucesso"

@then('a resposta deve ter status code 201')
def step_then_status_code_201(context):
    assert context.response.status_code == 201

@then('a resposta deve ter status code 400')
def step_then_status_code_400(context):
    assert context.response.status_code == 400
