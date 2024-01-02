from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self) -> str:
        return self.title
    
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.title
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    
    class Meta:
        unique_together = ('menuitem', 'user')
        
    def get_unit_price(self):
        return self.menuitem.price
    
    def get_price(self):
        return self.quantity * self.unit_price
        
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,
                                      related_name="delivery_crew", 
                                      blank=True,
                                      null=True, 
                                      on_delete=models.SET_NULL)
    status = models.BooleanField(db_index=True, default=0)
    # total = models.DecimalField(max_digits=6, 
    #                             decimal_places=2,
    #                             default=0)
                                # null=True,
                                # blank=True)
    date = models.DateField(db_index=True, auto_now_add=True)
    
    @property
    def total(self):
        from django.db.models import Sum
        return self.dishes.aggregate(Sum("price"))['price__sum']
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='dishes', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')
        