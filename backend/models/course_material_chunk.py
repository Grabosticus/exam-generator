from dataclasses import dataclass

"""
This class represents a chunk from some course material.
It contains the text from the chunk.
You can add metadata as new properties to it (e.g. lecture_number: int, lecture_title: str, ...)
"""
@dataclass
class CourseMaterialChunk:
    id: str # a general id of this chunk
    course_id: int # the id of the course the material of the chunk belongs to
    chunk_ind: int # the index of this chunk in the file that it was taken from
    text: str # the text in the chunk