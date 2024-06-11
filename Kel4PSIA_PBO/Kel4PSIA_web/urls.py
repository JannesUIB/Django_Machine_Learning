from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('get_clusters/', views.get_clusters, name='get_clusters'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('internaluser/', views.internal_user, name='internaluser'),
    path('internaluserform/', views.internal_user_form, name='internaluserform'),
    path('internaluseradd/', views.internal_user_add, name='internaluseradd'),
    path('internaluseredit/<int:user_id>', views.internal_user_edit, name='internaluseredit'),
    path('internaluserdelete/<int:user_id>', views.internal_user_delete, name='internaluserdelete'),

    path('cluster/', views.cluster, name='cluster'),
    path('clusterform/', views.cluster_form, name='clusterform'),
    path('clusteradd/', views.cluster_add, name='clusteradd'),
    path('clusteredit/<int:cluster_id>', views.cluster_edit, name='clusteredit'),
    path('clusterdelete/<int:cluster_id>', views.cluster_delete, name='clusterdelete'),

    path('contacts/', views.contacts, name='contacts'),
    path('contactsform/', views.contacts_form, name='contactsform'),
    path('contactsadd/', views.contacts_add, name='contactsadd'),
    path('contactsdetails/<int:contact_id>', views.contacts_details, name='contactsdetails'),
    path('contactsedit/<int:contact_id>', views.contacts_edit, name='contactsedit'),
    path('contactsupdate/<int:contact_id>', views.contacts_update, name='contactsupdate'),
    path('contactsdelete/<int:contact_id>', views.contacts_delete, name='contactsdelete'),

    path('projects/', views.projects, name='projects'),
    path('projectsform/', views.projects_form, name='projectsform'),
    path('projectsadd/', views.projects_add, name='projectsadd'),
    path('projectsdetails/<int:project_id>', views.projects_details, name='projectsdetails'),
    path('projectsedit/<int:project_id>', views.projects_edit, name='projectsedit'),
    path('projectsupdate/<int:project_id>', views.projects_update, name='projectsupdate'),
    path('projectsdelete/<int:project_id>', views.projects_delete, name='projectsdelete'),

    path('sales/', views.sales, name='sales'),
    path('salesadd/', views.sales_add, name='salesadd'),
    path('salesform/', views.sales_form, name='salesform'),
    path('salesdetail/<int:sales_id>', views.sales_detail, name='salesdetail'),
    path('salesedit/<int:sales_id>', views.sales_edit, name='salesedit'),
    path('salesdelete/<int:sales_id>', views.sales_delete, name='salesdelete'),
    path('salesupdate/<int:sales_id>', views.sales_update, name='salesupdate'),

    path('saleslineupdate/<int:sale_line_id>', views.sale_line_update, name='salelineupdate'),
    path('saleslinedelete/<int:sale_line_id>', views.sale_line_delete, name='salelinedelete'),

    path('prediction', views.prediction, name='prediction'),
    path('predict', views.predict, name='predict')
]