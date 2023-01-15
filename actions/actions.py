from typing import Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.policies.form_policy import FormPolicy
#from rasa.core.policies.mapping_policy import MappingPolicy
#from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.rule_policy import RulePolicy

class ActionSubmitHealthForm(Action):
    def name(self) -> str:
        return "action_submit_health_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Submit the form and deactivate the form
        form_name = "health_form"
        tracker.submit_form(form_name)
        tracker.deactivate_form(form_name)
        return []
#@DefaultV1Recipe.register("HealthFormPolicy")
class HealthFormPolicy(FormPolicy):
    def name(self) -> Text:
        return "health_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        # list of slots that should be filled before form is submitted
        return ["blood_sugar_level", "health_condition", "diet",
                "symptoms", "medication", "diabetes_checkup",
                "physical_activity", "sleep"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "blood_sugar_level": self.from_text(intent=["inform"]),
            "health_condition": self.from_text(intent=["inform"]),
            "diet": self.from_text(intent=["inform"]),
            "symptoms": self.from_text(intent=["inform"]),
            "medication": self.from_text(intent=["inform"]),
            "diabetes_checkup": self.from_text(intent=["inform"]),
            "physical_activity": self.from_text(intent=["inform"]),
            "sleep": self.from_text(intent=["inform"])
        }
#@DefaultV1Recipe.register("RulePolicy")
class RulePolicy(RulePolicy):
    def __init__(self):
        self.form_name = "health_form"
        self.form_submit_action = "action_submit_health_form"

    async def predict_action_probabilities(
        self,
        tracker: Tracker,
        domain: Domain,
        interpreter: NaturalLanguageInterpreter,
    ):
        """Predicts the next action the bot should take."""
        if tracker.active_form.get("name") == self.form_name:
            return {self.form_submit_action: 1.0}
        else:
            return await super().predict_action_probabilities(
                tracker, domain, interpreter
            )

#create agent and set policies
from rasa.core.agent import Agent
agent = Agent(
    "path/to/your/domain.yml",
    policies=[HealthFormPolicy(),RulePolicy()]
)