describe('Fluxo E2E Completo do Usuário', () => {

    // Gera um nome de usuário e email únicos para cada execução do teste
    const uniqueId = new Date().getTime();
    const username = `usuario_${uniqueId}`;
    const email = `${username}@teste.com`;

    it('Deve registrar um novo usuário e testar todas as funcionalidades principais', () => {
        
        // --- PASSO 1: Registro ---
        cy.visit('http://127.0.0.1:8000/');
        cy.contains('a.auth-btn.register-btn', 'Cadastrar-se').click();
        
        cy.url().should('include', '/register/');
        cy.get('input[name="username"]').type(username);
        cy.get('input[name="email"]').type(email);
        cy.get('input[name="password"]').type('senha_segura_123');
        cy.get('input[name="confirm_password"]').type('senha_segura_123');
        cy.get('input[name="time_favorito"]').type('Meu Time Favorito FC');
        cy.contains('button', 'Registrar').click();

        // --- PASSO 2: Registrar Partida ---
        cy.url().should('eq', 'http://127.0.0.1:8000/');
        cy.contains('a.action-card', 'Registrar Nova Partida').click();

        cy.url().should('include', '/partidas/registrar/');
        cy.get('input[name="time_casa"]').type('Time da Casa Cypress');
        cy.get('input[name="time_visitante"]').type('Visitante Cypress');
        cy.contains('button', 'Registrar Ingresso').click();

        // --- PASSO 3: Avaliar Partida ---
        cy.url().should('include', '/partidas/');
        cy.contains('a.btn-avaliar', 'Avaliar Partida').first().click();

        cy.url().should('include', '/partidas/avaliar/');
        cy.get('label[for="nota_4"]').click(); // Clica na 4ª estrela
        cy.get('input[name="melhor_jogador"]').type('Jogador Teste');
        cy.get('input[name="pior_jogador"]').type('Pior Jogador Teste');
        cy.get('textarea[name="comentario_avaliacao"]').type('Comentário de teste para a partida.');
        cy.contains('button', 'Enviar Avaliação').click();

        // --- PASSO 4: Navegar para Avaliar Torcida ---
        cy.visit('http://127.0.0.1:8000/partidas/'); // Força a navegação
        cy.contains('a.btn-avaliar', 'Ver Avaliação').first().click();
        cy.url().should('include', '/partidas/ver/');
        cy.contains('a', 'Avaliar Torcida').click();

        // --- PASSO 5: Avaliar a Torcida (Etapas 1 e 2) ---
        cy.url().should('include', '/partida/avaliar_torcida/');
        cy.get('.star-rating-group').eq(0).find('input[value="4"]').click({ force: true });
        cy.get('.star-rating-group').eq(1).find('input[value="3"]').click({ force: true });
        cy.get('textarea[name="comentario"]').type('Review da performance da torcida.');
        cy.contains('button', 'Enviar Review').click();

        cy.url().should('include', '/2/'); // Verifica se foi para a segunda etapa
        cy.get('.star-rating-group').eq(0).find('input[value="5"]').click({ force: true });
        cy.get('.star-rating-group').eq(1).find('input[value="4"]').click({ force: true });
        cy.get('textarea[name="comentario"]').type('Segundo review, sobre o visual.');
        cy.contains('button', 'Enviar Review').click();

        // --- PASSO 6: Avaliar Estádio ---
        cy.visit('http://127.0.0.1:8000/'); // Força a navegação
        cy.contains('a.action-card', 'Avaliar Estádio').click();
        cy.contains('a', 'Nova Avaliação').click();
        cy.url().should('include', '/emocao/nova-avaliacao/');
        cy.get('input[name="estadio"]').type('Estádio Maracanã Teste');
        cy.get('input[name="avaliacao"][value="5"]').click({ force: true });
        cy.get('textarea[name="comentario"]').type('Comentário sobre o estádio.');
        cy.contains('button', 'Enviar Avaliação').click();

        // --- PASSO 7: Galeria de Mídia (Com Upload e Verificação) ---
        cy.visit('http://127.0.0.1:8000/'); // Força a navegação
        
        cy.contains('a.action-card', 'Galeria de Mídia').click();
        cy.url().should('include', '/galeria/');
        
        cy.contains('a', 'Adicionar mídia').click(); 
        cy.url().should('include', '/adicionar/');

        // --- CORREÇÃO DO UPLOAD ---
        // 1. Anexa o arquivo 'teste.jpg' (que vamos criar) no input 'imagem'
        cy.get('input[name="imagem"]').selectFile('cypress/fixtures/teste.jpg', { force: true });
        
        // 2. Agora sim clica em Enviar
        cy.contains('button', 'Enviar').click();

        // --- CORREÇÃO DA VERIFICAÇÃO ---
        // 3. Garante que fomos redirecionados para a galeria
        cy.url().should('include', '/midia/galeria/');

        // 4. Procura pela IMAGEM real que acabamos de enviar
        // (Isso procura por uma tag <img> cujo link (src) contenha a palavra 'teste')
        cy.get('img[src*="teste"]').should('be.visible');

        // 5. AGORA SIM, após verificar, vamos para a home para o Passo 8
        cy.visit('http://127.0.0.1:8000/');

        // --- PASSO 8: Adicionar Link de Jogo ---
        cy.get('.menu-toggle').click();
        cy.get('.sidebar').contains('a', 'Assistir Jogos').click();
        cy.url().should('include', '/midia/links/');
        cy.contains('a', 'Adicionar Novo Link').click();
        cy.url().should('include', '/midia/links/cadastrar/');
        cy.get('input[name="nome_do_jogo"]').type('Final da Copa de 2002');
        cy.get('input[name="url"]').type('https://www.youtube.com/watch?v=exemplo');
        cy.contains('button', 'Salvar Link').click();

        // --- FINALIZAÇÃO ---
        cy.visit('http://127.0.0.1:8000/');
        cy.url().should('eq', 'http://127.0.0.1:8000/');
    });
});