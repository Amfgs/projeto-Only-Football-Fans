describe('Avaliar Torcida', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar torcida da primeira partida', () => {
    cy.visit('http://127.0.0.1:8000/partidas/avaliar_torcida/5/') // ID da partida
    cy.get('input[name="time"]').type('Time Casa')
    cy.get('input[name="emocao"]').type('4')
    cy.get('input[name="presenca"]').type('5')
    cy.get('textarea[name="comentario"]').type('Torcida animada')
    cy.get('button[type="submit"]').click()

    cy.contains('Próximo') // ou redirecionamento para próxima etapa
  })
})
