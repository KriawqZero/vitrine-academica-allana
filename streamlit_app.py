import streamlit as st
import datetime

# Configuração da página
st.set_page_config(page_title="Vitrine Acadêmica de TCCs", layout="wide")

# Inicialização do estado da sessão
if "tccs" not in st.session_state:
    st.session_state.tccs = []
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

# Navegação simples
st.title("Vitrine Acadêmica de TCCs")
tab1, tab2 = st.tabs(["Cadastrar TCC", "Listar TCCs"])

# Função para gerar ID único
def generate_id():
    if not st.session_state.tccs:
        return 1
    return max([tcc.get('id', 0) for tcc in st.session_state.tccs]) + 1

# TAB 1: Cadastrar TCC
with tab1:
    st.header("Cadastrar Novo TCC")
    
    with st.form("form_tcc", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("Título do TCC *")
            autor = st.text_input("Autor *")
            curso = st.text_input("Curso *")
            
        with col2:
            ano = st.number_input("Ano *", min_value=2000, max_value=datetime.datetime.now().year + 1, 
                                value=datetime.datetime.now().year)
            orientador = st.text_input("Orientador")
        
        resumo = st.text_area("Resumo *", height=100)
        
        submitted = st.form_submit_button("Salvar TCC", type="primary")
        
        if submitted:
            # Validação simples
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
                    "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.tccs.append(new_tcc)
                st.success("TCC cadastrado com sucesso!")

# TAB 2: Listar TCCs
with tab2:
    st.header("Lista de TCCs")
    
    if not st.session_state.tccs:
        st.info("Nenhum TCC cadastrado ainda.")
    else:
        # Mostrar TCCs
        for tcc in st.session_state.tccs:
            with st.container():
                if st.session_state.editing_id == tcc["id"]:
                    # Modo edição
                    with st.form(f"edit_{tcc['id']}"):
                        st.subheader("Editando TCC")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            titulo_edit = st.text_input("Título", value=tcc["titulo"])
                            autor_edit = st.text_input("Autor", value=tcc["autor"])
                            curso_edit = st.text_input("Curso", value=tcc["curso"])
                        with col2:
                            ano_edit = st.number_input("Ano", min_value=2000, max_value=datetime.datetime.now().year + 1, 
                                                     value=tcc["ano"])
                            orientador_edit = st.text_input("Orientador", value=tcc.get("orientador", ""))
                        
                        resumo_edit = st.text_area("Resumo", value=tcc["resumo"], height=80)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Salvar"):
                                if titulo_edit and autor_edit and curso_edit and resumo_edit:
                                    # Atualizar TCC
                                    for i, t in enumerate(st.session_state.tccs):
                                        if t["id"] == tcc["id"]:
                                            st.session_state.tccs[i].update({
                                                "titulo": titulo_edit,
                                                "autor": autor_edit,
                                                "curso": curso_edit,
                                                "ano": ano_edit,
                                                "orientador": orientador_edit,
                                                "resumo": resumo_edit
                                            })
                                            break
                                    st.session_state.editing_id = None
                                    st.success("TCC atualizado!")
                                    st.rerun()
                                else:
                                    st.error("Preencha todos os campos obrigatórios")
                        
                        with col2:
                            if st.form_submit_button("Cancelar"):
                                st.session_state.editing_id = None
                                st.rerun()
                
                else:
                    # Modo visualização
                    with st.expander(f"{tcc['titulo']} - {tcc['autor']} ({tcc['ano']})"):
                        st.write(f"**Curso:** {tcc['curso']}")
                        if tcc.get("orientador"):
                            st.write(f"**Orientador:** {tcc['orientador']}")
                        st.write(f"**Cadastrado em:** {tcc['data_cadastro']}")
                        st.write(f"**Resumo:** {tcc['resumo']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Editar", key=f"edit_btn_{tcc['id']}"):
                                st.session_state.editing_id = tcc["id"]
                                st.rerun()
                        with col2:
                            if st.button("Excluir", key=f"del_btn_{tcc['id']}"):
                                st.session_state.tccs = [t for t in st.session_state.tccs if t["id"] != tcc["id"]]
                                st.success("TCC excluído!")
                                st.rerun() 