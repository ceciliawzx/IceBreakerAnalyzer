from test_data import users
from reports_generation import generate_reports, get_report_for_user, get_reports_for_user

reports = generate_reports(users)
print(get_reports_for_user(reports, 'A'))
report = get_report_for_user(reports, 'A', 'D')

print(report)
