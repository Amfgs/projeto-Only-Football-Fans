describe('Registrar Partida', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve registrar uma nova partida', () => {
    cy.visit('http://127.0.0.1:8000/partidas/registrar/')
    
    cy.get('input[name="time_casa"]').type('Time A')
    cy.get('input[name="time_visitante"]').type('Time B')
    cy.get('input[name="data"]').type('2025-10-19T18:30') // Exemplo de data/hora
    cy.contains('button', 'Registrar').click()

    // Verifica se a nova partida aparece na lista
    cy.url().should('eq', 'http://127.0.0.1:8000/partidas/')
    cy.contains('Time A x Time B')
  })
})
