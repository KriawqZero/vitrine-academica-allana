import streamlit as st
import datetime

def show_cadastro():
    """Exibe a página de cadastro de usuário"""
    st.title("Cadastro de Usuário")
    
    st.markdown("### Crie sua conta na Vitrine Acadêmica:")
    
    with st.form("cadastro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_completo = st.text_input("Nome Completo *", placeholder="Digite seu nome completo")
            email = st.text_input("E-mail *", placeholder="exemplo@email.com")
            usuario = st.text_input("Nome de Usuário *", placeholder="Digite um nome de usuário")
            
        with col2:
            instituicao = st.text_input("Instituição *", placeholder="Nome da sua instituição")
            curso = st.text_input("Curso", placeholder="Seu curso (opcional)")
        
        col3, col4 = st.columns(2)
        with col3:
            senha = st.text_input("Senha *", type="password", placeholder="Digite uma senha segura")
        with col4:
            confirmar_senha = st.text_input("Confirmar Senha *", type="password", placeholder="Confirme sua senha")
        
        # Termos de uso
        aceitar_termos = st.checkbox("Aceito os termos de uso e política de privacidade *")
        
        st.markdown("---")
        submitted = st.form_submit_button("Criar Conta", type="primary", use_container_width=True)
        
        if submitted:
            # Validação
            erros = []
            
            if not nome_completo or not email or not usuario or not instituicao or not senha:
                erros.append("Preencha todos os campos obrigatórios (*)")
            
            if senha != confirmar_senha:
                erros.append("As senhas não coincidem")
            
            if len(senha) < 6:
                erros.append("A senha deve ter pelo menos 6 caracteres")
            
            if not aceitar_termos:
                erros.append("Você deve aceitar os termos de uso")
            
            if "@" not in email:
                erros.append("Digite um e-mail válido")
            
            # Verificar se usuário já existe
            if "usuarios" in st.session_state:
                for user in st.session_state.usuarios:
                    if user.get("usuario") == usuario:
                        erros.append("Nome de usuário já existe! Escolha outro.")
                        break
                    if user.get("email") == email:
                        erros.append("E-mail já cadastrado! Use outro e-mail.")
                        break
            
            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                # Cadastro bem-sucedido
                novo_usuario = {
                    "nome_completo": nome_completo,
                    "email": email,
                    "usuario": usuario,
                    "senha": senha,
                    "instituicao": instituicao,
                    "curso": curso,
                    "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                
                # Salvar no session_state
                if "usuarios" not in st.session_state:
                    st.session_state.usuarios = []
                st.session_state.usuarios.append(novo_usuario)
                
                st.success("Conta criada com sucesso!")
                st.balloons()
                
                st.info("""
                **Parabéns!** Sua conta foi criada com sucesso.
                
                **Próximos passos:**
                1. Faça login na página de Login
                2. Comece a cadastrar seus TCCs
                
                **Dados da conta criada:**
                - **Nome:** {nome}
                - **Usuário:** {usuario}
                - **E-mail:** {email}
                - **Instituição:** {instituicao}
                """.format(
                    nome=nome_completo,
                    usuario=usuario,
                    email=email,
                    instituicao=instituicao
                ))
                
                if st.button("Ir para Login"):
                    st.session_state.current_page = "login"
                    st.rerun()
    
    # Link para login
    st.markdown("---")
    st.markdown("**Já tem uma conta?**")
    if st.button("Fazer Login"):
        st.session_state.current_page = "login"
        st.rerun()

if __name__ == "__main__":
    show_cadastro() 