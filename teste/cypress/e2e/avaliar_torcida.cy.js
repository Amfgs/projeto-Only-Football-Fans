describe('Avaliar Torcida', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/login/')
    cy.get('input[name="username"]').type('meuUsuario')
    cy.get('input[name="password"]').type('minhaSenha')
    cy.get('button[type="submit"]').click()
    cy.contains('Avaliar Torcida').click()
  })

  it('Avalia a torcida do time 1', () => {
    cy.get('textarea[name="comentario"]').type('Torcida muito animada!')
    cy.get('select[name="emocao"]').select('4')
    cy.get('select[name="presenca"]').select('5')
    cy.get('button[type="submit"]').click()
  })
})
