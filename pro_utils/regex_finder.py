import re
from pro_utils.read_files import read_excel_files


def re_match_single(pattern, input_str):  # return [] if no match found
    res = re.search(pattern, input_str, re.IGNORECASE)
    res = res.group() if res else ''
    return res


def re_match_no_group(pattern, input_str):
    """
        regex function
        Args:
            pattern: regular expression needed to match in input_str
            input_str: input string

        Returns:
            list object, containing all matched information in inpur_str
        """
    res = []
    for match_obj in re.finditer(pattern, input_str):
        res.append(match_obj.group())
    return res


if __name__ == "__main__":
    pattern_to = r'prov.*\n'
    #test = read_excel_files('test_test.xlsx')['TransLate']
    test = 'werh'
    print(test)
    for ele in test:
        res = re_match_no_group(pattern_to, ele)
    print(res)