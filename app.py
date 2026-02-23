# --- VIZUÁLNÍ KONTROLA A EDITACE ---
    st.write("### 🔍 Kontrola a editace textů")
    st.info("💡 Tipy: Klikněte do buňky a přepište text. Délka se automaticky přepočítá.")

    # Vytvoření základního DataFrame
    df_to_edit = pd.DataFrame({
        "Typ": ["Nadpis"] * len(h_list) + ["Popis"] * len(d_list),
        "Text": h_list + d_list
    })

    # Zobrazení editoru
    # num_rows="dynamic" umožní uživateli i přidávat/mazat řádky přímo v tabulce
    edited_df = st.data_editor(
        df_to_edit, 
        use_container_width=True,
        num_rows="fixed", # nebo "dynamic" pokud chceš přidávat řádky
        column_config={
            "Typ": st.column_config.TextColumn("Typ", disabled=True), # Typ nechceme měnit
            "Text": st.column_config.TextColumn("Text (editovatelný)", width="large"),
        }
    )

    # Přepočítání finálních seznamů z editovaných dat
    h_final = edited_df[edited_df["Typ"] == "Nadpis"]["Text"].tolist()
    d_final = edited_df[edited_df["Typ"] == "Popis"]["Text"].tolist()

    # --- NÁHLEDY (nyní používají ty editované texty) ---
    st.write("### 👁️ Náhledy s upravenými texty")
    # ... zbytek kódu pro náhledy a export by nyní používal h_final a d_final ...
