# pdf_to_table

https://tabula.technology/

https://pypi.org/project/PyPDF4/
pip install PyPDF4

https://pypi.org/project/tabula-py/

https://riverbankcomputing.com/software/pyqt/download

https://coinmarketcap.com/currencies/safemoon-v2/historical-data/

pip install pandas

How To Install Pip On Windows
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

pip install pandas

//https://pypi.org/project/PyQtWebEngine/

https://pypi.org/project/PyQt6-WebEngine/

https://github.com/juliakaplan98/pdf_to_table.git

pip install openpyxl

https://xlsxwriter.readthedocs.io/index.html#
pip install XlsxWriter

# Below are quick example

# Append Row to DataFrame

list_row = ["Hyperion", 27000, "60days", 2000]
df.loc[len(df)] = list_row

# Using pandas.concat() to append a row

new_row = pd.DataFrame({'Courses':'Hyperion', 'Fee':24000, 'Duration':'55days', 'Discount':1800}, index=[0])
df2 = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)

# Append specific row/index name using DataFrame.loc[]

df.loc['7', :] = ['Hive',25000,'45days',2000]

# Append row in DataFrame using DataFrame.loc[]

df.loc['7'] = ['Hive',25000,'45days',2000]

# New list to append Row to DataFrame

list = ["Hyperion", 27000, "60days", 2000]
df.loc[len(df)] = list
print(df)

# Using pandas.concat() to append a row

new_row = pd.DataFrame({'Courses':'Hyperion', 'Fee':24000, 'Duration':'55days', 'Discount':1800}, index=[0])
df2 = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)
print (df2)

# Append specific row/index name using DataFrame.loc[]

df.loc['7', :] = ['Hive',25000,'45days',2000]
print(df)

# Append row in DataFrame using DataFrame.loc[]

df.loc['7'] = ['Hive',25000,'45days',2000]
print(df)

import pandas as pd
technologies = ({
'Courses':["Spark","Hadoop","pandas","Java","Pyspark"],
'Fee' :[20000,25000,30000,22000,26000],
'Duration':['30days','40days','35days','60days','50days'],
'Discount':[1000,2500,1500,1200,3000]
})
df = pd.DataFrame(technologies)
print(df)

# Using pandas.concat() to add a row

new_row = pd.DataFrame({'Courses':'Hyperion', 'Fee':24000, 'Duration':'55days', 'Discount':1800}, index=[0])
df2 = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
print (df2)

# Add specific row/index name using DataFrame.loc[]

df.loc['Index5', :] = ['Hive',25000,'45days',2000]
print(df)

# Add row in DataFrame using DataFrame.loc[]

df.loc['Index5'] = ['Hive',25000,'45days',2000]
print(df)

Sumire Matsubara
