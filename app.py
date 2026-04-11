<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>{% block title %}Cobrança Inteligente{% endblock %}</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <!-- PWA Meta Tags -->
    <link rel="manifest" href="/static/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Cobrança Auto">
    <meta name="theme-color" content="#1e3c72">
    
    <!-- Ícones iOS -->
    <link rel="apple-touch-icon" href="/static/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
    <link rel="shortcut icon" href="/static/favicon.ico">
    
    <style>
        /* (Mantenha todo o CSS que já estava antes, não vou repetir aqui para não encher o bloco) */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Roboto, system-ui, sans-serif; }
        body { background: #f4f7fc; min-height: 100vh; display: flex; flex-direction: column; }
        .header { background: #1e3c72; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 1rem 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 10; }
        .header h1 { font-size: 1.6rem; font-weight: 600; display: flex; align-items: center; gap: 10px; }
        .nav-bar { background: white; padding: 0.6rem 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; flex-wrap: wrap; gap: 0.8rem 1.5rem; border-bottom: 1px solid #e0e7ef; }
        .nav-bar a { color: #2c3e50; text-decoration: none; font-weight: 500; padding: 0.5rem 0; border-bottom: 3px solid transparent; display: inline-flex; align-items: center; gap: 8px; }
        .main-content { flex: 1; padding: 1.5rem; max-width: 1200px; margin: 0 auto; width: 100%; }
        .card { background: white; border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 6px 18px rgba(0,0,0,0.05); }
        .btn { background: #2a5298; color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 40px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; }
        .footer { text-align: center; padding: 1.5rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: auto; }
        /* Banner de Instalação */
        #installBanner { display: none; position: fixed; bottom: 20px; left: 20px; right: 20px; background: #1e3c72; color: white; padding: 15px 20px; border-radius: 50px; box-shadow: 0 6px 20px rgba(0,0,0,0.3); z-index: 9999; justify-content: space-between; align-items: center; }
        #installBanner button { background: white; color: #1e3c72; border: none; padding: 8px 20px; border-radius: 30px; font-weight: bold; margin-left: 10px; }
    </style>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header class="header">
        <h1><i class="fas fa-car"></i> Cobrança Auto Fácil</h1>
    </header>
    <nav class="nav-bar">
        <a href="{{ url_for('index') }}"><i class="fas fa-home"></i> Dashboard</a>
        <a href="{{ url_for('listar_clientes') }}"><i class="fas fa-users"></i> Clientes</a>
        <a href="{{ url_for('nova_parcela') }}"><i class="fas fa-file-invoice-dollar"></i> Nova Parcela</a>
        <a href="{{ url_for('novo_cliente') }}"><i class="fas fa-user-plus"></i> Novo Cliente</a>
    </nav>

    <main class="main-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <p>&copy; {{ now.year }} Cobrança Auto Fácil – Lembretes inteligentes para seu negócio</p>
    </footer>

    <!-- BANNER DE INSTALAÇÃO (Não é popup de sistema, é convite visual) -->
    <div id="installBanner">
        <span><i class="fas fa-download"></i> Instale o App para acesso rápido e notificações</span>
        <div>
            <button id="installBtn">Instalar</button>
            <button id="closeBanner" style="background:transparent; color:white; font-size:20px;">&times;</button>
        </div>
    </div>

    <script>
        // 1. REGISTRO DO SERVICE WORKER (Para notificações Push)
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js')
                    .then(reg => console.log('✅ Service Worker registrado'))
                    .catch(err => console.log('❌ Erro SW:', err));
            });
        }

        // 2. SOLICITAÇÃO DE PERMISSÃO PARA NOTIFICAÇÕES (Pop-up do sistema - aparece UMA VEZ)
        // Só pede se ainda não foi concedida ou negada
        if ('Notification' in window && Notification.permission === 'default') {
            // Aguarda 3 segundos após o carregamento para não atrapalhar a navegação
            setTimeout(() => {
                Notification.requestPermission();
            }, 3000);
        }

        // 3. VERIFICAÇÃO DE LEMBRETES (Push)
        async function verificarLembretesENotificar() {
            if (Notification.permission !== 'granted') return;
            
            try {
                const response = await fetch('/api/lembretes');
                const data = await response.json();
                if (data.lembretes && data.lembretes.length > 0) {
                    data.lembretes.forEach(item => {
                        navigator.serviceWorker.ready.then(reg => {
                            reg.showNotification('🔔 Cobrança Auto Fácil', {
                                body: `${item.cliente} - Parcela ${item.parcela} vence em ${item.dias} dias. ${item.valor}`,
                                icon: '/static/android-icon-192x192.png',
                                badge: '/static/favicon-96x96.png',
                                vibrate: [200, 100, 200],
                                tag: `parcela-${item.cliente}-${item.parcela}`,
                                renotify: true
                            });
                        });
                    });
                }
            } catch (e) {
                console.log('Erro ao buscar lembretes:', e);
            }
        }

        // Verifica ao carregar e a cada 30 minutos
        window.addEventListener('load', () => {
            setTimeout(verificarLembretesENotificar, 5000);
        });
        setInterval(verificarLembretesENotificar, 30 * 60 * 1000);

        // 4. LÓGICA DO BANNER DE INSTALAÇÃO (PWA)
        let deferredPrompt;
        const banner = document.getElementById('installBanner');
        const installBtn = document.getElementById('installBtn');
        const closeBtn = document.getElementById('closeBanner');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            // Só mostra o banner se o app não estiver instalado
            if (!window.matchMedia('(display-mode: standalone)').matches) {
                banner.style.display = 'flex';
            }
        });

        installBtn.addEventListener('click', () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                    banner.style.display = 'none';
                });
            }
        });

        closeBtn.addEventListener('click', () => {
            banner.style.display = 'none';
        });

        // Esconde se já estiver em modo standalone (app instalado)
        if (window.matchMedia('(display-mode: standalone)').matches) {
            banner.style.display = 'none';
        }
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
