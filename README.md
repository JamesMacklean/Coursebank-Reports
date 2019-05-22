# To Use:

1. Install with `pip install -e .` within this folder within the edx platform virtual environment.
2. Add "coursebank_reports" to the "ADDL_INSTALLED_APPS" array in `lms.env.json` (you may have to create it if it doesn't exist.)
3. Run migrations.
4. Start/restart the LMS.


## Templates Directory
Add this to envs.common:
TEMPLATES = {
  'DIRS' : [
  ...
  OPENEDX_ROOT / 'features' / 'coursebank-reports' / 'coursebank_reports' / 'templates',
  ]
}

## ADD TO LMS URLS
urlpatterns += [
    url(r'', include('coursebank_reports.urls')),
]
