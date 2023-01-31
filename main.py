from crawlers import main_crawler

PDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx"
GDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/GranDemandaBT.aspx"

main_crawler(PDBT_LINK, "pdbt")
main_crawler(GDBT_LINK, "gdbt")

print("\n================================")
