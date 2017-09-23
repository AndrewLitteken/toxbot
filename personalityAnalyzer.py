from watson_developer_cloud import PersonalityInsightsV3
import json
# Creates personality profile based on previous result if provided

class PersonalityAnalyzer:
	def __init__(self, username=None, password=None, version=None):
		
		self.personality_analyzer = self.__init_analyzer(username, password,version)
		
	def __init_analyzer(self, username: str, password: str, version: str):
		return PersonalityInsightsV3(
			version=version,
			username=username,
			password=password)
	
	def create_profile(self, text_profile):
		profile = self.personality_analyzer.profile(json.dumps(text_profile, ensure_ascii=False), content_type='application/json', raw_scores=True, consumption_preferences=False)
	
		return profile
		
	def create_scores(self, profile):
		score_dict = {}

		for personality in profile["personality"]:
			category = personality["name"]
			score_dict[category] = {"score": personality["percentile"]}
			children = []
	
			for child in personality["children"]:
				children.append({"name": child["name"], "score": child["percentile"]}) 
	
			score_dict[category]["children"]=children
	
		thresh_sum = 0
		for key in score_dict.keys():
			if key == 'Conscientiousness' and key == 'Extraversion':
				if score_dict[key]["score"] > 0.5:
					general_sum -= 1 - score_dict[key]["score"]	
				else:
					general_sum += score_dict[key]["score"]
			elif key == 'Openness' and key == 'Emotional Range':
				if score_dict[key]["score"] > 0.85:
					thresh_sum -= score_dict[key]["score"]
				else:
					tresh_sum += 1 - score_dict[key]["score"]
			elif key == "Agreeableness":
				if score_dict[key]["score"] < 0.5:
					thresh_sum -= 1 - score_dict[key]["score"]
				else:
					thresh_sum += score_dict[key]["score"]
		
			for child in score_dict[key]["children"]:
				name = child['name']
			
				if name == 'Assertiveness' or name == 'Excitement-seeking' or name == 'Immoderation' or name == 'Authority Challenging' or name=='Fiery':
					if child['score'] > 0.65:
						thresh_sum -= child['score']
					else:
						thresh_sum += 1 - child['score']
				elif name == 'Cooperation' or name == 'Modesty' or name == 'Uncompromising' or name == 'Trust' or name == 'Cautiousness' or name == ' Achievement Striving' or name == 'Dutifulness' or name == 'Cheerfulness':
					if child['score'] < 0.45:
						thresh_sum -= 1 - child['score']
					else:
						thresh_sum += child['score']
		score = 0
		if thresh_sum > 1:
			score = 1
		elif thresh_sum < -1:
			score = -1
		else:
			score = thresh_sum

		return score

	def analyze_personality(self, messages_info):
		messages_to_analyze={"contentItems": [] }
		score_total=0
		for message in messages_info:
			messages_to_analyze["contentItems"].append(message[0])
			#score_total+=message[1]
		score_avg = score_total/len(messages_to_analyze)
		new_profile=self.create_profile(messages_to_analyze)
		new_scores=self.create_scores(new_profile)
		return new_scores
