from __future__ import annotations

import os
import streamlit as st
from dotenv import load_dotenv
from orchestrator import MultiAgentAssessment, to_markdown

load_dotenv()
st.set_page_config(page_title="Multi-Agent Assessment", page_icon="🧑‍🏫", layout="wide")
st.title("🧑‍🏫 Multi-Agent Assessment")
st.caption("Pipeline sequencial de três agentes: professor → estudante → revisor.")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("OpenAI API key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    model = st.text_input("Modelo", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    st.divider()
    st.markdown("**Fluxo de agentes**\n\n1. Professor cria questões e gabarito.\n2. Aluno recebe somente a prova e responde.\n3. Revisor compara respostas e gabarito, atribuindo nota e feedback.")

with st.form("assessment_form"):
    col1, col2 = st.columns(2)
    with col1:
        discipline = st.text_input("Disciplina", "Ciência da Computação")
        topic = st.text_input("Tópico", "Estruturas de Dados: árvores e grafos")
    with col2:
        difficulty = st.selectbox("Dificuldade", ["Básica", "Intermediária", "Avançada"], index=1)
        count = st.slider("Quantidade de questões", min_value=3, max_value=8, value=5)
    submitted = st.form_submit_button("Executar os três agentes", type="primary", use_container_width=True)

if submitted:
    if not api_key.strip():
        st.error("Informe uma chave própria da OpenAI na barra lateral ou configure OPENAI_API_KEY no .env.")
    else:
        try:
            pipeline = MultiAgentAssessment(api_key=api_key.strip(), model=model.strip())
            with st.status("Executando pipeline multiagente...", expanded=True) as status:
                def report_step(message: str) -> None:
                    status.update(label=message, state="running", expanded=True)
                result = pipeline.run(discipline, topic, difficulty, count, on_step=report_step)
                status.update(label="Pipeline concluído", state="complete", expanded=False)
            st.session_state.assessment_result = result
            st.success("Os três agentes concluíram suas etapas.")
        except Exception as exc:
            st.error(f"Falha na execução: {exc}")

result = st.session_state.get("assessment_result")
if result:
    review = result["review"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Nota atribuída", f"{review['score']:.1f} / {review['max_score']:.1f}")
    c2.metric("Questões", len(result["exam"]["questions"]))
    c3.metric("Agentes", 3)
    tab1, tab2, tab3, tab4 = st.tabs(["Prova", "Respostas", "Revisão", "Relatório"])
    with tab1:
        for question in result["exam"]["questions"]:
            st.markdown(f"**Questão {question['id']} — {question['type']}**")
            st.write(question["question"])
            for key, value in question.get("options", {}).items():
                st.write(f"{key}) {value}")
            with st.expander("Ver gabarito e explicação"):
                st.write(f"Resposta esperada: {question['correct_answer']}")
                st.write(question.get("explanation", ""))
    with tab2:
        st.json(result["student"])
    with tab3:
        st.markdown(f"### Feedback geral\n{review.get('overall_feedback', '')}")
        st.json(review.get("corrections", []))
    with tab4:
        report = to_markdown(result)
        st.markdown(report)
        st.download_button("Baixar relatório Markdown", report, file_name="relatorio-avaliacao.md", mime="text/markdown")
else:
    st.info("Preencha disciplina e tópico e execute o pipeline. A aplicação faz três chamadas sequenciais ao modelo configurado.")
