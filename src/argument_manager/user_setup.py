
class user_setup:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def add_characteristic_to_db(self, slots):
        if intent is not None:
            ##add this
            slot_to_add = slots[1]
            ## add type, value
            print(slots[1])
            dict_for_query = {slot_to_add['name']:slot_to_add['value']}

            # todo: CLAY, add this to Query Manager (adds a specific user characteristic given user token)
            QueryManager.add_user_element(self.auth_token, dict_for_query)

        return self.find_next_question()
    def find_next_question(self):
        #find the next user setup question

        # todo: CLAY, add this to Query Manager (finds the next question we should ask given user token)
        next_question = QueryManager.find_next_user_setup(self.auth_token)
        if next_question == "age":
            response = "Can you tell me how old you are? For example, I am 1 week old! Since I'm so young I need you" \
                       "to tell me in a full sentence so I can understand you."
        elif next_question == "education":
            response = "What is your highest level of education? You can say something like I graduated" \
                       "high school, or I have a masters degree."
        elif next_question == "industry_name":
            response = "What industry do you work in? You can say something like I work in computer science, or" \
                       "I work in the healthcare industry."
        elif next_question == "job_title":
            response = "What do you do for work? Are you a software engineer? Or perhaps a teacher?"
        elif next_question == 'language':
            response = "What is your preferred language? What language would you prefer to speak in the country " \
                       "you'd like to move to. I'm a little new at this, though, so you need to tell me in a full " \
                       "sentence."
        else:
            response = None

        if not response is None:
            speechlet = self.build_question_response(response)
        else:
            return None
    def build_question_response(self, output):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'shouldEndSession': False
        }
