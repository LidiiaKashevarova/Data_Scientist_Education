install.packages("pxweb")
library("remotes")
remotes::install_github("ropengov/pxweb")
library(pxweb)
library(jsonlite)

# Get PXWEB metadata about a table
px_meta <- pxweb_get("https://api.scb.se/OV0104/v1/doris/sv/ssd/START/TK/TK1001/TK1001A/PersBilarDrivMedel")
px_meta

# create a PXWEB query
pxweb_query_list <- list(
  "Region" = c("00"),
  "Drivmedel" = c("100", "110", "120", "130"),
  "Tid" = c(
    
    "2018M01", "2018M02", "2018M03", "2018M04", "2018M05", "2018M06",
    "2018M07", "2018M08", "2018M09", "2018M10", "2018M11", "2018M12",
    "2019M01", "2019M02", "2019M03", "2019M04", "2019M05", "2019M06",
    "2019M07", "2019M08", "2019M09", "2019M10", "2019M11", "2019M12",
    "2020M01", "2020M02", "2020M03", "2020M04", "2020M05", "2020M06",
    "2020M07", "2020M08", "2020M09", "2020M10", "2020M11", "2020M12",
    "2021M01", "2021M02", "2021M03", "2021M04", "2021M05", "2021M06",
    "2021M07", "2021M08", "2021M09", "2021M10", "2021M11", "2021M12",
    "2022M01", "2022M02", "2022M03", "2022M04", "2022M05", "2022M06",
    "2022M07", "2022M08", "2022M09", "2022M10", "2022M11", "2022M12",
    "2023M01", "2023M02", "2023M03", "2023M04", "2023M05", "2023M06",
    "2023M07", "2023M08", "2023M09", "2023M10", "2023M11", "2023M12"
  )
)

pxq <- pxweb_query(pxweb_query_list)
pxq

#Downloading data 
pxd <- pxweb_get(
  "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/TK/TK1001/TK1001A/PersBilarDrivMedel",
  pxq
)
pxd

pxdf <- as.data.frame(pxd, column.name.type = "text", variable.value.type = "text")
head(pxdf)

View(pxdf)

#save the table in Excel
library(openxlsx)
file_path <- "your_file_path/your_filename.xlsx"
write.xlsx(pxdf, file_path)
