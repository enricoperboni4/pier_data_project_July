import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Load and Clean the Data
# @st.cache  # This function will be cached
# def load_and_clean_data():
#     # Load
#     data = pd.read_csv('/pier_data_project_July/day_approach_maskedID_timeseries.csv')
    
    
#     return data

# Load your data
data = pd.read_csv('day_approach_maskedID_timeseries.csv')

# Streamlit App
# st.title("Salary Estimates vs. Company Rating by Job Title")
st.markdown('<h1 style="font-size: 24px;">Injury Prediction for Competitive Runners</h1>', unsafe_allow_html=True)

# Funzione per creare categorie e conteggi
def create_km_categories(data, column, bins, labels):
    # Crea una copia del DataFrame per non modificare l'originale
    data_copy = data.copy()
    data_copy[f'{column}_category'] = pd.cut(data_copy[column], bins=bins, labels=labels)
    counts = data_copy[f'{column}_category'].value_counts().reset_index()
    counts.columns = ['km_category', 'count']
    return counts

# Configurazione per tutte le variabili
km_configs = {
    'km_counts': {
        'column': 'total km',
        'bins': [0, 5, 10, 15, 20, float('inf')],
        'labels': ['0-5km', '5-10km', '10-15km', '15-20km', '20+km']
    },
    'km_counts_Z3': {
        'column': 'km Z3-4',
        'bins': [0, 5, 10, 15, 20, float('inf')],
        'labels': ['0-5km', '5-10km', '10-15km', '15-20km', '20+km']
    },
    'km_counts_Z5T1': {
        'column': 'km Z5-T1-T2',
        'bins': [0, 1, 2, 3, 5, float('inf')],
        'labels': ['0-1km', '1-2km', '2-3km', '3-5km', '5+km']
    },
    'km_counts_sprinting': {
        'column': 'km sprinting',
        'bins': [0, 1, 2, 3, 5, float('inf')],
        'labels': ['0-1km', '1-2km', '2-3km', '3-5km', '5+km']
    }
}

# Crea tutti i conteggi in un loop
km_data = {}
for name, config in km_configs.items():
    km_data[name] = create_km_categories(
        data, config['column'], config['bins'], config['labels']
    )


titles = {
    'km_counts': 'Total km Distribution',
    'km_counts_Z3': 'km Z3-4 Distribution', 
    'km_counts_Z5T1': 'km Z5-T1-T2 Distribution',
    'km_counts_sprinting': 'km sprinting Distribution'
}

# Create dropdown
data_selector = st.selectbox("Select Dataset", options=list(km_data.keys()))

# Visualizzazione unificata
st.subheader(titles[data_selector])
fig = px.bar(km_data[data_selector], x='km_category', y='count', title=titles[data_selector])
st.plotly_chart(fig)

st.markdown("---")
st.header("Analisi Carico di Lavoro vs Indicatori di Benessere")

# Identifica colonne ID atleta e indicatori di infortunio
athlete_cols = [col for col in data.columns if 'id' in col.lower()]
injury_indicators = [col for col in data.columns if any(keyword in col.lower() 
                    for keyword in ['injury', 'pain', 'wellness', 'fatigue', 'recovery', 'perceived'])]

if athlete_cols and injury_indicators:
    athlete_col = athlete_cols[0]
    st.info(f"Trovate {len(injury_indicators)} variabili correlate al benessere/infortuni")
    
    # Selettore per l'indicatore da analizzare
    selected_indicator = st.selectbox(
        "Seleziona indicatore di benessere:",
        options=injury_indicators,
        index=0
    )
    
    # Layout a 2 colonne per i grafici
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Top atleti per km totali
        st.subheader("Top 20 Atleti per Km Totali")
        athlete_km_totals = data.groupby(athlete_col)['total km'].sum().sort_values(ascending=False).head(20)
        
        fig1 = px.bar(
            x=range(len(athlete_km_totals)),
            y=athlete_km_totals.values,
            labels={'x': 'Atleti (ordinati per km)', 'y': 'Km Totali'},
            title='Distribuzione Km per Atleta'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 2. Scatter plot: km vs indicatore selezionato
        st.subheader(f"Km vs {selected_indicator}")
        fig2 = px.scatter(
            data, 
            x='total km', 
            y=selected_indicator,
            opacity=0.6,
            title=f'Relazione tra Km e {selected_indicator}'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Seconda riga di grafici
    col3, col4 = st.columns(2)
    
    with col3:
        # 3. Box plot: distribuzione km per quartili dell'indicatore
        st.subheader(f"Distribuzione Km per Livelli di {selected_indicator}")
        try:
            # Pulisci i dati prima di creare quartili
            data_temp = data.copy()
            
            # Rimuovi valori NaN
            clean_data = data_temp[selected_indicator].dropna()
            
            # Verifica se ci sono abbastanza valori unici
            unique_values = clean_data.nunique()
            
            if unique_values < 4:
                # Se meno di 4 valori unici, usa cut invece di qcut
                st.info(f"Troppo pochi valori unici ({unique_values}) per quartili. Usando intervalli fissi.")
                data_temp['indicator_quartile'] = pd.cut(
                    data_temp[selected_indicator], 
                    bins=min(unique_values, 4),
                    labels=[f'Gruppo {i+1}' for i in range(min(unique_values, 4))]
                )
            else:
                # Prova qcut con gestione duplicati
                data_temp['indicator_quartile'] = pd.qcut(
                    data_temp[selected_indicator], 
                    q=4, 
                    labels=['Q1 (Basso)', 'Q2', 'Q3', 'Q4 (Alto)'], 
                    duplicates='drop'
                )
            
            # Rimuovi righe con quartili NaN
            data_temp = data_temp.dropna(subset=['indicator_quartile'])
            
            if len(data_temp) > 0:
                fig3 = px.box(
                    data_temp, 
                    x='indicator_quartile', 
                    y='total km',
                    title=f'Distribuzione Km per Livelli di {selected_indicator}'
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                raise ValueError("Nessun dato valido dopo la creazione dei quartili")
            
        except Exception as e:
            # Fallback: istogramma semplice
            st.warning(f"Impossibile creare quartili per {selected_indicator}. Errore: {str(e)}")
            fig3 = px.histogram(
                data, 
                x='total km', 
                nbins=30,
                title='Distribuzione Km Totali'
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # 4. Scatter plot tra due indicatori (se disponibili)
        if len(injury_indicators) > 1:
            st.subheader("Relazione tra Indicatori")
            second_indicator = st.selectbox(
                "Secondo indicatore:",
                options=[ind for ind in injury_indicators if ind != selected_indicator],
                index=0
            )
            
            fig4 = px.scatter(
                data,
                x=selected_indicator,
                y=second_indicator,
                color='total km',
                opacity=0.7,
                title=f'{selected_indicator} vs {second_indicator}',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            # Alternativa: distribuzione dell'indicatore selezionato
            st.subheader(f"Distribuzione {selected_indicator}")
            fig4 = px.histogram(
                data, 
                x=selected_indicator, 
                nbins=30,  # Cambiato da 'bins' a 'nbins'
                title=f'Distribuzione {selected_indicator}'
            )
            st.plotly_chart(fig4, use_container_width=True)

    # Sezione correlazioni
    st.subheader("Correlazioni con Total Km")
    correlations = {}
    for indicator in injury_indicators[:5]:  # Prime 5 per non sovraccaricare
        corr = data['total km'].corr(data[indicator])
        correlations[indicator] = corr
    
    # Mostra correlazioni in una tabella
    corr_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['Correlazione'])
    corr_df = corr_df.sort_values('Correlazione', key=abs, ascending=False)
    st.dataframe(corr_df.style.format({'Correlazione': '{:.3f}'}))
    
else:
    st.warning("⚠️ Impossibile identificare colonne ID atleta o indicatori di benessere nel dataset")
    
    # Analisi generale alternativa
    st.subheader("Analisi Generale del Carico di Lavoro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuzione generale km
        fig_general1 = px.histogram(
            data, 
            x='total km', 
            nbins=30,  # Cambiato da 'bins' a 'nbins'
            title='Distribuzione Km Totali'
        )
        st.plotly_chart(fig_general1, use_container_width=True)
    
    with col2:
        # Distribuzione sessioni
        fig_general2 = px.histogram(
            data, 
            x='nr. sessions', 
            nbins=10,  # Cambiato da 'bins' a 'nbins'
            title='Distribuzione Numero Sessioni'
        )
        st.plotly_chart(fig_general2, use_container_width=True)


