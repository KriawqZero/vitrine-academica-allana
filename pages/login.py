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
            st.info("""
            **Credenciais para teste:**
            
            **Usuário:** Allana  
            **Senha:** allana123
            """)
    
    if submitted:
        # Validação mockada
        if usuario == "Allana" and senha == "allana123":
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")
            st.warning("Verifique suas credenciais e tente novamente.")
    
    return False

if __name__ == "__main__":
    show_login() 