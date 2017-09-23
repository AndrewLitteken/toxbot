from watson_developer_cloud import ToneAnalyzerV3


class ToneAnalyzer:
    def __init__(self, username=None, password=None, version=None):
        """

        :param username: Watson BlueMix Api username key
        :param password: Watson BlueMix Api password token
        :param version: version of tone-analyzer used in this instance

        """
        self.tone_analyzer = self.__init_analyzer(username, password, version)
        # Can modify this
        self._thresh_ratio = 0.3
        self._general_ratio = 0.7

    @staticmethod
    def __init_analyzer(username: str, password: str, version: str):
        return ToneAnalyzerV3(
            username=username,
            password=password,
            version=version)

    def get_score(self, message):
        data = self.tone_analyzer.tone(text=message)

        score_dict = {}
        for t in data['document_tone']['tone_categories']:
            for ele in t['tones']:
                score_dict[ele['tone_name']] = ele['score']

        general_sum = 0
        thresh_sum = 0

        for key in score_dict.keys():
            if key == 'Openness' or key == 'Conscientiousness' or key == 'Agreeableness':
                if score_dict[key] < 0.5:
                    general_sum -= 1 - score_dict[key]
                else:
                    general_sum += score_dict[key]
            elif key == 'Anger' or key == 'Disgust' or key == 'Fear':
                if score_dict[key] > 0.5:
                    thresh_sum -= score_dict[key]
                else:
                    thresh_sum += 1 - score_dict[key]
            elif key == 'Joy':
                if score_dict[key] > 0.5:
                    thresh_sum += score_dict[key]
                else:
                    thresh_sum -= 1 - score_dict[key]

        general_sum *= self._general_ratio
        thresh_sum *= self._thresh_ratio

        print(general_sum, thresh_sum)
        return general_sum + thresh_sum


# myT = ToneAnalyzer("a54c1a30-92fe-4c1f-b34a-02936047e396", "8WTlVVDHFHCt", '2016-05-19')
# print(myT.get_score(""))


# Plot data points and hand rate some