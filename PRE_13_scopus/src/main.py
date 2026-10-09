from .s01_ingest import s01_ingest
from .s02_make_documents_by_year_plot import s01_ingest, s02_make_documents_by_year_plot
from .s03_countries_create import s03_countries_create
from .s04_countries_clean import s04_countries_clean
from .s05_countries_frequency_report import s05_countries_frequency_report
from .s06_countries_frequency_plot import s06_countries_frequency_plot
from .s07_countries_world_map import s07_countries_world_map

def main():

    s01_ingest()
    s02_make_documents_by_year_plot()
    s03_countries_create()
    s04_countries_clean()
    s05_countries_frequency_report()
    s06_countries_frequency_plot()
    s07_countries_world_map()


if __name__ == "__main__":
    main()
