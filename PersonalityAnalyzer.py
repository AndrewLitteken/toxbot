Jonathan Baker:
	2nd floor Hurley
	End of the hall
Connor Higgins:
	Jack walked in I left it with him already
	Is that okay?
	He's at the desk and says he will be past 5
Jonathan Baker:
	Yup 
	Sounds good
	Wait
	Can you pick me up at main? :P
Connor Higgins:
	I'm leaving now, will there still be someone to let me on campus?
Jonathan Baker:
	Main circle? 
	You don't need to get on campus 
Connor Higgins:
	I'll try to find my way then, sure
Jonathan Baker:
	Hmmmm
Connor Higgins:
	I'm near eddy street
	Shouldn't be too long now
	I'm here
Jonathan Baker:
	Forgot my charger
	I'm coming 
Connor Higgins:
	Okay
Jonathan Baker:
	username='a54c1a30-92fe-4c1f-b34a-02936047e396',
#           password='8WTlVVDHFHCt',
#           version='2016-05-19')
Connor Higgins:
	So I just thought of something. If we are just training it to know if a message is toxic or not based on our neural network, what is the tone analyzer of Watson even doing?
	I'm going to be leaving soon, you want me to pick you up?
	Well, if you're awake, you have until I get there to text me, leaving now though
Jonathan Baker:
	Oh lol
	Heading over now 
Connor Higgins:
	ttps://github.com/AndrewLitteken/att-hack-2017.git
Jonathan Baker:
	from watson_developer_cloud import PersonalityInsightsV3
import json


# Creates personality profile based on previous result if provided

class PersonalityAnalyzer:
    def __init__(self, username=None, password=None, version=None):

        self.personality_analyzer = self.__init_analyzer(username, password, version)

    @staticmethod
    def __init_analyzer(username: str, password: str, version: str):
        return PersonalityInsightsV3(
            version=version,
            username=username,
            password=password)

    def create_profile(self, text_profile):
        profile = self.personality_analyzer.profile(json.dumps(text_profile, ensure_ascii=False),
                                                    content_type='application/json', raw_scores=True,
                                                    consumption_preferences=False)

        return profile

    @staticmethod
    def create_scores(profile):
        score_dict = {}

        for personality in profile["personality"]:
            category = personality["name"]
            score_dict[category] = {"score": personality["percentile"]}
            children = []

            for child in personality["children"]:
                children.append({"name": child["name"], "score": child["percentile"]})

            score_dict[category]["children"] = children

        thresh_sum = 0
        for key in score_dict.keys():
            if key == 'Openness' and key == 'Emotional Range':
                if score_dict[key]["score"] > 0.85:
                    thresh_sum -= score_dict[key]["score"]
                else:
                    thresh_sum += 1 - score_dict[key]["score"]
            elif key == "Agreeableness":
                if score_dict[key]["score"] < 0.3:
                    thresh_sum -= 1 - score_dict[key]["score"]
                else:
                    thresh_sum += score_dict[key]["score"]

            for child in score_dict[key]["children"]:
                name = child['name']

                if name == 'Assertiveness' or name == 'Excitement-seeking' or name == 'Immoderation' or name == 'Authority Challenging' or name == 'Fiery':
                    if child['score'] > 0.75:
                        thresh_sum -= child['score']
                    else:
                        thresh_sum += 1 - child['score']
                elif name == 'Cooperation' or name == 'Modesty' or name == 'Uncompromising' or name == 'Trust' or name == 'Cautiousness' or name == ' Achievement Striving' or name == 'Dutifulness' or name == 'Cheerfulness':
                    if child['score'] < 0.3:
                        thresh_sum -= 1 - child['score']
                    else:
                        thresh_sum += child['score']
                        
        print("\n\n" + str(thresh_sum) + "\n\n")
        score = thresh_sum / 8
        if score > 1:
            score = 1
        elif score < -1:
            score = -1

        return score

    def analyze_personality(self, messages_info):
        messages_to_analyze = {"contentItems": []}
        score_total = 0
        words = 0
        while words < 100:
            for message in messages_info:
                messages_to_analyze["contentItems"].append(message[0])
                words += len(message[0].split())
            # score_total+=message[1]
        print("\n\n\n\n\n\n\n" + str(messages_to_analyze) + "\n\n\n\n\n")
        score_avg = score_total / len(messages_to_analyze)

        try:
            new_profile = self.create_profile(messages_to_analyze)
            new_scores = self.create_scores(new_profile)
        except Exception:
            new_scores = 0

        return new_scores
