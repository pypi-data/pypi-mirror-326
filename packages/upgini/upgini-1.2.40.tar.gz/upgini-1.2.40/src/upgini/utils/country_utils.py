import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype

from upgini.utils.base_search_key_detector import BaseSearchKeyDetector


class CountrySearchKeyConverter:

    def __init__(self, country_col: str):
        self.country_col = country_col

    def convert(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.country_col] = (
            df[self.country_col]
            .astype("string")
            .str.upper()
            .str.replace(r"[^A-Z]", "", regex=True)
            .str.replace("UK", "GB", regex=False)
        )
        return df


class CountrySearchKeyDetector(BaseSearchKeyDetector):
    def _is_search_key_by_name(self, column_name: str) -> bool:
        return "country" in str(column_name).lower()

    def _is_search_key_by_values(self, column: pd.Series) -> bool:
        if not is_string_dtype(column) and not is_object_dtype(column):
            return False

        all_count = len(column)
        is_countries_count = len(column[column.astype("string").str.upper().isin(self.COUNTRY_CODES)])
        return is_countries_count / all_count > 0.1

    @staticmethod
    def convert_country_to_iso_code(df: pd.DataFrame, country_column: str) -> pd.DataFrame:
        if df[country_column].isin(CountrySearchKeyDetector.COUNTRIES.values()).all():
            return df

        df[country_column] = (
            df[country_column]
            .astype("string")
            .str.upper()
            .map(CountrySearchKeyDetector.COUNTRIES)
            .fillna(df[country_column])
        )

        return df

    COUNTRIES = {
        "BOLIVIA": "BO",
        "ALBANIA": "AL",
        "ALGERIA": "DZ",
        "ANDORRA": "AD",
        "ANGOLA": "AO",
        "ARGENTINA": "AR",
        "ARMENIA": "AM",
        "ARUBA": "AW",
        "AUSTRALIA": "AU",
        "AUSTRIA": "AT",
        "AZERBAIJAN": "AZ",
        "BAHAMAS": "BS",
        "BAHRAIN": "BH",
        "BANGLADESH": "BD",
        "BARBADOS": "BB",
        "BELARUS": "BY",
        "BELGIUM": "BE",
        "BELIZE": "BZ",
        "BENIN": "BJ",
        "BERMUDA": "BM",
        "BHUTAN": "BT",
        "BOSNIA AND HERZEGOVINA": "BA",
        "BOTSWANA": "BW",
        "BRAZIL": "BR",
        "BRUNEI DARUSSALAM": "BN",
        "BRUNEI": "BN",
        "BULGARIA": "BG",
        "BURKINA FASO": "BF",
        "BURMA": "MM",
        "BURUNDI": "BI",
        "CABO VERDE": "CV",
        "CAMBODIA": "KH",
        "CAMEROON": "CM",
        "CANADA": "CA",
        "CENTRAL AFRICAN REPUBLIC": "CF",
        "CHAD": "TD",
        "CHILE": "CL",
        "CHINA": "CN",
        "COLOMBIA": "CO",
        "CONGO": "CG",
        "COSTA RICA": "CR",
        "COTE D'IVOIRE": "CI",
        "CROATIA": "HR",
        "CUBA": "CU",
        "CYPRUS": "CY",
        "CZECHIA": "CZ",
        "CZECH REPUBLIC": "CZ",
        "DENMARK": "DK",
        "DJIBOUTI": "DJ",
        "DOMINICA": "DM",
        "DOMINICAN REPUBLIC": "DO",
        "ECUADOR": "EC",
        "EGYPT": "EG",
        "EL SALVADOR": "SV",
        "ENGLAND": "GB",
        "EQUATORIAL GUINEA": "GQ",
        "ERITREA": "ER",
        "ESTONIA": "EE",
        "ESWATINI": "SZ",
        "ETHIOPIA": "ET",
        "FIJI": "FJ",
        "FINLAND": "FI",
        "FRANCE": "FR",
        "GABON": "GA",
        "GAMBIA": "GM",
        "GEORGIA": "GE",
        "GERMANY": "DE",
        "GHANA": "GH",
        "GIBRALTAR": "GI",
        "GREAT BRITAIN": "GB",
        "GREECE": "GR",
        "GRENADA": "GD",
        "GUADELOUPE": "GP",
        "GUATEMALA": "GT",
        "GUINEA": "GN",
        "GUINEA-BISSAU": "GW",
        "GUYANA": "GY",
        "HAITI": "HT",
        "HOLY SEE": "VA",
        "HONDURAS": "HN",
        "HONG KONG": "HK",
        "HUNGARY": "HU",
        "ICELAND": "IS",
        "INDIA": "IN",
        "INDONESIA": "ID",
        "IRAN": "IR",
        "IRAQ": "IQ",
        "IRELAND": "IE",
        "ISRAEL": "IL",
        "ITALY": "IT",
        "JAMAICA": "JM",
        "JAPAN": "JP",
        "JORDAN": "JO",
        "KAZAKHSTAN": "KZ",
        "KENYA": "KE",
        "DPRK": "KP",
        "REPUBLIC OF KOREA": "KR",
        "KUWAIT": "KW",
        "KYRGYZSTAN": "KG",
        "LAOS": "LA",
        "LATVIA": "LV",
        "LEBANON": "LB",
        "LESOTHO": "LS",
        "LIBERIA": "LR",
        "LIBYA": "LY",
        "LIECHTENSTEIN": "LI",
        "LITHUANIA": "LT",
        "LUXEMBOURG": "LU",
        "NORTH MACEDONIA": "MK",
        "MADAGASCAR": "MG",
        "MALAWI": "MW",
        "MALAYSIA": "MY",
        "MALDIVES": "MV",
        "MALI": "ML",
        "MALTA": "MT",
        "MAURITANIA": "MR",
        "MEXICO": "MX",
        "MOLDOVA": "MD",
        "MONACO": "MC",
        "MONGOLIA": "MN",
        "MONTENEGRO": "ME",
        "MOROCCO": "MA",
        "MOZAMBIQUE": "MZ",
        "MYANMAR": "MM",
        "NAMIBIA": "NA",
        "NEPAL": "NP",
        "NETHERLANDS": "NL",
        "NEW ZEALAND": "NZ",
        "NICARAGUA": "NI",
        "NIGER": "NE",
        "NIGERIA": "NG",
        "NORTH KOREA": "KP",
        "NORTHERN IRELAND": "GB",
        "NORWAY": "NO",
        "OMAN": "OM",
        "PAKISTAN": "PK",
        "PALESTINE": "PS",
        "PANAMA": "PA",
        "PAPUA NEW GUINEA": "PG",
        "PARAGUAY": "PY",
        "PERU": "PE",
        "PHILIPPINES": "PH",
        "POLAND": "PL",
        "PORTUGAL": "PT",
        "PUERTO RICO": "PR",
        "QATAR": "QA",
        "ROMANIA": "RO",
        "RUSSIAN FEDERATION": "RU",
        "RUSSIA": "RU",
        "RWANDA": "RW",
        "SAHRAWI ARAB DEMOCRATIC REPUBLIC": "EH",
        "SAN MARINO": "SM",
        "SAUDI ARABIA": "SA",
        "SCOTLAND": "GB",
        "SENEGAL": "SN",
        "SERBIA": "RS",
        "SIERRA LEONE": "SL",
        "SINGAPORE": "SG",
        "SINT MAARTEN": "SX",
        "SLOVAKIA": "SK",
        "SLOVENIA": "SI",
        "SOMALIA": "SO",
        "SOUTH AFRICA": "ZA",
        "SOUTH KOREA": "KR",
        "SOUTH SUDAN": "SS",
        "SPAIN": "ES",
        "SRI LANKA": "LK",
        "SUDAN": "SD",
        "SURINAME": "SR",
        "SWEDEN": "SE",
        "SWITZERLAND": "CH",
        "SYRIA": "SY",
        "TAIWAN": "TW",
        "TAJIKISTAN": "TJ",
        "TANZANIA": "TZ",
        "THAILAND": "TH",
        "TOGO": "TG",
        "TUNISIA": "TN",
        "TURKEY": "TR",
        "TURKMENISTAN": "TM",
        "UGANDA": "UG",
        "UKRAINE": "UA",
        "UNITED ARAB EMIRATES": "AE",
        "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND": "GB",
        "UNITED STATES OF AMERICA": "US",
        "UNITED STATES": "US",
        "USA": "US",
        "URUGUAY": "UY",
        "UZBEKISTAN": "UZ",
        "VANUATU": "VU",
        "VATICAN": "VA",
        "VENEZUELA": "VE",
        "VIETNAM": "VN",
        "WALES": "GB",
        "WESTERN SAHARA": "EH",
        "YEMEN": "YE",
        "ZAMBIA": "ZM",
        "ZIMBABWE": "ZW",
    }

    COUNTRY_CODES = list(COUNTRIES.keys()) + list(set(COUNTRIES.values())) + ["Unknown code"]
