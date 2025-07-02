import streamlit as st

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
                    st.switch_page("pages/cadastro.py")
    
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

if __name__ == "__main__":
    show_login() 