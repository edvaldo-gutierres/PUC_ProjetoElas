import streamlit as st
from PIL import Image
import pandas as pd
import locale

# -------------------------------------------------------------------------------------------------------------------
# Configurações da página
st.set_page_config(
    page_title="Projeto Elas++",
    page_icon="👋",
    layout="wide"
)

# -------------------------------------------------------------------------------------------------------------------
# Autentificação
def creds_entered():
    if st.session_state["user"].strip() == "admin" and st.session_state["passwd"].strip() == "admin":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if st.session_state["passwd"]:
            st.warning("Informe Usuário e Senha")
        elif st.session_state["user"]:
            st.warning("Informe Usuário e Senha")
        else:
            st.error("Usuário/senha inválidos")


def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Usuário :", value="", key="user", on_change=creds_entered)
        st.text_input(label="Senha :", value="", key="passwd", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Usuário :", value="", key="user", on_change=creds_entered)
            st.text_input(label="Senha :", value="", key="passwd", type="password", on_change=creds_entered)
            return False


# -------------------------------------------------------------------------------------------------------------------
# Se autentificado

if authenticate_user():
    # Função para cada página
    # ---------------------------------------------------------------------------------------------------------------

    def page_home():
        image = Image.open('images/logo_puc.png')

        st.write("# Página Inicial - Projeto Elas++ 👋")

        st.image(image, caption='PUC Minas')

        st.markdown("""
                **Bem-vindo ao Projeto Elas++.** 

                _Este projeto foi criado para gerenciar e monitoras a captação de escolas e as oficinas realizadas pelo
                projeto._

                &nbsp;
                &nbsp;

                ---\n
               Prova de conceito desenvolvida pelo Grupo 3 do curso de Tecnologia de Banco de dados - 2º Semestre 2023.
               \n
               Dev. Python: Edvaldo Gutierres Ferreira
            """)

        st.sidebar.markdown("# Sejam bem vindos ao Projeto Elas")

        st.sidebar.success(" Selecione o módulo desejado.")


    def page_escola():
        import Controllers.EscolaController as EscolaController
        import services.database as db
        import models.Escola as escola;

        st.markdown("# Escola ️:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Escola"

        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Escola_List = []
                for item in EscolaController.consultar():
                    Escola_List.append([item.id_escola, item.nome_escola, item.endereco_escola, item.numero_escola,
                                        item.bairro_escola, item.cidade_escola])

                df = pd.DataFrame(Escola_List, columns=['ID Escola', 'Nome Escola', 'Endereço', 'nº', 'Bairro', 'Cidade'])

                df = df.set_index('ID Escola')
                # st.dataframe(df)

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Escola'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione Negócios para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Escola'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione um Negócio ou 'Exibir todos'.")


        if add_selectbox == "Cadastrar":

            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            with st.form(key='include_escola'):
                input_nome = st.text_input(label="Informe o Nome da Escola")
                input_endereco = st.text_input(label="Informe o Endereço")
                input_numero = st.number_input("Informe a número", step=1, key="numero", value=0)
                input_bairro = st.text_input(label="Informe o bairro")
                input_cidade = st.text_input(label="Informe a cidade")

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_nome:
                        st.warning("Por favor, preencha o nome da escola.")
                    if not input_endereco:
                        st.warning("Por favor, preencha o endereço da escola.")
                    if not input_numero:
                        st.warning("Por favor, preencha o número da escola.")
                    if not input_bairro:
                        st.warning("Por favor, preencha o bairro da escola.")
                    if not input_cidade:
                        st.warning("Por favor, preencha a cidade da escola.")
                    else:
                        EscolaController.cadastrar( escola.Escola(id_escola="",
                                                                  nome_escola=input_nome,
                                                                  endereco_escola=input_endereco,
                                                                  numero_escola=input_numero,
                                                                  bairro_escola=input_bairro,
                                                                  cidade_escola=input_cidade))

            with st.expander("Lista de escolas cadastradas"):
                Escola_List = []
                for item in EscolaController.consultar():
                    Escola_List.append([item.id_escola, item.nome_escola, item.endereco_escola, item.numero_escola,
                                        item.bairro_escola, item.cidade_escola])

                df = pd.DataFrame(Escola_List, columns=['ID Escola', 'Nome Escola', 'Endereço', 'nº', 'Bairro', 'Cidade'])

                df = df.set_index('ID Escola')
                # st.dataframe(df)

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Escola'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione Negócios para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Escola'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione um Negócio ou 'Exibir todos'.")


        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.id_escola for item in EscolaController.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            EscolaController.ExcluirForm(filtro_exclusao)



    def page_captacao():
        import Controllers.CaptacaoEscolaController as CaptacaoEscola
        import models.CaptacaoEscola as captacao
        import services.database as db

        st.markdown("# Escola ️:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Captação de Escola"

        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                CaptacaoEscola_List = []
                for item in CaptacaoEscola.consultar():
                    CaptacaoEscola_List.append([
                        item.id_captacao_escola, item.nome_escola, item.nome_contato_escola,
                        item.data_contato, item.data_proximo_contato, item.descricao_etapa,
                        item.situacao_etapa
                    ])

                df = pd.DataFrame(CaptacaoEscola_List, columns=[
                    'ID Captacao', 'Nome Escola', 'Nome Contato', 'Data Contato',
                    'Data Prox. Contato', 'Desc. Etapa', 'Situação Etapa'
                ])

                df = df.set_index('ID Captacao')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Escola'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione Escolas para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Escola'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Cadastrar":

            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            # Criar opções
            con_escola = db.conn.cursor()
            con_escola.execute("""
                                SELECT 
                                    `tab_escola`.`nome_escola`
                                FROM `db_projetoelas`.`tab_escola`;""")
            opcao_escola = [row[0] for row in con_escola.fetchall()]
            opcao_escola_branco = [''] + opcao_escola

            with (st.form(key='include_captacao_escola')):
                input_nome_escola = st.selectbox("Selecione a Escola", opcao_escola_branco)
                input_nome_contato_escola = st.text_input(label="Informe o Nome do Contato da Escola")
                input_data_contato = st.date_input("Data do Contato",format="DD/MM/YYYY")
                input_data_proximo_contato = st.date_input("Data do Próximo Contato",format="DD/MM/YYYY")
                input_descricao_etapa = st.text_area("Descrição da Etapa")
                input_situacao_etapa = st.selectbox("Situação da Etapa", ["Aprovado", "Em negociação", "Reprovado"])

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_nome_escola:
                        st.warning("Por favor, preencha o nome da escola.")
                    if not input_nome_contato_escola:
                        st.warning("Por favor, preencha o nome do contato da escola.")
                    if not input_data_contato:
                        st.warning("Por favor, preencha a data de contato.")
                    if not input_data_proximo_contato:
                        st.warning("Por favor, preencha a data do próximo contato.")
                    if not input_descricao_etapa:
                        st.warning("Por favor, preencha a descrição da etapa.")
                    if not input_situacao_etapa:
                        st.warning("Por favor, preencha a situacao da etapa.")
                    else:
                        CaptacaoEscola.cadastrar(captacao.CaptacaoEscola(id_captacao_escola="",
                                                                nome_escola=input_nome_escola,
                                                                nome_contato_escola=input_nome_contato_escola,
                                                                data_contato=input_data_contato,
                                                                data_proximo_contato=input_data_proximo_contato,
                                                                descricao_etapa=input_descricao_etapa,
                                                                situacao_etapa=input_situacao_etapa
                        ))


            with st.expander(f"Lista de {nome_modulo}"):
                Escola_List = []
                for item in CaptacaoEscola.consultar():
                    Escola_List.append([item.id_captacao_escola, item.nome_escola, item.nome_contato_escola,
                                        item.data_contato, item.data_proximo_contato, item.descricao_etapa,
                                        item.situacao_etapa])

                df = pd.DataFrame(Escola_List, columns=[
                    'ID Captacao', 'Nome Escola', 'Nome Contato', 'Data Contato',
                    'Data Prox. Contato', 'Descrição da Etapa', 'Situação Etapa'
                ])

                df = df.set_index('ID Captacao')
                # st.dataframe(df)

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Escola'].unique().tolist()
                filtro_selecionado = st.multiselect(f"Selecione {nome_modulo} para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Escola'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning(f"Nenhuma opção selecionada. Por favor, selecione um {nome_modulo} ou 'Exibir todos'.")


        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.id_captacao_escola for item in CaptacaoEscola.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            CaptacaoEscola.ExcluirForm(filtro_exclusao)



    def page_participante():
        import Controllers.ParticipantesProjetoController as ParticipantesProjeto
        import models.ParticipanteProjeto as participante
        import services.database as db

        st.markdown("# Participante ️:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Participante do Projeto"


        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Participante_List = []
                for item in ParticipantesProjeto.consultar():
                    Participante_List.append([
                        item.id_participante_projeto, item.nome_participante_projeto, item.telefone_participante,
                        item.email_participante, item.endereco_participante, item.numero_participante,
                        item.bairro_participante, item.cidade_participante, item.atuacao_participante,
                        item.curso_participante, item.nome_escola_participante
                    ])

                df = pd.DataFrame(Participante_List, columns=[
                    'ID Participante', 'Nome Participante', 'Telefone', 'E-mail',
                    'Endereço', 'nº', 'Bairro', 'Cidade', 'Atuação Participante',
                    'Curso', 'Escola Participante'
                ])

                df = df.set_index('ID Participante')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Participante'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione Escolas para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Participante'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Cadastrar":

            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            # Criar opções
            con_escola = db.conn.cursor()
            con_escola.execute("""
                                SELECT 
                                    `tab_escola`.`nome_escola`
                                FROM `db_projetoelas`.`tab_escola`;""")
            opcao_escola = [row[0] for row in con_escola.fetchall()]
            opcao_escola_branco = [''] + opcao_escola

            with (st.form(key='include_participante')):

                col1, col2 = st.columns(2)

                with col1:
                    input_nome_participante = st.text_input(label="Informe o Nome do participante")
                    input_email_participante = st.text_input(label="Informe o e-mail do participante")
                    input_numero_participante = st.number_input("Informe o número", step=1, key="numero", value=0)
                    input_cidade_participante = st.text_input(label="Informe a cidade do participante")
                    input_curso_participante = st.text_input(label="Informe o curso do participante")

                with col2:
                    input_telefone_participante = st.text_input(label="Informe o telefone do participante")
                    input_endereco_participante = st.text_input(label="Informe o endereço do participante")
                    input_bairro_participante = st.text_input(label="Informe o bairro do participante")
                    input_atuacao_participante = st.text_input(label="Informe a atuação do participante")
                    input_nome_escola = st.selectbox("Selecione a Escola", opcao_escola_branco)

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_nome_participante:
                        st.warning("Por favor, preencha o Nome do participante.")
                    if not input_telefone_participante:
                        st.warning("Por favor, preencha o telefone do participante.")
                    if not input_email_participante:
                        st.warning("Por favor, preencha o e-mail do participante.")
                    if not input_endereco_participante:
                        st.warning("Por favor, preencha o endereço do participante.")
                    if not input_numero_participante:
                        st.warning("Por favor, preencha o número.")
                    if not input_bairro_participante:
                        st.warning("Por favor, preencha o bairro do participante.")
                    if not input_cidade_participante:
                        st.warning("Por favor, preencha a cidade do participante")
                    if not input_atuacao_participante:
                        st.warning("Por favor, preencha a atuação do participante")
                    if not input_curso_participante:
                        st.warning("Por favor, preencha o curso do participante")
                    if not input_nome_escola:
                        st.warning("Por favor, escolha a escola")
                    else:
                        ParticipantesProjeto.cadastrar(participante.ParticipanteProjeto(
                            id_participante_projeto="",
                            nome_participante_projeto=input_nome_participante,
                            telefone_participante=input_telefone_participante,
                            email_participante=input_email_participante,
                            endereco_participante=input_endereco_participante,
                            numero_participante=input_numero_participante,
                            bairro_participante=input_bairro_participante,
                            cidade_participante=input_cidade_participante,
                            atuacao_participante=input_atuacao_participante,
                            curso_participante=input_curso_participante,
                            nome_escola_participante=input_nome_escola
                        ))


            with st.expander(f"Lista de {nome_modulo}"):
                Participante_List = []
                for item in ParticipantesProjeto.consultar():
                    Participante_List.append([item.id_participante_projeto, item.nome_participante_projeto,
                                              item.telefone_participante, item.email_participante,
                                              item.endereco_participante, item.numero_participante,
                                              item.bairro_participante, item.cidade_participante,
                                              item.atuacao_participante, item.curso_participante,
                                              item.nome_escola_participante])

                df = pd.DataFrame(Participante_List, columns=[
                    'ID Participante', 'Nome Participante', 'Telefone', 'E-mail',
                    'Endereço', 'nº', 'Bairro', 'Cidade', 'Atuação Participante',
                    'Curso', 'Escola Participante'
                ])

                df = df.set_index('ID Participante')
                # st.dataframe(df)

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Participante'].unique().tolist()
                filtro_selecionado = st.multiselect(f"Selecione {nome_modulo} para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Participante'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning(f"Nenhuma opção selecionada. Por favor, selecione um {nome_modulo} ou 'Exibir todos'.")


        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.nome_participante_projeto for item in ParticipantesProjeto.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            ParticipantesProjeto.ExcluirForm(filtro_exclusao)



    def page_oficina():
        import Controllers.OficinaController as OficinaController
        import models.Oficina as oficina
        import services.database as db

        st.markdown("# Oficina ️:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Oficina"

        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Oficina_List = []
                for item in OficinaController.consultar():
                    Oficina_List.append([item.id_tab_oficina, item.data_realizacao_oficina,
                                         item.local_realizacao_oficina, item.tema_oficina])

                df = pd.DataFrame(Oficina_List, columns=[
                    'ID Oficina', 'Data Realização', 'Local', 'Tema'
                ])

                df = df.set_index('ID Oficina')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Data Realização'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Data Realização'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Cadastrar":

            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            with (st.form(key='include_participante')):
                input_data = st.date_input(label="Informe a data da realização", format="DD/MM/YYYY")
                input_local = st.text_input(label="Informe o local da realização")
                input_tema = st.text_input(label="Informe o tema da oficina")

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_data:
                        st.warning("Por favor, preencha a data da realização.")
                    if not input_local:
                        st.warning("Por favor, preencha o local da realização.")
                    if not input_tema:
                        st.warning("Por favor, o tema da oficina.")
                    else:
                        OficinaController.cadastrar(oficina.Oficina(
                            id_tab_oficina="",
                            data_realizacao_oficina=input_data,
                            local_realizacao_oficina=input_local,
                            tema_oficina=input_tema)
                        )

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Oficina_List = []
                for item in OficinaController.consultar():
                    Oficina_List.append([item.id_tab_oficina, item.data_realizacao_oficina,
                                         item.local_realizacao_oficina, item.tema_oficina])

                df = pd.DataFrame(Oficina_List, columns=[
                    'ID Oficina', 'Data Realização', 'Local', 'Tema'
                ])

                df = df.set_index('ID Oficina')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Data Realização'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Data Realização'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.id_tab_oficina for item in OficinaController.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            OficinaController.ExcluirForm(filtro_exclusao)


    def page_alunas():
        import Controllers.AlunasController as AlunasController
        import models.Alunas as alunas
        import services.database as db

        st.markdown("# Alunas️:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Alunas"

        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Alunas_List = []
                for item in AlunasController.consultar():
                    Alunas_List.append([item.id_tab_alunas,
                                        item.nome_aluna,
                                        item.email_aluna,
                                        item.telefone_aluna,
                                        item.endereco_aluna,
                                        item.numero_aluna,
                                        item.bairro_aluna,
                                        item.cidade_aluna,
                                        item.renda_familiar_aluna,
                                        item.data_nascimento_aluna,
                                        item.ano_escolar_aluna,
                                        item.contato_area_ti,
                                        item.conhecido_trabalha_area_ti,
                                        item.nivel_afinidade_area,
                                        item.faria_curso_ti,
                                        item.curso_interesse_area,
                                        item.nome_escola_aluna_frequenta])

                df = pd.DataFrame(Alunas_List, columns=[
                    'ID Alunas', 'Nome', 'e-mail', 'Telefone', 'Endereço', 'nº', 'Bairro', 'Cidade', 'Renda Familiar',
                    'Data Nascimento', 'Ano Escolar', 'Contato Área T.I.', 'Conhecido Trabalha em T.I.',
                    'Nível afinidade T.I.', 'Faria Curso de TI?', 'Curso Interesse', 'Escola que Frequenta']
                                  )

                df = df.set_index('ID Alunas')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Cadastrar":

            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            # Criar opções
            con_escola = db.conn.cursor()
            con_escola.execute("""
                                SELECT 
                                    `tab_escola`.`nome_escola`
                                FROM `db_projetoelas`.`tab_escola`;""")
            opcao_escola = [row[0] for row in con_escola.fetchall()]
            opcao_escola_branco = [''] + opcao_escola

            con_renda = db.conn.cursor()
            con_renda.execute("""
                                SELECT `tab_renda_familiar`.`descricao_renda_familiar`
                                FROM `db_projetoelas`.`tab_renda_familiar`
                                ORDER BY `tab_renda_familiar`.`id_renda_familiar`;""")
            opcao_renda = [row[0] for row in con_renda.fetchall()]
            opcao_renda_branco = [''] + opcao_renda


            with (st.form(key='include_aluna')):

                col1, col2 = st.columns(2)

                with col1:
                    input_nome = st.text_input('Nome da Aluna')
                    input_telefone = st.text_input('Telefone da Aluna')
                    input_numero = st.number_input("Informe a número", step=1, key="numero", value=0)
                    input_cidade = st.text_input('Cidade da Aluna')
                    input_data_nascimento = st.date_input('Data de Nascimento da Aluna', format="DD/MM/YYYY")
                    input_contato_area_ti = st.radio('Contato com Área de TI?', ['Sim', 'Não'])
                    input_nivel_afinidade = st.text_input('Nível de Afinidade com a Área')
                    input_curso_interesse = st.text_input('Curso de Interesse na Área de TI')


                with col2:
                    input_email = st.text_input('Email da Aluna')
                    input_endereco = st.text_input('Endereço da Aluna')
                    input_bairro = st.text_input('Bairro da Aluna')
                    input_renda_familiar = st.selectbox("Selecione a Renda Familiar", opcao_renda_branco)
                    input_ano_escolar = st.selectbox('Ano Escolar da Aluna',
                                                     ['1º Ano - Ensino Médio', '2º Ano - Ensino Médio',
                                                      '3º Ano - Ensino Médio'])
                    input_conhecido_trabalha_area_ti = st.radio('Conhecido Trabalha na Área de TI?', ['Sim', 'Não'])
                    input_faria_curso_ti = st.text_input('Curso de interesse na Área de TI')
                    input_nome_escola = st.selectbox("Selecione a Escola", opcao_escola_branco)

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_nome:
                        st.warning("Por favor, preencha o Nome da Aluna.")
                    if not input_email:
                        st.warning("Por favor, preencha o Email da Aluna.")
                    if not input_telefone:
                        st.warning("Por favor, preencha o Telefone da Aluna.")
                    if not input_endereco:
                        st.warning("Por favor, preencha o Endereço da Aluna.")
                    if not input_numero:
                        st.warning("Por favor, preencha o número.")
                    if not input_bairro:
                        st.warning("Por favor, preencha o Bairro da Aluna.")
                    if not input_cidade:
                        st.warning("Por favor, preencha a Cidade da Aluna.")
                    if not input_renda_familiar:
                        st.warning("Por favor, preencha a Renda Familiar.")
                    if not input_data_nascimento:
                        st.warning("Por favor, preencha a Data de Nascimento.")
                    if not input_ano_escolar:
                        st.warning("Por favor, preencha o Ano Escolar.")
                    if not input_contato_area_ti:
                        st.warning("Por favor, preencha o Contato na area de TI.")
                    if not input_conhecido_trabalha_area_ti:
                        st.warning("Por favor, preencha o Conhecido trabalha na area de TI.")
                    if not input_nivel_afinidade:
                        st.warning("Por favor, preencha o nível de afinidade.")
                    if not input_faria_curso_ti:
                        st.warning("Por favor, preencha o faria curso de TI.")
                    if not input_curso_interesse:
                        st.warning("Por favor, preencha o curso de interesse em TI.")
                    if not input_nome_escola:
                        st.warning("Por favor, escolha a escola que frequenta.")

                    else:
                        AlunasController.cadastrar(alunas.Aluna(
                            id_tab_alunas="",
                            nome_aluna=input_nome,
                            email_aluna=input_email,
                            telefone_aluna=input_telefone,
                            endereco_aluna=input_endereco,
                            numero_aluna=input_numero,
                            bairro_aluna=input_bairro,
                            cidade_aluna=input_cidade,
                            renda_familiar_aluna=input_renda_familiar,
                            data_nascimento_aluna=input_data_nascimento,
                            ano_escolar_aluna=input_ano_escolar,
                            contato_area_ti=input_contato_area_ti,
                            conhecido_trabalha_area_ti=input_conhecido_trabalha_area_ti,
                            nivel_afinidade_area=input_nivel_afinidade,
                            faria_curso_ti=input_faria_curso_ti,
                            curso_interesse_area=input_curso_interesse,
                            nome_escola_aluna_frequenta=input_nome_escola
                        ))

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Alunas_List = []
                for item in AlunasController.consultar():
                    Alunas_List.append([item.id_tab_alunas,
                                        item.nome_aluna,
                                        item.email_aluna,
                                        item.telefone_aluna,
                                        item.endereco_aluna,
                                        item.numero_aluna,
                                        item.bairro_aluna,
                                        item.cidade_aluna,
                                        item.renda_familiar_aluna,
                                        item.data_nascimento_aluna,
                                        item.ano_escolar_aluna,
                                        item.contato_area_ti,
                                        item.conhecido_trabalha_area_ti,
                                        item.nivel_afinidade_area,
                                        item.faria_curso_ti,
                                        item.curso_interesse_area,
                                        item.nome_escola_aluna_frequenta])

                df = pd.DataFrame(Alunas_List, columns=[
                    'ID Alunas', 'Nome', 'e-mail', 'Telefone', 'Endereço', 'nº', 'Bairro', 'Cidade', 'Renda Familiar',
                    'Data Nascimento', 'Ano Escolar', 'Contato Área T.I.', 'Conhecido Trabalha em T.I.',
                    'Nível afinidade T.I.', 'Faria Curso de TI?', 'Curso Interesse', 'Escola que Frequenta']
                                  )

                df = df.set_index('ID Alunas')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")


        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.nome_aluna for item in AlunasController.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            AlunasController.ExcluirForm(filtro_exclusao)



    def page_feedback():
        import Controllers.FeedbackController as FeedbackController
        import models.Feedback as feedback
        import services.database as db

        st.markdown("# Feedback:pencil:")
        st.sidebar.markdown("### Escolha uma opção! ")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "### Qual operação você deseja realizar?",
            # ("Consultar", "Cadastrar", "Alterar", "Excluir")
            ("Consultar", "Cadastrar", "Excluir")
        )

        nome_modulo = "Feedback"

        if add_selectbox == "Consultar":

            st.subheader(f":blue[_Consultar {nome_modulo}_]")

            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Feedback_List = []
                for item in FeedbackController.consultar():
                    Feedback_List.append([item.id_tab_feedback, item.nome_aluna,
                                          item.tema_oficina, item.tema_interessante,
                                          item.nivel_atividade, item.mais_gostou,
                                          item.base_nps, item.melhorias])

                df = pd.DataFrame(Feedback_List, columns=[
                    'ID Feedback', 'Nome Aluna', 'Tema Oficina', 'Tema Interessante', 'Nível Atividade',
                    'mais gostou', 'Base NPS', 'Melhorias']
                                  )

                df = df.set_index('ID Feedback')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Aluna'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Aluna'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")



        if add_selectbox == "Cadastrar":
            st.subheader(f":blue[_Cadastrar {nome_modulo}_]")

            # Criar opções
            con_aluna = db.conn.cursor()
            con_aluna.execute("""
                                SELECT 
                                    `tab_alunas`.`nome_aluna`
                                FROM `db_projetoelas`.`tab_alunas`;
                            """)
            opcao_aluna = [row[0] for row in con_aluna.fetchall()]
            opcao_aluna_branco = [''] + opcao_aluna

            con_tema = db.conn.cursor()
            con_tema.execute("""
                                SELECT 
                                    `tab_oficina`.`tema_oficina`
                                FROM `db_projetoelas`.`tab_oficina`;
                            """)
            opcao_tema = [row[0] for row in con_tema.fetchall()]
            opcao_tema_branco = [''] + opcao_tema

            with (st.form(key='include_feedback')):
                input_nome_aluna = st.selectbox('Informe o Nome da Aluna',opcao_aluna_branco)
                input_tema = st.selectbox("Informe o Tema da Oficina", opcao_tema_branco)
                input_tema_interessante = st.text_input(label="Informe o Tema Interessante")
                input_nivel = st.selectbox("Nível da Atividade", ['','Ruim', 'Médio', 'Bom'])
                input_mais_gostou = st.text_input(label="O que mais gostou?")
                input_nps = st.number_input(label="Dê uma nota", step=1, min_value=0, max_value=10)
                input_melhorias = st.text_input(label="Sugestão de Melhoria")

                input_button_submit = st.form_submit_button("Cadastrar")

                if input_button_submit:
                    if not input_nome_aluna:
                        st.warning("Por favor, preencha o Nome da Aluna.")
                    if not input_tema:
                        st.warning("Por favor, preencha o Tema da Oficina.")
                    if not input_tema_interessante:
                        st.warning("Por favor, preencha o Tema Interessante.")
                    if not input_nivel:
                        st.warning("Por favor, preencha o Nível da Atividade.")
                    if not input_mais_gostou:
                        st.warning("Por favor, preencha o que mais gostou.")
                    if not input_nps:
                        st.warning("Por favor, dê uma nota.")
                    if not input_melhorias:
                        st.warning("Por favor, preencha a sugestão de melhoria.")
                    else:
                        FeedbackController.cadastrar(feedback.Feedback(
                            id_tab_feedback="",
                            nome_aluna=input_nome_aluna,
                            tema_oficina=input_tema,
                            tema_interessante=input_tema_interessante,
                            nivel_atividade=input_nivel,
                            mais_gostou=input_mais_gostou,
                            base_nps=input_nps,
                            melhorias=input_melhorias
                        ))


            with st.expander(f"Lista de {nome_modulo} cadastrados"):
                Feedback_List = []
                for item in FeedbackController.consultar():
                    Feedback_List.append([item.id_tab_feedback, item.nome_aluna,
                                          item.tema_oficina, item.tema_interessante,
                                          item.nivel_atividade, item.mais_gostou,
                                          item.base_nps, item.melhorias])

                df = pd.DataFrame(Feedback_List, columns=[
                    'ID Feedback', 'Nome Aluna', 'Tema Oficina', 'Tema Interessante', 'Nível Atividade',
                    'mais gostou', 'Base NPS', 'Melhorias']
                                  )

                df = df.set_index('ID Feedback')

                # Adicionar um seletor (selectbox) para filtrar
                opcoes_filtro = ['Exibir todos'] + df['Nome Aluna'].unique().tolist()
                filtro_selecionado = st.multiselect("Selecione para Filtrar:", opcoes_filtro,
                                                    default=['Exibir todos'])

                # Adicione um espaço em branco extra
                st.write("")
                st.write("")

                if 'Exibir todos' in filtro_selecionado:
                    st.dataframe(df)  # Mostrar o DataFrame completo
                elif filtro_selecionado:
                    df_filtrado = df[df['Nome Aluna'].isin(filtro_selecionado)]
                    st.dataframe(df_filtrado)  # Mostrar o DataFrame filtrado
                else:
                    st.warning("Nenhuma opção selecionada. Por favor, selecione uma Escola ou 'Exibir todos'.")



        if add_selectbox == "Excluir":
            st.subheader(f":blue[_Lista de {nome_modulo} cadastradas_]")

            # Recupere os valores únicos
            valores_de_opcoes = [item.nome_aluna for item in FeedbackController.consultar()]

            # Adicione "Exibir todos" às opções do multiselect e defina-o como padrão
            valores_de_opcoes = ["Exibir todos"] + valores_de_opcoes

            filtro_exclusao = st.multiselect("Selecione os itens para excluir:", valores_de_opcoes,
                                             default=["Exibir todos"])

            # Chame a função ExcluirForm com o filtro de exclusão selecionado
            FeedbackController.ExcluirForm(filtro_exclusao)








    # -----------------------------------------------------------------------------------------------------------------
    # Adicione uma descrição ou instruções para a tela inicial
    add_selectbox = st.sidebar.selectbox(
        "Selecione o módulo desejado.",
        # ("Consultar", "Cadastrar", "Alterar", "Excluir")
        ("Home", "Escola", "Captação de Escola", "Extensionista", "Oficina", "Alunas", "Feedback")
    )

    if add_selectbox == "Home":
        # Redireciona para a página de negócio
        page_home()

    #-------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Escola":
        nome = "Escola"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_escola()

    # -------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Captação de Escola":
        nome = "Captação de Escola"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_captacao()

    # -------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Extensionista":
        nome = "Extensionista"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_participante()

    # -------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Oficina":
        nome = "Oficina"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_oficina()

    # -------------------------------------------------------------------------------------------------------------------

    # if add_selectbox == "Renda Familiar":
    #     nome = "Renda Familiar"
    #     # Redireciona para a página
    #     st.write(f"Você selecionou a página de {nome}.")
    #     st.write(f"Aqui você pode gerenciar informações de {nome}.")
    #     # page_linha_produto()

    # -------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Alunas":
        nome = "Alunas"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_alunas()

    # -------------------------------------------------------------------------------------------------------------------

    if add_selectbox == "Feedback":
        nome = "Feedback"
        # Redireciona para a página
        st.write(f"Você selecionou a página de {nome}.")
        st.write(f"Aqui você pode gerenciar informações de {nome}.")
        page_feedback()

    # -------------------------------------------------------------------------------------------------------------------