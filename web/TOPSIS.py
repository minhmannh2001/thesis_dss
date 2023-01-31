import pandas as pd

normalized_df = pd.read_csv('./../data/normalized_data.csv')

major_dict = {
    'KHMT': 'Khoa học Máy tính',
    'KTMT': 'Kỹ Thuật Máy tính',
    'CNPM': 'Công nghệ Phần mềm',
    'TTMMT': 'Truyền thông và Mạng máy tính',
    'HTTT': 'Hệ thống Thông tin'
}

def get_best_solution(normalized_df):
    best_solution = {}

    for col in normalized_df.columns:
        if 'id' in col:
            best_solution[col] = 0
        else:
            best_solution[col] = normalized_df[col].max()
    
    return best_solution

def get_worst_solution(normalized_df):
    worst_solution = {}

    for col in normalized_df.columns:
        if 'id' in col:
            worst_solution[col] = 0
        else:
            worst_solution[col] = normalized_df[col].min()
    
    return worst_solution

def search(query_result):

    major_match = []
    for index, row in normalized_df.iterrows():
        if row['related_major'] == major_dict[query_result['major']]:
            major_match.append(1)
        else:
            major_match.append(0)
    
    normalized_df['normalized_major_attribute'] = major_match
    
    type_of_training_match = []
    for index, row in normalized_df.iterrows():
        if str(row['degree']) == 'nan':
            type_of_training_match.append(0)
        else:
            if query_result['type_of_training'] in row['degree']:
                type_of_training_match.append(1)
            else:
                type_of_training_match.append(0)
    normalized_df['normalized_degree_attribute'] = type_of_training_match
    
    # normalized_df.drop(columns=['related_major', 'degree'], inplace=True)

    best_solution = get_best_solution(normalized_df.drop(columns=['related_major', 'degree']))
    # print(best_solution)

    worst_solution = get_worst_solution(normalized_df.drop(columns=['related_major', 'degree']))
    # print(worst_solution)

    rank = []
    for index, row in normalized_df.iterrows():
        distance_from_worst_solution = 0
        distance_from_best_solution = 0
        for col in normalized_df.columns:
            if col not in ['related_major', 'degree']:
                if query_result['age'] == 'no' and col == 'normalized_age_attribute':
                    continue
                if query_result['degree'] == 'no' and col == 'normalized_degrees_point_attribute':
                    continue
                if query_result['award'] == 'no' and col == 'normalized_no_awards_attribute':
                    continue
                else:
                    distance_from_worst_solution += (row[col] - worst_solution[col]) ** 2
                    distance_from_best_solution += (best_solution[col] - row[col]) ** 2
        
        distance_from_worst_solution = distance_from_worst_solution ** 1/2
        distance_from_best_solution = distance_from_best_solution ** 1/2

        rank.append(distance_from_worst_solution / (distance_from_worst_solution + distance_from_best_solution))
    
    normalized_df['rank'] = rank
    sorted_df = normalized_df.sort_values(by=['rank'], ascending=False)
    top_ten = sorted_df.iloc[:10]
    return top_ten['pk_thesis_id'].values
    
