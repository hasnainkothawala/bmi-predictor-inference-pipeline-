from com.models import base_model
from datetime import date


class Bmi_Model(base_model.Base_Model):

    def __init__(self, app_id, age, gender, height, weight, issue_date=date.today().strftime("%b-%d-%Y")):
        super().__init__()
        self.app_id: int = app_id
        self.age: int = age
        self.gender: str = gender
        self.height: int = height
        self.weight: int = weight
        self.issue_date: date = issue_date
        self.bmi: float = None
        self.quote: float = None

    def get_final_quote(self, basequote):
        if self.gender == 'Female':
            self.quote = 0.9 * basequote  # give a 10 percent off for females
        else:
            self.quote = basequote
        return self.quote

    def calculate_bmi(self):
        # defining a function for BMI
        self.bmi = self.weight / ((self.height / 100) ** 2)

        return self.bmi

    def business_logic(self):

        self.calculate_bmi()
        if (self.age in list(range(18, 40))) and ((17.49 > self.bmi) or (self.bmi > 38.5)):
            message = 'Age is between 18 to 39 and BMI is either less than 17.49 or greater than 38.5'
            return {"Quote": self.get_final_quote(750), "Message": message, "BMI": self.bmi}

        elif (self.age in list(range(40, 60))) and ((18.49 > self.bmi) or (self.bmi > 38.5)):

            message = 'Age is between 40 to 59 and BMI is either less than 18.49 or greater then 38.5'
            return {"Quote": self.get_final_quote(1000), "Message": message, "BMI": self.bmi}

        elif (self.age > 60) and ((18.49 > self.bmi) or (self.bmi > 45.5)):
            message = 'Age is greater than 60 and BMI is either less than 18.49 or greater than 38.5'
            return {"Quote": self.get_final_quote(2000), "Message": message, "BMI": self.bmi}

        else:
            message = 'BMI is in right range'
            return {"Quote": self.get_final_quote(500), "Message": message, "BMI": self.bmi}
