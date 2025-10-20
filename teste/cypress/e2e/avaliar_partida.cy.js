describe('Avaliar Partida', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar a primeira partida da lista', () => {
    cy.visit('http://127.0.0.1:8000/partidas/avaliar/5/') // Atualizar ID dinamicamente se quiser
    cy.get('input[name="nota"]').type('4')
    cy.get('input[name="melhor_jogador"]').type('Messi')
    cy.get('input[name="pior_jogador"]').type('Maradona')
    cy.get('textarea[name="comentario"]').type('Partida interessante.')
    cy.get('button[type="submit"]').click()

    cy.contains('Avaliação registrada com sucesso!')
  })
})
