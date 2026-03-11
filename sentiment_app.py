import streamlit as st
from textblob import TextBlob
import pandas as pd

# ── Configuration de la page ──────────────────
st.set_page_config(
    page_title='Analyseur de Sentiments',
    page_icon='🎭',
    layout='centered'
)

# ── Initialisation du session_state ───────────
if 'historique' not in st.session_state:
    st.session_state.historique = []

# ── En-tête ────────────────────────────────────
st.title('🎭 Analyseur de Sentiments IA')
st.write('Entrez un texte et découvrez son sentiment !')
st.divider()

# ── Zone de saisie ─────────────────────────────
texte = st.text_area(
    'Votre texte à analyser :',
    placeholder='Ex: This product is absolutely amazing!',
    height=150
)

# ── Bouton d'action ────────────────────────────
if st.button('🔍 Analyser le sentiment', type='primary'):
    if texte:
        # Analyse
        blob = TextBlob(texte)
        score = blob.sentiment.polarity
        
        # Classer le sentiment
        if score > 0.1:
            sentiment = 'POSITIF'
            emoji = '😊'
        elif score < -0.1:
            sentiment = 'NÉGATIF'
            emoji = '😞'
        else:
            sentiment = 'NEUTRE'
            emoji = '😐'
        
        # Ajouter à l'historique
        st.session_state.historique.append({
            'Texte': texte[:50] + ('...' if len(texte) > 50 else ''),
            'Score': round(score, 2),
            'Sentiment': sentiment
        })
        
        # Garder seulement les 5 dernières analyses
        if len(st.session_state.historique) > 5:
            st.session_state.historique = st.session_state.historique[-5:]
        
        # Afficher les résultats
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric('Score de sentiment', f'{score:.2f}')
        col2.metric('Résultat', f'{emoji} {sentiment}')
        
        # Message coloré
        if score > 0.1:
            st.success(f'Texte POSITIF détecté {emoji}')
        elif score < -0.1:
            st.error(f'Texte NÉGATIF détecté {emoji}')
        else:
            st.info(f'Texte NEUTRE détecté {emoji}')
    else:
        st.warning('Veuillez entrer du texte avant d\'analyser !')

# ── Affichage de l'historique ─────────────────
if st.session_state.historique:
    st.divider()
    st.subheader('📊 Historique des 5 dernières analyses')
    
    # Créer un DataFrame pour l'affichage
    df_historique = pd.DataFrame(st.session_state.historique)
    st.dataframe(df_historique, use_container_width=True)
    
    # Graphique d'évolution des scores
    st.subheader('📈 Évolution des sentiments')
    scores_data = pd.DataFrame({
        'Score': [item['Score'] for item in st.session_state.historique]
    })
    st.line_chart(scores_data)
    
    # Bouton de téléchargement CSV
    csv = df_historique.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='📥 Télécharger l\'historique (CSV)',
        data=csv,
        file_name='historique_sentiments.csv',
        mime='text/csv'
    )
