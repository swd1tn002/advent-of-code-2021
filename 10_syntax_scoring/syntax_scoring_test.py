from syntax_scoring import *


def test_read_input():
    lines = read_input()

    assert lines[0] == '({[[{[(([({((<[]>{[][]})[{<>[]}{[]{}}])[<[<><>][[]{}]>{[{}()][{}]}]}(<[{<>{}}[()]]<[{}[]]>><[{()}({}())]'
    assert lines[-1] == '<[{([<<<{{[<<({}())[<>]>[{[]{}}[()]]>{{[<>{}]{<><>}}<({}[]){()<>}>}]}}[{{({{()()}(()[])}<<['


def test_is_corrupted():
    assert is_corrupted('(]') == True
    assert is_corrupted('{()()()>') == True
    assert is_corrupted('(((()))}') == True
    assert is_corrupted('<([]){()}[{}])') == True


def test_incomplete():
    assert is_corrupted('[({(<(())[]>[[{[]{<()<>>') == False
    assert is_corrupted('[(()[<>])]({[<{<<[]>>(') == False
    assert is_corrupted('(((({<>}<{<{<>}{[]{[]{}') == False
    assert is_corrupted('{<[[]]>}<{[{[{[]{()[[[]') == False
    assert is_corrupted('<{([{{}}[<[[[<>{}]]]>[]]') == False


def test_get_syntax_error_score():
    assert get_syntax_error_score('{([(<{}[<>[]}>{[]{[(<()>') == 1197


def test_close_incomplete_line():
    assert close_incomplete_line('<([{') == '}])>'
    assert close_incomplete_line('{<[[]]>}<{[{[{[]{()[[[]') == ']]}}]}]}>'


def test_get_syntax_completion_score():
    assert get_syntax_completion_score(']]}}]}]}>') == 995444
