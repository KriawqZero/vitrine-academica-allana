import streamlit as st
import datetime

def show_exibir_tccs():
    """Exibe a página de listagem e gerenciamento de TCCs"""
    st.title("Lista de TCCs Cadastrados")
    
    # Verifica se está logado
    if not st.session_state.get("logged_in", False):
        st.warning("Você precisa fazer login para acessar esta página.")
        return
    
    # Inicialização do estado da sessão
    if "tccs" not in st.session_state:
        st.session_state.tccs = []
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None
    
    # Estatísticas
    if st.session_state.tccs:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de TCCs", len(st.session_state.tccs))
        with col2:
            anos = [tcc.get('ano', 0) for tcc in st.session_state.tccs]
            st.metric("Ano mais recente", max(anos) if anos else "N/A")
        with col3:
            cursos = set([tcc.get('curso', '') for tcc in st.session_state.tccs])
            st.metric("Cursos únicos", len(cursos))
        
        st.markdown("---")
    
    # Filtros
    if st.session_state.tccs:
        st.markdown("### Filtros:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtro_propriedade = st.selectbox(
                "Filtrar por proprietário:",
                ["Todos os TCCs", "Apenas meus TCCs", "TCCs de outros"]
            )
        
        with col2:
            filtro_curso = st.selectbox(
                "Filtrar por curso:",
                ["Todos"] + sorted(list(set([tcc.get('curso', '') for tcc in st.session_state.tccs])))
            )
        
        with col3:
            anos_disponiveis = sorted(list(set([tcc.get('ano', 0) for tcc in st.session_state.tccs])), reverse=True)
            filtro_ano = st.selectbox(
                "Filtrar por ano:",
                ["Todos"] + anos_disponiveis
            )
        
        with col4:
            busca_texto = st.text_input("Buscar no título:", placeholder="Digite para buscar...")
        
        st.markdown("---")
    
    # Lista de TCCs
    if not st.session_state.tccs:
        st.info("Nenhum TCC cadastrado ainda.")
        if st.button("Cadastrar primeiro TCC"):
            st.session_state.current_page = "enviartcc"
            st.rerun()
    else:
        # Aplicar filtros
        tccs_filtrados = st.session_state.tccs.copy()
        usuario_id = st.session_state.get("usuario_logado", {}).get("usuario", "")
        
        # Filtro por proprietário
        if filtro_propriedade == "Apenas meus TCCs":
            tccs_filtrados = [tcc for tcc in tccs_filtrados if tcc.get('usuario_id') == usuario_id]
        elif filtro_propriedade == "TCCs de outros":
            tccs_filtrados = [tcc for tcc in tccs_filtrados if tcc.get('usuario_id') != usuario_id]
        
        if filtro_curso != "Todos":
            tccs_filtrados = [tcc for tcc in tccs_filtrados if tcc.get('curso', '') == filtro_curso]
        
        if filtro_ano != "Todos":
            tccs_filtrados = [tcc for tcc in tccs_filtrados if tcc.get('ano', 0) == filtro_ano]
        
        if busca_texto:
            tccs_filtrados = [tcc for tcc in tccs_filtrados 
                            if busca_texto.lower() in tcc.get('titulo', '').lower()]
        
        st.markdown(f"### Exibindo {len(tccs_filtrados)} TCC(s):")
        
        # Mostrar TCCs filtrados
        for tcc in tccs_filtrados:
            with st.container():
                if st.session_state.editing_id == tcc["id"]:
                    # Verificar se o usuário pode editar este TCC
                    usuario_id = st.session_state.get("usuario_logado", {}).get("usuario", "")
                    if tcc.get('usuario_id') == usuario_id:
                        # Modo edição
                        mostrar_edicao_tcc(tcc)
                    else:
                        st.error("Você só pode editar seus próprios TCCs!")
                        st.session_state.editing_id = None
                        mostrar_tcc(tcc)
                else:
                    # Modo visualização
                    mostrar_tcc(tcc)

def mostrar_tcc(tcc):
    """Exibe um TCC em modo de visualização"""
    # Verificar se é TCC do usuário logado
    usuario_id = st.session_state.get("usuario_logado", {}).get("usuario", "")
    eh_meu_tcc = tcc.get('usuario_id') == usuario_id
    
    # Usar identificação diferente para TCCs do usuário logado
    if eh_meu_tcc:
        titulo_expandir = f"{tcc['titulo']} - {tcc['autor']} ({tcc['ano']}) - SEU TCC"
    else:
        titulo_expandir = f"{tcc['titulo']} - {tcc['autor']} ({tcc['ano']})"
    
    with st.expander(titulo_expandir, expanded=False):
        if eh_meu_tcc:
            st.info("Este é um TCC cadastrado por você.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Curso:** {tcc['curso']}")
            if tcc.get("orientador"):
                st.write(f"**Orientador:** {tcc['orientador']}")
            if tcc.get("instituicao"):
                st.write(f"**Instituição:** {tcc['instituicao']}")
            if tcc.get("palavras_chave"):
                st.write(f"**Palavras-chave:** {tcc['palavras_chave']}")
            st.write(f"**Cadastrado em:** {tcc['data_cadastro']}")
            if tcc.get("usuario_cadastro"):
                st.write(f"**Cadastrado por:** {tcc['usuario_cadastro']}")
        
        st.markdown("**Resumo:**")
        st.write(tcc['resumo'])
        
        # Botões de ação - só mostrar editar/excluir para o próprio usuário
        if eh_meu_tcc:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("Editar", key=f"edit_btn_{tcc['id']}"):
                    st.session_state.editing_id = tcc["id"]
                    st.rerun()
            with col2:
                if st.button("Excluir", key=f"del_btn_{tcc['id']}"):
                    st.session_state.tccs = [t for t in st.session_state.tccs if t["id"] != tcc["id"]]
                    st.success("TCC excluído!")
                    st.rerun()
        else:
            st.caption("Você só pode editar/excluir seus próprios TCCs.")

def mostrar_edicao_tcc(tcc):
    """Exibe um TCC em modo de edição"""
    with st.form(f"edit_{tcc['id']}"):
        st.subheader("Editando TCC")
        
        col1, col2 = st.columns(2)
        with col1:
            titulo_edit = st.text_input("Título", value=tcc["titulo"])
            autor_edit = st.text_input("Autor", value=tcc["autor"])
            curso_edit = st.text_input("Curso", value=tcc["curso"])
        with col2:
            ano_edit = st.number_input("Ano", 
                                     min_value=2000, 
                                     max_value=datetime.datetime.now().year + 1, 
                                     value=tcc["ano"])
            orientador_edit = st.text_input("Orientador", value=tcc.get("orientador", ""))
        
        resumo_edit = st.text_area("Resumo", value=tcc["resumo"], height=100)
        
        col3, col4 = st.columns(2)
        with col3:
            palavras_edit = st.text_input("Palavras-chave", value=tcc.get("palavras_chave", ""))
        with col4:
            instituicao_edit = st.text_input("Instituição", value=tcc.get("instituicao", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar", type="primary"):
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
                                "resumo": resumo_edit,
                                "palavras_chave": palavras_edit,
                                "instituicao": instituicao_edit
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

if __name__ == "__main__":
    show_exibir_tccs() 