import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionObterTokenAcesso(Action):

    def name(self) -> str:
        return "action_obter_token_acesso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        numero_conta = tracker.get_slot('numero_conta')
        senha = tracker.get_slot('senha')

        if not numero_conta or not senha:
            dispatcher.utter_message(response="utter_solicitar_informacoes_bancarias")
            return []

        # Exemplo de requisição para gerar token de acesso
        response = requests.post('https://api.banco.com/token', data={
            'numero_conta': numero_conta,
            'senha': senha
        })

        if response.status_code == 200:
            token = response.json().get('access_token')
            return [SlotSet("token_acesso", token)]
        else:
            dispatcher.utter_message(response="utter_informacoes_invalidas")
            return []


class ActionConsultarSaldo(Action):

    def name(self) -> str:
        return "action_consultar_saldo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        token_acesso = tracker.get_slot('token_acesso')
        if not token_acesso:
            dispatcher.utter_message(response="utter_solicitar_informacoes_bancarias")
            return []

        headers = {
            'Authorization': f'Bearer {token_acesso}',
            'Content-Type': 'application/json',
        }
        response = requests.get('https://api.banco.com/saldo', headers=headers)

        if response.status_code == 200:
            saldo = response.json().get('saldo')
            dispatcher.utter_message(response="utter_saldo", saldo=saldo)
        else:
            dispatcher.utter_message(text="Não foi possível obter o saldo.")

        return []


class ActionConsultarTransacoes(Action):

    def name(self) -> str:
        return "action_consultar_transacoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        token_acesso = tracker.get_slot('token_acesso')
        if not token_acesso:
            dispatcher.utter_message(response="utter_solicitar_informacoes_bancarias")
            return []

        headers = {
            'Authorization': f'Bearer {token_acesso}',
            'Content-Type': 'application/json',
        }
        response = requests.get('https://api.banco.com/transacoes', headers=headers)

        if response.status_code == 200:
            transacoes = response.json().get('transacoes')
            dispatcher.utter_message(response="utter_transacoes", transacoes=transacoes)
        else:
            dispatcher.utter_message(text="Não foi possível obter as transações.")

        return []
