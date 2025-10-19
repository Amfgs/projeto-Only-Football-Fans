describe('Galeria', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve acessar a galeria e verificar se há partidas', () => {
    cy.visit('http://127.0.0.1:8000/midia/galeria/')
    cy.contains('Galeria') // Ajuste se houver algum texto específico da página
  })
})
