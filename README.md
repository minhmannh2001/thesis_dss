# thesis_dss
A decision support system helps students select the thesis and the teacher which are proper for them.

We are using TOPSIS model to create a DSS system

File Structure
- data: collected data about teachers and thesises
    - sqlite/thesis-DSS.db: database consists of 2 tables: teacher and thesis # we will remove it
    - Cơ sở dữ liệu - Đồ án - *.csv: raw collected data from university website
    - Cơ sở dữ liệu - Giáo viên - *,csv: raw collected data from university website
    - teachers.csv: prepocessed data about teachers after running file scripts/1_normalization.ipynb
    - thesises.csv: prepocessed data about thesises after running file scripts/1_normalization.ipynb
    - normalized_data.csv: normalized data after running file scripts/0_preprocess.ipynb
- scripts: prepocess and normalize tasks
    - 0_preprocess.ipynb
    - 1_normalization.ipynb
- web: Flask apps for demo purpose
    - templates: html template for website
    - main.py: used for running website
    - TOPSIS.py: TOPSIS model