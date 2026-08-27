import streamlit as st

# Dizionario del menù: (dose_bambini, dose_adulti) in grammi
menu = {
    "Latte e derivati": {
        "Latte per colazione": (200, 200),
        "Latte per merenda": (125, 125),
        "Yogurt": (125, 125),
        "Formaggio freschi/Mozzarella": (70, 100),
        "Formaggio per insalata di riso": (20, 30),
        "Formaggio stagionato": (50, 50),
    },
    "Carne, pesce, uova": {
        "Carne rossa o bianca": (80, 100),
        "Carne conservata/Affettato/Insaccato": (50, 50),
        "Pesce/Molluschi/Crostacei fresco/surgelato": (80, 150),
        "Pesce conservato (Tonno)": (50, 50),
        "Uova": (50, 50),
    },
    "Legumi": {
        "Legumi freschi": (90, 150),
        "Legumi secchi": (30, 50),
    },
    "Cereali e derivati, tuberi": {
        "Pasta/Riso/Orzo/Farro/Polenta": (70, 80),
        "Pasta fresca all'uovo": (80, 100),
        "Pasta all'uovo ripiena/Gnocchi": (125, 125),
        "Pasta all'uovo per minestra": (40, 50),
        "Riso per insalate": (50, 60),
        "Pizza": (200, 200),
        "Patate/Patate per purè/Tuberi": (150, 200),
        "Pane": (50, 50),
        "Sostituti del pane (Cracker, Grissini, Taralli)": (40, 30),
        "Prodotti da forno dolci (Brioche, Croissant, Cornetto, Cereali, Fette biscottate)": (40, 30),
    },
    "Verdure e ortaggi": {
        "Verdura cruda/Insalate a foglia": (50, 80),
        "Verdura da cuocere": (150, 200),
    },
    "Frutta": {
        "Frutta fresca": (100, 150),
        "Frutta secca a guscio e semi oleosi": (30, 30),
        "Succhi di frutta": (200, 200),
        "Spremute/Succhi di frutta": (200, 200),
    },
    "Grassi da condimento": {
        "Olio extravergine/Burro": (10, 10)
    },
    "Dolciumi": {
        "Torte": (50, 70),
        "Dolci al cucchiaio/Gelati/Sorbetti": (100, 100),
        "Cioccolato/Biscotti": (40, 30),
        "Zucchero/Miele": (2.5, 5),
        "Nutella/Marmellata": (25, 10)
    },
    "Altro": {
        "Sugo per pasta (Ragù, Pesto, Panna)": (20, 30),
        "Passata di pomodoro per pasta": (50, 70),
        "Tè per colazione": (250, 250),
    }
}


st.title("🍽️🐞 Calcolatore dosi menù")
st.write("Inserisci il numero di bambine/i e adulti per calcolare le dosi totali secondo gli standard **SINU**.")

categoria = st.selectbox("Seleziona categoria:", list(menu.keys()))
cibo = st.selectbox("Seleziona alimento:", list(menu[categoria].keys()))

bambini = st.number_input("Numero bambine:", min_value=0, step=1)
adulti = st.number_input("Numero adulti:", min_value=0, step=1)

if st.button("Calcola"):
    dose_b, dose_a = menu[categoria][cibo]
    totale = bambini * dose_b + adulti * dose_a
    st.success(f"Totale: {totale} g = {totale/1000:.2f} kg")
    st.info(f"Dose: {dose_b} g/bambina, {dose_a} g/adulto (Standard SINU: Società Italiana di Nutrizione Umana)")

st.markdown("---")
st.markdown(
    """
    © 2025 - Realizzato da *Anna Sofia Moro*    
    📧 Contatti per suggerimenti: [annasofiamoro@gmail.com](mailto:annasofiamoro@gmail.com)
    """
)
