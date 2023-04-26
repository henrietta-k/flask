"""
Contains questions that will be asked
"""

questions_ext = ["Scale: How grave is its negative impact?",
             "Scope: How widespread is the impact? (Eg. the number of individuals affected or the extend of environmental damage.) ",
             "Irremediable character: How hard is it to counteract or make good the resulting harm? ",
             "How severe is the potential negative human rights impacts? ",
             "How likely is the potential negative human rights impact? ",
             "What is the scale of the potential positive impact? ",
             "What is the scope of the potential positive impact? ",
             "What is the likelihood of the potential positive impact? "]

bounds_ext = [0, 0, 0, 0, 0, 0, 0, 0]

questions_int = []

bounds_int = []

ext_q_dict = {} #Questions
int_q_dict = {}

for i, q in enumerate(questions_ext):
    ext_q_dict[q] = bounds_ext[i]
for i, q in enumerate(questions_int):
    int_q_dict[q] = bounds_int[i]
