from watson_developer_cloud import LanguageTranslatorV2


class TranslationModule:
    def __init__(self, username: str, password: str):
        try:
            self._language_translator = LanguageTranslatorV2(username=str(username),
                                                             password=str(password))

            self._possible_models = set()

            temp = self._language_translator.get_models()['models']
            for ele in temp:
                if ele['target'] == 'en':
                    self._possible_models.add(ele['source'])

        except Exception:
            print("Cannot connect to translation service. Aborting.")
            exit()

    def _get_model(self, message):
        """

        :param message: predicts which language it is in to translate from
        :return: the model predicted
        """
        try:
            return self._language_translator.identify(message)['languages'][0]['language']
        except Exception:
            return None

    def translate_message(self, message):
        """

        :param message: message to be translated;
        :return: the message if no model is available or the translated message
        """
        model = self._get_model(message)
        if model is None or model not in self._possible_models:
            return message
        else:
            try:
                return self._language_translator.translate(message, source=model, target='en')
            except Exception:
                return message
