from django.urls import path, include
from portaladmin import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("", views.index, name="home"),
    path("fetch-submission-id", views.fetch_submission_id),
    path("fetch-submission-text/<int:id>", views.fetch_submission_text),
    path("model-selection/", views.model_selection, name="model_selection"),
    path("model-run/", views.run_model, name="model_selection"),
    path("about/", views.about, name="about"),
    path("task_status/", views.task_status, name="task_status")
]
urlpatterns += staticfiles_urlpatterns()