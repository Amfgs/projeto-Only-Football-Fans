describe('Página inicial do Django', () => {
  it('deve encontrar algum texto na home', () => {
    cy.visit('http://localhost:8000/login/') // Certifique-se que o Django está rodando
    cy.contains('Login') // Troque por algum texto que realmente exista na sua página
  })
})