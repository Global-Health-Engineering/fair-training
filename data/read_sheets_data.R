# header ------------------------------------------------------------------

# This script accesses the tables stored as Google Sheets which contain data
# for the proposal. Google Sheets are edited manually and data is then read
# from here and stored locally as CSVs.

# library -------------------------------------------------------------------

library(googlesheets4)
library(readr)
library(dplyr)

# script ------------------------------------------------------------------

# gs4_auth()

## tbl-01-work-packages --------------------------------------------------

## WP, Name, Goal, Lead

read_sheet("1cxn0YMK4CYDUjlLuautg4aBNzBE-dArvBAMF1jnJXu8") |>
  write_csv(here::here("data/tables/tbl-01-work-packages.csv"), na = "")

## tbl-02-wp-activities-research-questions ----------------------------------

## WP, Name, Project Activity, Research Question, Lead, Q1, Q2, Q3, Q4

read_sheet("14DwpPjRWP73SPWMIgO_EpxFua7xIOAcl6iq3-ivrgK0") |>
  write_csv(here::here("data/tables/tbl-02-wp-activities-research-questions.csv"), na = "")

## tbl-03-budget-justification ----------------------------------------------

## Cost Category, Cost Sub Category, Cost Item, Description, Cost, Source,
## Institution, Justification

read_sheet("1PISLgDOJJ26eeb6m4VUouVEGL-052HWvdFXA90rJp4o") |>
  write_csv(here::here("data/tables/tbl-03-budget-justification.csv"), na = "")

## tbl-04-budget-template ---------------------------------------------------

## the official budget table; copy/paste the final figures into the DOCX

read_sheet("1N0_GrO5iZWtQPhYfl5Je35BtgQvAOmehRL6tSTZg5lw") |>
  write_csv(here::here("data/tables/tbl-04-budget-template.csv"), na = "")

