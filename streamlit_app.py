import streamlit as st
import datetime
from typing import Dict, List, Optional

# Configuração da página
st.set_page_config(
    page_title="📚 Vitrine Acadêmica de TCCs",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado com TailwindCSS
def load_custom_css():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        .card {
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
        }
        .stat-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .filter-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .tcc-item {
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            background: white;
            transition: all 0.3s ease;
        }
        .tcc-item:hover {
            box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            border: none;
            cursor: pointer;
        }
        .btn-secondary {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            border: none;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do estado da sessão
def init_session_state():
    if "tccs" not in st.session_state:
        st.session_state.tccs = []
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None
    if "filter_curso" not in st.session_state:
        st.session_state.filter_curso = "Todos"
    if "filter_ano" not in st.session_state:
        st.session_state.filter_ano = "Todos"

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
    st.success("✅ TCC cadastrado com sucesso!")
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
            st.success("✅ TCC atualizado com sucesso!")
            st.session_state.editing_id = None
            return True
    return False

# Função para excluir TCC
def delete_tcc(tcc_id: int):
    st.session_state.tccs = [tcc for tcc in st.session_state.tccs if tcc["id"] != tcc_id]
    st.success("✅ TCC excluído com sucesso!")
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
    st.markdown('<div class="main-header"><h1>📝 Cadastrar Novo TCC</h1></div>', unsafe_allow_html=True)
    
    with st.form("form_tcc", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("📋 Título do TCC *", placeholder="Digite o título do trabalho")
            autor = st.text_input("👤 Autor *", placeholder="Nome completo do autor")
            curso = st.text_input("🎓 Curso *", placeholder="Nome do curso")
            
        with col2:
            ano = st.number_input("📅 Ano *", min_value=2000, max_value=datetime.datetime.now().year + 1, value=datetime.datetime.now().year)
            orientador = st.text_input("👨‍🏫 Orientador", placeholder="Nome do orientador")
            palavras_chave = st.text_input("🏷️ Palavras-chave", placeholder="Separadas por vírgula")
            
        resumo = st.text_area("📄 Resumo *", height=150, placeholder="Descreva brevemente o trabalho desenvolvido")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("💾 Salvar TCC", use_container_width=True)
            
        if submitted:
            if add_tcc(titulo, autor, curso, ano, resumo, orientador, palavras_chave):
                st.balloons()

# Página de listagem
def page_listar():
    st.markdown('<div class="main-header"><h1>📚 Vitrine de TCCs</h1></div>', unsafe_allow_html=True)
    
    # Estatísticas
    total_tccs = len(st.session_state.tccs)
    cursos_unicos = len(set([tcc["curso"] for tcc in st.session_state.tccs])) if st.session_state.tccs else 0
    ano_atual = datetime.datetime.now().year
    tccs_ano_atual = len([tcc for tcc in st.session_state.tccs if tcc["ano"] == ano_atual])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <h3 style="margin: 0; font-size: 2rem;">📊 {total_tccs}</h3>
            <p style="margin: 0;">TCCs Cadastrados</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <h3 style="margin: 0; font-size: 2rem;">🎓 {cursos_unicos}</h3>
            <p style="margin: 0;">Cursos Diferentes</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <h3 style="margin: 0; font-size: 2rem;">📅 {tccs_ano_atual}</h3>
            <p style="margin: 0;">TCCs de {ano_atual}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    if not st.session_state.tccs:
        st.markdown('''
        <div class="card text-center">
            <h3>📭 Nenhum TCC cadastrado ainda</h3>
            <p>Comece cadastrando o primeiro TCC na aba "Cadastrar TCC"</p>
        </div>
        ''', unsafe_allow_html=True)
        return
    
    # Filtros
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("🔍 Filtros de Busca")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursos_disponiveis = ["Todos"] + sorted(list(set([tcc["curso"] for tcc in st.session_state.tccs])))
        curso_filter = st.selectbox("Filtrar por Curso", cursos_disponiveis, key="filter_curso")
    
    with col2:
        anos_disponiveis = ["Todos"] + sorted(list(set([str(tcc["ano"]) for tcc in st.session_state.tccs])), reverse=True)
        ano_filter = st.selectbox("Filtrar por Ano", anos_disponiveis, key="filter_ano")
    
    with col3:
        search_term = st.text_input("🔍 Buscar por palavra-chave", placeholder="Buscar em títulos, autores, resumos...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    tccs_filtrados = filter_tccs(st.session_state.tccs, curso_filter, ano_filter, search_term)
    
    if not tccs_filtrados:
        st.warning("⚠️ Nenhum TCC encontrado com os filtros aplicados.")
        return
    
    st.subheader(f"📋 {len(tccs_filtrados)} TCC(s) encontrado(s)")
    
    # Listagem de TCCs
    for tcc in sorted(tccs_filtrados, key=lambda x: x["ano"], reverse=True):
        with st.container():
            if st.session_state.editing_id == tcc["id"]:
                # Modo de edição
                with st.form(f"edit_form_{tcc['id']}"):
                    st.markdown("### ✏️ Editando TCC")
                    
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
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.form_submit_button("💾 Salvar Alterações"):
                            update_tcc(tcc["id"], titulo_edit, autor_edit, curso_edit, ano_edit, resumo_edit, orientador_edit, palavras_chave_edit)
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar"):
                            st.session_state.editing_id = None
                            st.rerun()
            
            else:
                # Modo de visualização
                st.markdown(f'''
                <div class="tcc-item">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                        <h3 style="margin: 0; color: #667eea; font-size: 1.25rem;">{tcc["titulo"]}</h3>
                        <span style="background: #667eea; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.875rem;">{tcc["ano"]}</span>
                    </div>
                    
                    <div style="margin-bottom: 1rem;">
                        <p style="margin: 0.25rem 0;"><strong>👤 Autor:</strong> {tcc["autor"]}</p>
                        <p style="margin: 0.25rem 0;"><strong>🎓 Curso:</strong> {tcc["curso"]}</p>
                        {f'<p style="margin: 0.25rem 0;"><strong>👨‍🏫 Orientador:</strong> {tcc["orientador"]}</p>' if tcc.get("orientador") else ""}
                        {f'<p style="margin: 0.25rem 0;"><strong>🏷️ Palavras-chave:</strong> {tcc["palavras_chave"]}</p>' if tcc.get("palavras_chave") else ""}
                        <p style="margin: 0.25rem 0;"><strong>📅 Cadastrado em:</strong> {tcc["data_cadastro"]}</p>
                    </div>
                    
                    <div style="margin-bottom: 1rem;">
                        <strong>📄 Resumo:</strong>
                        <p style="margin-top: 0.5rem; text-align: justify; line-height: 1.6;">{tcc["resumo"]}</p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{tcc['id']}", use_container_width=True):
                        st.session_state.editing_id = tcc["id"]
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_{tcc['id']}", use_container_width=True):
                        if st.session_state.get(f"confirm_delete_{tcc['id']}", False):
                            delete_tcc(tcc["id"])
                        else:
                            st.session_state[f"confirm_delete_{tcc['id']}"] = True
                            st.warning("⚠️ Clique novamente para confirmar a exclusão")
                            st.rerun()

# Função principal
def main():
    load_custom_css()
    init_session_state()
    
    # Sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2>📚 Vitrine Acadêmica</h2>
        <p>Sistema de Gestão de TCCs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu principal
    menu_options = {
        "📝 Cadastrar TCC": page_cadastrar,
        "📚 Listar TCCs": page_listar
    }
    
    selected_page = st.sidebar.radio(
        "Navegação",
        list(menu_options.keys()),
        index=0
    )
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Estatísticas Rápidas")
    st.sidebar.metric("Total de TCCs", len(st.session_state.tccs))
    
    if st.session_state.tccs:
        anos = [tcc["ano"] for tcc in st.session_state.tccs]
        st.sidebar.metric("Ano mais recente", max(anos))
        st.sidebar.metric("Ano mais antigo", min(anos))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 0.5rem;">
        <small>
        💡 <strong>Dica:</strong> Use os filtros para encontrar TCCs específicos!
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    # Executar página selecionada
    menu_options[selected_page]()

if __name__ == "__main__":
    main()
