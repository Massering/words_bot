import pandas as pd

df = pd.read_csv('all.txt', names=['Lemma'])
df1 = pd.read_csv('hard.txt', names=['Lemma'])
df = pd.concat((df, df1), ignore_index=True)
# print(df)
#
# with open('all.txt', 'w', encoding='utf8') as file:
#     for i in df['Lemma']:
#         if str(i) != 'nan':
#             file.write(i + '\n')
print(df)
