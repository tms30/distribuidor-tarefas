
import streamlit as st
import random

st.set_page_config(page_title="Distribuidor de Tarefas", layout="centered")
st.title("🎯 Distribuidor Aleatório de Tarefas")

# Definindo código de administrador
codigo_admin = st.sidebar.text_input("Código de administrador", type="password")
modo_admin = codigo_admin == "1234"  # Troca para o teu código

# Sessão para manter o estado
if 'tarefas' not in st.session_state:
    st.session_state.tarefas = []
if 'pessoas' not in st.session_state:
    st.session_state.pessoas = []
if 'exclusoes' not in st.session_state:
    st.session_state.exclusoes = {}
if 'atribuicoes' not in st.session_state:
    st.session_state.atribuicoes = {}

# Se o usuário for administrador
if modo_admin:
    st.header("1. Adicionar Pessoas do Grupo")
    nome_pessoa = st.text_input("Nome da Pessoa")
    if st.button("Adicionar Pessoa"):
        if nome_pessoa and nome_pessoa not in st.session_state.pessoas:
            st.session_state.pessoas.append(nome_pessoa)

    st.write("**Pessoas no grupo:**", st.session_state.pessoas)

    st.header("2. Adicionar Tarefas")
    nome_tarefa = st.text_input("Descrição da Tarefa")
    if st.button("Adicionar Tarefa"):
        if nome_tarefa:
            st.session_state.tarefas.append(nome_tarefa)

    st.write("**Tarefas adicionadas:**", st.session_state.tarefas)

else:
    st.info("Apenas administradores podem adicionar pessoas e tarefas.")

st.header("3. Configurações de Distribuição")
repeticao = st.checkbox("Permitir que a mesma pessoa receba várias tarefas", value=True)

st.subheader("Excluir pessoas de tarefas específicas")
for tarefa in st.session_state.tarefas:
    excluidos = st.multiselect(f"Excluir da tarefa: '{tarefa}'", st.session_state.pessoas, key=f"excl_{tarefa}")
    st.session_state.exclusoes[tarefa] = excluidos

if st.button("Distribuir Tarefas"):
    atribuicoes = {}
    pessoas_disponiveis = st.session_state.pessoas.copy()
    for tarefa in st.session_state.tarefas:
        elegiveis = [p for p in st.session_state.pessoas if p not in st.session_state.exclusoes.get(tarefa, [])]
        if not elegiveis:
            atribuicoes[tarefa] = "⚠️ Sem pessoa elegível"
            continue

        if not repeticao:
            random.shuffle(elegiveis)
            for pessoa in elegiveis:
                if pessoa in pessoas_disponiveis:
                    atribuicoes[tarefa] = pessoa
                    pessoas_disponiveis.remove(pessoa)
                    break
            else:
                atribuicoes[tarefa] = "⚠️ Ninguém disponível"
        else:
            atribuicoes[tarefa] = random.choice(elegiveis)

    st.session_state.atribuicoes = atribuicoes

if st.session_state.atribuicoes:
    st.header("📋 Resultado da Distribuição")
    for tarefa, pessoa in st.session_state.atribuicoes.items():
        st.write(f"- **{tarefa}** → {pessoa}")

if st.button("🔄 Resetar Tudo"):
    st.session_state.tarefas = []
    st.session_state.pessoas = []
    st.session_state.exclusoes = {}
    st.session_state.atribuicoes = {}

# Remover pessoas ou tarefas (apenas disponível para administradores)
if modo_admin:
    st.header("4. Remover Pessoas e Tarefas")
    pessoa_remover = st.selectbox("Escolha uma pessoa para remover", st.session_state.pessoas)
    if st.button(f"Remover {pessoa_remover}"):
        st.session_state.pessoas.remove(pessoa_remover)
        st.write(f"{pessoa_remover} foi removido do grupo.")
        st.rerun()  # Atualiza a interface

    tarefa_remover = st.selectbox("Escolha uma tarefa para remover", st.session_state.tarefas)
    if st.button(f"Remover {tarefa_remover}"):
        st.session_state.tarefas.remove(tarefa_remover)
        st.write(f"Tarefa '{tarefa_remover}' foi removida.")
        st.rerun()  # Atualiza a interface
