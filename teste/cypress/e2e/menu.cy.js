describe('Menu lateral', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('Jaime')
    cy.get('input[name="password"]').type('Jaime**12')
    cy.get('button[type="submit"]').click()
  })

  it('Exibe a barra lateral do menu', () => {
    cy.contains('Menu').should('be.visible') // troque para o texto correto
  })

})
