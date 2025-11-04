describe('Fluxo E2E Completo do Usuário', () => {

    // Gera um nome de usuário e email únicos para cada execução do teste
    // Isso evita conflitos de "usuário já existe" no registro
    const uniqueId = new Date().getTime();
    const testUsername = `usuario_${uniqueId}`;
    const testEmail = `usuario_${uniqueId}@teste.com`;
    const testPassword = 'senha_segura_123';

    it('Deve registrar um novo usuário e testar todas as funcionalidades principais', () => {
        
        // --- PASSO 1: Visitar a página principal e clicar em Cadastrar ---
        cy.visit('http://127.0.0.1:8000/');
        cy.contains('a.auth-btn.register-btn', 'Cadastrar-se').click();

        // --- PASSO 2: Preencher o formulário de registro ---
        cy.url().should('include', '/register/');
        
        // Preenche os campos do formulário
        cy.get('input[name="username"]').type(testUsername);
        cy.get('input[name="email"]').type(testEmail); // O seu HTML de registro pede um e-mail
        cy.get('input[name="password"]').type(testPassword);
        cy.get('input[name="confirm_password"]').type(testPassword);
        cy.get('input[name="time_favorito"]').type('Meu Time Favorito FC');
        
        // Clica no botão Registrar
        cy.contains('button', 'Registrar').click();

        // --- PASSO 3: Registrar Nova Partida ---
        cy.url().should('eq', 'http://127.0.0.1:8000/'); // Verifica se voltou para a home
        
        // Clica no card "Registrar Nova Partida" do dashboard (home.html)
        cy.contains('a.action-card', 'Registrar Nova Partida').click();
        
        cy.url().should('include', '/partidas/registrar/');
        
        // Preenche os times
        cy.get('input[name="time_casa"]').type('Time da Casa Cypress');
        cy.get('input[name="time_visitante"]').type('Visitante Cypress');
        
        // Clica no botão "Registrar Ingresso"
        cy.contains('button', 'Registrar Ingresso').click();

        // --- PASSO 4: Avaliar a Partida ---
        cy.url().should('include', '/partidas/'); // Deve ser redirecionado para a lista
        
        // Clica no primeiro botão "Avaliar Partida" que encontrar
        cy.contains('a.btn-avaliar', 'Avaliar Partida').first().click();
        
        cy.url().should('include', '/partidas/avaliar/'); // URL deve conter /avaliar/ID/
        
        // Seleciona 4 estrelas (clicando no label da quarta estrela)
        cy.get('label[for="nota_4"]').click();
        
        // Preenche os campos de texto
        cy.get('input[name="melhor_jogador"]').type('Jogador Teste');
        cy.get('input[name="pior_jogador"]').type('Pior Jogador Teste');
        cy.get('textarea[name="comentario_avaliacao"]').type('Comentário de teste para a partida.');
        
        // Clica em "Enviar Avaliação"
        cy.contains('button', 'Enviar Avaliação').click();
// --- PASSO 5: Avaliar a Torcida (Fluxo de 2 etapas) ---
        
        // (FIX) O app não redireciona sozinho após o Passo 4. 
        // Vamos visitar a página de listagem manualmente.
        cy.visit('http://127.0.0.1:8000/partidas/');
        
        // (FIX) Agora podemos verificar se estamos na URL CORRETA (não apenas 'include')
        cy.url().should('eq', 'http://127.0.0.1:8000/partidas/'); 

        // Agora o botão deve ser "Ver Avaliação"
        cy.contains('a.btn-avaliar', 'Ver Avaliação').first().click();
        
        // Na página "ver_avaliacao.html", clica em "Avaliar Torcida"
        cy.contains('a', 'Avaliar Torcida').click();

     // --- Etapa 1 da Avaliação da Torcida (Página 1: /avaliar_torcida/X/) ---
        cy.url().should('include', '/partida/avaliar_torcida/');
        
        // Tenta clicar no 4º input (value="4") dentro do PRIMEIRO grupo .star-rating-container
        cy.get('.star-rating-container').eq(0).find('input[value="4"]').click({ force: true });
        
        // Tenta clicar no 3º input (value="3") dentro do SEGUNDO grupo .star-rating-container
        cy.get('.star-rating-container').eq(1).find('input[value="3"]').click({ force: true });

        cy.get('textarea[name="comentario"]').type('Review da performance da torcida.');
        cy.contains('button', 'Enviar Review').click();

        // --- Etapa 2 da Avaliação da Torcida (Página 2: /.../2/) ---
        cy.url().should('include', '/2/'); // Verifica se foi para a segunda etapa
        
        // Tenta clicar no 5º input (value="5") dentro do PRIMEIRO grupo .star-rating-container
        cy.get('.star-rating-container').eq(0).find('input[value="5"]').click({ force: true });

        // Tenta clicar no 4º input (value="4") dentro do SEGUNDO grupo .star-rating-container
        cy.get('.star-rating-container').eq(1).find('input[value="4"]').click({ force: true });

        cy.get('textarea[name="comentario"]').type('Segundo review, sobre o visual.');
        cy.contains('button', 'Enviar Review').click();
        // --- PASSO 6: Avaliar Estádio ---
        // (Após o último review, o app deve redirecionar. Vamos garantir clicando em Home)
        cy.get('.header-title a').click(); // Clica em "Only Football Fans" no header
        
        cy.url().should('eq', 'http://127.0.0.1:8000/');
        
        cy.contains('a.action-card', 'Avaliar Estádio').click();
        
        // Clica em "Nova Avaliação"
        cy.contains('a', 'Nova Avaliação').click();
        
        // Preenche o formulário de avaliação do estádio
        cy.get('input[name="nome_estadio"]').type('Estádio Maracanã Teste');
        cy.get('input[name="nota"][value="5"]').click({ force: true }); // 5 estrelas
        cy.get('textarea[name="comentario"]').type('Comentário sobre o estádio.');
        cy.contains('button', 'Enviar Avaliação').click();

        // --- PASSO 7: Galeria de Mídia ---
        cy.get('.header-title a').click(); // Clica em "Only Football Fans" no header
        cy.url().should('eq', 'http://127.0.0.1:8000/');
        
        cy.contains('a.action-card', 'Galeria de Mídia').click();
        cy.url().should('include', '/galeria/');
        
        // Clica em "Adicionar mídia"
        cy.contains('a', 'Adicionar mídia').click(); 
        
        // (Apenas clica em "Enviar" como instruído, mesmo sem anexar arquivo)
        cy.contains('button', 'Enviar').click();
        
        // Clica em "Only Football Fans" no header (Conforme Passo 7)
        cy.get('.header-title a').click();

        // --- PASSO 8: Adicionar Link de Jogo ---
        cy.url().should('eq', 'http://127.0.0.1:8000/');
        
        // Abre o menu lateral
        cy.get('.menu-toggle').click();
        
        // Clica em "Assistir Jogos"
        cy.get('.sidebar').contains('a', 'Assistir Jogos').click();
        cy.url().should('include', '/links/');
        
        // Clica em "Adicionar Novo Link"
        cy.contains('a', 'Adicionar Novo Link').click();
        
        // Preenche o formulário de link
        cy.get('input[name="nome_do_jogo"]').type('Final da Copa de 2002');
        cy.get('input[name="url"]').type('https://www.youtube.com/watch?v=exemplo');
        cy.contains('button', 'Salvar Link').click();
        
        // Volta para a página inicial
        cy.get('.header-title a').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/');
    });

});