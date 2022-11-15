# -*- coding: utf -*-
import pandas as pd
import glob
cities = {"Moscow": "Москва", 'Saint Petersburg': 'Санкт-Петербург', 'Yekaterinburg': 'Екатеринбург',
              'Nizhny Novgorod': 'Нижний Новгород', 'Novosibirsk': "Новосибирск", "Rostov-on-Don": "Ростов-на-Дону"}
products=['Лист_рулон_гк','Лист_рулон_хк','Лист_рулон_оцинк','Лист_рулон_окраш']
for city in cities:
    for prod in products:
        files=[file for file in glob.glob(rf"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\{city}\{prod}\*.xlsx")]
        combined=pd.DataFrame()
        for file in files:
            file=pd.read_excel(file)
            combined = pd.concat([combined, file])
        combined=combined.drop(columns='Поставщик.1',axis=1)
        # print(combined)
        combined.to_excel(rf"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\Объединенные файлы\{city}\{prod}.xlsx",index=False)



#     # file.drop(file.columns[[0]],axis=1)
#     combined=pd.concat([combined,file])
# # file = pd.read_excel(r"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\Moscow\Лист_рулон_гк\prod1_thickness_8.xlsx")
# # file.drop(file.columns[[0]], axis=1)
#
# # combined.to_csv(r"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\Moscow\Лист_рулон_гк\msk_prod1.csv")
# # combined.decode('Windows-1251')
# # combined.drop(combined.columns[[0]],axis=1)
# combined.to_excel(r"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\Moscow\msk_prod2.xlsx")
# comb_right=pd.read_excel(r"C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\Moscow\msk_prod2.xlsx")
# comb_right.drop(comb_right.columns[0],axis=1)
