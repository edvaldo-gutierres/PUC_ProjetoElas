import services.database as db
import streamlit as st
import models.CaptacaoEscola as captacao_escola

def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT `tab_captacao_escola`.`id_captacao_escola`,
                `tab_captacao_escola`.`nome_escola`,
                `tab_captacao_escola`.`nome_contato_escola`,
                `tab_captacao_escola`.`data_contato`,
                `tab_captacao_escola`.`data_proximo_contato`,
                `tab_captacao_escola`.`descricao_etapa`,
                `tab_captacao_escola`.`situacao_etapa`
            FROM `db_projetoelas`.`tab_captacao_escola`;
        """)
        captacao_list = []

        for row in cursor.fetchall():
            captacao_list.append(captacao_escola.CaptacaoEscola(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        return captacao_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar captacao escola: {err}")
        return


def cadastrar(captacao):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO `db_projetoelas`.`tab_captacao_escola`
            (`nome_escola`,
            `nome_contato_escola`,
            `data_contato`,
            `data_proximo_contato`,
            `descricao_etapa`,
            `situacao_etapa`)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (captacao.nome_escola, captacao.nome_contato_escola, captacao.data_contato, captacao.data_proximo_contato, captacao.descricao_etapa, captacao.situacao_etapa))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()


def excluir(id_captacao_escola):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM `db_projetoelas`.`tab_captacao_escola`
            WHERE id_captacao_escola = %s
        """, (id_captacao_escola,))
        db.conn.commit()
        cursor.close()
        st.success("Registro excluído com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()


def ExcluirForm(filtro_exclusao):
    colms = st.columns((2 ,2 ,2 ,2 ,2 ,2 ,2))
    campos = ['ID Captacao', 'Nome Escola', 'Nome Contato', 'Data Contato', 'Data Prox. Contato', 'Desc. Etapa', 'Situação Etapa']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():  # Esta função deve consultar a tabela tab_captacao_escola
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_captacao_escola in filtro_exclusao:
            col1, col2, col3, col4, col5, col6, col7 = st.columns((2, 2, 2, 2, 2, 2, 2))
            col1.write(item.id_captacao_escola)
            col2.write(item.nome_escola)
            col3.write(item.nome_contato_escola)
            col4.write(item.data_contato)
            col5.write(item.data_proximo_contato)
            col6.write(item.descricao_etapa)
            col7.write(item.situacao_etapa)

            button_space_excluir = col7.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_captacao_escola}_btnExcluir",
                                                           type="primary")

            if on_click_excluir:
                try:
                    excluir(item.id_captacao_escola)
                    button_space_excluir.button("Excluído", key=f"{item.id_captacao_escola}_btnExcluido")
                    # st.write(':red[_Cadastro excluído com sucesso!!!_]')
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o cadastro: {str(err)}")

            # Implemente botões de ação e lógica adicional conforme necessário

            # Adicione uma linha separadora com espaçamento ajustado
            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)
