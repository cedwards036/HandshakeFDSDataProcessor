from src.extract.custom_parsers import CustomParser, NullCustomParser
from src.extract.response_extractor import ResponseExtractor
from src.extract.response_parser import parse_responses


def extract(filepath: str, custom_parser: CustomParser = NullCustomParser()):
    return parse_responses(ResponseExtractor(filepath).extract(), custom_parser)
