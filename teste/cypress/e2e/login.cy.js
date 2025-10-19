describe('Login', () => {
  it('Deve logar com usuário válido e manter sessão', () => {
    cy.visit('http://127.0.0.1:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.url().should('eq', 'http://127.0.0.1:8000/') // Página do menu
  })

  it('Mostra erro com usuário inválido', () => {
    cy.visit('http://127.0.0.1:8000/login/')
    cy.get('input[name="username"]').type('usuarioInvalido')
    cy.get('input[name="password"]').type('senhaErrada')
    cy.get('button[type="submit"]').click()
    cy.contains('Usuário ou senha incorretos')
  })
})
