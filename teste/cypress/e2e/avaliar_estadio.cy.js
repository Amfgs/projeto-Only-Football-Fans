describe('Avaliar Estádio', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar um estádio', () => {
    cy.visit('http://127.0.0.1:8000/emocao/avaliacao/inicio/')
    cy.get('input[name="estadio"]').type('Estádio Legal')
    cy.get('input[name="avaliacao"]').type('5')
    cy.get('textarea[name="comentario"]').type('Ótima experiência!')
    cy.get('button[type="submit"]').click()

    cy.contains('Avaliação registrada com sucesso!') // Ajuste se o template for diferente
  })
})
