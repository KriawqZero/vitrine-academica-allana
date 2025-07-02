import streamlit as st
import datetime

def show_enviar_tcc():
    """Exibe a página de cadastro de TCCs"""
    st.title("Cadastrar Novo TCC")
    
    # Verifica se está logado
    if not st.session_state.get("logged_in", False):
        st.warning("Você precisa fazer login para acessar esta página.")
        return
    
    # Inicialização do estado da sessão para TCCs
    if "tccs" not in st.session_state:
        st.session_state.tccs = []
    
    st.markdown("### Preencha as informações do seu TCC:")
    
    with st.form("form_tcc", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("Título do TCC *", placeholder="Digite o título do trabalho")
            autor = st.text_input("Autor *", placeholder="Nome do autor")
            curso = st.text_input("Curso *", placeholder="Nome do curso")
            
        with col2:
            ano = st.number_input("Ano *", 
                                min_value=2000, 
                                max_value=datetime.datetime.now().year + 1, 
                                value=datetime.datetime.now().year)
            orientador = st.text_input("Orientador", placeholder="Nome do orientador (opcional)")
        
        resumo = st.text_area("Resumo *", 
                            height=150, 
                            placeholder="Escreva um resumo do seu trabalho...")
        
        # Campos adicionais
        col3, col4 = st.columns(2)
        with col3:
            palavras_chave = st.text_input("Palavras-chave", 
                                         placeholder="Separadas por vírgula")
        with col4:
            instituicao = st.text_input("Instituição", 
                                      placeholder="Nome da instituição")
        
        st.markdown("---")
        submitted = st.form_submit_button("Salvar TCC", type="primary", use_container_width=True)
        
        if submitted:
            # Validação
            if not titulo or not autor or not curso or not resumo:
                st.error("Preencha todos os campos obrigatórios (*)")
            else:
                new_tcc = {
                    "id": generate_id(),
                    "titulo": titulo,
                    "autor": autor,
                    "curso": curso,
                    "ano": ano,
                    "orientador": orientador,
                    "resumo": resumo,
                    "palavras_chave": palavras_chave,
                    "instituicao": instituicao,
                    "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "usuario_cadastro": st.session_state.get("usuario", "Desconhecido")
                }
                st.session_state.tccs.append(new_tcc)
                st.success("TCC cadastrado com sucesso!")
                st.balloons()

def generate_id():
    """Gera um ID único para o TCC"""
    if not st.session_state.tccs:
        return 1
    return max([tcc.get('id', 0) for tcc in st.session_state.tccs]) + 1

if __name__ == "__main__":
    show_enviar_tcc() 