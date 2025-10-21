describe('Cadastro de Usuário', () => {
  it('Deve cadastrar e depois logar sem usar commands.js', () => {
    cy.visit('http://127.0.0.1:8000/login/')

    cy.contains('Cadastre-se aqui').click()

    cy.get('input[name="username"]').type('novoUsuario4')
    cy.get('input[name="email"]').type('novo4@usuario.com')
    cy.get('input[name="password"]').type('senha123')
    cy.get('input[name="confirm_password"]').type('senha123')
    cy.get('input[name="time_favorito"]').type('Sport')

    cy.contains('button', 'Registrar').click()

  })
})
