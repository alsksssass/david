"""
Spaceship Titanic 데이터 분석 스크립트
Kaggle Spaceship Titanic 데이터셋을 분석합니다.
"""

import csv
import statistics
from collections import Counter, defaultdict


def read_csv_file(file_path):
    """
    CSV 파일을 읽어서 딕셔너리 리스트로 반환합니다.
    
    Args:
        file_path (str): 읽을 CSV 파일 경로
        
    Returns:
        list: 딕셔너리 리스트 (각 행이 딕셔너리)
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def merge_data(train_data, test_data):
    """
    train 데이터와 test 데이터를 병합합니다.
    test 데이터에는 Transported 컬럼이 없으므로 None으로 설정합니다.
    
    Args:
        train_data (list): train 데이터
        test_data (list): test 데이터
        
    Returns:
        list: 병합된 데이터
    """
    merged_data = []
    
    # train 데이터 추가
    for row in train_data:
        merged_data.append(row)
    
    # test 데이터 추가 (Transported 컬럼이 없으므로 None 추가)
    for row in test_data:
        row_copy = row.copy()
        row_copy['Transported'] = None
        merged_data.append(row_copy)
    
    return merged_data


def get_total_count(data):
    """
    전체 데이터 수량을 반환합니다.
    
    Args:
        data (list): 데이터 리스트
        
    Returns:
        int: 전체 데이터 수량
    """
    return len(data)


def convert_to_numeric(value):
    """
    문자열 값을 숫자로 변환합니다.
    빈 문자열이나 None인 경우 None을 반환합니다.
    
    Args:
        value: 변환할 값
        
    Returns:
        float or None: 변환된 숫자 또는 None
    """
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def convert_to_bool(value):
    """
    문자열 값을 불린으로 변환합니다.
    
    Args:
        value: 변환할 값
        
    Returns:
        bool or None: 변환된 불린 또는 None
    """
    if value is None or value == '':
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
    return None


def calculate_correlation_for_numeric(data, feature_name, target_name):
    """
    수치형 변수와 Transported 간의 상관계수를 계산합니다.
    
    Args:
        data (list): 데이터 리스트
        feature_name (str): 분석할 특성 이름
        target_name (str): 타겟 변수 이름
        
    Returns:
        float: 상관계수 (또는 None)
    """
    feature_values = []
    target_values = []
    
    for row in data:
        feature_val = convert_to_numeric(row.get(feature_name))
        target_val = convert_to_bool(row.get(target_name))
        
        if feature_val is not None and target_val is not None:
            feature_values.append(feature_val)
            target_values.append(1 if target_val else 0)
    
    if len(feature_values) < 2:
        return None
    
    # 피어슨 상관계수 계산
    n = len(feature_values)
    mean_feature = statistics.mean(feature_values)
    mean_target = statistics.mean(target_values)
    
    numerator = sum((feature_values[i] - mean_feature) * 
                    (target_values[i] - mean_target) 
                    for i in range(n))
    
    variance_feature = sum((x - mean_feature) ** 2 for x in feature_values)
    variance_target = sum((x - mean_target) ** 2 for x in target_values)
    
    denominator = (variance_feature * variance_target) ** 0.5
    
    if denominator == 0:
        return None
    
    correlation = numerator / denominator
    return correlation


def calculate_categorical_correlation(data, feature_name, target_name):
    """
    범주형 변수와 Transported 간의 관련성을 계산합니다.
    카이제곱 통계를 기반으로 합니다.
    
    Args:
        data (list): 데이터 리스트
        feature_name (str): 분석할 특성 이름
        target_name (str): 타겟 변수 이름
        
    Returns:
        float: 관련성 점수 (0~1 사이)
    """
    contingency_table = defaultdict(lambda: {'True': 0, 'False': 0})
    total_with_target = 0
    
    for row in data:
        feature_val = row.get(feature_name)
        target_val = row.get(target_name)
        
        if feature_val is not None and feature_val != '' and target_val is not None:
            target_str = str(target_val)
            if target_str in ['True', 'False']:
                contingency_table[feature_val][target_str] += 1
                total_with_target += 1
    
    if total_with_target == 0:
        return None
    
    # 간단한 관련성 측정: 각 카테고리별 Transported 비율의 분산
    transport_rates = []
    for category, counts in contingency_table.items():
        total = counts['True'] + counts['False']
        if total > 0:
            rate = counts['True'] / total
            transport_rates.append(rate)
    
    if len(transport_rates) < 2:
        return None
    
    # 비율의 표준편차가 클수록 관련성이 높음
    try:
        std_dev = statistics.stdev(transport_rates)
        # 0~1 사이로 정규화 (최대값 0.5로 가정)
        normalized_score = min(std_dev / 0.5, 1.0)
        return normalized_score
    except statistics.StatisticsError:
        return None


def find_most_correlated_feature(data):
    """
    Transported와 가장 관련성이 높은 항목을 찾습니다.
    
    Args:
        data (list): 데이터 리스트
        
    Returns:
        tuple: (특성 이름, 상관계수/관련성 점수)
    """
    numeric_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    categorical_features = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']
    
    correlations = {}
    
    # 수치형 변수 분석
    for feature in numeric_features:
        corr = calculate_correlation_for_numeric(data, feature, 'Transported')
        if corr is not None:
            correlations[feature] = abs(corr)
    
    # 범주형 변수 분석
    for feature in categorical_features:
        corr = calculate_categorical_correlation(data, feature, 'Transported')
        if corr is not None:
            correlations[feature] = corr
    
    if not correlations:
        return None, None
    
    # 가장 높은 상관계수를 가진 특성 찾기
    max_feature = max(correlations.items(), key=lambda x: x[1])
    return max_feature[0], max_feature[1]


def categorize_age(age_value):
    """
    나이를 연령대별로 분류합니다.
    
    Args:
        age_value: 나이 값 (문자열 또는 숫자)
        
    Returns:
        str: 연령대 ('10대', '20대', '30대', '40대', '50대', '60대', '70대', '기타')
    """
    age = convert_to_numeric(age_value)
    if age is None:
        return '기타'
    
    if 10 <= age < 20:
        return '10대'
    elif 20 <= age < 30:
        return '20대'
    elif 30 <= age < 40:
        return '30대'
    elif 40 <= age < 50:
        return '40대'
    elif 50 <= age < 60:
        return '50대'
    elif 60 <= age < 70:
        return '60대'
    elif 70 <= age < 80:
        return '70대'
    else:
        return '기타'


def visualize_transported_by_age(data):
    """
    연령대별 Transported 여부를 시각화합니다.
    
    Args:
        data (list): 데이터 리스트
    """
    try:
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings('ignore')
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'AppleGothic'
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print('matplotlib이 설치되어 있지 않습니다.')
        return
    
    age_groups = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    transported_counts = {age: {'True': 0, 'False': 0} for age in age_groups}
    
    for row in data:
        age_group = categorize_age(row.get('Age'))
        transported = row.get('Transported')
        
        if age_group in age_groups and transported is not None:
            transported_str = str(transported)
            if transported_str in ['True', 'False']:
                transported_counts[age_group][transported_str] += 1
    
    # 그래프 데이터 준비
    transported_true = [transported_counts[age]['True'] for age in age_groups]
    transported_false = [transported_counts[age]['False'] for age in age_groups]
    
    # 그래프 그리기
    x = range(len(age_groups))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar([i - width/2 for i in x], transported_true, width, 
                    label='Transported=True', color='#2ecc71')
    bars2 = ax.bar([i + width/2 for i in x], transported_false, width, 
                    label='Transported=False', color='#e74c3c')
    
    ax.set_xlabel('연령대', fontsize=12)
    ax.set_ylabel('인원 수', fontsize=12)
    ax.set_title('연령대별 Transported 여부', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(age_groups)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('transported_by_age.png', dpi=300, bbox_inches='tight')
    print('그래프가 "transported_by_age.png"로 저장되었습니다.')
    plt.close()


def visualize_age_distribution_by_destination(data):
    """
    Destination별 연령대 분포를 시각화합니다.
    
    Args:
        data (list): 데이터 리스트
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import warnings
        warnings.filterwarnings('ignore')
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'AppleGothic'
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print('matplotlib이 설치되어 있지 않습니다.')
        return
    
    # Destination별 연령대 분포 수집
    destination_age_groups = defaultdict(lambda: Counter())
    
    for row in data:
        destination = row.get('Destination')
        age_group = categorize_age(row.get('Age'))
        
        if destination is not None and destination != '' and age_group != '기타':
            destination_age_groups[destination][age_group] += 1
    
    if not destination_age_groups:
        print('시각화할 데이터가 없습니다.')
        return
    
    # 그래프 그리기
    destinations = sorted(destination_age_groups.keys())
    age_groups = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(destinations))
    width = 0.12
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
    
    for i, age_group in enumerate(age_groups):
        values = [destination_age_groups[dest][age_group] for dest in destinations]
        ax.bar(x + i * width, values, width, label=age_group, color=colors[i % len(colors)])
    
    ax.set_xlabel('Destination', fontsize=12)
    ax.set_ylabel('인원 수', fontsize=12)
    ax.set_title('Destination별 연령대 분포', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 3)
    ax.set_xticklabels(destinations, rotation=15, ha='right')
    ax.legend(title='연령대', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('age_distribution_by_destination.png', dpi=300, bbox_inches='tight')
    print('그래프가 "age_distribution_by_destination.png"로 저장되었습니다.')
    plt.close()


def main():
    """메인 실행 함수"""
    print('=' * 60)
    print('Spaceship Titanic 데이터 분석 시작')
    print('=' * 60)
    
    # Phase 1: CSV 파일 읽기
    print('\n[Phase 1] CSV 파일 읽기 중...')
    train_data = read_csv_file('train.csv')
    test_data = read_csv_file('test.csv')
    print(f'Train 데이터: {len(train_data)}개 행')
    print(f'Test 데이터: {len(test_data)}개 행')
    print(f'Train 데이터 샘플 (첫 번째 행): {train_data[0] if train_data else "없음"}')
    
    # Phase 2: 데이터 병합
    print('\n[Phase 2] 데이터 병합 중...')
    merged_data = merge_data(train_data, test_data)
    print(f'병합된 데이터: {len(merged_data)}개 행')
    
    # Phase 3: 전체 데이터 수량 파악
    print('\n[Phase 3] 전체 데이터 수량 파악')
    total_count = get_total_count(merged_data)
    print(f'전체 데이터 수량: {total_count}개')
    
    # Phase 4: Transported와 가장 관련성 높은 항목 찾기
    print('\n[Phase 4] Transported와 가장 관련성 높은 항목 찾기...')
    most_correlated_feature, correlation_score = find_most_correlated_feature(merged_data)
    if most_correlated_feature:
        print(f'가장 관련성이 높은 항목: {most_correlated_feature}')
        print(f'관련성 점수: {correlation_score:.4f}')
    else:
        print('관련성 높은 항목을 찾을 수 없습니다.')
    
    # Phase 5: 연령대별 Transported 시각화
    print('\n[Phase 5] 연령대별 Transported 시각화...')
    visualize_transported_by_age(merged_data)
    
    # Phase 6: 보너스 - Destination별 연령대 분포 시각화
    print('\n[Phase 6] Destination별 연령대 분포 시각화...')
    visualize_age_distribution_by_destination(merged_data)
    
    print('\n' + '=' * 60)
    print('분석 완료!')
    print('=' * 60)


if __name__ == '__main__':
    main()

