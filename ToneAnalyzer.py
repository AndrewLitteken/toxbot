from watson_developer_cloud import ToneAnalyzerV3
from sklearn.neural_network import MLPClassifier


class ToneAnalyzer:
    def __init__(self, username=None, password=None, version=None, text=None, score=None, first_init=False):
        """

        :param username: Watson BlueMix Api username key
        :param password: Watson BlueMix Api password token
        :param version: version of tone-analyzer used in this instance

        """
        self.tone_analyzer = self.__init_analyzer(username, password, version)
        self._training_files = (text, score)
        if first_init:
            self._first_init()
        self.clf = self.train_model()

    @staticmethod
    def __init_analyzer(username: str, password: str, version: str):
        return ToneAnalyzerV3(
            username=username,
            password=password,
            version=version)

    def _first_init(self):
        with open(self._training_files[0]) as f:
            with open('_save_values.txt', 'w') as of:
                for line in f:
                    data = self.tone_analyzer.tone(text=line.strip())
                    score_dict = {}
                    for t in data['document_tone']['tone_categories']:
                        for ele in t['tones']:
                            score_dict[ele['tone_name']] = ele['score']
                    for key in sorted(score_dict.keys()):
                        of.write(str(score_dict[key]) + ' ')
                    of.write('\n')

    def train_model(self):
        x_matrix = []
        with open('_save_values.txt') as f:
            for line in f:
                x_matrix.append([float(x) for x in line.rstrip().split()])

        y_matrix = []
        with open(self._training_files[1]) as f:
            for line in f:
                y_matrix.append(line.rstrip())
        print(x_matrix)
        print(y_matrix)
        t_clf = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)
        t_clf.fit(x_matrix, y_matrix)

        return t_clf

    def get_score(self, message):
        data = self.tone_analyzer.tone(text=message)

        score_dict = {}
        for t in data['document_tone']['tone_categories']:
            for ele in t['tones']:
                score_dict[ele['tone_name']] = ele['score']

        temp = []
        for key in sorted(score_dict.keys()):
            temp.append(score_dict[key])

        # general_sum = 0
        # thresh_sum = 0

        # for key in score_dict.keys():
        #    if key == 'Openness' or key == 'Conscientiousness' or key == 'Agreeableness':
        #         if score_dict[key] < 0.5:
        #             general_sum -= 1 - score_dict[key]
        #         else:
        #             general_sum += score_dict[key]
        #     elif key == 'Anger' or key == 'Disgust' or key == 'Fear':
        #         if score_dict[key] > 0.5:
        #             thresh_sum -= score_dict[key]
        #         else:
        #             thresh_sum += 1 - score_dict[key]
        #     elif key == 'Joy':
        #         if score_dict[key] > 0.5:
        #             thresh_sum += score_dict[key]
        #         else:
        #             thresh_sum -= 1 - score_dict[key]

        # general_sum *= self._general_ratio
        # thresh_sum *= self._thresh_ratio

        # print(general_sum, thresh_sum)
        # return general_sum + thresh_sum
        print("Predict: ", self.clf.predict([temp]))
        print("Probabilities: ", self.clf.predict_proba([temp])[0])

        prob = self.clf.predict_proba([temp])[0]
        return -1 * prob[0] + prob[2]

        # print("Sum Score: ", net_score)
        # print(sum(self.clf.predict_proba([temp])[0]))

# myT = ToneAnalyzer("30414254-d997-450b-a250-6bee15973725", "cgIxQsZpDFGt", '2016-05-19',
#                   './data/text', './data/scores', False)
#print(myT.get_score("I love you"))
#print(myT.get_score("You are the best streamer I've ever seen and are super good at the game"))
#print(myT.get_score("I wish I was as good as you"))
#print(myT.get_score("die in a hole"))
#print(myT.get_score("suck my cock"))


# Plot data points and hand rate some
