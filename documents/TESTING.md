# Website Testing

###  Python Linter
- Pep8 website appears to not be working when visited. This was confirmed on Slack by posts from CI.
- All files, instead, checked against Github's local pycodestyle PROBLEMS tab.
- Any issues found have been rectified and all pages now pass with no errors or warnings to show with the exception of the settings.py file to avoid any unwanted effects.

---
## Manual testing

### Profile (https://pp5-devise-api.herokuapp.com/profiles)
- GET, POST, PUT, PATCH and DELETE tested manually on **29/3/23** and found to be working as intended

### Project (https://pp5-devise-api.herokuapp.com/projects)
- GET, POST, PUT, PATCH and DELETE tested manually on **29/3/23** and found to be working as intended

### Task (https://pp5-devise-api.herokuapp.com/tasks)
- GET, POST, PUT, PATCH and DELETE tested manually on **29/3/23** and found to be working as intended

### Contributor (https://pp5-devise-api.herokuapp.com/contributors)
- GET, POST, PUT, PATCH and DELETE tested manually on **29/3/23** and found to be working as intended

---
## Automatic testing

### Project (https://github.com/BeckySkel/project-5-backend/blob/main/projects/tests.py)
- The following automatic tests have been carried out on the Project resource. All pass.
- ProjectListViewTests(APITestCase)
  - test_can_list_projects(self)
  - test_logged_in_user_can_create_project(self)
  - test_logged_out_user_cannot_create_project(self)

- ProjectDetailViewTest(APITestCase)
  - test_can_retrieve_project_with_valid_id(self)
  - test_cannot_retrieve_project_with_invalid_id(self)
  - test_user_can_update_owned_project(self)
  - test_user_cannot_update_others_project(self)


### Task (https://github.com/BeckySkel/project-5-backend/blob/main/tasks/tests.py)
- The following automatic tests have been carried out on the Task resource. All pass.
- TaskListViewTests(APITestCase)
  - test_can_list_tasks(self)
  - test_logged_in_user_can_create_task(self)
  - test_logged_out_user_cannot_create_task(self)
- TaskDetailViewTest(APITestCase)
  - test_can_retrieve_task_with_valid_id(self)
  - test_cannot_retrieve_task_with_invalid_id(self)
  - test_user_can_update_owned_task(self)
  - test_user_cannot_update_task_if_not_creator_or_contrib(self)


### Contributor (https://github.com/BeckySkel/project-5-backend/blob/main/contributors/tests.py)
- The following automatic tests have been carried out on the Contributor resource. All pass.
- ContributorListViewTests(APITestCase)
  - test_can_list_contributors(self)
  - test_logged_in_user_can_add_contributor(self)
  - test_logged_out_user_cannot_add_contributor(self)
  - test_cannot_add_self_as_contributor(self)
  - test_cannot_add_contributor_to_unowned_project(self)


---
## Bugs
### Resolved Bugs
- Using allauth for user validation lead to incorrect redirect on email validation. Fixed by creating custom confirm email view.
- I originally planned to include profile images but this caused bugs when trying to deploy to Heroku. The code was removed temporarily but never returned as I deamed it unnecessary.
- Python version specified as python-3.9.14 due to errors when trying to deploy to Heroku. Changing the python version allowed the app to deploy sucessfully.

### Unresolved Bugs
- None identified.
