import services.database as db
import streamlit as st
import models.Oficina as oficina

def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT id_tab_oficina, data_realizacao_oficina, local_realizacao_oficina, tema_oficina
            FROM tab_oficina;
        """)
        oficina_list = []

        for row in cursor.fetchall():
            oficina_list.append(oficina.Oficina(row[0], row[1], row[2], row[3]))

        return oficina_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar oficina: {err}")
        return None

def cadastrar(oficina):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO tab_oficina (data_realizacao_oficina, local_realizacao_oficina, tema_oficina)
            VALUES (%s, %s, %s)
        """, (oficina.data_realizacao_oficina, oficina.local_realizacao_oficina, oficina.tema_oficina))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()

def excluir(id_oficina):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM tab_oficina WHERE id_tab_oficina = %s
        """, (id_oficina,))
        db.conn.commit()
        cursor.close()
        st.success("Registro excluído com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()

def ExcluirForm(filtro_exclusao):
    colms = st.columns((1, 3, 3, 3, 3))
    campos = ['ID', 'Data de Realização', 'Local de Realização', 'Tema da Oficina']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_tab_oficina in filtro_exclusao:
            col1, col2, col3, col4, col5 = st.columns((1, 3, 3, 3, 3))
            col1.write(item.id_tab_oficina)
            col2.write(item.data_realizacao_oficina)
            col3.write(item.local_realizacao_oficina)
            col4.write(item.tema_oficina)

            button_space_excluir = col5.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_tab_oficina}_btnExcluir", type="primary")

            if on_click_excluir:
                try:
                    excluir(item.id_tab_oficina)
                    button_space_excluir.button("Excluído", key=f"{item.id_tab_oficina}_btnExcluido")
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o cadastro: {str(err)}")

            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)