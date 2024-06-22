from store.models import Product, Customer


class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request

        # get current session key if it exist
        cart = self.session.get('session_key')

        # if user is new, no key, create it
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart wark all pages
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            # Update the quantity
            self.cart[product_id] = int(self.cart[product_id]) + int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # deal w logged user

        if self.request.user.is_authenticated:
            # get user user customer
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            # {'3':2, '2',4}--->{''3'':2, ''2'',4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to the customer model. up was for json!
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            # Update the quantity
            self.cart[product_id] = int(self.cart[product_id]) + int(product_qty)
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #deal w logged user

        if self.request.user.is_authenticated:
            # get user user customer
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            # {'3':2, '2',4}--->{''3'':2, ''2'',4}
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the customer model. up was for json!
            current_user.update(old_cart=str(carty))
    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # lookup  keys in our prodcts db model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0

        for key, value in quantities.items():
            # Convert key string
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total

    def __len__(self):
        return len(self.cart)

    # cart prod
    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in databse model

        products = Product.objects.filter(id__in=product_ids)
        # return looked up prodcuts
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart {'3':1, '2':4} look like this
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            # get user user customer
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            # {'3':2, '2',4}--->{''3'':2, ''2'',4}
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the customer model. up was for json!
            current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing

    def delete(self, product):
        # {'4':2 }
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            # get user user customer
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            # {'3':2, '2',4}--->{''3'':2, ''2'',4}
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the customer model. up was for json!
            current_user.update(old_cart=str(carty))

    def clear(self):
        # Clear the cart from the session
        self.cart = {}
        self.session['session_key'] = self.cart
        self.session.modified = True

        # If the user is authenticated, also clear the saved cart in the database
        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            current_user.update(old_cart="")


