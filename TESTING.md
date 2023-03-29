# Website Testing

###  Python Linter
- Pep8 website appears to not be working when visited. This was confirmed on Slack by posts from CI.
- All files, instead, checked against Github's local pycodestyle PROBLEMS tab.
- Any issues found have been rectified and all pages now pass with no errors or warnings to show with the exception of the settings.py file to avoid any unwanted effects.

---
## Manual testing

### Homepage (https://pp5-devise.herokuapp.com/)
- All internal links tested manually on **29/12/22** and found to be working as intended
- All external links (social media links) tested manually on **29/12/22** and found to be working as intended
- All dynamic content tested manually on **29/12/22** and found to be working as intended
- All login-state sensitive content and links tested manually on **29/12/22** and found to be working as intended

---
## Automatic testing

### Homepage (https://pp5-devise.herokuapp.com/)
- All internal links tested manually on **29/12/22** and found to be working as intended
- All external links (social media links) tested manually on **29/12/22** and found to be working as intended
- All dynamic content tested manually on **29/12/22** and found to be working as intended
- All login-state sensitive content and links tested manually on **29/12/22** and found to be working as intended

---
## Bugs
### Resolved Bugs
- Using allauth for user validation lead to incorrect redirect on email validation. Fixed by creating custom confirm email view.
- I originally planned to include profile images but this caused bugs when trying to deploy to Heroku. The code was removed temporarily but never returned as I deamed it unnecessary.
- Python version specified as python-3.9.14 due to errors when trying to deploy to Heroku. Changing the python version allowed the app to deploy sucessfully.

### Unresolved Bugs
- None identified.
