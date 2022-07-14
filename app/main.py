from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from queue import Queue
from typing import Any
from flask import Flask, request, jsonify, make_response
from flask import Response
from com.models.bmi_predictor_model import Bmi_Model
from base_dao import BMI_DAO, Base_DAO
from settings import AppSettings


class Inference_app:
    def __init__(self, cfg: AppSettings, api: Base_DAO, app: Flask):
        self.cfg = cfg
        self.api = api
        self.app = app
        self.logger = self.cfg.logger
        self.n_workers = max(1, cpu_count() - 1)
        self.files_queue = Queue()
        self.tpe = ThreadPoolExecutor(max_workers=1)
        self.app_address = None

    def start(self):
        self.logger.info("Starting Attribute Extraction Processing ...")
        self.app.run(host=self.cfg.APP_HOST, port=self.cfg.APP_PORT)

    @staticmethod
    def index():
        return Response("Index", status=200)

    @staticmethod
    def return_failure(message: Any) -> Response:
        return make_response(
            jsonify({"message": str(message)}),
            500,
        )

    def validate(self, data: dict):
        app_id, age, gender, height, weight = data['app_id'], data['age'], data['gender'], data['height'], data[
            'weight']
        messages = []

        if not isinstance(app_id, int):
            messages.append("app_id  must be a int!")
        if not isinstance(age, int):
            messages.append("age  must be a int!")
        if not isinstance(gender, str):
            messages.append("gender  must be a string!")
        else:
            if gender not in ['Male', 'Female', 'Others']:
                messages.append("Invalid gender type, possible values ['Male', 'Female', 'Others'] ")
        if not isinstance(height, int):
            messages.append("Height  must be a int!")
        if not isinstance(weight, int):
            messages.append("Weight  must be a int!")

        if len(messages) == 0:
            return {"status_code": 200, "message": ["Validation Success"]}
        else:
            return {"status_code": 400, "message": messages}

    def process_data(self, data) -> dict:
        app_id, age, gender, height, weight = data['app_id'], data['age'], data['gender'], data['height'], data['weight']

        bmi_model = Bmi_Model(app_id, age, gender, height, weight)
        bmi_resp = bmi_model.business_logic()

        dao = BMI_DAO(app_id=bmi_model.app_id, age=bmi_model.age, gender=bmi_model.gender, height=bmi_model.height,
                      weight=bmi_model.weight, bmi=bmi_model.bmi,
                      issue_date=bmi_model.issue_date)
        self.api.insert_preds_to_db(dao.__dict__)
        return bmi_resp

    def predict(self):
        if not request.json:
            return self.return_failure("Empty data, bad request!")
        data = request.json
        self.logger.debug(f"Data received: {data}")

        if not isinstance(data, dict):
            raise TypeError("Passed data must be a dict!")

        validation_resp = self.validate(data)
        if validation_resp["status_code"] == 200:
            bmi_resp = self.process_data(data=data)
            return make_response(jsonify(bmi_resp))

        else:
            return make_response(jsonify(validation_resp["status_code"], validation_resp["message"]))

    def setup_api(self):
        self.app.add_url_rule(rule="/", view_func=self.index, methods=["GET"])
        self.app.add_url_rule(rule="/predict", view_func=self.predict, methods=["POST"])


def main():
    cfg = AppSettings()
    dao = Base_DAO()
    app = Flask(f"App - {__name__}")
    inference_app = Inference_app(cfg, dao, app)
    inference_app.setup_api()
    inference_app.start()


if __name__ == "__main__":
    main()
