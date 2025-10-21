describe('Avaliar Torcida', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar torcida dos times 1 e 2', () => {
    cy.visit('http://127.0.0.1:8000/partidas/avaliar_torcida/1/')

    // Opção 1: usando o input escondido
    cy.get('input[name="emocao"][value="4"]').check({ force: true })
    cy.get('input[name="presenca"][value="5"]').check({ force: true })
    cy.get('textarea[name="comentario"]').type('Torcida animada demais!')
    cy.contains('button', 'Mandar o Review da Torcida').click()
  

    cy.get('input[name="emocao"][value="4"]').check({ force: true })
    cy.get('input[name="presenca"][value="5"]').check({ force: true })
    cy.get('textarea[name="comentario"]').type('Torcida fraca demais!')
    cy.contains('button', 'Mandar o Review da Torcida').click()
  })
})
