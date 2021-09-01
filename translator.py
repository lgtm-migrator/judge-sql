from enum import Enum, auto

from dodona_command import ErrorType


class Translator:
    class Language(Enum):
        EN = auto()
        NL = auto()

    class Text(Enum):
        ADD_A_SEMICOLON = auto()
        SUBMISSION_CONTAINS_MORE_QUERIES = auto()
        SUBMISSION_CONTAINS_LESS_QUERIES = auto()
        DIFFERENT_ROW_COUNT = auto()
        DIFFERENT_COLUMN_COUNT = auto()
        COMPARING_QUERY_OUTPUT_CSV_CONTENT = auto()
        COMPARING_QUERY_OUTPUT_TYPES = auto()
        QUERY_SHOULD_ORDER_ROWS = auto()
        QUERY_SHOULD_NOT_ORDER_ROWS = auto()
        ROWS_ARE_BEING_ORDERED = auto()
        ROWS_ARE_NOT_BEING_ORDERED = auto()

    def __init__(self, language: Language):
        self.language = language

    @classmethod
    def from_str(cls, language: str) -> "Translator":
        if language == "nl":
            return cls(cls.Language.NL)

        # default value is EN
        return cls(cls.Language.EN)

    def human_error(self, error: ErrorType) -> str:
        return self.error_translations[self.language][error]

    def error_status(self, error: ErrorType) -> dict[str, str]:
        return {
            "enum": error,
            "human": self.human_error(error),
        }

    def translate(self, message: Text, **kwargs) -> str:
        return self.text_translations[self.language][message].format(**kwargs)

    error_translations = {
        Language.EN: {
            ErrorType.INTERNAL_ERROR: "Internal error",
            ErrorType.COMPILATION_ERROR: "The query is not valid",
            ErrorType.MEMORY_LIMIT_EXCEEDED: "Memory limit exceeded",
            ErrorType.TIME_LIMIT_EXCEEDED: "Time limit exceeded",
            ErrorType.OUTPUT_LIMIT_EXCEEDED: "Output limit exceeded",
            ErrorType.RUNTIME_ERROR: "Crashed while testing",
            ErrorType.WRONG: "Test failed",
            ErrorType.WRONG_ANSWER: "Test failed",
            ErrorType.CORRECT: "All tests succeeded",
            ErrorType.CORRECT_ANSWER: "All tests succeeded",
        },
        Language.NL: {
            ErrorType.INTERNAL_ERROR: "Interne fout",
            ErrorType.COMPILATION_ERROR: "Ongeldige query",
            ErrorType.MEMORY_LIMIT_EXCEEDED: "Geheugenlimiet overschreden",
            ErrorType.TIME_LIMIT_EXCEEDED: "Tijdslimiet overschreden",
            ErrorType.OUTPUT_LIMIT_EXCEEDED: "Outputlimiet overschreden",
            ErrorType.RUNTIME_ERROR: "Gecrasht bij testen",
            ErrorType.WRONG: "Test gefaald",
            ErrorType.WRONG_ANSWER: "Test gefaald",
            ErrorType.CORRECT: "Alle testen geslaagd",
            ErrorType.CORRECT_ANSWER: "Alle testen geslaagd",
        },
    }

    text_translations = {
        Language.EN: {
            Text.ADD_A_SEMICOLON: "Add a semicolon ';' at the end of each SQL query.",
            Text.SUBMISSION_CONTAINS_MORE_QUERIES: "Error: the submitted solution contains more queries ({submitted}) than expected ({expected}). Make sure that all queries correctly terminate with a semicolon.",
            Text.SUBMISSION_CONTAINS_LESS_QUERIES: "Error: the submitted solution contains less queries ({submitted}) than expected ({expected}). Make sure that all queries correctly terminate with a semicolon.",
            Text.DIFFERENT_ROW_COUNT: "Expected row count {expected}, your row count was {submitted}.",
            Text.DIFFERENT_COLUMN_COUNT: "Expected column count {expected}, your column count was {submitted}.",
            Text.COMPARING_QUERY_OUTPUT_CSV_CONTENT: "Comparing query output csv content",
            Text.COMPARING_QUERY_OUTPUT_TYPES: "Comparing query output SQL types",
            Text.QUERY_SHOULD_ORDER_ROWS: "Query should return ordered rows.",
            Text.QUERY_SHOULD_NOT_ORDER_ROWS: "No explicit row ordering should be enforced in query.",
            Text.ROWS_ARE_BEING_ORDERED: "rows are being ordered",
            Text.ROWS_ARE_NOT_BEING_ORDERED: "rows are not being ordered",
        },
        Language.NL: {
            Text.ADD_A_SEMICOLON: "Voeg een puntkomma ';' toe aan het einde van elke SQL query.",
            Text.SUBMISSION_CONTAINS_MORE_QUERIES: "Error: de ingediende oplossing bestaat uit meer queries ({submitted}) dan verwacht ({expected}). Zorg ervoor dat elke query correct eindigt op een puntkomma.",
            Text.SUBMISSION_CONTAINS_LESS_QUERIES: "Error: de ingediende oplossing bestaat uit minder queries ({submitted}) dan verwacht ({expected}). Zorg ervoor dat elke query correct eindigt op een puntkomma.",
            Text.DIFFERENT_ROW_COUNT: "Verwachtte {expected} rijen, uw aantal rijen is {submitted}.",
            Text.DIFFERENT_COLUMN_COUNT: "Verwachtte {expected} kolommen, uw aantal kolommen is {submitted}.",
            Text.COMPARING_QUERY_OUTPUT_CSV_CONTENT: "Vergelijken van de query output in csv formaat",
            Text.COMPARING_QUERY_OUTPUT_TYPES: "Vergelijken van de query output SQL types",
            Text.QUERY_SHOULD_ORDER_ROWS: "De query moet de rijen gesorteerd teruggeven.",
            Text.QUERY_SHOULD_NOT_ORDER_ROWS: "De query mag de rijen niet expliciet gaan sorteren.",
            Text.ROWS_ARE_BEING_ORDERED: "rijen worden gesorteerd",
            Text.ROWS_ARE_NOT_BEING_ORDERED: "rijen worden niet gesorteerd",
        },
    }
