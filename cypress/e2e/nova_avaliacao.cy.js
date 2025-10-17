describe('Nova Avaliação de Estádio', () => {

  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/emocao/nova_avaliacao/')
  })

  it('Deve mostrar erro se os campos obrigatórios não forem preenchidos', () => {
    cy.get('button[type="submit"]').click()
    cy.contains('Preencha todos os campos obrigatórios.').should('be.visible')
  })

  it('Deve mostrar erro se a avaliação não for um número', () => {
    cy.get('input[name="estadio"]').type('Maracanã')
    cy.get('input[name="avaliacao"]').type('abc')
    cy.get('textarea[name="comentario"]').type('Lugar incrível!')
    cy.get('button[type="submit"]').click()
    cy.contains('A avaliação deve ser um número entre 1 e 5.').should('be.visible')
  })

  it('Deve enviar o formulário corretamente e mostrar a página de sucesso', () => {
    cy.get('input[name="estadio"]').type('Maracanã')
    cy.get('input[name="avaliacao"]').type('5')
    cy.get('textarea[name="comentario"]').type('Ambiente espetacular!')
    cy.get('button[type="submit"]').click()

    cy.contains('Avaliação registrada com sucesso').should('be.visible')
  })

})
