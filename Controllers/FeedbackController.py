import services.database as db
import streamlit as st
import models.Feedback as feedback

def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT `tab_feedback`.`id_tab_feedback`,
                `tab_feedback`.`nome_aluna`,
                `tab_feedback`.`tema_oficina`,
                `tab_feedback`.`tema_interessante`,
                `tab_feedback`.`nivel_atividade`,
                `tab_feedback`.`mais_gostou`,
                `tab_feedback`.`base_nps`,
                `tab_feedback`.`melhorias`
            FROM `db_projetoelas`.`tab_feedback`;

        """)
        feedback_list = []

        for row in cursor.fetchall():
            feedback_list.append(feedback.Feedback(row[0], row[1], row[2], row[3], row[4], row[5], row[6],row[7]))

        return feedback_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar feedback: {err}")
        return None


def cadastrar(feedback):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO tab_feedback (nome_aluna, tema_oficina, tema_interessante, nivel_atividade, mais_gostou, 
            base_nps, melhorias) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (feedback.nome_aluna, feedback.tema_oficina, feedback.tema_interessante, feedback.nivel_atividade,
              feedback.mais_gostou, feedback.base_nps, feedback.melhorias))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()


def excluir(id_tab_feedback):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM tab_feedback WHERE id_tab_feedback = %s
        """, (id_tab_feedback,))
        db.conn.commit()
        cursor.close()
        st.success("Registro excluído com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()


def ExcluirForm(filtro_exclusao):
    colms = st.columns((1, 3, 3, 3, 3, 3, 3, 3, 3))
    campos = ['ID', 'Nome Aluna', 'Tema Oficina', 'Tema Interessante', 'Nível Atividade', 'Mais Gostou', 'Base NPS', 'Melhorias']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_tab_feedback in filtro_exclusao:
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns((1, 3, 3, 3, 3, 3, 3, 3, 3))
            col1.write(item.id_tab_feedback)
            col2.write(item.nome_aluna)
            col3.write(item.tema_oficina)
            col4.write(item.tema_interessante)
            col5.write(item.nivel_atividade)
            col6.write(item.mais_gostou)
            col7.write(item.base_nps)
            col8.write(item.melhorias)

            button_space_excluir = col9.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_tab_feedback}_btnExcluir",
                                                           type="primary")

            if on_click_excluir:
                try:
                    excluir(item.id_tab_feedback)
                    button_space_excluir.button("Excluído", key=f"{item.id_tab_feedback}_btnExcluido")
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o feedback: {str(err)}")

            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)


