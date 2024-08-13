Feature: Cadastro de usuário
  Como um novo usuário
  Eu quero me registrar no blog
  Para que eu possa criar postagens e comentários

  Scenario: Usuário se registra com dados válidos
    Given que estou na página de cadastro
    When eu preencho "username" com "novo_usuario"
    And eu preencho "email" com "usuario@example.com"
    And eu preencho "password" com "senha_segura"
    And eu clico em "Registrar"
    Then eu devo ver a mensagem "Cadastro realizado com sucesso"

  Scenario: Usuário se registra com email já existente
    Given que estou na página de cadastro
    When eu preencho "username" com "novo_usuario"
    And eu preencho "email" com "existente@example.com"
    And eu preencho "password" com "senha_segura"
    And eu clico em "Registrar"
    Then eu devo ver a mensagem "Email já está em uso"
