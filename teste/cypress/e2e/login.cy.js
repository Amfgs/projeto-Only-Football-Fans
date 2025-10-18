describe('Login', () => {
  it('Deve logar com usuário válido', () => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/home') // ou página inicial
  })

  it('Mostra erro com usuário inválido', () => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('usuarioInvalido')
    cy.get('input[name="password"]').type('senhaErrada')
    cy.get('button[type="submit"]').click()
    cy.contains('Usuário ou senha incorretos')
  })
})
