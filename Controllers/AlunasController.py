import services.database as db
import streamlit as st
import models.Alunas as alunas


def consultar():
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT 
                id_tab_alunas, 
                nome_aluna, 
                email_aluna, 
                telefone_aluna, 
                endereco_aluna, 
                numero_aluna, 
                bairro_aluna, 
                cidade_aluna, 
                renda_familiar_aluna, 
                data_nascimento_aluna, 
                ano_escolar_aluna, 
                contato_area_ti, 
                conhecido_trabalha_area_ti, 
                nivel_afinidade_area, 
                faria_curso_ti, 
                curso_interesse_area, 
                nome_escola_aluna_frequenta 
            FROM tab_alunas;
        """)
        alunas_list = []

        for row in cursor.fetchall():
            alunas_list.append(alunas.Aluna(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                            row[7], row[8], row[9], row[10], row[11], row[12], row[13],
                                            row[14], row[15], row[16]))

        return alunas_list

    except db.mysql.connector.Error as err:
        print(f"Erro ao consultar alunas: {err}")
        return None



def cadastrar(alunas):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO tab_alunas (nome_aluna, email_aluna, telefone_aluna, endereco_aluna, numero_aluna, bairro_aluna, cidade_aluna, renda_familiar_aluna, data_nascimento_aluna, ano_escolar_aluna, contato_area_ti, conhecido_trabalha_area_ti, nivel_afinidade_area, faria_curso_ti, curso_interesse_area, nome_escola_aluna_frequenta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (alunas.nome_aluna, alunas.email_aluna, alunas.telefone_aluna, alunas.endereco_aluna,
              alunas.numero_aluna, alunas.bairro_aluna, alunas.cidade_aluna,
              alunas.renda_familiar_aluna, alunas.data_nascimento_aluna, alunas.ano_escolar_aluna,
              alunas.contato_area_ti, alunas.conhecido_trabalha_area_ti, alunas.nivel_afinidade_area,
              alunas.faria_curso_ti, alunas.curso_interesse_area, alunas.nome_escola_aluna_frequenta))
        db.conn.commit()
        cursor.close()
        st.success("Dados inseridos com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados: {err}")
        db.conn.rollback()


def excluir(id_tab_alunas):
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            DELETE FROM tab_alunas WHERE id_tab_alunas = %s
        """, (id_tab_alunas,))
        db.conn.commit()
        cursor.close()
        st.success("Registro excluído com sucesso!")
    except db.mysql.connector.Error as err:
        st.error(f"Não foi possível excluir: {err}")
        db.conn.rollback()


def ExcluirForm(filtro_exclusao):
    colms = st.columns((3, 6, 6, 6, 7, 6, 6, 6, 6, 6, 6, 6, 8, 7, 6, 7, 6, 8))
    campos = ['ID', 'Nome', 'Email', 'Telefone', 'Endereço', 'Número', 'Bairro', 'Cidade', 'Renda Familiar',
              'Data Nasc.', 'Ano Escolar', 'Contato TI', 'Conhecido em TI', 'Afinidade TI', 'Curso TI',
              'Interesse Curso', 'Escola']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)

    for item in consultar():
        if "Exibir todos" in filtro_exclusao or filtro_exclusao is None or item.id_tab_alunas in filtro_exclusao:
            (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13,
             col14, col15, col16, col17, col18) = st.columns((3, 6, 6, 6, 7, 6, 6, 6, 6, 6, 6, 6, 8, 7, 6, 7, 6, 8))
            col1.text(item.id_tab_alunas)
            col2.text(item.nome_aluna)
            col3.text(item.email_aluna)
            col4.text(item.telefone_aluna)
            col5.text(item.endereco_aluna)
            col6.text(item.numero_aluna)
            col7.text(item.bairro_aluna)
            col8.text(item.cidade_aluna)
            col9.text(item.renda_familiar_aluna)
            col10.text(item.data_nascimento_aluna.strftime('%d/%m/%Y'))  # Formatando a data
            col11.text(item.ano_escolar_aluna)
            col12.text(item.contato_area_ti)
            col13.text(item.conhecido_trabalha_area_ti)
            col14.text(item.nivel_afinidade_area)
            col15.text(item.faria_curso_ti)
            col16.text(item.curso_interesse_area)
            col17.text(item.nome_escola_aluna_frequenta)

            button_space_excluir = col18.empty()
            on_click_excluir = button_space_excluir.button("Excluir", key=f"{item.id_tab_alunas}_btnExcluir",
                                                           type="primary")

            if on_click_excluir:
                try:
                    excluir(item.id_tab_alunas)
                    button_space_excluir.button("Excluído", key=f"{item.id_tab_alunas}_btnExcluido")
                except db.mysql.connector.Error as err:
                    st.error(f"Não foi possível excluir o cadastro: {str(err)}")

            st.write('<hr style="height: 1px; margin: 5px 0; background-color: #ccc;">', unsafe_allow_html=True)
