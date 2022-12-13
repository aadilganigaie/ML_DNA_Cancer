import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt

pipe_lr = joblib.load(open(r'modelpath', 'rb'))

#predictmentalhealth
def predict_mhealth(docs):
    results = pipe_lr.predict([docs])
    return results[0]

def get_predictions_proba(docs):
    results = pipe_lr.predict_proba([docs])
    return results

def main():
    st.title("DNA Cancer Detection")
    menu = ['Home', 'Monitor', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('ML Cancer Detection')

        with st.form(key = 'Cancer_clf'):
            raw_text = st.text_area('Enter DNA Sequence')
            submit_text = st.form_submit_button(label = 'Predict')

        if submit_text:
            col1, col2 = st.beta_columns(2)

            prediction = predict_mhealth(raw_text)
            probability = get_predictions_proba(raw_text)


            with col1:
                st.success('Original Text')
                st.write(raw_text)

                st.success("prediction")
                st.write(prediction)
                st.write('Confidence: {}'.format(np.max(probability)))
            with col2:
                st.success('Prediction Probability')

                #st.write(probability)
                proba_df = pd.DataFrame(probability, columns = pipe_lr.classes_)
                #st.write(proba_df.T)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ['Detection', 'Probability']

                fig = alt.Chart(proba_df_clean).mark_bar().encode(x = 'Detection', y = 'Probability', color = 'Detection')
                st.altair_chart(fig, use_container_width = True)


    elif choice == 'Monitor':
        st.subheader('Monitor App')

    else:
        st.subheader('About')





if __name__ == '__main__':
    main()
