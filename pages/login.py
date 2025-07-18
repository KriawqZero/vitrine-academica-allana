import streamlit as st
import sys
import os

# Adicionar o diretório pages ao path para importar as páginas
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Importar as outras páginas
from cadastro import show_cadastro
from enviartcc import show_enviar_tcc
from exibirtccs import show_exibir_tccs

# Configuração da página
st.set_page_config(
    page_title="Vitrine Acadêmica de TCCs", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do estado da sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "usuarios" not in st.session_state:
    st.session_state.usuarios = []
if "current_page" not in st.session_state:
    # Se não há usuários cadastrados, direcionar para cadastro
    if not st.session_state.usuarios:
        st.session_state.current_page = "cadastro"
    else:
        st.session_state.current_page = "login"

def show_sidebar():
    """Exibe a barra lateral com navegação"""
    with st.sidebar:
        st.title("Vitrine Acadêmica")
        st.markdown("---")
        
        if not st.session_state.logged_in:
            # Menu para usuários não logados
            st.markdown("### Acesso")
            
            if st.button("Login", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
            
            if st.button("Cadastrar-se", use_container_width=True):
                st.session_state.current_page = "cadastro"
                st.rerun()
                
        else:
            # Menu para usuários logados
            st.success(f"Olá, {st.session_state.usuario}!")
            st.markdown("---")
            
            st.markdown("### Navegação")
            
            if st.button("Enviar TCC", use_container_width=True):
                st.session_state.current_page = "enviartcc"
                st.rerun()
            
            if st.button("Listar TCCs", use_container_width=True):
                st.session_state.current_page = "exibirtccs"
                st.rerun()
            
            st.markdown("---")
            st.markdown("### Conta")
            
            if st.button("Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.usuario = None
                st.session_state.usuario_logado = None
                st.session_state.current_page = "login"
                st.success("Logout realizado com sucesso!")
                st.rerun()
        
        # Informações do sistema
        st.markdown("---")
        st.markdown("### Sobre")
        st.info("""
        **Vitrine Acadêmica de TCCs**
        
        Sistema para cadastro e exibição de Trabalhos de Conclusão de Curso.
        
        Desenvolvido com Streamlit
        """)

def show_main_content():
    """Exibe o conteúdo principal baseado na página atual"""
    
    # Roteamento de páginas
    if st.session_state.current_page == "login":
        show_login()
        
    elif st.session_state.current_page == "cadastro":
        show_cadastro()
        
    elif st.session_state.current_page == "enviartcc":
        if st.session_state.logged_in:
            show_enviar_tcc()
        else:
            st.warning("Você precisa fazer login para acessar esta página.")
            st.session_state.current_page = "login"
            st.rerun()
            
    elif st.session_state.current_page == "exibirtccs":
        if st.session_state.logged_in:
            show_exibir_tccs()
        else:
            st.warning("Você precisa fazer login para acessar esta página.")
            st.session_state.current_page = "login"
            st.rerun()
    
    else:
        # Página padrão (home/dashboard)
        show_dashboard()

def show_dashboard():
    """Exibe o dashboard principal"""
    st.title("Bem-vindo à Vitrine Acadêmica de TCCs")
    
    if not st.session_state.logged_in:
        st.markdown("""
        ### O que é a Vitrine Acadêmica?
        
        A **Vitrine Acadêmica de TCCs** é uma plataforma dedicada ao cadastro, organização e exibição de Trabalhos de Conclusão de Curso (TCCs).
        
        ### Funcionalidades:
        
        - **Cadastro de TCCs**: Registre seus trabalhos acadêmicos com todas as informações relevantes
        - **Listagem Organizada**: Visualize todos os TCCs cadastrados de forma organizada
        - **Busca e Filtros**: Encontre trabalhos por curso, ano, palavras-chave
        - **Edição**: Atualize informações dos seus TCCs quando necessário
        - **Gestão de Usuários**: Sistema de login e cadastro de usuários
        
        ### Como começar:
        
        1. **Faça seu cadastro** ou **entre com sua conta**
        2. **Cadastre seus TCCs** com todas as informações
        3. **Explore** os trabalhos de outros usuários
        4. **Gerencie** seus trabalhos acadêmicos
        
        ---
        **Use o menu lateral para navegar pelo sistema!**
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Fazer Login", type="primary", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
        
        with col2:
            if st.button("Criar Conta", use_container_width=True):
                st.session_state.current_page = "cadastro"
                st.rerun()
    
    else:
        # Dashboard para usuários logados
        st.markdown(f"### Bem-vindo(a), {st.session_state.usuario}!")
        
        # Estatísticas rápidas
        if "tccs" in st.session_state and st.session_state.tccs:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_tccs = len(st.session_state.tccs)
                st.metric("Total de TCCs", total_tccs)
            
            with col2:
                # Contar TCCs do usuário logado usando o ID do usuário
                usuario_id = st.session_state.get("usuario_logado", {}).get("usuario", "")
                meus_tccs = len([tcc for tcc in st.session_state.tccs 
                               if tcc.get('usuario_id') == usuario_id])
                st.metric("Meus TCCs", meus_tccs)
            
            with col3:
                cursos_unicos = len(set([tcc.get('curso', '') for tcc in st.session_state.tccs]))
                st.metric("Cursos", cursos_unicos)
        
        st.markdown("### Ações Rápidas")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cadastrar Novo TCC", type="primary", use_container_width=True):
                st.session_state.current_page = "enviartcc"
                st.rerun()
        
        with col2:
            if st.button("Ver Todos os TCCs", use_container_width=True):
                st.session_state.current_page = "exibirtccs"
                st.rerun()

def show_login():
    """Exibe a página de login"""
    st.title("Login - Vitrine Acadêmica")
    
    # Verifica se já está logado
    if st.session_state.get("logged_in", False):
        st.success(f"Bem-vinda, {st.session_state.get('usuario', 'Usuário')}!")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.usuario = None
                st.rerun()
        return True
    
    # Formulário de login
    st.markdown("### Entre com suas credenciais:")
    
    with st.form("login_form"):
        col1, col2 = st.columns([2, 3])
        
        with col1:
            usuario = st.text_input("Usuário:", placeholder="Digite seu usuário")
            senha = st.text_input("Senha:", type="password", placeholder="Digite sua senha")
            
            submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
        
        with col2:
            # Verificar se existem usuários cadastrados
            if "usuarios" in st.session_state and st.session_state.usuarios:
                st.info(f"""
                **Usuários cadastrados:** {len(st.session_state.usuarios)}
                
                Use o nome de usuário e senha que você cadastrou no sistema.
                """)
            else:
                st.warning("""
                **Nenhum usuário cadastrado ainda.**
                
                Faça seu cadastro primeiro para poder fazer login.
                """)
                
                if st.button("Ir para Cadastro", key="btn_cadastro_from_login"):
                    st.session_state.current_page = "cadastro"
                    st.rerun()
    
    if submitted:
        # Validação baseada em usuários cadastrados
        if not usuario or not senha:
            st.error("Preencha todos os campos!")
            return False
        
        # Verificar se existem usuários cadastrados
        if "usuarios" not in st.session_state or not st.session_state.usuarios:
            st.error("Nenhum usuário cadastrado no sistema!")
            st.info("Cadastre-se primeiro antes de fazer login.")
            return False
        
        # Buscar usuário nos cadastrados
        usuario_encontrado = None
        for user in st.session_state.usuarios:
            if user.get("usuario") == usuario and user.get("senha") == senha:
                usuario_encontrado = user
                break
        
        if usuario_encontrado:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario_encontrado.get("nome_completo", usuario)
            st.session_state.usuario_logado = usuario_encontrado
            st.success(f"Login realizado com sucesso! Bem-vindo(a), {usuario_encontrado.get('nome_completo', usuario)}!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")
            st.warning("Verifique suas credenciais e tente novamente.")
    
    return False

def main():
    """Função principal da aplicação"""
    # Mostrar barra lateral
    show_sidebar()
    
    # Mostrar conteúdo principal
    show_main_content()

if __name__ == "__main__":
    main() 