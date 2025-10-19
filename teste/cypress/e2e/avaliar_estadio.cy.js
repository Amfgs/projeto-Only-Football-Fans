describe('Avaliar Estádio', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.contains('Avaliar Estádio').click()
  })

  it('Envia avaliação de estádio', () => {
    cy.get('input[name="estadio"]').type('Maracanã')
    cy.get('input[name="avaliacao"]').type('5')
    cy.get('textarea[name="comentario"]').type('Ambiente incrível!')
    cy.get('button[type="submit"]').click()
    cy.contains('Sucesso') // troque se houver outra mensagem
  })
})
