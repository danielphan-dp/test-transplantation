from typing import List

import nltk
from codebleu import calc_codebleu



def bleu(test: List[str], pred: List[str]) -> float:
    """
    Calculate BLEU score, using smoothing method 2 with auto reweighting, in the range of 0~100.

    :param test: list of test code tokens
    :param pred: list of predicted tokens
    :return: BLEU score
    """
    if len(pred) == 0 or len(test) == 0:
        return 0.0
    return 100.0 * nltk.translate.bleu_score.sentence_bleu(
        [test],
        pred,
        smoothing_function=nltk.translate.bleu_score.SmoothingFunction().method2,
        auto_reweigh=True,
    )


def batch_bleu(host_tests: List[List[str]], preds: List[List[str]]) -> List[float]:
    """
    Calculate BLEU score for a batch of sentences.

    :param host_tests: list of test sentences from the host project
    :param preds: list of predicted sentences
    :return: list of BLEU scores
    """
    if len(host_tests) != len(preds):
        raise ValueError("host_tests and preds must have the same length")
    return [bleu(test, pred) for test, pred in zip(host_tests, preds)]


def corpus_bleu(host_tests: List[List[str]], preds: List[List[str]]) -> float:
    """
    Calculate corpus-level BLEU score for a batch of sentences.

    :param host_tests: list of test sentences from the host project
    :param preds: list of predicted sentences
    :return: corpus-level BLEU score
    """
    if len(host_tests) != len(preds):
        raise ValueError("host_tests and preds must have the same length")
    return 100.0 * nltk.translate.bleu_score.corpus_bleu(
        [[test] for test in host_tests],
        preds,
        smoothing_function=nltk.translate.bleu_score.SmoothingFunction().method2,
        auto_reweigh=True,
    )


def code_bleu(test: str, pred: str, lang: str = "python") -> float:
    """
    Calculate CodeBLEU score in the range of 0~100.

    :param test: test code string
    :param pred: predicted code string
    :param lang: programming language (default: python)
    :return: CodeBLEU score
    """
    if not pred or not test:
        return 0.0
    
    result = calc_codebleu(
        [test], 
        [pred], 
        lang=lang,
        weights=(0.25, 0.25, 0.25, 0.25),
        tokenizer=None
    )
    return 100.0 * result['codebleu']


def batch_code_bleu(host_tests: List[str], preds: List[str], lang: str = "python") -> List[float]:
    """
    Calculate CodeBLEU score for a batch of code snippets.

    :param host_tests: list of test code strings from the host project
    :param preds: list of predicted code strings
    :param lang: programming language (default: python)
    :return: list of CodeBLEU scores
    """
    if len(host_tests) != len(preds):
        raise ValueError("host_tests and preds must have the same length")
    return [code_bleu(test, pred, lang) for test, pred in zip(host_tests, preds)]


def corpus_code_bleu(host_tests: List[str], preds: List[str], lang: str = "python") -> float:
    """
    Calculate corpus-level CodeBLEU score.

    :param host_tests: list of test code strings from the host project
    :param preds: list of predicted code strings
    :param lang: programming language (default: python)
    :return: corpus-level CodeBLEU score
    """
    if len(host_tests) != len(preds):
        raise ValueError("host_tests and preds must have the same length")
    if len(preds) == 0:
        return 0.0
    
    result = calc_codebleu(
        host_tests,
        preds,
        lang=lang,
        weights=(0.25, 0.25, 0.25, 0.25),
        tokenizer=None
    )
    return 100.0 * result['codebleu']



def main():
    # Test the codebleu module
    test_code = "def foo(x):\n    return x + 1\n"
    pred_code = "def foo(x):\n    return x + 1\n"
    print("CodeBLEU score:", code_bleu(test_code, pred_code))

if __name__ == "__main__":
    main()