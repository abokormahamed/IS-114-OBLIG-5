import pandas as pd
from kgmodel import Foresatt, Barn, Soknad, Barnehage

# Globale DataFrames
forelder = pd.DataFrame()
barnehage = pd.DataFrame()
barn = pd.DataFrame()
soknad = pd.DataFrame()

def initialize_globals():
    """Initialiser globale DataFrames fra Excel."""
    global forelder, barnehage, barn, soknad
    forelder = pd.read_excel('kgdata.xlsx', sheet_name='foresatt')
    barnehage = pd.read_excel('kgdata.xlsx', sheet_name='barnehage')
    barn = pd.read_excel('kgdata.xlsx', sheet_name='barn')
    soknad = pd.read_excel('kgdata.xlsx', sheet_name='soknad')

def form_to_object_soknad(sd):
    """Konverterer formdata fra søknadsskjema til et Soknad-objekt."""
    try:
        foresatt_1 = Foresatt(0, sd.get('navn_forelder_1', '').strip(), sd.get('adresse_forelder_1', '').strip(),
                              sd.get('tlf_nr_forelder_1', '').strip(), sd.get('personnummer_forelder_1', '').strip())
        foresatt_2 = Foresatt(0, sd.get('navn_forelder_2', '').strip(), sd.get('adresse_forelder_2', '').strip(),
                              sd.get('tlf_nr_forelder_2', '').strip(), sd.get('personnummer_forelder_2', '').strip())
        barn_1 = Barn(0, sd.get('personnummer_barnet_1', '').strip())
        soknad = Soknad(0, foresatt_1, foresatt_2, barn_1,
                        sd.get('fortrinnsrett_barnevern', ''), sd.get('fortrinnsrett_sykdom_i_familien', ''),
                        sd.get('fortrinnsrett_sykdome_paa_barnet', ''), sd.get('fortrinssrett_annet', ''),
                        sd.get('liste_over_barnehager_prioritert_5', ''), sd.get('har_sosken_som_gaar_i_barnehagen', ''),
                        sd.get('tidspunkt_for_oppstart', ''), sd.get('brutto_inntekt_husholdning', ''))
        return soknad
    except Exception as e:
        print(f"Feil i form_to_object_soknad: {e}")
        raise

def insert_soknad(s):
    """Legger inn en ny søknad i soknad-DataFrame."""
    global soknad
    try:
        new_id = 1 if soknad.empty else soknad['sok_id'].max() + 1
        new_row = pd.DataFrame([[
            new_id, s.foresatt_1.foresatt_id, s.foresatt_2.foresatt_id, s.barn_1.barn_id, s.fr_barnevern,
            s.fr_sykd_familie, s.fr_sykd_barn, s.fr_annet, s.barnehager_prioritert, s.sosken__i_barnehagen,
            s.tidspunkt_oppstart, s.brutto_inntekt
        ]], columns=soknad.columns)
        soknad = pd.concat([soknad, new_row], ignore_index=True)
        return soknad
    except Exception as e:
        print(f"Feil i insert_soknad: {e}")
        raise

def select_alle_barnehager():
    """Henter alle barnehager fra datakilden og returnerer en liste av Barnehage-objekter."""
    return barnehage.apply(lambda r: Barnehage(r['barnehage_id'], r['barnehage_navn'],
                                               r['barnehage_antall_plasser'], r['barnehage_ledige_plasser']),
                           axis=1).to_list()

def commit_all():
    """Lagre alle endringer i DataFrames til Excel-filen."""
    try:
        with pd.ExcelWriter('kgdata.xlsx', mode='a', if_sheet_exists='replace') as writer:
            forelder.to_excel(writer, sheet_name='foresatt', index=False)
            barnehage.to_excel(writer, sheet_name='barnehage', index=False)
            barn.to_excel(writer, sheet_name='barn', index=False)
            soknad.to_excel(writer, sheet_name='soknad', index=False)
        print("Alle data er lagret til 'kgdata.xlsx'.")
    except Exception as e:
        print(f"Feil ved lagring til Excel: {e}")
        raise
