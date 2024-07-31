from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
import zipfile

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def plot_df(df):
    # ファイルの読み込み、可視化、解析の処理を実装します。
    xx = df.iloc[:, 0].values
    yy = df.iloc[:, 1].values

    fig = plt.figure(figsize=(4,3), tight_layout=True)
    ax = fig.add_subplot(1,1,1)
    ax.set_title('CSV Plot')
    ax.plot(xx,yy,'ro-',label='Data')
    ax.legend()
    ax.grid()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
 
    return fig

def main():
    st.title("CSV file Viewer")
    
    download_zip_file = st.empty()
    uploaded_files = st.file_uploader("CSV files upload", accept_multiple_files=True, type=["csv"])

    figures = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with NamedTemporaryFile(delete=False) as f:
                fp = Path(f.name)
                fp.write_bytes(uploaded_file.getvalue())
                
                df_ = pd.read_csv(f'{f.name}')

            fp.unlink()
            
            fig = plot_df(df_)
            st.pyplot(fig)
            figures.append((fig, uploaded_file.name))

        def create_zip():
            in_memory = BytesIO()
            with zipfile.ZipFile(in_memory, 'w', zipfile.ZIP_DEFLATED) as zf:
                for fig, name in figures:
                    img_bytes = BytesIO()
                    fig.savefig(img_bytes, format='png')
                    img_bytes.seek(0)
                    zf.writestr(f"{Path(name).stem}.png", img_bytes.read())
            in_memory.seek(0)
            return in_memory

        zip_buffer = create_zip()
        download_zip_file.download_button(
            label="Download (zip)",
            data=zip_buffer,
            file_name='graphs.zip',
            mime='application/zip'
        )


if __name__ == "__main__":
    main()
    
    # streamlit run .\CSV_viewer.py
