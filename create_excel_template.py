import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('gantt_chart_template.csv')

# Excel 파일로 저장
df.to_excel('gantt_chart_template.xlsx', index=False)

print("Excel 템플릿이 생성되었습니다.")
