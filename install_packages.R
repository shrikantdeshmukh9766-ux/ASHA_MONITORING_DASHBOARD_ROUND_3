packages <- c(
"gtsummary",
"flextable",
"officer",
"dplyr",
"readxl"
)

installed <- packages %in% rownames(installed.packages())

if(any(!installed)){
  install.packages(packages[!installed])
}