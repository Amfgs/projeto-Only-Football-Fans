describe('Registrar Partida', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.contains('Agenda').click()
  })

  it('Registra uma nova partida', () => {
    cy.get('select[name="time_casa"]').select('Time A') // troque os nomes
    cy.get('select[name="time_visitante"]').select('Time B')
    cy.get('input[name="data"]').type('2025-10-25')
    cy.get('button[type="submit"]').click()
    cy.contains('Partida registrada') // troque se houver mensagem
  })
})
