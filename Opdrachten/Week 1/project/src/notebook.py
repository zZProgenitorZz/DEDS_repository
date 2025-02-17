#%% md
# # Werkcollege-opdrachten Week 1.3
#%% md
# ## Dependencies importeren
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# Zet eventuele warnings uit.
#%%
import pandas as pd
import sqlite3
import warnings
warnings.simplefilter("ignore")
import numpy as np
import openpyxl

from datetime import date, datetime

#%% md
# Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map
#%% md
# ## Databasetabellen inlezen
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.
#%%

def makeConnection():
    con = sqlite3.connect('../../go_sales_train.sqlite')
    return con


#%% md
# Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
# - product
# - product_type
# - product_line
# - sales_staff
# - sales_branch
# - retailer_site
# - country
# - order_header
# - order_details
# - returned_item
# - return_reason
#%%

def loadProduct(con):
    product = pd.read_sql_query('select * from product', con)
    return product

def loadProductType(con):
    product_type = pd.read_sql_query("SELECT * FROM product_type", con)
    return product_type

def loadProductLine(con):
    product_line = pd.read_sql_query("SELECT * FROM product_line", con)
    return product_line

def loadSalesStaff(con):
    sales_staff = pd.read_sql_query("SELECT * FROM sales_staff", con)
    return sales_staff

def loadSalesBranch(con):
    sales_branch = pd.read_sql_query("SELECT * FROM sales_branch", con)
    return sales_branch

def loadRetailerSite(con):
    retailer_site = pd.read_sql_query("SELECT * FROM retailer_site", con)
    return retailer_site

def loadCountry(con):
    country = pd.read_sql_query("SELECT * FROM country", con)
    return country

def loadOrderHeader(con):
    order_header = pd.read_sql_query("SELECT * FROM order_header", con)
    return order_header

def loadOrderDetail(con):
    order_details = pd.read_sql_query("SELECT * FROM order_details", con)
    return order_details

def loadReturnedItems(con):
    returned_item = pd.read_sql_query("SELECT * FROM returned_item", con)
    return returned_item

def loadReturnedReasons(con):
    return_reason = pd.read_sql_query("SELECT * FROM return_reason", con)
    return return_reason



#%% md
# Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.
#%% md
# Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:
#%%

def loadTables(con):
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    return pd.read_sql(sql_query, con)


#Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.
#%% md
# erachter 
#%% md
# Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>
#%% md
# ## Selecties op één tabel zonder functies
#%% md
# Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)
#%%

def vraag1(con):
    product = loadProduct(con)
    product_Lhonderd_Hvijftig = (product['PRODUCTION_COST'] > 50) & (product['PRODUCTION_COST'] < 100)
    resultaat = product.loc[(product_Lhonderd_Hvijftig), ('PRODUCT_NUMBER', 'PRODUCTION_COST')]
    return resultaat

#%% md
# Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 
#%%
def vraag2(con):
    product = loadProduct(con)
    product_margin_Ltwee_Hzes = (product['MARGIN'] > 0.6) | (product['MARGIN'] < 0.2)
    resultaat = product.loc[(product_margin_Ltwee_Hzes), ('PRODUCT_NUMBER', 'MARGIN')]
    return resultaat

#%% md
# Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)
#%%

def vraag3(con):
    country = loadCountry(con)
    country_francs = country['CURRENCY_NAME'] == 'francs'
    resultaat = country.loc[(country_francs), ['COUNTRY']]
    return resultaat
#%% md
# Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 
#%%
# sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#
# pd.read_sql(sql_query, sales_conn)

def vraag4(con):
    product = loadProduct(con)
    product_margin_Hvijftig = product['MARGIN'] > 0.5
    resultaat = product.loc[(product_margin_Hvijftig), ['INTRODUCTION_DATE']].drop_duplicates('INTRODUCTION_DATE')
    return resultaat
#%% md
# Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)
#%%

def vraag5(con):
    sales_branch = loadSalesBranch(con)
    sales_branch_adres_twee_notNan = sales_branch['ADDRESS2'].notna() & sales_branch['REGION'].notna()
    resultaat = sales_branch.loc[(sales_branch_adres_twee_notNan), ['ADDRESS1', 'CITY']]
    return resultaat



#%% md
# Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 
#%%

def vraag6(con):
    country = loadCountry(con)
    country_with_dollars = (country['CURRENCY_NAME'] == 'dollars') | (country['CURRENCY_NAME'] == 'new dollar')
    resultaat = country.loc[(country_with_dollars), ['COUNTRY']].sort_values('COUNTRY')
    return resultaat
#%% md
# Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 
#%%

def vraag7(con):
    retailer_site = loadRetailerSite(con)
    klanten_uit_D = (retailer_site['POSTAL_ZONE'].str[0] == 'D') & (retailer_site['ADDRESS2'].notna())
    resultaat = retailer_site.loc[(klanten_uit_D), ['ADDRESS1', 'ADDRESS2', 'CITY']]
    return resultaat




#%% md
# ## Selecties op één tabel met functies
#%% md
# Geef het totaal aantal producten dat is teruggebracht (1 waarde) 
#%%

def vraag8(con):
    returned_item = loadReturnedItems(con)
    returned_aantal_items = returned_item['RETURN_QUANTITY'].sum()
    return print(returned_aantal_items)

#%% md
# Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)
#%%

def vraag9(con):
    sales_branch = loadSalesBranch(con)
    aantal_region_sales_branch = sales_branch['REGION'].nunique()
    return print(aantal_region_sales_branch)

#%% md
# Maak 3 variabelen:
# - Een met de laagste
# - Een met de hoogste
# - Een met de gemiddelde (afgerond op 2 decimalen)
# 
# marge van producten (3 kolommen, 1 rij) 
#%%

def vraag10(con):
    product = loadProduct(con)
    product_H = product['MARGIN'].max()
    product_L = product['MARGIN'].min()
    product_Average = product['MARGIN'].mean().round(2)
    df_resultaat = pd.DataFrame({'Hoogste_Margin' : [product_H], 'Laagste_Margin' : [product_L], "Average_Margin" : [product_Average]})
    return df_resultaat
#%% md
# Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)
#%%

def vraag11(con):
    retailer_site = loadRetailerSite(con)
    aantal_Klanten_vestigingen_zonderTweedeAdres = retailer_site['ADDRESS2'].isna()
    resultaat = retailer_site.loc[(aantal_Klanten_vestigingen_zonderTweedeAdres), :].shape[0]
    return print(resultaat)



#%% md
# Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 
#%%

def vraag12(con):
    order_details = loadOrderDetail(con)
    gem_kostprijs_verkochte_producten = (order_details['UNIT_SALE_PRICE']) < (order_details['UNIT_PRICE'])
    nieuw_order_details = order_details.loc[(gem_kostprijs_verkochte_producten), :]
    resultaat = nieuw_order_details['UNIT_SALE_PRICE'].mean().round(2)
    return print(resultaat)

#%% md
# Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 
#%%

def vraag13(con):
    sales_staff = loadSalesStaff(con)
    aantal_staff_per_functie = sales_staff.groupby('POSITION_EN', as_index = False)['SALES_STAFF_CODE'].nunique().rename(columns = {'SALES_STAFF_CODE':'aantal_medewerker'})
    return aantal_staff_per_functie

#%% md
# Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 
#%%

def vraag14(con):
    sales_staff = loadSalesStaff(con)
    tele_Met_Medewerkers = sales_staff.groupby('WORK_PHONE', as_index = False)['SALES_STAFF_CODE'].nunique().rename(columns = {'SALES_STAFF_CODE':'aantal_medewerker'})
    tele_Met_Vier_Medewerkers = tele_Met_Medewerkers.loc[(tele_Met_Medewerkers['aantal_medewerker'] > 4), :]
    return tele_Met_Vier_Medewerkers

#%% md
# ## Selecties op meerdere tabellen zonder functies
#%% md
# Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 
#%%


def vraag15(con):
    retailer_site = loadRetailerSite(con)
    country = loadCountry(con)
    retailer_site_country_merge = pd.merge(retailer_site, country, left_on='COUNTRY_CODE', how='inner', right_on='COUNTRY_CODE')
    adres_stad_Nederland = retailer_site_country_merge.loc[(retailer_site_country_merge['COUNTRY'] == 'Netherlands'), ['ADDRESS1', 'CITY']]
    return adres_stad_Nederland




#%% md
# Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen)
#%%

def vraag16(con):
    product = loadProduct(con)
    product_type = loadProductType(con)
    product_producttype_merge = pd.merge(product, product_type, on='PRODUCT_TYPE_CODE', how='inner')
    product_van_type_eyewear = product_producttype_merge.loc[product_producttype_merge['PRODUCT_TYPE_EN'] == 'Eyewear', 'PRODUCT_NAME']
    return product_van_type_eyewear

#%% md
# Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 
#%%

# sales_branch_staff_merge = pd.merge(sales_staff, sales_branch, on = 'SALES_BRANCH_CODE', how = 'inner')
#
# sales_branch_manager = sales_branch_staff_merge.loc[(sales_branch_staff_merge['POSITION_EN'] == 'Branch Manager'), :]
#
#
#
# order_header_retailer_merge = pd.merge(retailer_site, order_header, on = 'RETAILER_SITE_CODE', how = 'inner')
#
# order_header_retailer_merge = order_header_retailer_merge.drop_duplicates(subset=['ADDRESS1'])
#
# final_merge = pd.merge(sales_branch_manager,order_header_retailer_merge, on = 'SALES_BRANCH_CODE', how = 'inner', )
#
# result = final_merge[['ADDRESS2_x', 'FIRST_NAME', 'LAST_NAME']]
#
# nt = result['ADDRESS2_x'].notna()
#
# resultaat = result.loc[nt, :]
#
# resultaat


#FUCK DIT KUT OPGAVE



#%% md
# Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 
#%%

def vraag18(con):
    sales_staff = loadSalesStaff(con)
    order_header = loadOrderHeader(con)
    sales_orders_merge = pd.merge(sales_staff, order_header, on='SALES_STAFF_CODE', how='left')
    manager = sales_orders_merge[sales_orders_merge['POSITION_EN'].str.contains('Manager', case=False, na=False)]
    result = manager[['POSITION_EN', 'ORDER_DATE']].drop_duplicates()
    return result



#%% md
# Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 
#%%
def vraag19(con):
    product = loadProduct(con)
    product_type = loadProductType(con)
    order_details = loadOrderDetail(con)
    product_producttype_merge = pd.merge(product, product_type, on = 'PRODUCT_TYPE_CODE', how = 'inner' )
    product_order_merge = pd.merge(product_producttype_merge, order_details, on = 'PRODUCT_NUMBER', how = 'inner')
    zeven_vijftig_plus_orders = product_order_merge[product_order_merge['QUANTITY'] > 750]
    result = zeven_vijftig_plus_orders[['PRODUCT_NAME', 'PRODUCT_TYPE_EN']].drop_duplicates('PRODUCT_NAME')
    return result
#%% md
# Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 
#%%

def vraag20(con):
    product = loadProduct(con)
    order_details = loadOrderDetail(con)
    product_order_merge = pd.merge(product, order_details, on='PRODUCT_NUMBER', how='inner')
    veertig_korting = product_order_merge[((product_order_merge['UNIT_PRICE'] - product_order_merge['UNIT_SALE_PRICE']) / product_order_merge['UNIT_PRICE']) > 0.4]
    result = veertig_korting[['PRODUCT_NAME']].drop_duplicates()
    return result
#%% md
# Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 
#%%

def vraag21(con):
    order_details = loadOrderDetail(con)
    returned_item = loadReturnedItems(con)
    return_reason = loadReturnedReasons(con)

    odtr_merge = pd.merge(order_details, returned_item, on='ORDER_DETAIL_CODE', how='inner')
    odtr_reason_merge = pd.merge(odtr_merge, return_reason, on='RETURN_REASON_CODE', how='inner')

    odtr_final = odtr_reason_merge[(odtr_reason_merge['RETURN_QUANTITY'] / odtr_reason_merge['QUANTITY']) > 0.9]

    result = odtr_final[['RETURN_DESCRIPTION_EN']].drop_duplicates()

    return result
#%% md
# ## Selecties op meerdere tabellen met functies
#%% md
# Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 
#%%
def vraag22(con):
    product_type = loadProductType(con)
    product = loadProduct(con)
    product_producttype_merge = pd.merge(product_type, product, on='PRODUCT_TYPE_CODE', how='left')
    result = product_producttype_merge.groupby('PRODUCT_TYPE_EN', as_index=False)['PRODUCT_NUMBER'].count().rename(columns={'PRODUCT_NUMBER': 'Aantal_producten'})
    return result

#%% md
# Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 
#%%
def vraag23(con):
    country = loadCountry(con)
    retailer_site = loadRetailerSite(con)

    retailer_site_country_merge = pd.merge(country, retailer_site, on='COUNTRY_CODE', how='left')

    result = retailer_site_country_merge.groupby('COUNTRY', as_index=False)['RETAILER_SITE_CODE'].count().rename(
        columns={'RETAILER_SITE_CODE': 'Aantal_vestigingen'})

    return result
#%% md
# Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen) 
#%%
def vraag24(con):
    product_type = loadProductType(con)
    product = loadProduct(con)
    order_details = loadOrderDetail(con)

    product_producttype_merge = pd.merge(product_type, product, on='PRODUCT_TYPE_CODE', how='right')
    cooking_gear_product = product_producttype_merge[product_producttype_merge['PRODUCT_TYPE_EN'] == 'Cooking Gear']
    last_merger = pd.merge(cooking_gear_product, order_details, on='PRODUCT_NUMBER', how='inner')

    result = last_merger.groupby('PRODUCT_NAME', as_index=False).agg(
        {'QUANTITY': 'sum', 'UNIT_SALE_PRICE': 'mean'}).round({'UNIT_SALE_PRICE': 2}).sort_values('QUANTITY')

    return result

#%% md
# Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 
#%%

def vraag25(con):
    country = loadCountry(con)
    sales_branch = loadSalesBranch(con)
    retailer_site = loadRetailerSite(con)

    country_sales_branch_merge = pd.merge(country, sales_branch, on='COUNTRY_CODE', how='left')
    country_retail_merge = pd.merge(country_sales_branch_merge, retailer_site, on='COUNTRY_CODE', how='inner')

    result = country_retail_merge.groupby(['COUNTRY', 'CITY_x'], as_index=False)['CITY_y'].count().rename(
        columns={'CITY_x': 'verkoper', 'CITY_y': 'klanten'})

    return result





#%% md
# ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops
#%% md
# Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 
#%%

# merger = pd.merge(sales_staff, order_header, on = 'SALES_STAFF_CODE', how = 'outer')
#
# result = merger.loc[merger['ORDER_NUMBER'].isna(), ['FIRST_NAME', 'LAST_NAME']]


def vraag26(con):
    sales_staff = loadSalesStaff(con)
    order_header = loadOrderHeader(con)

    verkopers = order_header['SALES_STAFF_CODE'].dropna().unique()

    result = sales_staff.loc[~sales_staff['SALES_STAFF_CODE'].isin(verkopers), ['FIRST_NAME', 'LAST_NAME']]

    return result

#%% md
# Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 
#%%


def vraag27(con):
    product = loadProduct(con)

    average_margin = product['MARGIN'].mean()
    filtered_df = product[product['MARGIN'] < average_margin]

    result = pd.DataFrame({
        'Aantal producten': [filtered_df.shape[0]],
        'Gemiddelde marge': [filtered_df['MARGIN'].mean().round(2)]
    })

    return result

#%% md
# Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 
#%%


def vraag28(con):
    order_details = loadOrderDetail(con)
    returned_item = loadReturnedItems(con)
    product = loadProduct(con)

    order_vijfhonderd = order_details[order_details['UNIT_SALE_PRICE'] > 500]
    all_returned = returned_item['ORDER_DETAIL_CODE'].dropna().unique()
    never_returned = order_vijfhonderd.loc[
        ~order_vijfhonderd['ORDER_DETAIL_CODE'].isin(all_returned), ['PRODUCT_NUMBER']]

    result = product.loc[product['PRODUCT_NUMBER'].isin(never_returned.squeeze()), ['PRODUCT_NAME']]

    return result

#%% md
# Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
# Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).
#%%

def vraag29(con):
    sales_staff = loadSalesStaff(con)
    medewerkers_data = sales_staff.loc[:, ["LAST_NAME", "POSITION_EN"]]
    for index, medewerker in medewerkers_data.iterrows():
        rol = medewerkers_data.at[index, 'POSITION_EN']
        if "Manager" in rol:
            medewerkers_data.at[index, 'IS-MANAGER'] = "Ja"
        else:
            medewerkers_data.at[index, 'IS-MANAGER'] = "Nee"
    medewerkers_data = medewerkers_data.drop("POSITION_EN", axis=1)
    return medewerkers_data


#%% md
# Met de onderstaande code laat je Python het huidige jaar uitrekenen.
#%%
from datetime import date
date.today().year
#%% md
# Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.
#%%
from datetime import datetime

date_str = '16-8-2013'
date_format = '%d-%m-%Y'
date_obj = datetime.strptime(date_str, date_format)

date_obj.year
#%% md
# Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
# (2 kolommen, 102 rijen) 
#%%

def vraag30(con):
    sales_staff = loadSalesStaff(con)
    medewerkers_data = sales_staff.loc[:, ["LAST_NAME", "DATE_HIRED"]]

    huidig_jaar = date.today().year

    for index, medewerker in medewerkers_data.iterrows():
        date_hired = medewerkers_data.at[index, 'DATE_HIRED']

        date_str = date_hired
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, date_format)

        aantal_jaar_in_dienst = huidig_jaar - date_obj.year


        if aantal_jaar_in_dienst < 25:
            medewerkers_data.at[index, 'DIENSTVERBAND'] = "Kort in dienst"
        else:
            medewerkers_data.at[index, 'DIENSTVERBAND'] = "Lang in dienst"

    medewerkers_data = medewerkers_data.drop("DATE_HIRED", axis=1)
    return medewerkers_data
#%% md

con = makeConnection()
vraag1(con).to_excel("../data/processed/vraag1.xlsx")
vraag2(con).to_excel("../data/processed/vraag2.xlsx")
vraag3(con).to_excel("../data/processed/vraag3.xlsx")
vraag4(con).to_excel("../data/processed/vraag4.xlsx")
vraag5(con).to_excel("../data/processed/vraag5.xlsx")
vraag6(con).to_excel("../data/processed/vraag6.xlsx")
vraag7(con).to_excel("../data/processed/vraag7.xlsx")

vraag14(con).to_excel("../data/processed/vraag14.xlsx")
vraag15(con).to_excel("../data/processed/vraag15.xlsx")
vraag16(con).to_excel("../data/processed/vraag16.xlsx")

vraag18(con).to_excel("../data/processed/vraag18.xlsx")
vraag19(con).to_excel("../data/processed/vraag19.xlsx")
vraag21(con).to_excel("../data/processed/vraag21.xlsx")
vraag22(con).to_excel("../data/processed/vraag22.xlsx")
vraag23(con).to_excel("../data/processed/vraag23.xlsx")
vraag24(con).to_excel("../data/processed/vraag24.xlsx")
vraag25(con).to_excel("../data/processed/vraag25.xlsx")
vraag26(con).to_excel("../data/processed/vraag26.xlsx")
vraag27(con).to_excel("../data/processed/vraag27.xlsx")
vraag28(con).to_excel("../data/processed/vraag28.xlsx")
vraag29(con).to_excel("../data/processed/vraag29.xlsx")
vraag30(con).to_excel("../data/processed/vraag30.xlsx")

