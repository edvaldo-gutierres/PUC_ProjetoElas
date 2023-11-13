import services.database as db
import streamlit as st
import models.ParticipanteProjeto as participante_projeto

def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT `tab_participante_projeto`.`id_participante_projeto`,
                `tab_participante_projeto`.`nome_participante_projeto`,
                `tab_participante_projeto`.`telefone_participante`,
                `tab_participante_projeto`.`email_participante`,
                `tab_participante_projeto`.`endereco_participante`,
                `tab_participante_projeto`.`numero_participante`,
                `tab_participante_projeto`.`bairro_participante`,
                `tab_participante_projeto`.`cidade_participante`,
                `tab_participante_projeto`.`atuacao_participante`,
                `tab_participante_projeto`.`curso_participante`,
                `tab_participante_projeto`.`nome_escola_participante`
            FROM `db_projetoelas`.`tab_participante_projeto`;
        """)
        participante_projeto_list = []

        for row in cursor.fetchall():
            participante_projeto_list.append(participante_projeto.ParticipanteProjeto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

        return participante_projeto_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar participante do projeto: {err}")
        return None


def cadastrar(participante_projeto):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO `db_projetoelas`.`tab_participante_projeto`
            (`nome_participante_projeto`,
            `telefone_participante`,
            `email_participante`,
            `endereco_participante`,
            `numero_participante`,
            `bairro_participante`,
            `cidade_participante`,
            `atuacao_participante`,
            `curso_participante`,
            `nome_escola_participante`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (participante_projeto.nome_participante_projeto, participante_projeto.telefone_participante,
              participante_projeto.email_participante, participante_projeto.endereco_participante,
              participante_projeto.numero_participante, participante_projeto.bairro_participante,
              participante_projeto.cidade_participante, participante_projeto.atuacao_participante,
              participante_projeto.curso_participante, participante_projeto.nome_escola_participante))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()


def excluir_participante(id_participante_projeto):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM `db_projetoelas`.`tab_participante_projeto`
            WHERE id_participante_projeto = %s
        """, (id_participante_projeto,))
        db.conn.commit()
        cursor.close()
        st.success("Registro excluído com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()



def ExcluirForm(filtro_exclusao):
    colms = st.columns((1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3))
    campos = ['ID', 'Nome', 'Telefone', 'Email', 'Endereço', 'Número', 'Bairro', 'Cidade', 'Atuação', 'Curso', 'Nome Escola']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():  # Adaptado para a tabela tab_participante_projeto
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_participante_projeto in filtro_exclusao:
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns((1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3))
            col1.write(item.id_participante_projeto)
            col2.write(item.nome_participante_projeto)
            col3.write(item.telefone_participante)
            col4.write(item.email_participante)
            col5.write(item.endereco_participante)
            col6.write(item.numero_participante)
            col7.write(item.bairro_participante)
            col8.write(item.cidade_participante)
            col9.write(item.atuacao_participante)
            col10.write(item.curso_participante)
            col11.write(item.nome_escola_participante)

            button_space_excluir = col11.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_participante_projeto}_btnExcluir", type="primary")

            if on_click_excluir:
                try:
                    excluir_participante(item.id_participante_projeto)
                    button_space_excluir.button("Excluído", key=f"{item.id_participante_projeto}_btnExcluido")
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o cadastro: {str(err)}")

            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)
