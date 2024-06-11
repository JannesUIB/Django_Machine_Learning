from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.template import loader
from django.core import serializers
from .models import InternalUsers, Sales, SalesPaymentDetails, Project, Contact, Cluster
import pickle
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from django.http import JsonResponse
import json
import sweetify


from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to the URL named 'login'

def get_clusters(request):
    project_id = request.GET.get('project_id')
    clusters = Cluster.objects.filter(project_id=project_id)
    # Serialize queryset to JSON
    cluster_data = serializers.serialize('json', clusters)
    # Convert serialized data to Python objects
    clusters_list = []
    for item in json.loads(cluster_data):
        cluster_fields = item['fields']
        cluster_fields['id'] = item['pk']  # Add 'id' field to the cluster fields
        clusters_list.append(cluster_fields)
    return JsonResponse({'clusters': clusters_list})

def index(request):
  template = loader.get_template('index.html')
  user_name = request.session.get('user_name')
  is_admin = request.session.get('is_admin')

  return render(request, "index.html", {"user_name" : user_name, 'is_admin' : is_admin})

def login(request):
  if request.method == 'POST':
        try:
          username = request.POST.get('email')
          password = request.POST.get('password')
          user = InternalUsers.objects.get(email=username,password=password)
          if user is not None:
              # Store the user's name in the session
              request.session['user_name'] = user.name
              request.session['is_admin'] = user.is_admin
              return redirect('index')
          else:
              return render(request, 'login.html')
        except:
            sweetify.warning(request, 'Wrong Email/Password Please Try Again')
            return render(request, 'login.html')
           
  return render(request, 'login.html')

def projects(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  table_datas = Project.objects.all()
  return render(request, "projects.html", {'data': table_datas})

def projects_form(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  internal_user_objs = InternalUsers.objects.all()

  return render(request, "projects_form.html", {'internal_users' : internal_user_objs})

def projects_details(request, project_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  project_obj = Project.objects.get(id=project_id)
  internal_user_objs = InternalUsers.objects.all()
  sales_obj = Sales.objects.filter(projects=project_obj)
  return render(request, "projects_details.html", {'projects' : project_obj,'internal_users' : internal_user_objs, 'sales_data' : sales_obj})

def projects_edit(request, project_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  project_obj = Project.objects.get(id=project_id)
  internal_user_objs = InternalUsers.objects.all()

  return render(request, "projects_edit.html", {'projects' : project_obj,'internal_users' : internal_user_objs})

def projects_add(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Project()
    internal_user_obj = InternalUsers.objects.get(id=request.POST.get('project_manager'))
    new_table.name= request.POST.get('project_name')
    new_table.project_description= request.POST.get('project_description')
    new_table.project_manager = internal_user_obj
    new_table.project_manager_email = request.POST.get('project_manager_email')
    new_table.save()
    
    table_datas = Project.objects.all()

  return render(request, "projects.html", {'data': table_datas})

def projects_update(request, project_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Project.objects.get(id=project_id)
    internal_user_obj = InternalUsers.objects.get(id=request.POST.get('project_manager'))
    new_table.name= request.POST.get('project_name')
    new_table.project_description= request.POST.get('project_description')
    new_table.project_manager = internal_user_obj
    new_table.project_manager_email = request.POST.get('project_manager_email')
    new_table.save()
    
  project_obj = Project.objects.get(id=project_id)
  internal_user_objs = InternalUsers.objects.all()
  sales_obj = Sales.objects.filter(projects=project_obj)

  return render(request, "projects_details.html", {'projects' : project_obj,'internal_users' : internal_user_objs, 'sales_data' : sales_obj})

def projects_delete(request, project_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  try:
      item_to_delete = Project.objects.get(id=project_id)
  except Project.DoesNotExist:
      table_datas = Project.objects.all()
      return render(request, "projects.html", {'data': table_datas})

  item_to_delete.delete()
  table_datas = Project.objects.all()
  return render(request, "projects.html", {'data': table_datas})

def contacts(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  table_datas = Contact.objects.all()
  return render(request, "contacts.html", {'data': table_datas})

def contacts_form(request):
  return render(request, "contacts_form.html")

def contacts_details(request, contact_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  contact_obj = Contact.objects.get(id=contact_id)
  return render(request, "contacts_details.html", {'contact' : contact_obj})

def contacts_edit(request, contact_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  contact_obj = Contact.objects.get(id=contact_id)
  return render(request, "contacts_edit.html", {'contact' : contact_obj})

def contacts_form(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  return render(request, "contacts_form.html")

def contacts_add(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Contact()
    new_table.name= request.POST.get('contact_name')
    new_table.pendapatan_per_bulan= request.POST.get('contact_main_income')
    new_table.pendapatan_lain_lain= request.POST.get('contact_other_income')
    new_table.status_pernikahan = request.POST.get('contact_status_pernikahan')
    new_table.jumlah_anak = request.POST.get('contact_kids')
    new_table.status_pernikahan = request.POST.get('contact_status_pernikahan')
    new_table.nomor_telepon = request.POST.get('contact_phone')
    new_table.email = request.POST.get('contact_email')
    new_table.save()
    
    table_datas = Contact.objects.all()

  return render(request, "contacts.html", {'data': table_datas})

def contacts_update(request, contact_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Contact.objects.get(id=contact_id)
    new_table.name= request.POST.get('contact_name')
    new_table.pendapatan_per_bulan= request.POST.get('contact_main_income')
    new_table.pendapatan_lain_lain= request.POST.get('contact_other_income')
    new_table.status_pernikahan = request.POST.get('contact_status_pernikahan')
    new_table.jumlah_anak = request.POST.get('contact_kids')
    new_table.status_pernikahan = request.POST.get('contact_status_pernikahan')
    new_table.nomor_telepon = request.POST.get('contact_phone')
    new_table.email = request.POST.get('contact_email')
    new_table.save()
    
  return render(request, "contacts_details.html", {'contact' : new_table})

def contacts_delete(request, contact_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  try:
      item_to_delete = Contact.objects.get(id=contact_id)
  except Contact.DoesNotExist:
      table_datas = Contact.objects.all()
      return render(request, "contacts.html", {'data': table_datas})

  item_to_delete.delete()
  table_datas = Contact.objects.all()
  return render(request, "contacts.html", {'data': table_datas})


def internal_user(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  table_datas = InternalUsers.objects.all()

  return render(request, "internaluser.html", {'data': table_datas})

def internal_user_form(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')

  return render(request, "internaluserform.html")

def internal_user_add(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = InternalUsers()
    new_table.name= request.POST.get('user_name')
    new_table.email= request.POST.get('user_email')
    new_table.password= request.POST.get('user_password')
    new_table.save()
    
    table_datas = InternalUsers.objects.all()

  return render(request, "internaluser.html", {'data': table_datas})

def internal_user_edit(request, user_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = InternalUsers.objects.get(id=user_id)
    new_table.name= request.POST.get('user_name')
    new_table.email= request.POST.get('user_email')
    new_table.password= request.POST.get('user_password')
    new_table.save()
    
    table_datas = InternalUsers.objects.all()

  return render(request, "internaluser.html", {'data': table_datas})

def internal_user_delete(request, user_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  try:
      item_to_delete = InternalUsers.objects.get(id=user_id)
  except InternalUsers.DoesNotExist:
      table_datas = InternalUsers.objects.all()
      return render(request, "internaluser.html", {'data': table_datas})

  item_to_delete.delete()
  table_datas = InternalUsers.objects.all()
  return render(request, "internaluser.html", {'data': table_datas})


def cluster(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
     
  table_datas = Cluster.objects.all()
  project_obj = Project.objects.all()

  return render(request, "cluster.html", {'data': table_datas,'Project': project_obj})

def cluster_form(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  project_obj = Project.objects.all()
  return render(request, "cluster_form.html", {'Project': project_obj})

def cluster_add(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Cluster()
    project_id = Project.objects.get(id=request.POST.get('cluster_project'))
    new_table.name= request.POST.get('cluster_name')
    new_table.cluster_type= request.POST.get('cluster_type')
    new_table.cluster_location= request.POST.get('cluster_location')
    new_table.project= project_id
    new_table.save()
    
    table_datas = Cluster.objects.all()
    project_obj = Project.objects.all()


  return render(request, "cluster.html", {'data': table_datas,'Project': project_obj})

def cluster_edit(request, cluster_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    new_table = Cluster.objects.get(id=cluster_id)
    project_id = Project.objects.get(id=request.POST.get('cluster_project'))
    new_table.name= request.POST.get('cluster_name')
    new_table.cluster_type= request.POST.get('cluster_type')
    new_table.cluster_location= request.POST.get('cluster_location')
    new_table.project= project_id
    new_table.save()
    
    table_datas = Cluster.objects.all()
    project_obj = Project.objects.all()

  return render(request, "cluster.html", {'data': table_datas,'Project': project_obj})

def cluster_delete(request, cluster_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  project_obj = Project.objects.all()
  try:
      item_to_delete = Cluster.objects.get(id=cluster_id)
  except Cluster.DoesNotExist:
      table_datas = Cluster.objects.all()
      return render(request, "cluster.html", {'data': table_datas,'Project': project_obj})

  item_to_delete.delete()
  table_datas = Cluster.objects.all()
  return render(request, "cluster.html", {'data': table_datas,'Project': project_obj})


def sales(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  table_datas = Sales.objects.all()
  
  return render(request, 'sales.html', {'data': table_datas})

def sales_form(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  contact_obj = Contact.objects.all()
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.all()
  internal_users_obj = InternalUsers.objects.all()
  return render(request, "sales_form.html", {'contacts' : contact_obj, 'projects' : project_obj, 'internal_users' : internal_users_obj, 'clusters': cluster_obj})

def sales_detail(request, sales_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  sales_obj = Sales.objects.get(id=sales_id)
  sale_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)
  contact_obj = Contact.objects.all()
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.all()
  internal_users_obj = InternalUsers.objects.all()

  return render(request, "sales_details.html", {'sale_data' : sales_obj, 'sale_lines' : sale_line_objs, 'contacts' : contact_obj, 'projects' : project_obj,'internal_users' : internal_users_obj, 'clusters': cluster_obj})

def sales_edit(request, sales_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  sales_obj = Sales.objects.get(id=sales_id)
  sale_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)
  contact_obj = Contact.objects.all()
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.filter(project_id=sales_obj.projects.id)
  internal_users_obj = InternalUsers.objects.all()

  return render(request, "sales_edit.html", {'sale_data' : sales_obj, 'sale_lines' : sale_line_objs, 'contacts' : contact_obj, 'projects' : project_obj,'internal_users' : internal_users_obj, 'clusters': cluster_obj})

def sales_add(request):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    contact_obj = Contact.objects.get(id=request.POST.get('sales_contacts'))
    project_obj = Project.objects.get(id=request.POST.get('sales_projects'))
    cluster_obj = Cluster.objects.get(id=request.POST.get('sales_cluster'))
    internal_user_obj = InternalUsers.objects.get(id=request.POST.get('sales_projects_manager'))
    new_sales = Sales()
    new_sales.name= request.POST.get('nama_sale')
    new_sales.contacts= contact_obj
    new_sales.projects= project_obj
    new_sales.cluster= cluster_obj
    new_sales.project_manager = internal_user_obj
    new_sales.project_manager_email = request.POST.get('sales_project_manager_email')
    new_sales.lama_cicil = request.POST.get('sales_lama_cicil')
    new_sales.down_payment = request.POST.get('sales_down_payment')
    new_sales.project_type = request.POST.get('sales_project_type')
    new_sales.project_location = request.POST.get('sales_project_location')
    new_sales.sales_total= 0
    new_sales.save()
    
    sale_line_json = request.POST.get('saleLines', '[]')
    sale_line_data = json.loads(sale_line_json)

    sales_total = 0
    # Create SaleLine instances
    for line in sale_line_data:
        new_sale_line = SalesPaymentDetails()
        new_sale_line.name = ""
        new_sale_line.sales_ref = new_sales
        new_sale_line.description = line['description']
        new_sale_line.jumlah_cicil = line['jumlah_cicil']
        new_sale_line.tahun_cicil = line['tahun_cicil']
        new_sale_line.bulan_cicil = line['bulan_cicil']
        sales_total += int(line['jumlah_cicil'])
        new_sale_line.save()

    new_sales.sales_total = sales_total

    new_sales.save()
    table_datas = Sales.objects.all()
  return render(request, "sales.html", {'data': table_datas})

def sales_update(request, sales_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    contact_obj = Contact.objects.get(id=request.POST.get('sales_contacts'))
    project_obj = Project.objects.get(id=request.POST.get('sales_projects'))
    cluster_obj = Cluster.objects.get(id=request.POST.get('sales_cluster'))
    
    internal_user_obj = InternalUsers.objects.get(id=request.POST.get('sales_projects_manager'))
    new_sales = Sales.objects.get(id=sales_id)
    new_sales.name= request.POST.get('nama_sale')
    new_sales.contacts= contact_obj
    new_sales.projects= project_obj
    new_sales.cluster= cluster_obj
    new_sales.project_manager = internal_user_obj
    new_sales.project_manager_email = request.POST.get('sales_project_manager_email')
    new_sales.lama_cicil = request.POST.get('sales_lama_cicil')
    new_sales.down_payment = request.POST.get('sales_down_payment')
    new_sales.project_type = request.POST.get('sales_project_type')
    new_sales.project_location = request.POST.get('sales_project_location')
    new_sales.sales_total= 0
    new_sales.save()
    
    sale_line_json = request.POST.get('saleLines', '[]')
    sale_line_data = json.loads(sale_line_json)

    sales_total = 0
    # Create SaleLine instances
    for line in sale_line_data:
        if line['LineId']:
          sales_total += int(line['jumlah_cicil'])
          continue
        else:
          new_sale_line = SalesPaymentDetails()
          new_sale_line.name = ""
          new_sale_line.sales_ref = new_sales
          new_sale_line.description = line['description']
          new_sale_line.jumlah_cicil = line['jumlah_cicil']
          new_sale_line.tahun_cicil = line['tahun_cicil']
          new_sale_line.bulan_cicil = line['bulan_cicil']
          sales_total += int(line['jumlah_cicil'])
          new_sale_line.save()

    new_sales.sales_total = sales_total

    new_sales.save()
    
  sales_obj = Sales.objects.get(id=sales_id)
  sale_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)
  contact_obj = Contact.objects.all()
  project_obj = Project.objects.all()
  internal_users_obj = InternalUsers.objects.all()
  cluster_obj = Cluster.objects.all()

  return render(request, "sales_details.html", {'sale_data' : sales_obj, 'sale_lines' : sale_line_objs, 'contacts' : contact_obj, 'projects' : project_obj,'internal_users' : internal_users_obj, 'clusters': cluster_obj})
  
def sales_delete(request, sales_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  sales_obj = Sales.objects.get(id=sales_id)
  sales_order_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)

  for line in sales_order_line_objs:
    line.delete()
  
  sales_obj.delete()
  table_datas = Sales.objects.all()
  return render(request, "sales.html", {'data': table_datas})

def sale_line_update(request, sale_line_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  if request.method == "POST":
    sale_line_obj = SalesPaymentDetails.objects.get(id=sale_line_id)
    sale_line_obj.description= request.POST.get('description')
    sale_line_obj.jumlah_cicil= request.POST.get('jumlah_cicil')
    sale_line_obj.tahun_cicil= request.POST.get('tahun_cicil')
    sale_line_obj.bulan_cicil= request.POST.get('bulan_cicil')
    sale_line_obj.save()

    sales_data = Sales.objects.get(id=sale_line_obj.sales_ref.id)
    sales_lines = SalesPaymentDetails.objects.filter(sales_ref=sales_data)

    sales_total = 0
    # Create SaleLine instances
    for line in sales_lines:
      sales_total += line.jumlah_cicil

    sales_data.sales_total = sales_total

    sales_data.save()

    sales_obj = Sales.objects.get(id=sales_data.id)
    sale_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)
    contact_obj = Contact.objects.all()
    project_obj = Project.objects.all()
    cluster_obj = Cluster.objects.all()
    internal_users_obj = InternalUsers.objects.all()

  return render(request, "sales_details.html", {'sale_data' : sales_obj, 'sale_lines' : sale_line_objs, 'contacts' : contact_obj, 'projects' : project_obj,'internal_users' : internal_users_obj, 'clusters': cluster_obj})

def sale_line_delete(request, sale_line_id):
  user_name = request.session.get('user_name')
  if user_name is None:
     return redirect('login')
  sale_line_obj = SalesPaymentDetails.objects.get(id=sale_line_id)
  sale_id = sale_line_obj.sales_ref.id

  sale_line_obj.delete()
  
  sales_data = Sales.objects.get(id=sale_id)
  sales_lines = SalesPaymentDetails.objects.filter(sales_ref=sales_data)

  sales_total = 0
  # Create SaleLine instances
  for line in sales_lines:
    sales_total += line.jumlah_cicil

  sales_data.sales_total = sales_total

  sales_data.save()
  sales_lines = SalesPaymentDetails.objects.filter(sales_ref=sales_data.id)

  sales_obj = Sales.objects.get(id=sales_data.id)
  sale_line_objs = SalesPaymentDetails.objects.filter(sales_ref=sales_obj)
  contact_obj = Contact.objects.all()
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.all()
  internal_users_obj = InternalUsers.objects.all()

  return render(request, "sales_details.html", {'sale_data' : sales_obj, 'sale_lines' : sale_line_objs, 'contacts' : contact_obj, 'projects' : project_obj,'internal_users' : internal_users_obj, 'clusters': cluster_obj})


def predict(request):
  # Load the trained model
  model = pickle.load(open("Kel4PSIA_web/model.pkl", "rb"))
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.all()
  # Define the input features (sample data)
  input_data = {
      'project': [request.POST.get('project')],
      'cluster': [request.POST.get('cluster')],
      'location': [request.POST.get('location')],
      'type': [request.POST.get('type')],
      'price': [request.POST.get('price')],
      'rate': [request.POST.get('rate')],
      'term_month': [request.POST.get('term_month')],
      'price_after_rate': [request.POST.get('price_after_rate')],
      'credit': [request.POST.get('credit')],
      'total_income': [request.POST.get('total_income')],
      'bi_status': [request.POST.get('bi_status')],
      'status': [request.POST.get('marital_status')],
      'children': [request.POST.get('childrens')],
  }
  df = pd.DataFrame(input_data)
  
  # Make a prediction
  prediction = model.predict(df)
  
  print("the predictions", prediction)
  if prediction[0] == 1:
    sweetify.success(request, 'Customer have a high percentage to credit this house',persistent='Noted!')
  else:
    sweetify.warning(request, 'Customer have a low percentage to credit this house',persistent='Noted!')
  # Render the result in the template
  return render(request, "prediction.html", {"prediction": prediction,"projects": project_obj, 'clusters': cluster_obj})

def prediction(request):
  # Load the trained model
  project_obj = Project.objects.all()
  cluster_obj = Cluster.objects.all()
  
  # Render the result in the template
  return render(request, "prediction.html", {"projects": project_obj, 'clusters': cluster_obj})

