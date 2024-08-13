from behave import given, when, then
import json
from core.app import app


@given('que estou na página de cadastro')
def step_given_on_registration_page(context):
    context.client = app.test_client()

@when('eu preencho "{field}" com "{value}"')
def step_when_fill_field(context, field, value):
    if not hasattr(context, 'data'):
        context.data = {}
    context.data[field] = value

@when('eu clico em "{button_text}"')
def step_when_click_button(context, button_text):
    if button_text == 'Registrar':
        response = context.client.post('/register', data=json.dumps(context.data), content_type='application/json')
        context.response = response

@then('eu devo ver a mensagem "{message}"')
def step_then_see_message(context, message):
    assert context.response.json['message'] == message