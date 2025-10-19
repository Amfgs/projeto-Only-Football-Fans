describe('Menu lateral', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
  })

  it('Exibe a barra lateral do menu', () => {
    cy.contains('Menu').should('be.visible') // troque para o texto correto
  })

  it('Clica em Agenda e vai para registrar_partida', () => {
    cy.contains('Agenda').click()
    cy.url().should('include', 'registrar_partida') // troque conforme url real
  })
})
