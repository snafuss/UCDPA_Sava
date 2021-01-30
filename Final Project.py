# importing the Kaggle API
# pip install kaggle
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def import_format_csv(filename):
    imported_csv = pd.read_csv(filename)
    imported_csv.columns = [header.lower() for header in imported_csv.columns]
    return imported_csv

file = "country_vaccinations.csv"
vaccinesdf = import_format_csv(file)
#print(vaccinesdf.head())
#print(vaccinesdf.shape)
#print(vaccinesdf)

file2 = "population_by_country_2020.csv"
popdf = import_format_csv(file2)
#print(popdf.head())
#renaming columns to make homogenous.
popdf.rename(columns={'country (or dependency)':'country', 'population (2020)':'population'}, inplace=True)


# identified the NAN values and drop when no data is present for people_fully_vaccinated
vaccinesdf[["people_fully_vaccinated"]] = vaccinesdf[["people_fully_vaccinated"]].dropna()
#print(vaccinesdf[["people_fully_vaccinated"]])

# set d type of column "date" as initially "object"
vaccinesdf[["date"]] = vaccinesdf[["date"]].apply(pd.to_datetime)
#print(vaccinesdf.dtypes)

# group by&loc
total_vac_per_country = vaccinesdf.loc[vaccinesdf.groupby('country').date.idxmax()]

# sort largest to smallest value
total_vac_per_country = total_vac_per_country.sort_values(by='people_fully_vaccinated', ascending=False)
#print(total_vac_per_country[["country", "people_fully_vaccinated"]])

# filter for countries where number of vaccinations is more than 1mil
vaccine_gt_1m = total_vac_per_country[total_vac_per_country.people_fully_vaccinated > 1000000][
    ["country", "people_fully_vaccinated"]]

# iterate over rows with iterrows()
for index, row in vaccine_gt_1m.iterrows():
    print(str(row[1]) + " people have been fully vaccinated in " + row[0])

#merge vaccinedf with first two columns of popdf
#print(popdf.columns)
vacc_tot_pop = pd.merge(total_vac_per_country, popdf[["country","population"]], on='country')
print(vacc_tot_pop)

# sort new df ppl fully vacc and total population/country
vacc_tot_pop = vacc_tot_pop.sort_values(by='people_fully_vaccinated', ascending=False)
print(vacc_tot_pop[["country","population","people_fully_vaccinated"]])

# List for ordered sets of objects accessable via position + indexing
percent_list =[]
for index, row in vacc_tot_pop.iterrows():
    percent_list.append(row.people_fully_vaccinated / row.population * 100)
vacc_tot_pop['percent_vaccinated'] = percent_list

# could be done using the following code as well.
vacc_tot_pop['percent_vaccinated'] = vacc_tot_pop['people_fully_vaccinated'] / vacc_tot_pop['population'] * 100
print(vacc_tot_pop)

#Numpy array - print to see header, different names to previous
dataarray = np.genfromtxt(file2, delimiter=',', names=True, dtype=None, encoding= None, skip_header=0)
print(dataarray.dtype.names)
print(np.shape(dataarray))
print(dataarray['Population_2020'].mean())

#Visualisation
plotting = sns.displot(vacc_tot_pop.sort_values(by='percent_vaccinated', ascending=False), x="country", y="percent_vaccinated")
plt.xlabel("Countries")
plt.ylabel("Percent of vaccinated population")
plt.title("COVID-19 Global Vaccination Rate")
plt.xticks(rotation=90)
plt.show()


# daily vacs per 1mil country pop
#vaccinesdf["daily_vaccinations_per_million"] = 1000000 * vaccinesdf[["people_fully_vaccinated"]"] / homelessness["state_pop"]

# Subset rows for indiv_per_10k greater than 20
#high_homelessness = homelessness[homelessness["indiv_per_10k"] > 20]

# Sort high_homelessness by descending indiv_per_10k
#high_homelessness_srt = high_homelessness.sort_values("indiv_per_10k", ascending=False)

# From high_homelessness_srt, select the state and indiv_per_10k cols
#result = high_homelessness_srt[["state", "indiv_per_10k"]]
#print(result)



