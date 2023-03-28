import pandas as pd

test_list = [2, 4, 22, 3, 3, 2, 6, 9, 4, 4]
each_num = [5, 20, 33, 36, 49, 46, 9, 77, 90, 39]
services_tmp_list = [[0]*test_list[i] for i in range(10)]
print(services_tmp_list)
q_table = pd.DataFrame(
            services_tmp_list,  # q_table initial values
            columns=list(range(22)))
print(q_table)