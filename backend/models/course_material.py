from dataclasses import dataclass

"""
This class represents the course material that is passed to the LLM.
"""
@dataclass
class CourseMaterial:
    text: str # the text of the course material

    metadata: dict # the metadata of the course material e.g. 'topic', 'contains_formula', etc.