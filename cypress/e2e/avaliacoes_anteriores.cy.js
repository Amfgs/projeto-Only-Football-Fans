describe('Avaliações Anteriores', () => {

  it('Deve carregar a página e exibir as avaliações do usuário', () => {
    cy.visit('http://127.0.0.1:8000/emocao/avaliacoes_anteriores/')
    cy.contains('Avaliações Anteriores').should('be.visible')

    // Caso tenha avaliações cadastradas
    cy.get('.avaliacao-card').should('exist')
  })

  it('Deve navegar entre as páginas de avaliações', () => {
    cy.visit('http://127.0.0.1:8000/emocao/avaliacoes_anteriores/?page=2')
    cy.contains('Avaliações Anteriores').should('be.visible')
  })

})
