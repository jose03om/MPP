import time
import streamlit as st
import os
from analysis import analyze_data  # Certifique-se de que o módulo 'analysis' está no caminho correto
import plotly.express as px
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

class FolderChangeHandler(FileSystemEventHandler):
    def __init__(self, update_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_func = update_func

    def on_any_event(self, event):
        self.update_func()

def display_urgencia_results(urgencia_folder):
    if os.path.exists(urgencia_folder):
        st.markdown("""
            <style>
            .blinking {
                animation: blinkingText 1.2s infinite;
            }
            @keyframes blinkingText {
                0% { color: red; }
                49% { color: red; }
                60% { color: transparent; }
                99% { color:transparent; }
                100% { color: red; }
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("<h2>Urgência <span class='blinking'>⚠️</span></h2>", unsafe_allow_html=True)
        for municipality in os.listdir(urgencia_folder):
            municipality_path = os.path.join(urgencia_folder, municipality)
            if os.path.isdir(municipality_path):
                st.markdown(f"<div style='background-color:#E15658;color:white;padding:5px;border-radius:5px; width:300px; margin-bottom: 10px;'> {municipality}</div>", unsafe_allow_html=True)
                with st.expander(f"{municipality}"):
                    for memorando in os.listdir(municipality_path):
                        memorando_path = os.path.join(municipality_path, memorando)
                        if os.path.isdir(memorando_path):
                            num_files = len([f for f in os.listdir(memorando_path) if os.path.isfile(os.path.join(memorando_path, f))])
                            st.write(f"{memorando} ({num_files} arquivos)")
    else:
        st.write("No data available for URGÊNCIA.")

def display_monthly_results(month_folder, selected_month):
    if os.path.exists(month_folder):
        st.header(f"Analysis Results for {selected_month}")
        st.write(f"Analyzing all data for {selected_month}...")
        results = analyze_data(month_folder)
        
        # Group results by municipality
        grouped_results = {}
        file_counts = {}
        total_files = 0
        for folder, contents in results.items():
            date = os.path.basename(folder)
            for subfolder in contents["dirs"]:
                municipality = subfolder.split(" - ")[0]
                if municipality not in grouped_results:
                    grouped_results[municipality] = []
                    file_counts[municipality] = 0
                grouped_results[municipality].append((date, subfolder))
                subfolder_path = os.path.join(month_folder, folder, subfolder)
                num_files = len([f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))])
                file_counts[municipality] += num_files
                total_files += num_files
        
        # Display results
        if grouped_results:
            for municipality, memorandos in sorted(grouped_results.items()):
                with st.expander(f"{municipality} ({len(memorandos)} pastas)"):
                    for date, memorando in memorandos:
                        memorando_path = os.path.join(month_folder, date, memorando)
                        num_files = len([f for f in os.listdir(memorando_path) if os.path.isfile(os.path.join(memorando_path, f))])
                        st.write(f"{date} - {memorando} ({num_files} arquivos)")
        else:
            st.write("No data available for the selected month.")
        
        return file_counts, total_files
    else:
        st.write("No data available for the selected month.")
        return {}, 0

def main():
    st.title("Data Analysis Dashboard")
    
    # Create a two-column layout
    col1, col2 = st.columns(2)
    
    with col2:
        urgencia_folder = os.path.join("i:\\PROCESSOS VIA EMAIL\\1°FILA DE CHEGADA\\URGÊNCIA")
        st_autorefresh(interval=2000, key="datarefresh")
        display_urgencia_results(urgencia_folder)
    
    with col1:
        st.header("Monthly Data Analysis")
        
        # Create buttons for each month in a single row
        months = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", 
                  "MAIO", "JUNHO", "JULHO", "AGOSTO", 
                  "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
        
        if 'selected_month' not in st.session_state:
            st.session_state.selected_month = None
        
        for i in range(0, len(months), 6):
            cols = st.columns(6)
            for idx, (col, month) in enumerate(zip(cols, months[i:i+6])):
                if col.button(month, key=f"{month}_{i}_{idx}"):
                    st.session_state.selected_month = month
    
    if st.session_state.selected_month:
        with col2:
            # Get the list of days in the selected month
            month_folder = os.path.join("i:\\PROCESSOS VIA EMAIL\\1°FILA DE CHEGADA", st.session_state.selected_month)
            file_counts, total_files = display_monthly_results(month_folder, st.session_state.selected_month)
        
        # Create interactive bar chart in col1
        with col1:
            st.header("Grafico Geral de Processos por Mês")
            if file_counts and any(file_counts.values()):
                labels = sorted(file_counts.keys())
                sizes = [file_counts[label] for label in labels]
                fig = px.bar(
                    x=labels, 
                    y=sizes, 
                    title='Distribuições de Processos por Município', 
                    labels={'x': 'Município'}, 
                    color=labels, 
                    text=sizes,
                    color_discrete_sequence=px.colors.qualitative.Bold  # Define a sequência de cores
                )
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
                
                # Display the chart in full width
                st.plotly_chart(fig, use_container_width=True)
                
                # Display total number of files
                st.write(f"Total de arquivos: {total_files}")
            else:
                st.write("No data available for the selected month.")
    else:
        st.write("No data available for the selected month.")

if __name__ == "__main__":
    main()