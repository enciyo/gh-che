import dataclasses


@dataclasses.dataclass
class Conversation:
    prompt: str
    answer: str
    rating: str = "**"

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "answer": self.answer,
            "rating": self.rating,
        }

    @staticmethod
    def from_dict(data):
        return Conversation(data["prompt"], data["answer"], data["rating"])
