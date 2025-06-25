import streamlit as st
import datetime
from typing import Dict, List, Optional

# Configuração da página
st.set_page_config(
    page_title="Vitrine Acadêmica de TCCs",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do estado da sessão
def init_session_state():
    if "tccs" not in st.session_state:
        st.session_state.tccs = []
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None

# Função para gerar ID único
def generate_id() -> int:
    if not st.session_state.tccs:
        return 1
    return max([tcc.get('id', 0) for tcc in st.session_state.tccs]) + 1

# Função para validar dados do TCC
def validate_tcc_data(titulo: str, autor: str, curso: str, ano: int, resumo: str) -> Optional[str]:
    if not titulo.strip():
        return "O título é obrigatório"
    if not autor.strip():
        return "O autor é obrigatório"
    if not curso.strip():
        return "O curso é obrigatório"
    if not resumo.strip():
        return "O resumo é obrigatório"
    if ano < 2000 or ano > datetime.datetime.now().year + 1:
        return "Ano inválido"
    return None

# Função para adicionar TCC
def add_tcc(titulo: str, autor: str, curso: str, ano: int, resumo: str, orientador: str = "", palavras_chave: str = ""):
    validation_error = validate_tcc_data(titulo, autor, curso, ano, resumo)
    if validation_error:
        st.error(validation_error)
        return False
    
    new_tcc = {
        "id": generate_id(),
        "titulo": titulo.strip(),
        "autor": autor.strip(),
        "curso": curso.strip(),
        "ano": ano,
        "resumo": resumo.strip(),
        "orientador": orientador.strip(),
        "palavras_chave": palavras_chave.strip(),
        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    st.session_state.tccs.append(new_tcc)
    st.success("TCC cadastrado com sucesso!")
    return True

# Função para atualizar TCC
def update_tcc(tcc_id: int, titulo: str, autor: str, curso: str, ano: int, resumo: str, orientador: str = "", palavras_chave: str = ""):
    validation_error = validate_tcc_data(titulo, autor, curso, ano, resumo)
    if validation_error:
        st.error(validation_error)
        return False
    
    for i, tcc in enumerate(st.session_state.tccs):
        if tcc["id"] == tcc_id:
            st.session_state.tccs[i].update({
                "titulo": titulo.strip(),
                "autor": autor.strip(),
                "curso": curso.strip(),
                "ano": ano,
                "resumo": resumo.strip(),
                "orientador": orientador.strip(),
                "palavras_chave": palavras_chave.strip()
            })
            st.success("TCC atualizado com sucesso!")
            st.session_state.editing_id = None
            return True
    return False

# Função para excluir TCC
def delete_tcc(tcc_id: int):
    st.session_state.tccs = [tcc for tcc in st.session_state.tccs if tcc["id"] != tcc_id]
    st.success("TCC excluído com sucesso!")
    st.rerun()

# Função para filtrar TCCs
def filter_tccs(tccs: List[Dict], curso_filter: str, ano_filter: str, search_term: str = "") -> List[Dict]:
    filtered = tccs.copy()
    
    if curso_filter != "Todos":
        filtered = [tcc for tcc in filtered if tcc["curso"].lower() == curso_filter.lower()]
    
    if ano_filter != "Todos":
        filtered = [tcc for tcc in filtered if str(tcc["ano"]) == ano_filter]
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [
            tcc for tcc in filtered 
            if search_lower in tcc["titulo"].lower() 
            or search_lower in tcc["autor"].lower()
            or search_lower in tcc["resumo"].lower()
            or search_lower in tcc.get("palavras_chave", "").lower()
        ]
    
    return filtered

# Página de cadastro
def page_cadastrar():
    st.header("Cadastrar Novo TCC")
    
    with st.form("form_tcc", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("Título do TCC *", placeholder="Digite o título do trabalho")
            autor = st.text_input("Autor *", placeholder="Nome completo do autor")
            curso = st.text_input("Curso *", placeholder="Nome do curso")
            
        with col2:
            ano = st.number_input("Ano *", min_value=2000, max_value=datetime.datetime.now().year + 1, value=datetime.datetime.now().year)
            orientador = st.text_input("Orientador", placeholder="Nome do orientador")
            palavras_chave = st.text_input("Palavras-chave", placeholder="Separadas por vírgula")
            
        resumo = st.text_area("Resumo *", height=150, placeholder="Descreva brevemente o trabalho desenvolvido")
        
        submitted = st.form_submit_button("Salvar TCC", type="primary")
            
        if submitted:
            if add_tcc(titulo, autor, curso, ano, resumo, orientador, palavras_chave):
                st.balloons()

# Página de listagem
def page_listar():
    st.header("Vitrine de TCCs")
    
    # Estatísticas
    total_tccs = len(st.session_state.tccs)
    cursos_unicos = len(set([tcc["curso"] for tcc in st.session_state.tccs])) if st.session_state.tccs else 0
    ano_atual = datetime.datetime.now().year
    tccs_ano_atual = len([tcc for tcc in st.session_state.tccs if tcc["ano"] == ano_atual])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TCCs Cadastrados", total_tccs)
    with col2:
        st.metric("Cursos Diferentes", cursos_unicos)
    with col3:
        st.metric(f"TCCs de {ano_atual}", tccs_ano_atual)
    
    if not st.session_state.tccs:
        st.info("Nenhum TCC cadastrado ainda. Comece cadastrando o primeiro TCC na aba 'Cadastrar TCC'.")
        return
    
    # Filtros
    st.subheader("Filtros de Busca")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursos_disponiveis = ["Todos"] + sorted(list(set([tcc["curso"] for tcc in st.session_state.tccs])))
        curso_filter = st.selectbox("Filtrar por Curso", cursos_disponiveis)
    
    with col2:
        anos_disponiveis = ["Todos"] + sorted(list(set([str(tcc["ano"]) for tcc in st.session_state.tccs])), reverse=True)
        ano_filter = st.selectbox("Filtrar por Ano", anos_disponiveis)
    
    with col3:
        search_term = st.text_input("Buscar por palavra-chave", placeholder="Buscar em títulos, autores, resumos...")
    
    # Aplicar filtros
    tccs_filtrados = filter_tccs(st.session_state.tccs, curso_filter, ano_filter, search_term)
    
    if not tccs_filtrados:
        st.warning("Nenhum TCC encontrado com os filtros aplicados.")
        return
    
    st.subheader(f"{len(tccs_filtrados)} TCC(s) encontrado(s)")
    
    # Listagem de TCCs
    for tcc in sorted(tccs_filtrados, key=lambda x: x["ano"], reverse=True):
        with st.container():
            if st.session_state.editing_id == tcc["id"]:
                # Modo de edição
                with st.form(f"edit_form_{tcc['id']}"):
                    st.subheader("Editando TCC")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        titulo_edit = st.text_input("Título", value=tcc["titulo"])
                        autor_edit = st.text_input("Autor", value=tcc["autor"])
                        curso_edit = st.text_input("Curso", value=tcc["curso"])
                    
                    with col2:
                        ano_edit = st.number_input("Ano", min_value=2000, max_value=datetime.datetime.now().year + 1, value=tcc["ano"])
                        orientador_edit = st.text_input("Orientador", value=tcc.get("orientador", ""))
                        palavras_chave_edit = st.text_input("Palavras-chave", value=tcc.get("palavras_chave", ""))
                    
                    resumo_edit = st.text_area("Resumo", value=tcc["resumo"], height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Salvar Alterações", type="primary"):
                            update_tcc(tcc["id"], titulo_edit, autor_edit, curso_edit, ano_edit, resumo_edit, orientador_edit, palavras_chave_edit)
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("Cancelar"):
                            st.session_state.editing_id = None
                            st.rerun()
            
            else:
                # Modo de visualização
                with st.expander(f"{tcc['titulo']} - {tcc['autor']} ({tcc['ano']})", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Autor:** {tcc['autor']}")
                        st.write(f"**Curso:** {tcc['curso']}")
                        st.write(f"**Ano:** {tcc['ano']}")
                        
                        if tcc.get("orientador"):
                            st.write(f"**Orientador:** {tcc['orientador']}")
                        
                        if tcc.get("palavras_chave"):
                            st.write(f"**Palavras-chave:** {tcc['palavras_chave']}")
                        
                        st.write(f"**Cadastrado em:** {tcc['data_cadastro']}")
                        
                        st.write("**Resumo:**")
                        st.write(tcc["resumo"])
                    
                    with col2:
                        if st.button("Editar", key=f"edit_{tcc['id']}", use_container_width=True):
                            st.session_state.editing_id = tcc["id"]
                            st.rerun()
                        
                        if st.button("Excluir", key=f"delete_{tcc['id']}", use_container_width=True, type="secondary"):
                            if st.session_state.get(f"confirm_delete_{tcc['id']}", False):
                                delete_tcc(tcc["id"])
                            else:
                                st.session_state[f"confirm_delete_{tcc['id']}"] = True
                                st.warning("Clique novamente para confirmar a exclusão")
                                st.rerun()

# Função principal
def main():
    init_session_state()
    
    # Sidebar
    st.sidebar.title("Vitrine Acadêmica")
    st.sidebar.write("Sistema de Gestão de TCCs")
    
    # Menu principal
    menu_options = {
        "Cadastrar TCC": page_cadastrar,
        "Listar TCCs": page_listar
    }
    
    selected_page = st.sidebar.radio(
        "Navegação",
        list(menu_options.keys()),
        index=0
    )
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Estatísticas Rápidas")
    st.sidebar.metric("Total de TCCs", len(st.session_state.tccs))
    
    if st.session_state.tccs:
        anos = [tcc["ano"] for tcc in st.session_state.tccs]
        st.sidebar.metric("Ano mais recente", max(anos))
        st.sidebar.metric("Ano mais antigo", min(anos))
    
    st.sidebar.markdown("---")
    st.sidebar.info("Dica: Use os filtros para encontrar TCCs específicos!")
    
    # Executar página selecionada
    menu_options[selected_page]()

if __name__ == "__main__":
    main() 