import services.database as db
import streamlit as st
import models.Escola as escola

def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT `tab_escola`.`id_escola`,
                `tab_escola`.`nome_escola`,
                `tab_escola`.`endereco_escola`,
                `tab_escola`.`numero_escola`,
                `tab_escola`.`bairro_escola`,
                `tab_escola`.`cidade_escola`
            FROM `db_projetoelas`.`tab_escola`;
        """)
        escola_list = []

        for row in cursor.fetchall():
            escola_list.append(escola.Escola(row[0], row[1], row[2], row[3], row[4], row[5] ))

        return escola_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar escola: {err}")
        return


def cadastrar(escola):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""INSERT INTO `db_projetoelas`.`tab_escola`        
                        (
                        `nome_escola`,
                        `endereco_escola`,
                        `numero_escola`,
                        `bairro_escola`,
                        `cidade_escola`)VALUES ( %s, %s, %s, %s, %s)""",
                       (escola.nome_escola, escola.endereco_escola, escola.numero_escola, escola.bairro_escola,
                        escola.cidade_escola))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()



def excluir(id_escola):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM `db_projetoelas`.`tab_escola`
            WHERE id_escola = %s""", (id_escola,))
        db.conn.commit()
        cursor.close()
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()



def ExcluirForm(filtro_exclusao):
    colms = st.columns((2 ,2 ,2 ,2 ,2 ,2 ,2))
    campos = ['ID Escola', 'Nome Escola', 'Endereço', 'Número', 'Bairro', 'Cidade']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():  # Esta função deve consultar a tabela tab_escola
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_escola in filtro_exclusao:
            col1, col2, col3, col4, col5, col6, col7 = st.columns((2, 2, 2, 2, 2, 2, 2))
            col1.write(item.id_escola)
            col2.write(item.nome_escola)
            col3.write(item.endereco_escola)
            col4.write(item.numero_escola)
            col5.write(item.bairro_escola)
            col6.write(item.cidade_escola)

            button_space_excluir = col7.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_escola}_btnExcluir",
                                                           type="primary")

            if on_click_excluir:
                try:
                    excluir(item.id_escola)
                    button_space_excluir.button("Excluído", key=f"{item.id_escola}_btnExcluido")
                    st.write(':red[_Cadastro excluído com sucesso!!!_]')
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o cadastro: {str(err)}")

            # Adicione uma linha separadora com espaçamento ajustado
            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)

