#importing the Kaggle API
#pip install kaggle
import pandas as pd
import numpy as np
file= "country_vaccinations.csv"
vaccinesdf = pd.read_csv(file)
#print(vaccinesdf.info())
#print(vaccinesdf)

#sort rows to find top country vaccinations
vaccines_top = vaccinesdf[["country","people_fully_vaccinated"]]
vaccines_top = vaccines_top.sort_values(["people_fully_vaccinated"])
#print(vaccines_top)

#sort country by ppl_fully_vacs. fill blank cells w/ 0
vaccinesdf[["people_fully_vaccinated"]] = vaccinesdf[["people_fully_vaccinated"]].fillna(0)
#print(vaccinesdf[["people_fully_vaccinated"]])

#set d type of column "date" as initially "object"
vaccinesdf[["date"]] = vaccinesdf[["date"]].apply(pd.to_datetime)
#print(vaccinesdf.dtypes)

#group by
total_vac_per_country = vaccinesdf.loc[vaccinesdf.groupby('country').date.idxmax()]

#sort largets to smallest val
total_vac_per_country=total_vac_per_country.sort_values(by='people_fully_vaccinated', ascending=False)
print(total_vac_per_country[["country","people_fully_vaccinated"]])

#filter for countries where number of vaccinations is less than X
vaccine_gt_10k = total_vac_per_country[total_vac_per_country.people_fully_vaccinated > 10000][["country","people_fully_vaccinated"]]
#print(vaccine_gt_10k)


