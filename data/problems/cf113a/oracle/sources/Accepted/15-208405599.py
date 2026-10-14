class Context:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def get_token(self):
        return self.words[self.index]

    def next(self):
        self.index += 1

    def end(self):
        return self.index == len(self.words)

    def dump(self):
        return self.index

    def restore(self, dump):
        self.index = dump


class Parser:
    def parse(self, ctx) -> bool:
        raise NotImplementedError


class WordParser(Parser):
    END = None

    def parse(self, ctx):
        if ctx.end():
            return False
        token = ctx.get_token()
        if token.endswith(self.END):
            ctx.next()
            return True
        return False


class AdjectiveMale(WordParser):
    END = "lios"


class AdjectiveFemale(WordParser):
    END = "liala"


class NounMale(WordParser):
    END = "etr"


class NounFemale(WordParser):
    END = "etra"


class VerbMale(WordParser):
    END = "initis"


class VerbFemale(WordParser):
    END = "inites"


class AnyWordParser(Parser):
    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, ctx) -> bool:
        for parser in self.parsers:
            dump = ctx.dump()
            if parser.parse(ctx):
                return True
            ctx.restore(dump)
        return False


class SequenceParser(Parser):
    def __init__(self, parser):
        self.parser = parser

    def parse(self, ctx) -> bool:
        status = False
        while not ctx.end() and self.parser.parse(ctx):
            status = True
        return status


class PhraseParser(Parser):
    def __init__(self, parsers_sequence):
        self.parsers_sequence = parsers_sequence

    def parse(self, ctx) -> bool:
        dump = ctx.dump()
        for parser in self.parsers_sequence:
            if not parser.parse(ctx):
                ctx.restore(dump)
                return False
        return True


class OptionalParser(Parser):
    def __init__(self, parser):
        self.parser = parser

    def parse(self, ctx) -> bool:
        dump = ctx.dump()
        if not self.parser.parse(ctx):
            ctx.restore(dump)
        return True


class MalePhraseParser(PhraseParser):
    def __init__(self):
        adjective_parser = AdjectiveMale()
        adjectives_parser = SequenceParser(adjective_parser)
        optional_adjectives_parser = OptionalParser(adjectives_parser)
        noun_parser = NounMale()
        verb_parser = VerbMale()
        verbs_parser = SequenceParser(verb_parser)
        optional_verbs_parser = OptionalParser(verbs_parser)
        parsers_pipeline = (optional_adjectives_parser, noun_parser, optional_verbs_parser)
        super().__init__(parsers_pipeline)


class FemalePhraseParser(PhraseParser):
    def __init__(self):
        adjective_parser = AdjectiveFemale()
        adjectives_parser = SequenceParser(adjective_parser)
        optional_adjectives_parser = OptionalParser(adjectives_parser)
        noun_parser = NounFemale()
        verb_parser = VerbFemale()
        verbs_parser = SequenceParser(verb_parser)
        optional_verbs_parser = OptionalParser(verbs_parser)
        parsers_pipeline = (optional_adjectives_parser, noun_parser, optional_verbs_parser)
        super().__init__(parsers_pipeline)


class SentenceParser(Parser):
    def __init__(self):
        self.male_phrase_parser = MalePhraseParser()
        self.female_phrase_parser = FemalePhraseParser()
        self.any_word_parser = AnyWordParser((
            AdjectiveMale(), AdjectiveFemale(),
            NounMale(), NounFemale(),
            VerbMale(), VerbFemale()
        ))

    def parse(self, ctx) -> bool:
        dump = ctx.dump()
        if not self.male_phrase_parser.parse(ctx):
            ctx.restore(dump)
        else:
            return True
        if not self.female_phrase_parser.parse(ctx):
            ctx.restore(dump)
        else:
            return True
        if not self.any_word_parser.parse(ctx):
            ctx.restore(dump)
            return False
        return True


def main():
    data = input().split()
    ctx = Context(data)
    parser = SentenceParser()
    status = parser.parse(ctx)
    if status and ctx.end():
        print("YES")
    else:
        print("NO")


main()