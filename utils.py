"""
Contains questions that will be asked
"""

questions_ext = [("Scale of Negative Impact", "How grave is its negative impact?"),
                 ("Scope of Negative Impact", "How widespread is the impact? \n(Eg. the number of individuals affected or the extend of environmental damage.)"),
                 ("Irremediable Character", "How hard is it to counteract or make good the resulting harm?"),
                 ("Human Rights", "How severe is the potential negative human rights impacts?"),
                 ("Human Rights", "How likely is the potential negative human rights impact?"),
                 ("Scale of Positive Impact", "What is the scale of the potential positive impact?"),
                 ("Scope of Positive Impact", "What is the scope of the potential positive impact?"),
                 ("Likelihood", "What is the likelihood of the potential positive impact?")]

#NOTE: might not need this anymore
bounds_ext = [0, 0, 0, 0, 0, 0, 0, 0]

questions_int = []

bounds_int = []

ext_q_dict = {} #Questions
int_q_dict = {}

for i, q in enumerate(questions_ext):
    ext_q_dict[q] = bounds_ext[i]
for i, q in enumerate(questions_int):
    int_q_dict[q] = bounds_int[i]
