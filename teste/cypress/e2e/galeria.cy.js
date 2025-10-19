describe('Galeria', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.contains('Galeria').click()
  })

  it('Exibe as partidas na galeria', () => {
    cy.contains('Minha Galeria')
    cy.get('.card-partida').should('exist')
  })

  it('Abre página de adicionar mídia', () => {
    cy.contains('Adicionar mídia').first().click()
    cy.url().should('include', 'adicionar_midia')
  })
})
