import re

# some tokenizers
def tokzr_WORD(txt): return ('WORD', re.findall(r'(?ms)\W*(\w+)', txt))  # split words
def tokzr_SENT(txt): return ('SENTENCE', re.findall(r'(?ms)\s*(.*?(?:\.|\?|!))', txt))  # split sentences
def tokzr_QA(txt):
    l_qa = []
    for m in re.finditer(r'(?ms)^[\s#\-\*]*(?:Q|Question)\s*:\s*(?P<QUESTION>\S.*?\?)[\s#\-\*]+(?:A|Answer)\s*:\s*(?P<ANSWER>\S.*?)$', txt):  # split (Q, A) sequences
        for k in ['QUESTION', 'ANSWER']:
            l_qa.append(m.groupdict()[k])
    return ('QA', l_qa)
def tokzr_QA_non_canonical(txt):  # Note: not supported by tokenize_recursively() as not canonical.
    l_qa = []
    for m in re.finditer(r'(?ms)^[\s#\-\*]*(?:Q|Question)\s*:\s*(?P<QUESTION>\S.*?\?)[\s#\-\*]+(?:A|Answer)\s*:\s*(?P<ANSWER>\S.*?)$', txt):  # split (Q, A) sequences
        for k in ['QUESTION', 'ANSWER']:
            l_qa.append((k, m.groupdict()[k]))
    return l_qa

dict_tokzr = {  # control string: tokenizer function
    'WORD'    : tokzr_WORD,
    'SENTENCE': tokzr_SENT,
    'QA'      : tokzr_QA,
}

# the core function
def tokenize_recursively(l_tokzr, work_on, lev=0):
    if isinstance(work_on, basestring):
        ctrl, work_on = dict_tokzr[l_tokzr[0]](work_on)  # tokenize
    else:
        ctrl, work_on = work_on[0], work_on[1:]  # get right part
    ret = [ctrl]
    if len(l_tokzr) == 1:
        ret.append(work_on)  # add right part
    else:
        for wo in work_on:  # dive into tree
            t = tokenize_recursively(l_tokzr[1:], wo, lev + 1)
            ret.append(t)
    return ret

# just for printing
def nestedListLines(aList, ind='    ', d=0):
    """ Returns multi-line string representation of \param aList.  Use \param ind to indent per level. """
    sRet = '\n' + d * ind + '['
    nested = 0
    for i, e in enumerate(aList):
        if i:
            sRet += ', '
        if type(e) == type(aList):
            sRet += nestedListLines(e, ind, d + 1)
            nested = 1
        else:
            sRet += '\n' + (d + 1) * ind + repr(e) if nested else repr(e)
    sRet += '\n' + d * ind + ']' if nested else ']'
    return sRet

# main()
inp1 = """
    * Question: I want try something.  Should I?
    * Answer  : I'd assume so.  Give it a try.
"""
inp2 = inp1 + 'Q: What is a good way to achieve this?  A: I am not so sure. I think I will use Python.'
print inp1
# print repr(tokzr_WORD(inp1))
print repr(tokzr_SENT(inp1))
# print repr(tokzr_QA(inp1))
# print repr(tokzr_QA_non_canonical(inp1))  # Really this way?
# print

# for ctrl, inp in [  # example control sequences
#     ('SENTENCE-WORD', inp1),
#     ('QA-SENTENCE', inp2)
# ]:
#     res = tokenize_recursively(ctrl.split('-'), inp)
#     print nestedListLines(res)