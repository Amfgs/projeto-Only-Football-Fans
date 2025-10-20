describe('Avaliar Estádio', () => {
  beforeEach(() => {
    cy.login()
  })

  it('Deve avaliar um estádio', () => {
    cy.visit('http://127.0.0.1:8000/emocao/avaliacao/inicio/')

    // Clica no botão "Nova Avaliação"
    cy.contains('Nova Avaliação').click()

    // Preenche o formulário
    cy.get('input[name="estadio"]').type('Estádio Legal')

    // Seleciona a nota usando radio button
    cy.get('input[name="avaliacao"][value="5"]').check({ force: true })

    // Preenche o comentário
    cy.get('textarea[name="comentario"]').type('Ótima experiência!')

    // Envia o formulário
    cy.contains('button', 'Enviar Avaliação').click()

    // Verifica se a avaliação foi registrada
    cy.contains('Avaliação enviada com sucesso!')
  })
})
