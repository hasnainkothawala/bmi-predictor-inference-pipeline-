class Base_Model:
    def __init__(self, model_name=None, model_path=None, inference_mappings=[], model_version='v1'):
        self.model_name = model_name
        self.model_path = model_path
        self.inference_mappings = inference_mappings
        self.model_version = model_version
