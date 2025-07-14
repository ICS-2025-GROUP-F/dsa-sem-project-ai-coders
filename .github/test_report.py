from logic import report

print(" Class Average:", report.average_performance())

print("\n Top Performers:")
top = report.top_students()
for idx, student in enumerate(top, start=1):
    print(f"{idx}. {student['name']} - {student['average']}")
