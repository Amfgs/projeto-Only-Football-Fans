describe('Página de Início da Avaliação', () => {
  const urlInicio = 'http://localhost:8000/emocao/avaliacao/inicio/';

  beforeEach(() => {
    // Faz login via formulário
    cy.visit('http://localhost:8000/login/');
    cy.get('input[name="username"]').type('usuario_teste');
    cy.get('input[name="password"]').type('senha_teste');
    cy.get('form').submit();

    // Espera algum elemento da home aparecer
    cy.get('.botoes-container', { timeout: 10000 }).should('exist');
  });

  it('deve exibir os dois botões principais com os textos corretos', () => {
    cy.get('.botoes-container').should('be.visible');
    cy.get('.botao').should('have.length', 2);
    cy.contains('Nova Avaliação').should('exist');
    cy.contains('Avaliações Anteriores').should('exist');
  });

  it('deve navegar para Nova Avaliação ao clicar no botão correspondente', () => {
    cy.contains('Nova Avaliação').click();
    cy.url().should('include', '/emocao/nova-avaliacao');
  });

  it('deve navegar para Avaliações Anteriores ao clicar no botão correspondente', () => {
    cy.contains('Avaliações Anteriores').click();
    cy.url().should('include', '/emocao/avaliacao/anterior');
  });
});
