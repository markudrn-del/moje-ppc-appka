# --- PŘÍPRAVA DAT S POČÍTADLEM ---
        rows = []
        for i, txt in enumerate(lines):
            typ = "Nadpis" if i < 15 else "Popis"
            limit = 30 if typ == "Nadpis" else 90
            zbyva = limit - len(txt)
            rows.append({"Typ": typ, "Text": txt, "Zbývá": zbyva})
        
        df = pd.DataFrame(rows)
        st.write("### 📝 Editujte v tabulce:")

        # --- INTERAKTIVNÍ EDITOR S POČÍTADLEM ---
        ed_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True, 
            key="ed1",
            column_config={
                "Typ": st.column_config.TextColumn("Typ", disabled=True, width="small"),
                "Text": st.column_config.TextColumn("Text (editujte zde)", width="large"),
                "Zbývá": st.column_config.NumberColumn(
                    "Zbývá", 
                    help="Limit: Nadpis 30 / Popis 90 znaků",
                    disabled=True, # Počítadlo se přepočte po uložení buňky
                    width="small"
                )
            }
        )
        
        # Přepočet textů pro náhledy a export
        h_f = ed_df[ed_df["Typ"] == "Nadpis"]["Text"].tolist()
        d_f = ed_df[ed_df["Typ"] == "Popis"]["Text"].tolist()
