Feature: Login de Usuário
  Como um usuário registrado
  Eu quero fazer login na plataforma
  Para obter um token de acesso

  Scenario: Login com credenciais válidas
    Given eu forneço um e-mail e senha válidos
    When eu envio uma solicitação POST para "/login"
    Then a resposta deve conter um token de acesso
    And a resposta deve ter status code 200

  Scenario: Login com credenciais inválidas
    Given eu forneço um e-mail ou senha inválidos
    When eu envio uma solicitação POST para "/login"
    Then a resposta deve informar que o e-mail ou a senha é inválido
    And a resposta deve ter status code 401
