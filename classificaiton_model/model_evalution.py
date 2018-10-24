import logging


class ModelEvaluation:
    """
    Model Evaluation class to include all kinds of evaluation methods
    """

    def __init__(self, practical_res='', idea_res=''):
        self.real = practical_res
        self.ideal = idea_res

    def accuracy(self):
        if len(self.real)==0 or len(self.ideal)==0:
            logging.warning("Empty data")
            return 0.0
        if isinstance(self.real, str) or isinstance(self.real, int) or isinstance(self.real, float):
            if self.real == self.ideal:
                return print('Two data matches')
            else:
                return print("Two data don't match")
        count = 0
        if len(self.real) != len(self.ideal):
            raise ValueError("Data size must be equal")
        for self.real_ele, self.ideal_ele in zip(self.real, self.ideal):
            if self.real_ele == self.ideal_ele:
                count += 1
            else:
                print(self.real_ele, self.ideal_ele)
        return float(count)/float(len(self.real))

