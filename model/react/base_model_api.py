class BaseModelAPI:
    def __init__(self, model):
        self.model = model

    def __call__(self, message):
        pass

    def chat(self, prompt):
        pass