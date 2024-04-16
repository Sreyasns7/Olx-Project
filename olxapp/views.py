from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.urls import path
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path
from django.utils.crypto import get_random_string
from .models import CustomUser,Usermembers,ProductCategory, ProductSubcategory,Product,Message,Cart,Order,Feedback
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
import re
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django_countries import countries
from django.db import IntegrityError
from django.contrib.auth import password_validation
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.db.models import Q 
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


def main_login(request):
    if request.method == 'POST':
        pending_users = CustomUser.objects.filter(is_active=False)
        pending_count = pending_users.count()
        username = request.POST.get('uname')
        password = request.POST.get('upass')
        usr = authenticate(request, username=username, password=password)
        
        if usr is not None:
            auth_login(request, usr)
            if usr.is_superuser:
                # Superuser login, redirect to admin home
                return render(request, 'admin/admin_home.html', {'pending_count': pending_count})
            elif usr.user_type == '2':

                # Regular user login, redirect to user home
                return render(request, 'user/user_home.html')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = str(random.randint(100000, 999999))
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return render(request, 'registration_form.html')
        
        # Validate mobile number format
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            messages.error(request, 'Mobile number should be 10 digits')
            return render(request, 'registration_form.html')
        
        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'registration_form.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'registration_form.html')

        # Save user data
        user_image = request.FILES.get('user_image')
        user = CustomUser.objects.create_user(username=username,first_name=first_name,last_name=last_name, password=password, email=email, is_active=False)
        user.save()

        user_member = Usermembers(
            user_member=user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            country=country,
            state=state,
            district=district,
            mobile_number=mobile_number,
            user_image=user_image
        )
        user_member.save()

        # Send registration confirmation email
        subject = "Registration Confirmation"
        message = "Registration successful, wait for admin approval"
        send_mail(subject, "Hello " + username + ' ' + message, settings.EMAIL_HOST_USER, [email])

        # Display success message
        messages.success(request, 'User registration successful. Please wait for admin approval.')
        return render(request, 'registration_form.html')

    countries_list = [(code, name) for code, name in countries]
    return render(request, 'registration_form.html', {'countries': countries_list})

def approve_disapprove_users(request):
    pending_users = CustomUser.objects.filter(is_active=False)
    approved_users = CustomUser.objects.filter(is_active=True)
    pending_count = pending_users.count()

    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        action = request.POST.get('action')

        if not user_ids:
            messages.error(request, 'No users selected.')
            return redirect('approve_disapprove_users')

        users = get_object_or_404(CustomUser, id=user_ids[0])  # Use get_object_or_404 for a single user

        if action == 'approve':
            password = str(random.randint(100000, 999999))
            users.set_password(password)
            users.is_active = True
            users.save()

            subject = 'Registration Approved'
            message = f"Hello {users.username}, your username is {users.username} and your password is {password}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [users.email])

            messages.success(request, 'Selected users have been approved.')
            return redirect('approve_disapprove_users')

        elif action == 'disapprove':
            users.delete()

            messages.success(request, 'Selected users have been disapproved and deleted.')
            return redirect('approve_disapprove_users')

    return render(request, 'admin/approve.html', {'pending_users': pending_users, 'pending_count': pending_count, 'approved_users': approved_users})





def user_details(request):
    users = CustomUser.objects.filter(user_type=2)

    user_data = []
    for user in users:
        user_member = Usermembers.objects.get(user_member=user)

        user_info = {
            'username': user.username,
            'email': user.email,
            'address': user_member.address,
            'country': user_member.country,
            'state': user_member.state,
            'district': user_member.district,
            'mobile_number': user_member.mobile_number,  # Add the user ID to identify the user in the delete view
        }
        user_data.append(user_info)

    if request.method == 'POST':
        user_id_to_delete = request.POST.get('user_id_to_delete')
        if user_id_to_delete:
            user_to_delete = get_object_or_404(CustomUser, id=user_id_to_delete)
            user_to_delete.delete()
            return redirect('teacher_records')

    return render(request, 'admin/user_details.html', {'users': user_data})


def delete_user_details(request):
    if request.method == 'POST':
        user_id_to_delete = request.POST.get('user_id_to_delete')
        if user_id_to_delete:
            user_to_delete = get_object_or_404(CustomUser, username=user_id_to_delete)
            user_to_delete.delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('user_details')

    # Handle invalid requests or redirect to user_details
    messages.error(request, 'Failed to delete user.')
    return redirect('user_details')

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


@login_required(login_url='/login/')  
def reset_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('reset_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('reset_password')

        # Validate the new password
        try:
            # Use Django's built-in password validators
            password_validation.validate_password(new_password, user=request.user)

            # Add custom validation for additional patterns
            # For example, requiring at least one special character
            if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in new_password):
                raise ValidationError("The password must contain at least one special character.")

        except ValidationError as error:
            messages.error(request, '\n'.join(error.messages))
            return redirect('reset_password')

        # If the password passes validation, set and save it
        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password successfully changed.')
        return redirect('reset_password')

    return render(request, 'user/reset_password.html')

def edit_user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, user_type=2)
    user_member = get_object_or_404(Usermembers, user_member=user)

    if request.method == 'POST':
        # Update user details based on the submitted form data
        user.username = request.POST.get('username')
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email = request.POST.get('email')
        user_member.address = request.POST.get('address')
        user_member.country = request.POST.get('country')
        user_member.state = request.POST.get('state')
        user_member.district = request.POST.get('district')
        mobile_number = request.POST.get('mobile_number')

        # Validate email format and check for existing email
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user.email):
            messages.error(request, 'Invalid email format. Please enter a valid email address.')
            return render(request, 'user/edit_user_details.html', {'user': user, 'user_member': user_member})

        # Check for existing email
        try:
            CustomUser.objects.exclude(id=user.id).get(email=user.email)
            messages.error(request, 'Email already exists. Please choose a different one.')
            return render(request, 'user/edit_user_details.html', {'user': user, 'user_member': user_member})
        except CustomUser.DoesNotExist:
            pass

        # Validate mobile number format
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            messages.error(request, 'Mobile number should be a 10-digit number.')
            return render(request, 'user/edit_user_details.html', {'user': user, 'user_member': user_member})

        user_member.mobile_number = mobile_number

        # Validate username uniqueness
        try:
            CustomUser.objects.exclude(id=user.id).get(username=user.username)
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'user/edit_user_details.html', {'user': user, 'user_member': user_member})
        except CustomUser.DoesNotExist:
            pass

        # Save user and user_member
        user.save()
        user_member.save()

        messages.success(request, 'User details updated successfully!')
        return redirect('view_user_details', user_id=user_id)  # Redirect to the user details page after successful update

    return render(request, 'user/edit_user_details.html', {'user': user, 'user_member': user_member})


def view_user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, user_type=2)
    user_member = get_object_or_404(Usermembers, user_member=user)
    return render(request, 'user/view_user_details.html', {'user': user, 'user_member': user_member})


def add_categories(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')

        if category_name:
            new_category = ProductCategory(name=category_name)
            
            if category_image:
                new_category.image = category_image

            new_category.save()
            messages.success(request, 'Category added successfully!')

        # Add subcategory
        category_id = request.POST.get('category_id')
        subcategory_name = request.POST.get('subcategory_name')
        if category_id and subcategory_name:
            category = ProductCategory.objects.get(id=category_id)
            ProductSubcategory.objects.create(category=category, name=subcategory_name)
            messages.success(request, 'Subcategory added successfully!')

        return redirect('add_categories')

    categories = ProductCategory.objects.all()
    return render(request, 'admin/add_categories.html', {'categories': categories})


def product_categories(request):
    categories = ProductCategory.objects.all()
    return render(request, 'user/product_categories.html', {'categories': categories})

def subcategories_by_category(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    subcategories = ProductSubcategory.objects.filter(category=category)
    return render(request, 'user/subcategories_by_category.html', {'category': category, 'subcategories': subcategories})

def products_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(ProductSubcategory, id=subcategory_id)
    # Filter products with approved=True and status=unsold
    products = Product.objects.filter(subcategory=subcategory, approved=True, status='unsold')
    return render(request, 'user/products_by_subcategory.html', {'subcategory': subcategory, 'products': products})

def messaging(request, user_id):
    recipient = get_object_or_404(CustomUser, id=user_id)
    messages = None

    if request.user == recipient or Message.objects.filter(Q(sender=request.user, receiver=recipient) | Q(sender=recipient, receiver=request.user)).exists():
        messages = Message.objects.filter(
            (Q(sender=request.user, receiver=recipient) | Q(sender=recipient, receiver=request.user))
        ).order_by('timestamp')

    user_members = Usermembers.objects.exclude(user_member=request.user)  # Adjust this query as needed

    return render(request, 'user/messaging.html', {'recipient': recipient, 'messages': messages, 'user_members': user_members})

def send_message(request, user_id):
    if request.method == 'POST':
        recipient = get_object_or_404(CustomUser, id=user_id)
        content = request.POST.get('content', '')
        if content:
            Message.objects.create(sender=request.user, receiver=recipient, content=content)
            # messages.success(request, 'Message sent successfully!')
        # else:
            # messages.error(request, 'Message content cannot be empty.')

    return redirect('messaging', user_id=user_id)

def user_list(request):
    # Fetch the list of users that the current user has messaged
    messaged_users = Usermembers.objects.filter(user_member=request.user)
    return render(request, 'user/user_list.html', {'messaged_users': messaged_users})

@login_required
def add_product(request):
    if request.method == 'POST':
        # Get data from the form
        subcategory_id = request.POST['subcategory']
        seller_id = request.user.id
        name = request.POST['name']
        description = request.POST['description']
        year = request.POST['year']
        price = request.POST['price']
        image = request.FILES.get('image', None)

        # Create the pending product
        product = Product.objects.create(
            subcategory_id=subcategory_id,
            seller_id=seller_id,
            name=name,
            description=description,
            year=year,
            price=price,
            image=image,
            approved=False  # Set the approved field to False by default
        )

        messages.success(request, 'Product added successfully. Awaiting admin approval.')
        return redirect('add_product')  # Redirect to the dashboard or any other page

    categories = ProductCategory.objects.all()
    subcategories = ProductSubcategory.objects.all()

    return render(request, 'user/add_product.html', {'categories': categories, 'subcategories': subcategories})


@login_required
def admin_approval(request):
    if not request.user.is_staff:
        return redirect('dashboard')  # Redirect non-admin users

    pending_products = Product.objects.filter(approved=False)
    pending_count = pending_products.count()

    if request.method == 'POST':
        # Handle form submission for product approval or disapproval
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if product_id and action in ['approve', 'disapprove']:
            product = get_object_or_404(Product, id=product_id)

            if action == 'approve':
                product.approved = True
                product.save()
                # Notify the user about the approval if needed
                messages.success(request, f'Product "{product.name}" has been approved.')
            elif action == 'disapprove':
                product.delete()
                # Notify the user about the disapproval if needed
                messages.warning(request, f'Product "{product.name}" has been disapproved.')

    return render(request, 'admin/approval.html', {'pending_products': pending_products, 'pending_count': pending_count})



def user_products(request):
    logged_in_user = request.user
    user_products = Product.objects.filter(seller=logged_in_user)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_status = request.POST.get('status')
        product = Product.objects.get(id=product_id)
        product.status = new_status
        product.save()

    context = {
        'user_products': user_products,
    }

    return render(request, 'user/user_products.html', context)





def edit_product(request, product_id):
    # Get the logged-in user
    logged_in_user = request.user

    # Get the product instance
    product = get_object_or_404(Product, id=product_id)

    # Check if the product belongs to the logged-in user
    if product.seller != logged_in_user:
        return redirect('user_products')  # Redirect to user's product list if not authorized

    if request.method == 'POST':
        # Update product details based on the form submission
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.year = request.POST.get('year')
        product.price = request.POST.get('price')

        # Update product image if a new one is provided
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        # Save the changes
        product.save()

        messages.success(request, 'Product updated successfully!')

        # Redirect back to the user's product list after editing
        return redirect('user_products')

    context = {
        'product': product,
    }

    return render(request, 'user/edit_product.html', context)

def user_delete_product(request, product_id):
    # Get the logged-in user
    logged_in_user = request.user

    # Get the product instance
    product = get_object_or_404(Product, id=product_id)

    # Check if the product belongs to the logged-in user
    if product.seller != logged_in_user:
        return redirect('user_products')  # Redirect to user's product list if not authorized

    if request.method == 'POST':
        # Delete the product
        product.delete()
        
        messages.error(request, 'Product deleted successfully!')
        return redirect('user_products')  # Redirect to user's product list after deletion

    # If the request method is not POST, render the template with the product
    context = {
        'product': product,
    }

    return render(request, 'user/delete_product.html', context)





# cart 


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    try:
        user_member = Usermembers.objects.get(user_member=request.user)
    except Usermembers.DoesNotExist:
        # Handle the case where the Usermembers instance does not exist
        messages.error(request, 'Usermembers instance not found.')
        return redirect('some_error_page')  # You can customize this as needed

    cart_item, created = Cart.objects.get_or_create(user_member=user_member, user_product=product)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1


    cart_item.save()

    messages.success(request, 'Product Added To Cart')
    return redirect('cart_view')


def cart_remove(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pk)
        
        try:
            user_member = Usermembers.objects.get(user_member=request.user)
        except Usermembers.DoesNotExist:
            user_member = None

        cart_item = Cart.objects.filter(user_member=user_member, user_product=product)
        
        if cart_item:
            cart_item.delete()

        return redirect('cart_view')


def cart_view(request):
    if request.user.is_authenticated:
        try:
            user_member = Usermembers.objects.get(user_member=request.user)
            cart_items = Cart.objects.filter(user_member=user_member).select_related('user_product')
        except Usermembers.DoesNotExist:
            user_member = None
            cart_items = []

        # Filter out items with None user_product
        cart_items = [item for item in cart_items if item.user_product]

        total_price = sum(item.total_price for item in cart_items)
        categories = ProductCategory.objects.all()
        
        # Calculate the total number of items in the cart
        total_items = sum(item.quantity for item in cart_items)

        return render(request, 'user/cart.html', {'cart': cart_items, 'total_price': total_price, 'user_member': user_member, 'categories': categories, 'total_items': total_items})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'user/cart.html')  # You can customize this as needed

def decrement(request, pk):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(user_product_id=pk, user_member=request.user.usermembers)
        cart_item.quantity = max(1, cart_item.quantity - 1)
        cart_item.save()
        return redirect('cart_view')

def increment(request, pk):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(user_product_id=pk, user_member=request.user.usermembers)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart_view')

def checkout_process(request):
    if request.method == 'POST':
        # Handle feedback submission
        feedback_content = request.POST.get('feedback_content')
        if feedback_content:
            # Assuming user is logged in, you can replace it with your authentication logic
            user = request.user
            if user.is_authenticated:
                feedback = Feedback.objects.create(user=user, content=feedback_content)
                feedback.save()
                messages.success(request, 'Thank you for your feedback!')
            else:
                messages.error(request, 'You need to be logged in to submit feedback.')
        return redirect('checkout_process')  # Redirect to checkout success page

    return render(request, 'user/checkoutsuccess.html')


def feedback_list(request):
    # Retrieve all feedback objects from the database
    feedbacks = Feedback.objects.all()
    return render(request, 'admin/feedback_list.html', {'feedbacks': feedbacks})    





def place_order(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        shipping_address = request.POST.get('shipping_address')
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        

        # Validate the data (you might want to add more validation)
        if not username or not email or not shipping_address or not card_number or not cvv:
            messages.error(request, 'All fields are required.')
            return redirect('place_order')

        # Get the user member associated with the current user
        try:
            user_member = Usermembers.objects.get(user_member=request.user)
        except Usermembers.DoesNotExist:
            messages.error(request, 'Usermembers object not found for the current user.')
            return redirect('place_order')

        # Fetch the cart for the user_member
        try:
            cart = Cart.objects.get(user_member=user_member)
        except Cart.DoesNotExist:
            messages.error(request, 'Cart not found for the current user.')
            return redirect('place_order')

        # Calculate the total price from the cart
        total_price = cart.total_price

        seller_name=cart.seller_name

        # Pass the cart to the template context
        context = {'cart': cart}

        # Create the order
        order = Order.objects.create(
            user_member=user_member,
            cart=cart,
            name=username,
            email=email,
            card_number=card_number,
            shipping_address=shipping_address,
            cvv=cvv,
            total_price=total_price,
            seller_name=seller_name,
        )

        seller_ids = set(cart_item.product.seller_id for cart_item in cart.cart_items.all())
        if len(seller_ids) == 1:
            order.seller_id = seller_ids.pop()
            order.save()

        # Order placed successfully, now mark it as confirmed
        order.is_confirmed = True
        order.save()

        # Retrieve the product associated with the order
        product = Product.objects.get(cart=cart)
        # Update the status of the product to 'sold'
        product.status = 'sold'
        product.save()

        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', order_id=order.id)  # Change 'home' to the name of your home page URL pattern

    return render(request, 'user/place_order.html')


def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        # Handle the case where the order with the specified ID does not exist
        return render(request, 'order_not_found.html')

    return render(request, 'user/order_detail.html', {'order': order})

@login_required
def user_orders(request):
    try:
        user_member = Usermembers.objects.get(user_member=request.user)
        user_orders = Order.objects.filter(user_member=user_member)
    except Usermembers.DoesNotExist:
        user_orders = []

    return render(request, 'user/user_orders.html', {'user_orders': user_orders})



def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

@staff_member_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        product.delete()
        return redirect('product_list')

    return redirect('product_list')


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'admin/order_list.html', {'orders': orders})



from django.db.models import Q

@login_required
def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(approved=True, status='unsold').exclude(seller=request.user)
    
    if query:
        # Search by product name or subcategory name or subcategory id
        products = products.filter(
            Q(name__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__id__icontains=query)
        )
        
    return render(request, 'user/product_search.html', {'products': products})





def seller_order_details(request):
    # Retrieve orders associated with the seller_name user
    seller_orders = Order.objects.filter(seller_name=request.user.username)

    context = {
        'seller_orders': seller_orders
    }
    return render(request, 'user/seller_order_details.html', context)