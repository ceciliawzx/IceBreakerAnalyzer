from test_data import users
from reports_generation import generate_reports, get_report_for_user


reports = generate_reports(users)
report = get_report_for_user(reports, 'J', 'O')


print(report)
