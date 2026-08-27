import streamlit as st
import pandas as pd
import io

# ---------------------------------------------------------------------------
# Dizionario del menù: (dose_7_10, dose_11_14, dose_15_17, dose_adulti) in grammi
# Fonte principale: LARN/SINU - Tabella 4 "Porzioni indicative per l'età evolutiva
# (1-17 anni)". 
# ---------------------------------------------------------------------------
menu = {
    "Latte e derivati": {
        "Latte per colazione": (200, 200, 200, 200),
        "Latte per merenda": (125, 125, 125, 125),
        "Yogurt": (125, 125, 125, 125),
        "Formaggio freschi/Mozzarella": (70, 70, 100, 100),
        "Formaggio per insalata di riso": (20, 20, 30, 30),
        "Formaggio stagionato": (50, 50, 50, 50),
    },
    "Carne, pesce, uova": {
        "Carne rossa o bianca": (80, 100, 100, 100),
        "Carne conservata/Affettato/Insaccato": (50, 50, 50, 50),
        "Pesce/Molluschi/Crostacei fresco/surgelato": (80, 150, 150, 150),
        "Pesce conservato (Tonno)": (50, 50, 50, 50),
        "Uova": (50, 50, 50, 50),
    },
    "Legumi": {
        "Legumi freschi": (90, 120, 150, 150),
        "Legumi secchi": (30, 40, 50, 50),
    },
    "Cereali e derivati, tuberi": {
        "Pasta/Riso/Orzo/Farro/Polenta": (70, 100, 100, 80),
        "Pasta fresca all'uovo": (80, 100, 100, 100),
        "Pasta all'uovo ripiena": (125, 125, 125, 125),
        "Gnocchi": (180, 200, 200, 200),
        "Pasta all'uovo per minestra": (40, 50, 50, 50),
        "Riso per insalate": (50, 60, 60, 60),
        "Pizza": (200, 350, 350, 200),
        "Patate/Patate per purè/Tuberi": (150, 200, 200, 200),
        "Pane": (50, 50, 50, 50),
        "Sostituti del pane (Cracker, Grissini, Taralli)": (40, 40, 50, 30),
        "Prodotti da forno dolci (Brioche, Croissant, Cornetto, Cereali, Fette biscottate)": (40, 40, 50, 30),
    },
    "Verdure e ortaggi": {
        "Verdura cruda/Insalate a foglia": (50, 50, 80, 80),
        "Verdura da cuocere e ortaggi": (150, 200, 200, 200),
    },
    "Frutta": {
        "Frutta fresca": (100, 120, 150, 150),
        "Frutta secca a guscio e semi oleosi": (30, 30, 30, 30),
        "Succhi di frutta": (200, 200, 200, 200),
        "Spremute/Succhi di frutta": (200, 200, 200, 200),
    },
    "Grassi da condimento": {
        "Olio extravergine/Burro": (10, 10, 10, 10)
    },
    "Dolciumi": {
        "Torte": (50, 100, 100, 70),
        "Dolci al cucchiaio/Gelati/Sorbetti": (100, 125, 125, 100),
        "Cioccolato/Biscotti": (40, 30, 30, 30),
        "Zucchero/Miele": (2.5, 5, 5, 5),
        "Nutella/Marmellata": (25, 30, 30, 10)
    },
    "Altro": {
        "Sugo per pasta (Ragù, Pesto, Panna)": (20, 25, 30, 30),
        "Passata di pomodoro per pasta": (50, 60, 70, 70),
        "Tè per colazione": (250, 250, 250, 250),
    }
}

FASCE_BASE = ["Bambine/i (7-10 anni)", "Ragazze/i (11-14 anni)", "Ragazze/i (15-17 anni)", "Adulti/Capi"]
PASTI = ["Colazione", "Merenda", "Pranzo", "Cena"]

st.set_page_config(page_title="Calcolatore dosi menù", page_icon="🍽️", layout="wide")

# ---------------------------------------------------------------------------
# Stato dell'applicazione
# ---------------------------------------------------------------------------
st.session_state.setdefault("menu_items", [])   # elementi del menù del giorno
st.session_state.setdefault("fasce_extra", [])  # fasce d'età personalizzate

st.title("🍽️🐞 Calcolatore dosi menù")
st.write("Calcola le dosi secondo gli standard **SINU**, per un singolo alimento o per un menù completo.")
st.caption(
    "📚 Dosi basate su: [Standard Quantitativi delle Porzioni – SINU]"
    "(https://sinu.it/wp-content/uploads/2025/01/Standard-Quantitativi-delle-Porzioni.pdf)"
)

modalita = st.radio(
    "Cosa vuoi fare?",
    ["🔹 Calcolo rapido di un singolo alimento", "📅 Menù completo (più giorni e più pasti)"],
    horizontal=True,
)

st.divider()

# ===========================================================================
# MODALITÀ 1 — CALCOLO RAPIDO SINGOLO ALIMENTO
# ===========================================================================
if modalita == "🔹 Calcolo rapido di un singolo alimento":
    categoria_s = st.selectbox("Seleziona categoria:", list(menu.keys()), key="cat_singolo")
    cibo_s = st.selectbox("Seleziona alimento:", list(menu[categoria_s].keys()), key="cibo_singolo")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        n_710_s = st.number_input("Bambine/i 7-10:", min_value=0, step=1, key="n_710_singolo")
    with col_s2:
        n_1114_s = st.number_input("Ragazzi/e 11-14:", min_value=0, step=1, key="n_1114_singolo")
    with col_s3:
        n_1517_s = st.number_input("Ragazzi/e 15-17:", min_value=0, step=1, key="n_1517_singolo")
    with col_s4:
        n_adulti_s = st.number_input("Adulti:", min_value=0, step=1, key="n_adulti_singolo")

    if st.button("Calcola", key="calcola_singolo"):
        dose_710, dose_1114, dose_1517, dose_a_s = menu[categoria_s][cibo_s]
        totale_s = (
            n_710_s * dose_710
            + n_1114_s * dose_1114
            + n_1517_s * dose_1517
            + n_adulti_s * dose_a_s
        )
        st.success(f"Totale: {totale_s} g = {totale_s/1000:.2f} kg")
        st.info(
            f"Dose: {dose_710} g (7-10 anni) · {dose_1114} g (11-14 anni) · "
            f"{dose_1517} g (15-17 anni) · {dose_a_s} g (adulto) "
            "(Standard LARN/SINU: Società Italiana di Nutrizione Umana)"
        )

# ===========================================================================
# MODALITÀ 2 — MENÙ COMPLETO
# ===========================================================================
else:

    # -----------------------------------------------------------------
    # 1. PARTECIPANTI E GIORNI
    # -----------------------------------------------------------------
    st.header("1️⃣ Partecipanti e durata")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        n_710 = st.number_input("Bambine/i 7-10:", min_value=0, step=1, value=0)
    with col2:
        n_1114 = st.number_input("Ragazzi/e 11-14:", min_value=0, step=1, value=0)
    with col3:
        n_1517 = st.number_input("Ragazzi/e 15-17:", min_value=0, step=1, value=0)
    with col4:
        n_adulti = st.number_input("Adulti / Capi:", min_value=0, step=1, value=0)
    with col5:
        n_giorni = st.number_input("Numero di giorni (volo estivo):", min_value=1, step=1, value=1)

    with st.expander("➕ Aggiungi fasce d'età personalizzate (es. Lupetti 8-11)"):
        st.caption(
            "Per esigenze diverse dalle 4 fasce standard (es. Lupetti), imposta una "
            "percentuale rispetto alla dose adulto standard per calibrarle tu stessa."
        )
        fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 1])
        with fc1:
            nome_fascia = st.text_input("Nome fascia", key="nome_fascia_input", placeholder="Es. Esploratori/Guide 12-16")
        with fc2:
            numero_fascia = st.number_input("Numero persone", min_value=0, step=1, key="numero_fascia_input")
        with fc3:
            perc_fascia = st.number_input(
                "% dose adulto", min_value=10, max_value=200, value=100, step=5, key="perc_fascia_input"
            )
        with fc4:
            st.write("")
            st.write("")
            if st.button("Aggiungi"):
                if nome_fascia.strip() and numero_fascia > 0:
                    st.session_state.fasce_extra.append(
                        {"nome": nome_fascia.strip(), "numero": numero_fascia, "percentuale": perc_fascia}
                    )
                    st.rerun()
                else:
                    st.warning("Inserisci un nome e un numero di persone maggiore di 0.")

        if st.session_state.fasce_extra:
            for i, f in enumerate(st.session_state.fasce_extra):
                fr1, fr2 = st.columns([5, 1])
                fr1.write(f"**{f['nome']}** — {f['numero']} persone ({f['percentuale']}% dose adulto)")
                if fr2.button("🗑️", key=f"del_fascia_{i}"):
                    st.session_state.fasce_extra.pop(i)
                    st.rerun()

    totale_persone = n_710 + n_1114 + n_1517 + n_adulti + sum(f["numero"] for f in st.session_state.fasce_extra)
    st.caption(f"Totale partecipanti: **{totale_persone}** · Durata: **{n_giorni} giorni**")

    st.divider()

    # ---------------------------------------------------------------------------
    # 2. COSTRUZIONE MENÙ DEL GIORNO
    # ---------------------------------------------------------------------------
    st.header("2️⃣ Costruisci il menù del giorno")

    mc1, mc2, mc3, mc4 = st.columns([2, 2, 3, 1])
    with mc1:
        pasto = st.selectbox("Pasto:", PASTI)
    with mc2:
        categoria = st.selectbox("Categoria:", list(menu.keys()))
    with mc3:
        cibo = st.selectbox("Alimento:", list(menu[categoria].keys()))
    with mc4:
        st.write("")
        st.write("")
        if st.button("➕ Aggiungi al menù"):
            dose_710, dose_1114, dose_1517, dose_a = menu[categoria][cibo]
            st.session_state.menu_items.append(
                {
                    "pasto": pasto,
                    "categoria": categoria,
                    "cibo": cibo,
                    "dose_710": dose_710,
                    "dose_1114": dose_1114,
                    "dose_1517": dose_1517,
                    "dose_a": dose_a,
                }
            )
            st.rerun()

    # Mostra il menù costruito, raggruppato per pasto
    if st.session_state.menu_items:
        st.subheader("Menù del giorno")
        for p in PASTI:
            items_pasto = [
                (i, item) for i, item in enumerate(st.session_state.menu_items) if item["pasto"] == p
            ]
            if items_pasto:
                st.markdown(f"**{p}**")
                for i, item in items_pasto:
                    rc1, rc2 = st.columns([6, 1])
                    rc1.write(
                        f"- {item['cibo']} _{item['categoria']}_ "
                        f"({item['dose_710']} g · 7-10 | {item['dose_1114']} g · 11-14 | "
                        f"{item['dose_1517']} g · 15-17 | {item['dose_a']} g · adulto)"
                    )
                    if rc2.button("🗑️", key=f"del_item_{i}"):
                        st.session_state.menu_items.pop(i)
                        st.rerun()
        if st.button("🧹 Svuota tutto il menù"):
            st.session_state.menu_items = []
            st.rerun()
    else:
        st.info("Nessun alimento ancora aggiunto al menù del giorno.")

    st.divider()

    # ---------------------------------------------------------------------------
    # 3. CALCOLO TOTALI
    # ---------------------------------------------------------------------------
    st.header("3️⃣ Totali e lista della spesa")

    if not st.session_state.menu_items:
        st.warning("Aggiungi almeno un alimento al menù per calcolare i totali.")
    else:
        righe = []
        for item in st.session_state.menu_items:
            dose_710, dose_1114, dose_1517, dose_a = (
                item["dose_710"], item["dose_1114"], item["dose_1517"], item["dose_a"]
            )
            totale_persone_g = (
                n_710 * dose_710 + n_1114 * dose_1114 + n_1517 * dose_1517 + n_adulti * dose_a
            )
            for f in st.session_state.fasce_extra:
                totale_persone_g += f["numero"] * dose_a * (f["percentuale"] / 100)
            totale_g = totale_persone_g * n_giorni
            righe.append(
                {
                    "Pasto": item["pasto"],
                    "Categoria": item["categoria"],
                    "Alimento": item["cibo"],
                    "Totale (g)": round(totale_g, 1),
                    "Totale (kg)": round(totale_g / 1000, 2),
                }
            )

        df = pd.DataFrame(righe)

        # Aggregazione per alimento (nel caso lo stesso cibo compaia in più pasti)
        df_agg = (
            df.groupby(["Categoria", "Alimento"], as_index=False)[["Totale (g)", "Totale (kg)"]]
            .sum()
            .sort_values(["Categoria", "Alimento"])
        )

        tab1, tab2 = st.tabs(["📋 Per pasto", "🛒 Lista della spesa (aggregata)"])
        with tab1:
            st.dataframe(df, use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(df_agg, use_container_width=True, hide_index=True)

        totale_kg_generale = df_agg["Totale (kg)"].sum()
        st.success(f"**Totale generale: {totale_kg_generale:.2f} kg** su {n_giorni} giorni per {totale_persone} persone")

        # -----------------------------------------------------------------
        # Export CSV
        # -----------------------------------------------------------------
        csv_buffer = io.StringIO()
        df_agg.to_csv(csv_buffer, index=False, sep=";", decimal=",")
        st.download_button(
            "⬇️ Scarica lista della spesa (CSV)",
            data=csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="lista_spesa_cambusa.csv",
            mime="text/csv",
        )

        # -----------------------------------------------------------------
        # Export PDF (fpdf2)
        # -----------------------------------------------------------------
        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, "Lista della spesa - Cambusa", ln=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(
                0, 8,
                f"Partecipanti: {n_710} (7-10), {n_1114} (11-14), {n_1517} (15-17), {n_adulti} adulti"
                + (", " + ", ".join(f"{f['numero']} {f['nome']}" for f in st.session_state.fasce_extra)
                   if st.session_state.fasce_extra else "")
                + f" | Giorni: {n_giorni}",
                ln=True,
            )
            pdf.ln(4)

            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(80, 8, "Categoria", border=1)
            pdf.cell(70, 8, "Alimento", border=1)
            pdf.cell(20, 8, "kg", border=1, ln=True)
            pdf.set_font("Helvetica", "", 10)
            for _, r in df_agg.iterrows():
                pdf.cell(80, 8, str(r["Categoria"])[:40], border=1)
                pdf.cell(70, 8, str(r["Alimento"])[:35], border=1)
                pdf.cell(20, 8, f"{r['Totale (kg)']:.2f}", border=1, ln=True)

            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, f"Totale: {totale_kg_generale:.2f} kg", ln=True)

            pdf_bytes = bytes(pdf.output(dest="S"))
            st.download_button(
                "⬇️ Scarica lista della spesa (PDF)",
                data=pdf_bytes,
                file_name="lista_spesa_cambusa.pdf",
                mime="application/pdf",
            )
        except ImportError:
            st.caption("💡 Installa `fpdf2` (`pip install fpdf2`) per abilitare anche l'export in PDF.")

st.divider()
foot_col1, foot_col2 = st.columns(2)
with foot_col1:
    st.markdown("**🐞 Calcolatore dosi menù**")
    st.caption("Realizzato da *Anna Sofia Moro* · © 2026")
    st.caption("📧 Contatti per suggerimenti: [annasofiamoro@gmail.com](mailto:annasofiamoro@gmail.com)")
with foot_col2:
    st.markdown("**📚 Fonti**")
    st.caption(
        "Le dosi sono basate sugli standard nazionali LARN/SINU "
        "(Società Italiana di Nutrizione Umana):"
    )
    st.caption(
        "[Standard Quantitativi delle Porzioni – SINU (PDF)]"
        "(https://sinu.it/wp-content/uploads/2025/01/Standard-Quantitativi-delle-Porzioni.pdf)"
    )