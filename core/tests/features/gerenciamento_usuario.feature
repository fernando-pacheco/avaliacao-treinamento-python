Feature: Gerenciamento de Usuário
  Como um usuário autenticado
  Eu quero atualizar e excluir meu perfil
  Para manter minhas informações atualizadas

  Scenario: Atualizar um usuário com dados válidos
    Given eu estou autenticado
    And eu forneço dados de atualização válidos
    When eu envio uma solicitação PUT para "/user"
    And eu envio uma solicitação DELETE para "/user"
    Then as informações do usuário devem ser atualizadas
    And a resposta deve ter status code 201
