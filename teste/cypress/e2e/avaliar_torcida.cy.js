describe('Avaliar Torcida', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar torcida da primeira partida', () => {
    cy.visit('http://127.0.0.1:8000/partidas/avaliar_torcida/5/')

    // Opção 1: usando o input escondido
    cy.get('input[name="emocao"][value="4"]').check({ force: true })
    cy.get('input[name="presenca"][value="5"]').check({ force: true })

    // Opção 2 (se quiser usar label):
    // cy.get('label[for="emocao_4"]').click()
    // cy.get('label[for="presenca_5"]').click()

    cy.get('textarea[name="comentario"]').type('Torcida animada demais!')
    cy.contains('button', 'Mandar o Review da Torcida').click()

    cy.contains('Mandar o Review da Torcida') // Ajustar depois se houver redirecionamento
  })
})
