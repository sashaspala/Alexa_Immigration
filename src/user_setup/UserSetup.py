
class UserSetup():
    def __init__(self, auth_token, qm):
        self.auth_token = auth_token
        self.qm = qm
        self.slot_names = ['job_title', 'industry_name', 'age', 'language', 'education', 'user_name']

    def add_characteristic_to_db(self, slots):
        if slots is not None:
            ##determine what slot type it has it has
            type_name = self.get_slot_name(slots)
            slot_to_add = slots[type_name]['name']
            ## add type, value
            dict_for_query = {}
            dict_for_query[slot_to_add] = slots[type_name]['value']

            # adds a specific user characteristic given user token
            self.qm.add_user_element(self.auth_token, dict_for_query)

        return self.find_next_question()
    def get_slot_name(self, slots):
        for type in self.slot_names:
            if type in slots:
                return type
        return None
    def find_next_question(self):
        #find the next user setup question

        # finds the next question we should ask given user token
        next_question = self.qm.find_next_user_setup(self.auth_token)
        print(next_question)
        if next_question == "age":
            response = "Can you tell me how old you are? For example, I am 1 week old! Unfortunately, since I'm so " \
                       "young I need you to tell me in a full sentence so I can understand you."
        elif next_question == "name":
            response = "What would you like me to call you? It can be your actual name or a nickname."
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
            #TODO: added return statement here, remove if not needed --Yuzhe
            return speechlet
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
