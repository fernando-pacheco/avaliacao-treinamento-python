Feature: Registro de Usuário
  Como um usuário não autenticado
  Eu quero me registrar na plataforma
  Para poder acessar a aplicação

  Scenario: Registrar um usuário com nome de usuário já existente
    Given um usuário com nome de usuário "admin" já está registrado
    And eu forneço os dados de registro com o mesmo nome de usuário
    When eu envio uma solicitação POST para "/user"
    Then a resposta deve informar que o nome de usuário já está em uso
    And a resposta deve ter status code 400

  Scenario: Registrar um usuário com e-mail já existente
    Given um usuário com e-mail "admin@example.com" já está registrado
    And eu forneço os dados de registro com o mesmo e-mail
    When eu envio uma solicitação POST para "/user"
    Then a resposta deve informar que o e-mail já está em uso
    And a resposta deve ter status code 400

  Scenario: Registrar um novo usuário com dados válidos
    Given eu forneço os dados de registro válidos
    When eu envio uma solicitação POST para "/user"
    Then o usuário deve ser registrado com sucesso
    And a resposta deve ter status code 201