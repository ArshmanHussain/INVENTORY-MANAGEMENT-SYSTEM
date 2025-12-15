from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.category import Category
from models.product import Product

inventory = Blueprint("inventory", __name__)


@inventory.route("/")
@login_required
def dashboard():
    
    total_products = Product.query.count()
    total_categories = Category.query.count()
    low_stock = Product.query.filter(Product.stock_qty < 5).count()

    return render_template("dashboard.html",
                           total_products=total_products,
                           total_categories=total_categories,
                           low_stock=low_stock)

# PRODUCTS LIST
@inventory.route("/products")
@login_required
def products_list():
    search = request.args.get("search", "")

    query = Product.query

    if search:
        query = query.filter(
            (Product.name.like(f"%{search}%")) |
            (Product.sku.like(f"%{search}%"))
        )

    products = query.all()

    # category mapping
    categories = {c.id: c.name for c in Category.query.all()}
    return render_template("products/list.html", products=products, categories=categories)


# ADD PRODUCT
@inventory.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    categories = Category.query.all()

    if request.method == "POST":
        new_product = Product(
            name=request.form.get("name"),
            category_id=request.form.get("category_id"),
            sku=request.form.get("sku"),
            stock_qty=request.form.get("stock_qty"),
            cost_price=request.form.get("cost_price"),
            sale_price=request.form.get("sale_price")
        )
        db.session.add(new_product)
        db.session.commit()

        flash("Product added!", "success")
        return redirect(url_for("inventory.products_list"))

    return render_template("products/add.html", categories=categories)


# EDIT PRODUCT
@inventory.route("/products/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == "POST":
        product.name = request.form.get("name")
        product.category_id = request.form.get("category_id")
        product.sku = request.form.get("sku")
        product.stock_qty = request.form.get("stock_qty")
        product.cost_price = request.form.get("cost_price")
        product.sale_price = request.form.get("sale_price")

        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for("inventory.products_list"))

    return render_template("products/edit.html",
                           product=product,
                           categories=categories)


# DELETE PRODUCT
@inventory.route("/products/delete/<int:id>")
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted!", "info")
    return redirect(url_for("inventory.products_list"))

# CATEGORY LIST
@inventory.route("/categories")
@login_required
def categories_list():
    categories = Category.query.all()
    return render_template("categories/list.html", categories=categories)


# ADD CATEGORY
@inventory.route("/categories/add", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        new_cat = Category(name=name, description=description)
        db.session.add(new_cat)
        db.session.commit()

        flash("Category added!", "success")
        return redirect(url_for("inventory.categories_list"))

    return render_template("categories/add.html")


# EDIT CATEGORY
@inventory.route("/categories/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)

    if request.method == "POST":
        category.name = request.form.get("name")
        category.description = request.form.get("description")
        db.session.commit()

        flash("Category updated!", "success")
        return redirect(url_for("inventory.categories_list"))

    return render_template("categories/edit.html", category=category)


# DELETE CATEGORY
@inventory.route("/categories/delete/<int:id>")
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash("Category deleted!", "info")
    return redirect(url_for("inventory.categories_list"))
