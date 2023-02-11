from crawlers import main_crawler

PDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx"
GDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/GranDemandaBT.aspx"

# Identifiers and xpath definitions:
ids = {
    "year": "ContentPlaceHolder1_Fecha_ddAnio",
    "month": "ContentPlaceHolder1_Fecha2_ddMes",
    "state": "ContentPlaceHolder1_EdoMpoDiv_ddEstado",
    "town": "ContentPlaceHolder1_EdoMpoDiv_ddMunicipio",
    "division": "ContentPlaceHolder1_EdoMpoDiv_ddDivision",
    "table": '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table',
}

main_crawler(PDBT_LINK, "pdbt", ids)
main_crawler(GDBT_LINK, "gdbt", ids)

print("\n================================")
