describe('Avaliar Partida', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.contains('Agenda').click()
    cy.contains('Avaliar').click() // botão da tabela de partidas
  })

  it('Envia uma avaliação válida', () => {
    cy.get('input[name="nota"]').type('4')
    cy.get('input[name="melhor_jogador"]').type('Jogador Top')
    cy.get('input[name="pior_jogador"]').type('Zé Ruela')
    cy.get('textarea[name="comentario"]').type('Jogo emocionante!')
    cy.get('button[type="submit"]').click()
    cy.contains('Avaliação registrada') // troque se necessário
  })
})
